# Heather — Tax Calculation (Assessment 2 Question 2)

Date: Auto-generated

## Purpose
Calculate Heather's total tax payable including the Medicare levy using the course formulas and slides (Module 4 & 5). All arithmetic is shown and assumptions are documented.

## Assumptions (explicit)

**Note:** The brief asked to ignore the Medicare Levy Surcharge. This calculation applies the standard Medicare levy at 2% of taxable income and does not apply any surcharge.
- Salary is taken as $180,000 (stated in the brief).
- Travel reimbursement of $6,000 is treated as a reimbursement and NOT included in assessable income (Module 5 guidance: reimbursements are generally not income except cents/km).
- Repairs of $7,200 for 4 Broome St (primary residence) are NOT deductible.
- Repairs for rental properties ($9,300) are deductible in full.
- Insurance total is $2,500, and 50% ($1,250) is attributable to rental properties and deductible.
- Black pants ($660) are treated as a deductible uniform/occupational clothing expense.
- Travel related to workplace duties ($780) is deductible.
- Franked dividends and franking credits are included in assessable income; franking credits are applied as a tax offset against income tax payable (per Module 4 slides).
- Medicare levy is 2% of taxable income (Module 4 slides).
- Tax calculation uses the piecewise formulas shown in lectures:
  - For taxable income between $45,001 and $135,000: tax = (T − 45,000) * 30% + $4,288
  - For taxable income above $135,000: tax = (T − 135,000) * 37% + $31,288
  - For lower bands (<= 45,000) a standard 19% marginal rate above $18,200 is used as a reasonable default (not used here).

If you want alternative treatments (e.g. include the $6,000 reimbursement as assessable), tell me and I'll recompute.

## Inputs (from brief)
- Salary: $180,000.00
- Food allowance: $5,000.00
- Bonus: $10,000.00
- Travel reimbursement: $6,000.00 (treated as non-assessable)
- Rental 1: $20,000.00
- Rental 2: $15,000.00
- Unfranked dividend: $15,000.00
- Franked dividend: $19,000.00
- Franking credit: $2,000.00

### Deductions considered
- Repairs (rentals): $9,300.00
- Insurance (rental share): $1,250.00
- Black pants (uniform): $660.00
- Travel for work: $780.00
- Repairs (primary residence) $7,200.00 — NOT deductible and excluded from deductions

## Calculation

1. Assessable income (include salary, allowances, bonuses, rentals, dividends and franking credits):

```
Assessable income = Salary + Food allowance + Bonus + Rental1 + Rental2 + Unfranked dividend + Franked dividend + Franking credit
                   = $180,000.00 + $5,000.00 + $10,000.00 + $20,000.00 + $15,000.00 + $15,000.00 + $19,000.00 + $2,000.00
                   = $266,000.00
```

2. Allowable deductions (rental repairs, rental insurance share, uniform, work travel):

```
Deductions = $9,300.00 + $1,250.00 + $660.00 + $780.00
           = $11,990.00
```

3. Taxable income = Assessable income − Deductions

```
Taxable income = $266,000.00 − $11,990.00 = $254,010.00
```

4. Income tax (using lecture piecewise formulas)

Tax before franking credits = $75,321.70

(Computed using the bracket formula appropriate to taxable income.)

5. Franking credit offset

```
Tax after applying franking credit = Tax before franking − Franking credit
                                  = $75,321.70 − $2,000.00
                                  = $73,321.70
```

6. Medicare levy = 2% × Taxable income = $5,080.20

7. Total tax payable (Income tax after franking + Medicare levy):

```
Total tax payable = $73,321.70 + $5,080.20 = $78,401.90
```

## Results (summary)
- Assessable income: $266,000.00
- Deductions: $11,990.00
- Taxable income: $254,010.00
- Income tax before franking credit: $75,321.70
- Franking credit (tax offset): $2,000.00
- Income tax after franking: $73,321.70
- Medicare levy (2%): $5,080.20
- Total tax payable (including Medicare): $78,401.90

## Notes and next steps
- I have documented assumptions explicitly. If you want any item treated differently (e.g. include the $6,000 travel reimbursement as assessable income, or treat black pants as non-deductible), I will recompute and update the documentation.
- If you want a stepped worksheet (spreadsheet-style) or to show PAYG withholding or potential refunds, I can add that.

