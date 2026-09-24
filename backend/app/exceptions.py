"""Domain-specific explicit exceptions for the Interaction Engine."""


class InteractionEngineError(Exception):
    """Base exception class for all domain errors."""

    def __init__(self, message: str, code: str) -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class DrugNotFoundError(InteractionEngineError):
    """Raised when a requested drug or trade name cannot be found."""

    def __init__(self, drug_identifier: str) -> None:
        super().__init__(
            message=f"Drug identifier '{drug_identifier}' was not found in the database.",
            code="DRUG_NOT_FOUND",
        )


class EDAApiError(InteractionEngineError):
    """Raised when connection to Egyptian Drug Authority API fails or yields invalid data."""

    def __init__(self, details: str) -> None:
        super().__init__(
            message=f"EDA Integration Error: {details}",
            code="EDA_API_ERROR",
        )


class LLMServiceError(InteractionEngineError):
    """Raised when AI Agent processing fails."""

    def __init__(self, details: str) -> None:
        super().__init__(
            message=f"AI Agent Service Error: {details}",
            code="AI_AGENT_ERROR",
        )