import { render, screen } from "@testing-library/react";
import ScanFlow from "@/components/ScanFlow";

test("renders camera button", () => {
  render(<ScanFlow />);
  expect(screen.getByText(/صوّر علبة الدواء/)).toBeInTheDocument();
});