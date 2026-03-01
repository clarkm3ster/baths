# The Skeleton Key: Whole-Person Budget Engine

## Concept

The Skeleton Key is the central computation in THE DOME. Given a single person's
complete profile — their identity, current state across all domains, fiscal history,
and program enrollment — it computes a **WholePersonBudget** that shows:

1. **Who pays what** for this person across every level of government, healthcare
   delivery systems, and nonprofits
2. **What domains** the spending falls in (healthcare, housing, justice, food, etc.)
3. **What mechanisms** deliver the spending (cash transfers, in-kind benefits,
   service utilization, tax expenditures)
4. **Probability distributions** of future costs, including catastrophic event risks
5. **Scenario comparisons** showing what happens under DOME intervention vs. baseline

## The PersonBudgetKey

The input to the Skeleton Key is the `PersonBudgetKey`, which contains:

- Demographics (age, sex, location, household)
- Economic state (income, employment, assets/debts)
- Health indicators (chronic conditions, disability)
- Housing status and history
- Justice involvement history
- Program eligibility and enrollment
- Time horizons to compute (1-year, 5-year, 20-year, lifetime)

## Algorithm

### Step 1: Historical Spend Aggregation
Sum all fiscal events from the person's ledger by payer, domain, and mechanism.

### Step 2: Baseline Projection
Start with population baselines:
- Federal: $20,600/person/year
- State: $10,800/person/year
- Local: $7,200/person/year

### Step 3: Individual Risk Adjustment
Apply multipliers based on individual risk factors:
- Chronic conditions: 1.3-1.5× healthcare costs per condition
- Justice involvement: +$35K-60K/year per incarceration year
- Homelessness: +$35K-45K/year in reactive services
- Disability: +$18K-24K/year SSDI + Medicare
- Mental health: SUD +$15K-30K, depression +$5K-10K

### Step 4: Monte Carlo Simulation
Run 1,000 iterations per horizon:
- Sample annual costs from risk-adjusted distributions
- Simulate catastrophic events (hospitalization, incarceration, homelessness)
- Compute p50, p90, p99 cost percentiles

### Step 5: Wrong-Pocket Analysis
For each intervention scenario, compute the cross-payer settlement matrix showing
who saves when another agency invests.

## Output: WholePersonBudget

The output contains, for each time horizon:
- **PayerView**: Federal, state, local, healthcare, nonprofit spend breakdowns
- **DomainView**: Healthcare, housing, justice, food, education, etc.
- **MechanismView**: Cash, in-kind, services, tax expenditures
- **RiskProfile**: p50/p90/p99 cost distributions + catastrophic risks
- **Scenarios**: Path A (no DOME) vs Path B (DOME active) comparisons

## Why "Skeleton Key"?

Because it **unlocks** the ability to see a person's complete fiscal relationship
with government — past, present, and projected future — through a single computation.
This is what makes cross-agency coordination possible: when every stakeholder can see
the same unified cost picture, wrong-pocket problems become solvable.

## Settlement Matrix

The Skeleton Key also produces a **Settlement Matrix** for each scenario. This shows:
- Which payers invest in prevention (upfront costs)
- Which payers save from avoided downstream costs
- Recommended transfer payments so investing agencies are reimbursed

This turns "wrong pocket" from a political complaint into a budget rule.
