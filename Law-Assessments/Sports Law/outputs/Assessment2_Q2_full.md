# Assessment 2 — Question 2: Heather Tax Calculation

## Full scenario and questions (verbatim)

     1|SPM3113 ASSESSMENT 2 -- 35%
     2|
     3|Instructions
     4|
     5|Please carefully read the factual scenario below and use the **IRAC (Issue, Rule, Application, Conclusion) method** to advise Albert, Clare and Heather on their legal position. No referencing is needed for this assignment. However, please ensure that you cite primary sources (legislation and cases) for definitions and avoid using secondary sources such as textbooks and journal articles. Model answers have been provided for each module---please review them carefully before attempting the assignment. However, **do not** copy and paste the model answers word for word, as this would constitute plagiarism. Instead, use them as a guide to structure your response appropriately. The maximum word count for this assessment is 2,500 words, excluding calculation question(s). This assignment is graded out of 40 points but will be converted to a scale of 30 for the final mark.
     6|
     7|**Submission Details:**
     8|
     9|- Please submit in Word format. Do NOT submit as a PDF.
    10|
    11|- Submit your assignment through the submission link on Canvas.
    12|
    13|Due Date
    14|
    15|**11:59PM AWST 4 May 2026**
    16|
    17|Factual Scenario
    18|
    19|Clare, and Heather are best friends with different passions in life. Clare is a car enthusiasts who enjoy golfs, while Heather comes from a wealthy family consisting of her parents (both successful businesspeople earning more than a million per year), two employed brothers and two unemployed sisters aged between 20 to 29. Heather holds a doctorate degree in biotechnology. Heather is planning to expand her current business which specialises in selling cultured meat for pets. Heather is also a highly respected professor in biotechnology. She currently holds a position as a Professor of Biotechnology at UniPerth, earning approximately \$180,000 per year. Heather owns 3 houses in Perth - one is his primary residence (4 Broome St) and the others are rented out (1 Broome St and 2 Broome St). During the current year, Heather had the following other income and expenses:
    20|
    21|  ---------------------------------------------------------------------------------------------------------------------------
    22|  **Income:**                                                                                                 **\$**
    23|  ----------------------------------------------------------------------------------------------------------- ---------------
    24|  Food allowances                                                                                             5,000
    25|
    26|  Bonus for hitting research target                                                                           10,000
    27|
    28|  Travel reimbursement to Singapore for conference                                                            6,000
    29|
    30|  Rental from 1 Broome St                                                                                     20,000
    31|
    32|  Rental from 2 Broome St                                                                                     15,000
    33|
    34|  Unfranked Dividend from Grocery Limited                                                                     15,000
    35|
    36|  Dividend franked to 60% from Mining Limited                                                                 19,000
    37|
    38|  Franking credit                                                                                             2,000
    39|
    40|  **Expenses:**                                                                                               
    41|
    42|  Repairs and maintenance (4 Broome St)                                                                       7,200
    43|
    44|  Repairs and maintenance (1 Broome St, 2 Broome St)                                                          9,300
    45|
    46|  Insurance (50% of this amount is for his rental properties 1 Broome St and 2 Broome St)                     2,500
    47|
    48|  Black pants with uniPerth logo                                                                              660
    49|
    50|  Travel from police station that he works in to prisons for prison visits (which was part of his workload)   780
    51|  ---------------------------------------------------------------------------------------------------------------------------
    52|
    53|![](media/image1.png){width="3.4756944444444446in" height="3.4756944444444446in"}
    54|
    55|Clare, a renowned entrepreneur and photographer, has captivated Sydney\'s elite with her exclusive brand since 2023, Victory Cold Brew, a cold brew coffee that boasts a price tag of \$1,900 per liter. Known for its unique blend and exquisite packaging, the product contains real gold dust, creating a mesmerising visual elixir effect in dim light, described poetically as \"dancing in the moonlight.\" Clare's offline shop, located in Bellevue Hill---Sydney\'s most expensive suburb---is accessible only by invitation. Her TikTik presence follows a similar invite-only model,[^1] adding an extra layer of allure and exclusivity. She currently has around 150 followers, all of whom are American renowned singers, actresses, actors, and models.
    56|
    57|![](media/image2.png){width="3.213888888888889in" height="3.2256944444444446in"}Jimmy, a well-known rich 18-year-old in Sydney and a follower of Victory Cold Brew Tiktik account, finds himself enthralled by Clare\'s product. Inspired and equipped with abundant resources, Jimmy decides to create his own version of this coffee beginning of 2026. He calls it Jimmy Moonlight, and it sells for \$5 per liter. This new brew contains less gold dust than Victory Cold Brew but still sparkles beautifully when shaken. Jimmy quickly sets up a TikTik account for his brand, and to his delight, it explodes in popularity, gathering 15 million followers globally.
    58|
    59|Required
    60|
    61|Please answer **all** the below questions using the IRAC (Issue, Rule, Application, Conclusion) method except Question 2:
    62|
    63|1.  Please advise Heather on the most suitable business structure for her needs.
    64|
    65|2.  Please calculate Heather total tax payable including Medicare levy. Please ignore Medicare Levy Surcharge.
    66|
    67|3.  Clare is seeking advice on whether copyright protection applies to the visual elixir effect of Victory Cold Brew.
    68|
    69|4.  Clare is seeking advice on whether she can sue Jimmy for passing off.
    70|
    71|## Mark Distribution 
    72|
    73|  -----------------------------------------------------------------------
    74|  Question 1                          8 marks
    75|  ----------------------------------- -----------------------------------
    76|  Question 2                          12 marks
    77|
    78|  Question 3                          10 marks
    79|
    80|  Question 4                          10 marks
    81|
    82|  TOTAL                               40 marks
    83|  -----------------------------------------------------------------------
    84|
    85|[^1]: The \"invite-only\" model for TikTik followers means that a user can only follow a particular account if they have received a specific invitation from the account holder, making it an exclusive and restricted community.
    86|


