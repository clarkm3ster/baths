# BATHS

**Cosm x Chron = Flourishing**

BATHS is a game engine with two automated data agents — **Fragment** and **Cosm** — that scrape, accumulate, and assemble public data about the conditions of human existence across 28 US counties.

## Data Agents

### Fragment (`src/fragment/scrape.mjs`)

A scraper that collects every publicly available data point about what it means to be alive, by geography and time. It mirrors the fragmentation of human data.

**Sources** (no API keys required):
- **Census ACS 5-year** — demographics, income, poverty, housing, rent burden, health insurance, disability, education, commute, internet access, employment
- **BLS** — state unemployment rates
- **HUD** — fair market rents
- **EPA** — air quality data
- **USDA** — food access / food desert data
- **FEMA** — disaster declarations

**Gaps logged** (need API keys):
- CDC WONDER mortality
- FBI UCR crime statistics

Each run picks ~30 source-geography pairs that are oldest or never scraped (breadth-first strategy), so coverage expands with every run.

### Cosm (`src/cosm/assemble.mjs`)

Takes all fragments for a geography and assembles them around a single human life. Fragmented data organized around a person becomes a financial instrument.

For each county, Cosm assembles domes for 6 archetype profiles:

| Archetype | Age | Income | Household | Description |
|-----------|-----|--------|-----------|-------------|
| Marcus | 34 | $28k | 3 (2 kids) | Single dad, systems-heavy |
| Elena | 29 | $22k | 2 (1 kid) | Working poor |
| James | 72 | $14k | 1 | Elderly disabled |
| Rivera | 38 | $52k | 5 (3 kids) | Benefits cliff |
| Aisha | 19 | $12k | 1 | Aged out of foster care |
| Median | 38 | $59.5k | 2 (1 kid) | Benchmark |

Each dome calculates:
- **Program eligibility** — Medicaid, SNAP, Section 8, EITC, WIC, CHIP, LIHEAP, Head Start, Free School Lunch, SSI, TANF, Pell Grant
- **Fragmented cost** — total government spending across all programs with ~30% admin overhead
- **Coordinated cost** — estimated 40% reduction through coordination (conservative)
- **Delta** — the financial value of the dome
- **Cosm score** — minimum coverage across 12 domains (health, housing, economics, education, nutrition, safety, transportation, infrastructure, environment, legal, community, purpose)
- **Pattern detection** — geographic deltas, common gaps, program clusters

## Geography

28 priority US counties:

- **Philadelphia metro**: Philadelphia, Delaware, Montgomery, Bucks, Chester
- **NYC**: Manhattan, Brooklyn, Queens, Bronx
- **Major metros**: LA, Chicago, Houston, Phoenix, Dallas, Miami, Atlanta, Seattle, Baltimore, DC
- **Rural/Appalachia**: Bell County KY, Mercer County WV
- **Deep South**: Hinds County MS, Jefferson County AL
- **Midwest**: Detroit, Cleveland
- **New Jersey**: Essex, Hudson, Middlesex

## Data Structure

```
data/
├── fragments/{source-id}/{fips}.json   # Raw scraped data
├── domes/{fips}/{archetype}.json       # Assembled domes
├── patterns/patterns-{timestamp}.json  # Cross-dome patterns
├── meta/
│   ├── sources.json                    # What's been scraped and when
│   ├── coverage.json                   # Coverage statistics
│   └── gaps.json                       # What's missing
└── cosm.json                           # The evolving currency state
```

## Running

```bash
# Both agents (Fragment then Cosm)
npm run run

# Fragment only
npm run fragment

# Cosm only
npm run cosm
```

Requires Node.js 20+. No npm install needed — zero external dependencies.

## GitHub Actions

Runs automatically 5x daily (7am, 12pm, 5pm, 10pm, 3am UTC) via `.github/workflows/fragment-cosm.yml`. Also supports manual trigger via `workflow_dispatch`.

Each run:
1. Scrapes ~30 new fragment data points
2. Assembles domes for all geographies with available data
3. Detects cross-dome patterns
4. Commits updated data with fragment/dome counts
