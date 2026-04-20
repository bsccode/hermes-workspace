#!/usr/bin/env python3
"""
heather_tax_calc.py

Standalone script to reproduce Heather's tax calculation used for SPM3113 Assessment 2 Q2.
Prints results to stdout and writes a markdown summary file.

Usage:
    python3 heather_tax_calc.py

Outputs:
 - Prints results to stdout
 - Writes a verification markdown file alongside: heather_tax_calc_output.md

Note:
This version follows the lecture-based method and assumptions, not current ATO rates.
"""
from typing import Dict

# ---- Inputs taken from the assessment brief / lecture approach ----
SALARY = 180_000.00
FOOD_ALLOWANCE = 5_000.00
BONUS = 10_000.00
TRAVEL_REIMBURSEMENT = 6_000.00  # treated as non-assessable reimbursement by default
RENTAL_1 = 20_000.00
RENTAL_2 = 15_000.00
UNFRANKED_DIVIDEND = 15_000.00
FRANKED_DIVIDEND = 19_000.00
FRANKING_CREDIT = 2_000.00

# Deductions
REPAIRS_PRIMARY = 7_200.00       # private / primary residence: non-deductible
REPAIRS_RENTALS = 9_300.00       # deductible
INSURANCE_TOTAL = 2_500.00
INSURANCE_RENTAL_SHARE = 0.5 * INSURANCE_TOTAL
BLACK_PANTS = 660.00             # deductible here per lecture/example approach
TRAVEL_WORK = 780.00             # deductible work-related travel

OUTPUT_MD = "heather_tax_calc_output.md"


def income_tax(taxable_income: float) -> float:
    """
    Compute income tax using the lecture piecewise formulas.

    Lecture formulas used:
      - 0% for 0 - 18,200
      - 19% on amount over 18,200 up to 45,000
      - 30% on amount over 45,000 up to 135,000 plus $4,288
      - 37% on amount over 135,000 plus $31,288
    """
    if taxable_income <= 18_200:
        return 0.0
    elif taxable_income <= 45_000:
        return (taxable_income - 18_200) * 0.19
    elif taxable_income <= 135_000:
        return (taxable_income - 45_000) * 0.30 + 4_288.0
    else:
        return (taxable_income - 135_000) * 0.37 + 31_288.0


def r(value: float) -> float:
    """Round to 2 decimal places with a tiny offset to reduce float artefacts."""
    return round(value + 1e-9, 2)


def compute_dict(
    assess_reimbursement: bool = False,
    pants_deductible: bool = True
) -> Dict[str, float]:
    """
    Compute tax under specified assumptions.

    Parameters:
    - assess_reimbursement:
        If True, include TRAVEL_REIMBURSEMENT as assessable income.
    - pants_deductible:
        If True, include BLACK_PANTS in deductions.
    """
    assessable = (
        SALARY
        + FOOD_ALLOWANCE
        + BONUS
        + RENTAL_1
        + RENTAL_2
        + UNFRANKED_DIVIDEND
        + FRANKED_DIVIDEND
        + FRANKING_CREDIT
    )

    if assess_reimbursement:
        assessable += TRAVEL_REIMBURSEMENT

    deductions = REPAIRS_RENTALS + INSURANCE_RENTAL_SHARE + TRAVEL_WORK

    if pants_deductible:
        deductions += BLACK_PANTS

    taxable = assessable - deductions
    tax_before_franking = income_tax(taxable)
    tax_after_franking = tax_before_franking - FRANKING_CREDIT
    medicare = taxable * 0.02
    total = tax_after_franking + medicare

    return {
        "assessable": r(assessable),
        "deductions": r(deductions),
        "taxable": r(taxable),
        "tax_before_franking": r(tax_before_franking),
        "franking_credit": r(FRANKING_CREDIT),
        "tax_after_franking": r(tax_after_franking),
        "medicare": r(medicare),
        "total": r(total),
    }


def format_case(name: str, d: Dict[str, float]) -> str:
    """Format one scenario as markdown."""
    return (
        f"### {name}\n\n"
        f"- Assessable income: ${d['assessable']:,.2f}\n"
        f"- Deductions: ${d['deductions']:,.2f}\n"
        f"- Taxable income: ${d['taxable']:,.2f}\n"
        f"- Income tax before franking: ${d['tax_before_franking']:,.2f}\n"
        f"- Franking credit: ${d['franking_credit']:,.2f}\n"
        f"- Income tax after franking: ${d['tax_after_franking']:,.2f}\n"
        f"- Medicare levy (2%): ${d['medicare']:,.2f}\n"
        f"- Total tax payable: ${d['total']:,.2f}\n"
    )


def main() -> None:
    # Baseline scenario used for the assessment
    baseline = compute_dict(
        assess_reimbursement=False,
        pants_deductible=True
    )

    # Optional comparison scenarios
    include_reimbursement = compute_dict(
        assess_reimbursement=True,
        pants_deductible=True
    )
    no_pants = compute_dict(
        assess_reimbursement=False,
        pants_deductible=False
    )
    both_changes = compute_dict(
        assess_reimbursement=True,
        pants_deductible=False
    )

    md_content = "\n".join([
        "# Heather — Tax Calculation (script output)",
        "",
        "## Assumptions",
        "- Travel reimbursement is treated as non-assessable in the baseline scenario.",
        "- Black pants are treated as deductible in the baseline scenario, following the lecture/example approach.",
        "- Franking credit is included and then applied as a tax offset.",
        "- Medicare levy is 2% of taxable income.",
        "",
        "## Results",
        "",
        format_case("Baseline (default)", baseline),
        format_case("Include travel reimbursement", include_reimbursement),
        format_case("Black pants non-deductible", no_pants),
        format_case("Both changes", both_changes),
    ])

    print(md_content)

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"\nWrote results to {OUTPUT_MD}")


if __name__ == "__main__":
    main()
