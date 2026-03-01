# DOME API Documentation

Base URL: `http://localhost:8000/api/v1`

## Health Check

```
GET /health
```
Returns `{"status": "ok", "service": "dome", "version": "0.1.0"}`

---

## Person Management

### Create Person
```
POST /persons/
```
**Body**: `PersonCreateRequest` with identity, demographics, and current state fields.
**Returns**: Created person with `person_uid`.

### Get Person
```
GET /persons/{uid}
```
**Returns**: Full `Person` object with all nested data.

### Add Fiscal Events
```
POST /persons/{uid}/fiscal-events
```
**Body**: Array of `FiscalEventCreateRequest` objects.
**Returns**: Count of events added.

### Get Fiscal History
```
GET /persons/{uid}/fiscal-history
```
**Returns**: Complete fiscal ledger as array of `FiscalEvent` objects.

---

## Budget (The Skeleton Key)

### Compute Budget
```
POST /persons/{uid}/budget
```
**Body**: `BudgetComputeRequest` with horizon specs and Monte Carlo iterations.
**Returns**: `WholePersonBudget` with payer/domain/mechanism views and risk profile.

### Get Stored Budget
```
GET /persons/{uid}/budget
```
**Returns**: Most recently computed `WholePersonBudget`.

### Get Trajectory
```
GET /persons/{uid}/trajectory
```
**Returns**: `FiscalTrajectoryTag` (net_contributor, break_even, moderate_net_cost, high_net_cost, catastrophic_net_cost).

### Wrong-Pocket Analysis
```
GET /persons/{uid}/wrong-pocket?horizon_label=lifetime
```
**Returns**: Cross-payer savings matrix showing who saves when each intervention is applied.

---

## Cascade Detection

### Detect Cascades
```
POST /persons/{uid}/detect-cascades
```
**Body**: `CascadeDetectRequest` with lookback period and confidence threshold.
**Returns**: Array of `CascadeAlertSummary` objects.

### Get Cascade Alerts
```
GET /persons/{uid}/cascade-alerts
```
**Returns**: All active cascade alerts for this person.

---

## Interventions

### Generate Intervention Plan
```
POST /persons/{uid}/intervention-plan
```
**Body**: `InterventionPlanRequest` with target cascade alert and budget constraints.
**Returns**: `InterventionPlanSummary` with ordered interventions and expected ROI.

---

## Simulations

### Run Simulation
```
POST /persons/{uid}/simulate
```
**Body**: `SimulationRequest` with iterations and projection years.
**Returns**: `SimulationSummary` with Path A vs Path B costs and DOME ROI.

### Get Simulation Results
```
GET /persons/{uid}/simulation-results
```
**Returns**: Most recent simulation results.

---

## Dashboard & Benefits

### Coordinator Dashboard
```
GET /persons/{uid}/dashboard
```
**Returns**: `DashboardData` with summary of person's trajectory, alerts, costs, and top interventions.

### Benefits Cliff Analysis
```
GET /persons/{uid}/benefits-cliff
```
**Returns**: Array of `BenefitsCliffPoint` objects showing income levels, benefit values, effective marginal tax rates, and cliff points.

---

## Settlement Matrix

### Compute Settlement
```
POST /persons/{uid}/settlement
```
**Body**: `SettlementComputeRequest` with scenario_id, horizon, and risk-share parameters.
**Returns**: `SettlementMatrix` with per-payer positions and recommended transfers.

### Get Settlement
```
GET /persons/{uid}/settlement/{scenario_id}
```
**Returns**: Previously computed settlement matrix.

---

## Validation

### Holdout Test
```
POST /validation/holdout-test
```
**Returns**: Validation metrics (MAE, MAPE, RMSE, calibration by decile).

### Bias Audit
```
POST /validation/bias-audit
```
**Returns**: Bias report with checks for racial disparity, income disparity, surveillance bias, hypervisibility, and data density bias.

### Calibration Report
```
GET /validation/calibration-report
```
**Returns**: Current calibration metrics.
