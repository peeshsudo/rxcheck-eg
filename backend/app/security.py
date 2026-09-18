"""
Security utilities.

Changes from prior version:
- Constant-time admin key comparison (prevents timing attacks)
- Security headers middleware (clickjacking, MIME sniffing, CSP)
- Removes Server fingerprint header
"""
import hmac
import secrets
from fastapi import Header, HTTPException, status

from app.config import settings


async def require_admin_key(x_admin_key: str = Header(...)) -> None:
    """
    Verify the X-Admin-Key header using constant-time comparison.

    Why constant-time: a naive `==` check leaks the correct key byte-by-byte
    through response timing. hmac.compare_digest prevents that.

    Upgrade path: replace this with JWT + role checks once you have
    real user accounts (see docs/security.md).
    """
    expected = settings.backend_admin_key.encode()
    provided = x_admin_key.encode()

    # compare_digest requires equal-length inputs; pad to avoid leaks
    if len(expected) != len(provided):
        # still do a compare to keep timing flat
        hmac.compare_digest(provided, provided)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin key",
        )

    if not hmac.compare_digest(provided, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin key",
        )


def generate_secret(length: int = 48) -> str:
    """Utility: generate a secure random secret for .env."""
    return secrets.token_urlsafe(length)


# ============================================================
# Security headers middleware
# ============================================================

SECURITY_HEADERS = {
    "X-Frame-Options": "DENY",                       # no clickjacking
    "X-Content-Type-Options": "nosniff",             # no MIME sniffing
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=(self)",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": (
        "default-src 'self'; "
        "img-src 'self' data: blob:; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "connect-src 'self' http://localhost:8000"
    ),
}


async def add_security_headers(request, call_next):
    """FastAPI/Starlette middleware: attach security headers to every response."""
    response = await call_next(request)
    for header, value in SECURITY_HEADERS.items():
        response.headers[header] = value
    # Remove server fingerprint
    if "server" in response.headers:
        del response.headers["server"]
    return response