---


## Script: heather_tax_calc.py

```python

File unchanged since last read. The content from the earlier read_file result in this conversation is still current — refer to that instead of re-reading.

```


---


## Computation, method and answer

     1|# Heather — Tax Calculation (Assessment 2 Question 2)
     2|
     3|Date: Auto-generated
     4|
     5|## Purpose
     6|Calculate Heather's total tax payable including the Medicare levy using the course formulas and slides (Module 4 & 5). All arithmetic is shown and assumptions are documented.
     7|
     8|## Assumptions (explicit)
     9|- Salary is taken as $180,000 (stated in the brief).
    10|- Travel reimbursement of $6,000 is treated as a reimbursement and NOT included in assessable income (Module 5 guidance: reimbursements are generally not income except cents/km).
    11|- Repairs of $7,200 for 4 Broome St (primary residence) are NOT deductible.
    12|- Repairs for rental properties ($9,300) are deductible in full.
    13|- Insurance total is $2,500, and 50% ($1,250) is attributable to rental properties and deductible.
    14|- Black pants ($660) are treated as a deductible uniform/occupational clothing expense.
    15|- Travel related to workplace duties ($780) is deductible.
    16|- Franked dividends and franking credits are included in assessable income; franking credits are applied as a tax offset against income tax payable (per Module 4 slides).
    17|- Medicare levy is 2% of taxable income (Module 4 slides).
    18|- Tax calculation uses the piecewise formulas shown in lectures:
    19|  - For taxable income between $45,001 and $135,000: tax = (T − 45,000) * 30% + $4,288
    20|  - For taxable income above $135,000: tax = (T − 135,000) * 37% + $31,288
    21|  - For lower bands (<= 45,000) a standard 19% marginal rate above $18,200 is used as a reasonable default (not used here).
    22|
    23|If you want alternative treatments (e.g. include the $6,000 reimbursement as assessable), tell me and I'll recompute.
    24|
    25|## Inputs (from brief)
    26|- Salary: $180,000.00
    27|- Food allowance: $5,000.00
    28|- Bonus: $10,000.00
    29|- Travel reimbursement: $6,000.00 (treated as non-assessable)
    30|- Rental 1: $20,000.00
    31|- Rental 2: $15,000.00
    32|- Unfranked dividend: $15,000.00
    33|- Franked dividend: $19,000.00
    34|- Franking credit: $2,000.00
    35|
    36|### Deductions considered
    37|- Repairs (rentals): $9,300.00
    38|- Insurance (rental share): $1,250.00
    39|- Black pants (uniform): $660.00
    40|- Travel for work: $780.00
    41|- Repairs (primary residence) $7,200.00 — NOT deductible and excluded from deductions
    42|
    43|## Calculation
    44|
    45|1. Assessable income (include salary, allowances, bonuses, rentals, dividends and franking credits):
    46|
    47|```
    48|Assessable income = Salary + Food allowance + Bonus + Rental1 + Rental2 + Unfranked dividend + Franked dividend + Franking credit
    49|                   = $180,000.00 + $5,000.00 + $10,000.00 + $20,000.00 + $15,000.00 + $15,000.00 + $19,000.00 + $2,000.00
    50|                   = $266,000.00
    51|```
    52|
    53|2. Allowable deductions (rental repairs, rental insurance share, uniform, work travel):
    54|
    55|```
    56|Deductions = $9,300.00 + $1,250.00 + $660.00 + $780.00
    57|           = $11,990.00
    58|```
    59|
    60|3. Taxable income = Assessable income − Deductions
    61|
    62|```
    63|Taxable income = $266,000.00 − $11,990.00 = $254,010.00
    64|```
    65|
    66|4. Income tax (using lecture piecewise formulas)
    67|
    68|Tax before franking credits = $75,321.70
    69|
    70|(Computed using the bracket formula appropriate to taxable income.)
    71|
    72|5. Franking credit offset
    73|
    74|```
    75|Tax after applying franking credit = Tax before franking − Franking credit
    76|                                  = $75,321.70 − $2,000.00
    77|                                  = $73,321.70
    78|```
    79|
    80|6. Medicare levy = 2% × Taxable income = $5,080.20
    81|
    82|7. Total tax payable (Income tax after franking + Medicare levy):
    83|
    84|```
    85|Total tax payable = $73,321.70 + $5,080.20 = $78,401.90
    86|```
    87|
    88|## Results (summary)
    89|- Assessable income: $266,000.00
    90|- Deductions: $11,990.00
    91|- Taxable income: $254,010.00
    92|- Income tax before franking credit: $75,321.70
    93|- Franking credit (tax offset): $2,000.00
    94|- Income tax after franking: $73,321.70
    95|- Medicare levy (2%): $5,080.20
    96|- Total tax payable (including Medicare): $78,401.90
    97|
    98|## Notes and next steps
    99|- I have documented assumptions explicitly. If you want any item treated differently (e.g. include the $6,000 travel reimbursement as assessable income, or treat black pants as non-deductible), I will recompute and update the documentation.
   100|- If you want a stepped worksheet (spreadsheet-style) or to show PAYG withholding or potential refunds, I can add that.
   101|
   102|