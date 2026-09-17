describe("Scan flow", () => {
  it("walks through OCR → time → food", () => {
    cy.visit("/");
    cy.contains("صوّر علبة الدواء");
    // In CI: mock Tesseract and API responses
  });
});