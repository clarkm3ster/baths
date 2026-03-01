# DOME Data Model Documentation

## Overview

THE DOME uses 35+ interconnected Pydantic models organized into these categories:

## Identity Layer
- **IdentitySpine** — Master identity record linking a person across up to 30 government systems
- **AddressEntry** — Geocoded address with census tract FIPS and date range
- **CrossSystemIds** — 18 optional cross-system identifiers (Medicaid, Medicare, SNAP, HUD, HMIS, corrections, courts, education, etc.)

## Static Profile
- **StaticProfile** — Time-invariant birth conditions (birth tract, parental background, ACE score, birth weight, genetic risk flags)

## Dynamic State (8 Sub-States)
- **DynamicState** — Timestamped composite of all 8 domain states
- **BioState** — BMI, blood pressure, HbA1c, chronic conditions, functional limitations
- **MentalState** — Depression, anxiety, SUD severity, psychosis, suicide risk
- **EconState** — Income, employment, assets, debts, income volatility
- **HousingState** — Housing status, rent burden, homelessness history
- **FamilyState** — Household size, dependents, caregiving burden, social network
- **JusticeState** — Justice involvement, jail/prison days, police contacts, supervision
- **EducationState** — Credential level, enrollment, special ed history, literacy
- **ProgramState** (with **EligibilitySnapshot** + **EnrollmentSnapshot**) — 11 program eligibility/enrollment flags each

## DOME Metrics (9 Layers, 137 Metrics)
- **DomeMetrics** — Biometric, clinical, behavioral, economic, environmental, social, institutional, legal, and subjective wellbeing layers

## Fiscal Layer
- **FiscalEvent** — Single cost event in the life ledger (81 fields per the spec)
- **PersonBudgetKey** — The "skeleton key" input combining 22 person-level attributes
- **BudgetHorizon** — Time horizon specification (1y, 5y, 20y, lifetime)

## Budget Output
- **WholePersonBudget** — Complete budget output with multiple horizons
- **HorizonBudget** — Budget for a single time horizon with payer/domain/mechanism views
- **PayerView** / **PayerBreakdown** — Federal/state/local/healthcare/nonprofit spend
- **DomainBudget** / **ProgramSpend** — Spend by service domain and program
- **MechanismBudget** — Spend by delivery mechanism
- **RiskProfile** / **CatastrophicEventRisk** — Cost distribution with tail risks
- **ScenarioBudget** — Path A vs Path B comparison

## Trajectory
- **FiscalTrajectoryTag** — 5-tier lifetime fiscal classification (net contributor → catastrophic net cost)

## Cascade Detection
- **CascadeDefinition** / **CascadeLink** — Causal chain definitions with probability, lag, and strength
- **CascadeAlert** — Active cascade warning for a person

## Interventions
- **InterventionDefinition** — Intervention with cost range, target, and break probability
- **InterventionPlan** — Ordered set of interventions for a person with ROI

## Settlement Matrix
- **SettlementMatrix** — Cross-payer settlement resolving wrong-pocket problems
- **PayerSettlementRow** — Per-payer investment, savings, and net position
- **PayerTransfer** — Recommended inter-payer transfer with schedule

## Top-Level Aggregate
- **Person** — Complete person record combining all of the above
