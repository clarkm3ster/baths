# THE DOME — Full System Specification

## 1. Overview

THE DOME is a whole-person operating system that replaces fragmented government
programs with bespoke, prevention-based service delivery. It creates a unified view
of every person's relationship with government — past, present, and projected future —
enabling cross-agency coordination and evidence-based intervention.

## 2. Core Pipeline (11 Steps)

### Step 1: Entity Resolution
Link records across 30+ government systems (Medicaid, Medicare, SNAP, HUD, HMIS,
corrections, courts, education, etc.) into a single IdentitySpine using probabilistic
record linkage (Fellegi-Sunter matching).

### Step 2: Fiscal Ledger Population
For every linked person, populate an 81-field fiscal event ledger capturing every
dollar spent by every payer (federal, state, local, healthcare, nonprofit) across
every domain (healthcare, housing, justice, food, education, etc.).

### Step 3: 137-Metric Ingestion
Ingest metrics across 9 DOME layers: biometric, clinical, behavioral, economic,
environmental, social, institutional, legal, and subjective wellbeing.

### Step 4: Cross-Domain Risk Scoring
Compute risk scores (0-100) for each domain and a weighted composite score.

### Step 5: Cascade Detection
Detect active multi-domain deterioration cascades (6 types) that drive cost
escalation across siloed systems.

### Step 6: Intervention Recommendation
Select optimal interventions based on ROI (expected savings × break probability / cost)
using a greedy knapsack algorithm.

### Step 7: Benefits Cliff Analysis
Calculate effective marginal tax rates at every income level, identifying cliff
points where net resources decrease due to benefit phase-outs.

### Step 8: The Skeleton Key (WholePersonBudget)
THE central computation. Given a PersonBudgetKey, compute a complete budget showing
all costs by payer, domain, and mechanism across multiple time horizons (1y, 5y, 20y,
lifetime) with Monte Carlo probability distributions.

### Step 9: Fiscal Trajectory Classification
Classify into 5 tiers based on net fiscal impact NPV:
1. Net Contributor (NPV > +$100K)
2. Break Even (-$50K to +$100K)
3. Moderate Net Cost (-$500K to -$50K)
4. High Net Cost (-$2M to -$500K)
5. Catastrophic Net Cost (< -$2M)

### Step 10: Wrong-Pocket Resolution
Compute the cross-payer settlement matrix showing who pays, who saves, and
recommended inter-payer transfers to align incentives.

### Step 11: Monte Carlo Life Simulation
Run 1,000-iteration Path A (no DOME) vs Path B (DOME active) simulations to
project lifetime costs and compute DOME ROI.

## 3. Six Cascade Types

1. **Economic → Psychological → Biological → Fiscal**
   Job loss → depression → chronic disease → high healthcare utilization

2. **Environmental → Cognitive → Educational → Economic → Fiscal**
   Lead exposure → cognitive impairment → educational failure → low earnings

3. **Legal → Economic → Social → Geographic → Biological → Fiscal**
   Incarceration → employment barrier → social isolation → housing instability → health deterioration

4. **Social → Psychological → Biological → Fiscal**
   Social isolation → depression → substance use → medical crisis

5. **Environmental → Biological → Economic → Fiscal**
   Environmental hazard → respiratory disease → work limitation → income loss

6. **Economic → Social → Legal → Fiscal**
   Poverty → family stress → substance use → justice involvement

## 4. Settlement Matrix

The Settlement Matrix resolves wrong-pocket problems by computing:
- **Upfront investments**: dollars each payer contributes to prevention
- **Downstream savings**: avoided costs by payer under Path B vs Path A
- **Recommended transfers**: settlement schedule where benefiting payers reimburse investing payers

This turns "wrong pocket" from a political complaint into a budget rule.

## 5. Key Baselines

- Federal spend per person: $20,600/year (FY2025)
- Average lifetime taxes paid: $524,625
- Average lifetime healthcare spending: $316,600
- Super-utilizer threshold: top 5% = 54% of Medicaid spend
- Chronic homelessness cost: $35,000-45,000/year in reactive services
- Prison year: $35,000-60,000

## 6. Programs Covered

63 government programs across federal, state, and local levels including:
Medicare, Medicaid, CHIP, SNAP, TANF, Section 8, SSI, SSDI, EITC, Child Tax Credit,
Pell Grants, Head Start, WIOA, Federal/State Prisons, County Jails, Drug Courts,
SAMHSA, Ryan White, FQHC, and many more.

## 7. Validation Framework

- **Holdout validation**: Train/test split with MAE, MAPE, RMSE, R², decile calibration
- **Subgroup calibration**: Fairness checks by race, income, geography
- **Spend distribution**: KS test, percentile comparison, super-utilizer concentration
- **Bias audit**: 6 checks for racial disparity, income disparity, geographic disparity,
  hypervisibility bias, surveillance bias, and data density bias
