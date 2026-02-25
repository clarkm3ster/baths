/**
 * FRAGMENT — Census ACS Sources
 *
 * The Census American Community Survey is the backbone.
 * Hundreds of tables, no API key needed, county-level granularity.
 * Every table maps to specific dome layers.
 *
 * ACS 5-year estimates: most reliable for small geographies.
 * Variable reference: https://api.census.gov/data/2022/acs/acs5/variables.html
 */

import { censusACS, censusSubject } from './factories.mjs'

export default [

  // ══════════════════════════════════════════════════════════════════
  // DEMOGRAPHICS & POPULATION (Layer 8: Community)
  // ══════════════════════════════════════════════════════════════════

  censusACS({
    id: 'census-demographics',
    label: 'Census Demographics',
    layers: [8],
    variables: {
      total_pop: 'B01003_001E',
      median_age: 'B01002_001E',
      male_pop: 'B01001_002E',
      female_pop: 'B01001_026E',
      white_alone: 'B02001_002E',
      black_alone: 'B02001_003E',
      asian_alone: 'B02001_005E',
      hispanic_latino: 'B03003_003E',
      foreign_born: 'B05002_013E',
    },
  }),

  censusACS({
    id: 'census-age-detail',
    label: 'Census Age Distribution',
    layers: [4, 8],
    variables: {
      under_5: 'B01001_003E',
      age_5_9: 'B01001_004E',
      age_10_14: 'B01001_005E',
      age_15_17: 'B01001_006E',
      age_18_19: 'B01001_007E',
      age_20_24: 'B01001_010E',
      age_25_34: 'B01001_011E',
      age_35_44: 'B01001_012E',
      age_45_54: 'B01001_013E',
      age_55_64: 'B01001_016E',
      age_65_74: 'B01001_020E',
      age_75_84: 'B01001_023E',
      age_85_plus: 'B01001_025E',
    },
  }),

  censusACS({
    id: 'census-citizenship',
    label: 'Census Citizenship & Nativity',
    layers: [1, 2, 8],
    variables: {
      total_pop: 'B05001_001E',
      us_citizen_born_us: 'B05001_002E',
      us_citizen_born_pr: 'B05001_003E',
      us_citizen_born_abroad: 'B05001_004E',
      us_citizen_naturalized: 'B05001_005E',
      not_us_citizen: 'B05001_006E',
    },
  }),

  censusACS({
    id: 'census-language',
    label: 'Census Language Spoken at Home',
    layers: [2, 7, 8],
    variables: {
      pop_5_plus: 'B16001_001E',
      english_only: 'B16001_002E',
      spanish: 'B16001_003E',
      spanish_limited_english: 'B16001_005E',
      chinese: 'B16001_006E',
      vietnamese: 'B16001_009E',
      korean: 'B16001_012E',
      arabic: 'B16001_030E',
      other_languages: 'B16001_033E',
    },
  }),

  censusACS({
    id: 'census-mobility',
    label: 'Census Geographic Mobility',
    layers: [5, 8],
    variables: {
      pop_1yr_plus: 'B07001_001E',
      same_house: 'B07001_017E',
      moved_within_county: 'B07001_033E',
      moved_diff_county_same_state: 'B07001_049E',
      moved_diff_state: 'B07001_065E',
      moved_from_abroad: 'B07001_081E',
    },
  }),

  censusACS({
    id: 'census-household-type',
    label: 'Census Household Type & Size',
    layers: [5, 8],
    variables: {
      total_households: 'B11001_001E',
      family_households: 'B11001_002E',
      married_couple: 'B11001_003E',
      male_householder_no_spouse: 'B11001_005E',
      female_householder_no_spouse: 'B11001_006E',
      nonfamily_households: 'B11001_007E',
      living_alone: 'B11001_008E',
      avg_household_size: 'B25010_001E',
    },
  }),

  censusACS({
    id: 'census-grandparents',
    label: 'Census Grandparents as Caregivers',
    layers: [4, 8],
    variables: {
      grandparents_living_with: 'B10001_001E',
      grandparents_responsible: 'B10001_002E',
      responsible_under_1yr: 'B10002_002E',
      responsible_1_2yr: 'B10002_003E',
      responsible_3_4yr: 'B10002_004E',
      responsible_5_plus_yr: 'B10002_005E',
    },
  }),

  censusACS({
    id: 'census-children',
    label: 'Census Children & Family Structure',
    layers: [7, 8],
    variables: {
      children_total: 'B09001_001E',
      children_in_families: 'B09001_002E',
      children_with_two_parents: 'B09002_002E',
      children_with_mother_only: 'B09002_009E',
      children_with_father_only: 'B09002_015E',
      children_no_parent: 'B09002_020E',
    },
  }),

  censusACS({
    id: 'census-marital-status',
    label: 'Census Marital Status',
    layers: [8],
    variables: {
      pop_15_plus: 'B12001_001E',
      never_married_male: 'B12001_003E',
      never_married_female: 'B12001_012E',
      married_male: 'B12001_004E',
      married_female: 'B12001_013E',
      divorced_male: 'B12001_010E',
      divorced_female: 'B12001_019E',
      widowed_male: 'B12001_009E',
      widowed_female: 'B12001_018E',
    },
  }),

  censusACS({
    id: 'census-veteran-status',
    label: 'Census Veteran Status',
    layers: [1, 4, 6],
    variables: {
      civilian_pop_18plus: 'B21001_001E',
      veteran: 'B21001_002E',
      nonveteran: 'B21001_003E',
      male_veteran: 'B21001_005E',
      female_veteran: 'B21001_023E',
    },
  }),

  censusACS({
    id: 'census-group-quarters',
    label: 'Census Group Quarters',
    layers: [5, 8],
    variables: {
      total_gq_pop: 'B26001_001E',
      // Institutional: correctional, nursing, juvenile, etc.
      // Non-institutional: college, military, etc.
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // INCOME & POVERTY (Layer 3: Fiscal, Layer 6: Economic)
  // ══════════════════════════════════════════════════════════════════

  censusACS({
    id: 'census-income',
    label: 'Census Income & Poverty',
    layers: [3, 6],
    variables: {
      median_household_income: 'B19013_001E',
      per_capita_income: 'B19301_001E',
      poverty_total: 'B17001_001E',
      poverty_below: 'B17001_002E',
      gini_index: 'B19083_001E',
      snap_households: 'B22003_002E',
      public_assistance_income: 'B19057_002E',
      ssi_income: 'B19056_002E',
    },
  }),

  censusACS({
    id: 'census-income-distribution',
    label: 'Census Household Income Distribution',
    layers: [3, 6],
    variables: {
      total_households: 'B19001_001E',
      income_under_10k: 'B19001_002E',
      income_10k_15k: 'B19001_003E',
      income_15k_20k: 'B19001_004E',
      income_20k_25k: 'B19001_005E',
      income_25k_30k: 'B19001_006E',
      income_30k_35k: 'B19001_007E',
      income_35k_40k: 'B19001_008E',
      income_40k_45k: 'B19001_009E',
      income_45k_50k: 'B19001_010E',
      income_50k_60k: 'B19001_011E',
      income_60k_75k: 'B19001_012E',
      income_75k_100k: 'B19001_013E',
      income_100k_125k: 'B19001_014E',
      income_125k_150k: 'B19001_015E',
      income_150k_200k: 'B19001_016E',
      income_200k_plus: 'B19001_017E',
    },
  }),

  censusACS({
    id: 'census-poverty-detail',
    label: 'Census Poverty by Age & Sex',
    layers: [3, 6],
    variables: {
      poverty_det_total: 'B17001_001E',
      poverty_below_total: 'B17001_002E',
      poverty_male_under5: 'B17001_003E',
      poverty_male_5: 'B17001_004E',
      poverty_male_6_11: 'B17001_005E',
      poverty_male_12_14: 'B17001_006E',
      poverty_male_15: 'B17001_007E',
      poverty_male_16_17: 'B17001_008E',
      poverty_male_18_24: 'B17001_009E',
      poverty_male_25_34: 'B17001_010E',
      poverty_male_35_44: 'B17001_011E',
      poverty_male_45_54: 'B17001_012E',
      poverty_male_55_64: 'B17001_013E',
      poverty_male_65_74: 'B17001_014E',
      poverty_male_75_plus: 'B17001_015E',
    },
  }),

  censusACS({
    id: 'census-earnings',
    label: 'Census Individual Earnings',
    layers: [3, 6],
    variables: {
      total_with_earnings: 'B20001_001E',
      earnings_1_2500: 'B20001_002E',
      earnings_2500_5000: 'B20001_003E',
      earnings_5000_7500: 'B20001_004E',
      earnings_7500_10000: 'B20001_005E',
      earnings_10000_12500: 'B20001_006E',
      earnings_12500_15000: 'B20001_007E',
      earnings_15000_17500: 'B20001_008E',
      earnings_25000_30000: 'B20001_012E',
      earnings_50000_65000: 'B20001_018E',
      earnings_100000_plus: 'B20001_024E',
      median_earnings: 'B20002_001E',
    },
  }),

  censusACS({
    id: 'census-snap-detail',
    label: 'Census SNAP/Food Stamps Detail',
    layers: [1, 3],
    variables: {
      total_households_snap: 'B22001_001E',
      received_snap: 'B22001_002E',
      not_received_snap: 'B22001_005E',
      snap_below_poverty: 'B22002_003E',
      snap_above_poverty: 'B22002_006E',
    },
    transform: (data) => ({
      ...data,
      snap_participation_rate: data.total_households_snap > 0
        ? Math.round((data.received_snap / data.total_households_snap) * 1000) / 10
        : null,
    }),
  }),

  censusACS({
    id: 'census-public-assistance',
    label: 'Census Public Assistance Income',
    layers: [1, 3],
    variables: {
      total_households_pa: 'B19057_001E',
      with_public_assistance: 'B19057_002E',
      without_public_assistance: 'B19057_003E',
      with_ssi: 'B19056_002E',
      without_ssi: 'B19056_003E',
      with_retirement: 'B19059_002E',
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // HOUSING (Layer 5: Housing)
  // ══════════════════════════════════════════════════════════════════

  censusACS({
    id: 'census-housing',
    label: 'Census Housing',
    layers: [5],
    variables: {
      total_units: 'B25001_001E',
      occupied_units: 'B25002_002E',
      vacant_units: 'B25002_003E',
      owner_occupied: 'B25003_002E',
      renter_occupied: 'B25003_003E',
      median_home_value: 'B25077_001E',
      median_gross_rent: 'B25064_001E',
      median_monthly_housing_cost: 'B25105_001E',
    },
  }),

  censusACS({
    id: 'census-rent-burden',
    label: 'Census Rent Burden',
    layers: [3, 5],
    variables: {
      rent_total: 'B25070_001E',
      rent_30_35_pct: 'B25070_007E',
      rent_35_40_pct: 'B25070_008E',
      rent_40_50_pct: 'B25070_009E',
      rent_50_plus_pct: 'B25070_010E',
      rent_not_computed: 'B25070_011E',
    },
  }),

  censusACS({
    id: 'census-housing-age',
    label: 'Census Housing Age (Year Built)',
    layers: [5, 9],
    variables: {
      total_structures: 'B25034_001E',
      built_2020_later: 'B25034_002E',
      built_2010_2019: 'B25034_003E',
      built_2000_2009: 'B25034_004E',
      built_1990_1999: 'B25034_005E',
      built_1980_1989: 'B25034_006E',
      built_1970_1979: 'B25034_007E',
      built_1960_1969: 'B25034_008E',
      built_1950_1959: 'B25034_009E',
      built_1940_1949: 'B25034_010E',
      built_1939_earlier: 'B25034_011E',
    },
    transform: (data) => ({
      ...data,
      pre_1980_pct: data.total_structures > 0
        ? Math.round(((data.built_1970_1979 || 0) + (data.built_1960_1969 || 0) +
          (data.built_1950_1959 || 0) + (data.built_1940_1949 || 0) +
          (data.built_1939_earlier || 0)) / data.total_structures * 1000) / 10
        : null,
      // Lead paint risk proxy — pre-1978 housing
    }),
  }),

  censusACS({
    id: 'census-housing-units-structure',
    label: 'Census Housing Units in Structure',
    layers: [5],
    variables: {
      total_units_str: 'B25024_001E',
      detached_1unit: 'B25024_002E',
      attached_1unit: 'B25024_003E',
      units_2: 'B25024_004E',
      units_3_4: 'B25024_005E',
      units_5_9: 'B25024_006E',
      units_10_19: 'B25024_007E',
      units_20_49: 'B25024_008E',
      units_50_plus: 'B25024_009E',
      mobile_home: 'B25024_010E',
      boat_rv_van: 'B25024_011E',
    },
  }),

  censusACS({
    id: 'census-housing-cost-mortgage',
    label: 'Census Monthly Housing Costs (Owners)',
    layers: [3, 5],
    variables: {
      total_with_mortgage: 'B25087_001E',
      mortgage_under_500: 'B25087_002E',
      mortgage_500_999: 'B25087_003E',
      mortgage_1000_1499: 'B25087_009E',
      mortgage_1500_1999: 'B25087_015E',
      mortgage_2000_2499: 'B25087_021E',
      mortgage_2500_2999: 'B25087_027E',
      mortgage_3000_plus: 'B25087_033E',
    },
  }),

  censusACS({
    id: 'census-vacancy-status',
    label: 'Census Vacancy Status Detail',
    layers: [5],
    variables: {
      total_vacant: 'B25004_001E',
      for_rent: 'B25004_002E',
      rented_not_occupied: 'B25004_003E',
      for_sale: 'B25004_004E',
      sold_not_occupied: 'B25004_005E',
      seasonal: 'B25004_006E',
      migrant_workers: 'B25004_007E',
      other_vacant: 'B25004_008E',
    },
  }),

  censusACS({
    id: 'census-heating-fuel',
    label: 'Census House Heating Fuel',
    layers: [5, 9],
    variables: {
      total_occupied_fuel: 'B25040_001E',
      utility_gas: 'B25040_002E',
      bottled_tank_lp: 'B25040_003E',
      electricity: 'B25040_004E',
      fuel_oil: 'B25040_005E',
      coal: 'B25040_006E',
      wood: 'B25040_007E',
      solar: 'B25040_008E',
      no_fuel: 'B25040_010E',
    },
  }),

  censusACS({
    id: 'census-plumbing-kitchen',
    label: 'Census Plumbing & Kitchen Facilities',
    layers: [4, 5],
    variables: {
      total_plumbing: 'B25047_001E',
      complete_plumbing: 'B25047_002E',
      lacking_plumbing: 'B25047_003E',
      total_kitchen: 'B25051_001E',
      complete_kitchen: 'B25051_002E',
      lacking_kitchen: 'B25051_003E',
    },
  }),

  censusACS({
    id: 'census-overcrowding',
    label: 'Census Overcrowding (Occupants per Room)',
    layers: [4, 5],
    variables: {
      total_occ: 'B25014_001E',
      owner_1_or_less: 'B25014_003E',
      owner_1_01_1_50: 'B25014_004E',
      owner_1_51_2: 'B25014_005E',
      owner_2_01_plus: 'B25014_006E',
      renter_1_or_less: 'B25014_009E',
      renter_1_01_1_50: 'B25014_010E',
      renter_1_51_2: 'B25014_011E',
      renter_2_01_plus: 'B25014_012E',
    },
    transform: (data) => ({
      ...data,
      overcrowded_pct: data.total_occ > 0
        ? Math.round(((data.owner_1_01_1_50 || 0) + (data.owner_1_51_2 || 0) +
          (data.owner_2_01_plus || 0) + (data.renter_1_01_1_50 || 0) +
          (data.renter_1_51_2 || 0) + (data.renter_2_01_plus || 0)) / data.total_occ * 1000) / 10
        : null,
    }),
  }),

  // ══════════════════════════════════════════════════════════════════
  // HEALTH & INSURANCE (Layer 4: Health)
  // ══════════════════════════════════════════════════════════════════

  censusACS({
    id: 'census-health-insurance',
    label: 'Census Health Insurance',
    layers: [4],
    variables: {
      total_pop_insurance: 'B27001_001E',
      with_insurance: 'B27001_004E',
      male_under6_uninsured: 'B27001_005E',
      male_6_18_uninsured: 'B27001_008E',
      female_under6_uninsured: 'B27001_033E',
      female_6_18_uninsured: 'B27001_036E',
      medicaid_means_tested: 'B27007_004E',
      employer_insurance: 'B27010_003E',
    },
  }),

  censusACS({
    id: 'census-insurance-type',
    label: 'Census Health Insurance Type',
    layers: [4],
    variables: {
      total_civilian: 'B27010_001E',
      employer_provided: 'B27010_003E',
      direct_purchase: 'B27010_010E',
      medicare: 'B27010_017E',
      medicaid: 'B27010_024E',
      tricare: 'B27010_031E',
      va: 'B27010_037E',
      no_insurance: 'B27010_050E',
    },
  }),

  censusACS({
    id: 'census-disability',
    label: 'Census Disability',
    layers: [1, 4],
    variables: {
      total_disability_pop: 'B18101_001E',
      male_with_disability: 'B18101_004E',
      female_with_disability: 'B18101_023E',
      disability_under5: 'B18101_003E',
      disability_5_17: 'B18101_006E',
      disability_18_34: 'B18101_009E',
      disability_65_74: 'B18101_015E',
      disability_75_plus: 'B18101_018E',
    },
  }),

  censusACS({
    id: 'census-disability-type',
    label: 'Census Disability Type',
    layers: [1, 4],
    variables: {
      hearing_difficulty: 'B18102_004E',
      vision_difficulty: 'B18103_004E',
      cognitive_difficulty: 'B18104_004E',
      ambulatory_difficulty: 'B18105_004E',
      self_care_difficulty: 'B18106_004E',
      independent_living_difficulty: 'B18107_004E',
    },
  }),

  censusACS({
    id: 'census-disability-employment',
    label: 'Census Disability & Employment',
    layers: [4, 6],
    variables: {
      total_18_64: 'B18120_001E',
      with_disability_employed: 'B18120_003E',
      with_disability_unemployed: 'B18120_004E',
      with_disability_not_in_labor: 'B18120_005E',
      no_disability_employed: 'B18120_007E',
      no_disability_unemployed: 'B18120_008E',
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // EDUCATION (Layer 7: Education)
  // ══════════════════════════════════════════════════════════════════

  censusACS({
    id: 'census-education',
    label: 'Census Education',
    layers: [7],
    variables: {
      edu_pop_25plus: 'B15003_001E',
      less_than_9th: 'B15003_002E',
      high_school_diploma: 'B15003_017E',
      some_college: 'B15003_019E',
      bachelors: 'B15003_022E',
      masters: 'B15003_023E',
      doctorate: 'B15003_025E',
      school_enrollment_total: 'B14001_001E',
      school_enrollment_public: 'B14002_003E',
    },
  }),

  censusACS({
    id: 'census-school-enrollment',
    label: 'Census School Enrollment Detail',
    layers: [7],
    variables: {
      enrolled_total: 'B14001_001E',
      enrolled_nursery: 'B14001_003E',
      enrolled_k_8: 'B14001_005E',
      enrolled_9_12: 'B14001_006E',
      enrolled_undergraduate: 'B14001_008E',
      enrolled_graduate: 'B14001_009E',
      not_enrolled: 'B14001_010E',
    },
  }),

  censusACS({
    id: 'census-education-by-race',
    label: 'Census Educational Attainment by Race',
    layers: [7, 8],
    variables: {
      white_bachelors_plus: 'C15002A_006E',
      white_total_25plus: 'C15002A_001E',
      black_bachelors_plus: 'C15002B_006E',
      black_total_25plus: 'C15002B_001E',
      hispanic_bachelors_plus: 'C15002I_006E',
      hispanic_total_25plus: 'C15002I_001E',
      asian_bachelors_plus: 'C15002D_006E',
      asian_total_25plus: 'C15002D_001E',
    },
  }),

  censusACS({
    id: 'census-field-of-degree',
    label: 'Census Field of Bachelor\'s Degree',
    layers: [6, 7],
    variables: {
      total_bachelors: 'B15012_001E',
      science_engineering: 'B15012_002E',
      science_engineering_related: 'B15012_009E',
      business: 'B15012_010E',
      education: 'B15012_011E',
      arts_humanities: 'B15012_014E',
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // EMPLOYMENT & OCCUPATION (Layer 6: Economic)
  // ══════════════════════════════════════════════════════════════════

  censusACS({
    id: 'census-employment',
    label: 'Census Employment',
    layers: [6],
    variables: {
      pop_16_plus: 'B23025_001E',
      in_labor_force: 'B23025_002E',
      civilian_employed: 'B23025_004E',
      civilian_unemployed: 'B23025_005E',
      not_in_labor_force: 'B23025_007E',
      occupation_mgmt: 'C24010_003E',
      occupation_service: 'C24010_019E',
      occupation_production: 'C24010_030E',
    },
  }),

  censusACS({
    id: 'census-industry',
    label: 'Census Industry of Employment',
    layers: [6],
    variables: {
      total_employed_16plus: 'C24030_001E',
      agriculture: 'C24030_003E',
      construction: 'C24030_006E',
      manufacturing: 'C24030_007E',
      wholesale: 'C24030_008E',
      retail: 'C24030_009E',
      transportation: 'C24030_010E',
      information: 'C24030_013E',
      finance_insurance: 'C24030_014E',
      professional_scientific: 'C24030_017E',
      education_health: 'C24030_021E',
      arts_entertainment_food: 'C24030_024E',
      public_admin: 'C24030_027E',
    },
  }),

  censusACS({
    id: 'census-class-of-worker',
    label: 'Census Class of Worker',
    layers: [6],
    variables: {
      total_civilian_employed: 'B24080_001E',
      private_wage: 'B24080_002E',
      self_employed_incorporated: 'B24080_009E',
      self_employed_not_inc: 'B24080_010E',
      government_local: 'B24080_004E',
      government_state: 'B24080_005E',
      government_federal: 'B24080_006E',
      unpaid_family: 'B24080_011E',
    },
  }),

  censusACS({
    id: 'census-work-hours',
    label: 'Census Usual Hours Worked',
    layers: [6],
    variables: {
      total_workers_16plus: 'B23018_001E',
      worked_1_14hrs: 'B23018_002E',
      worked_15_34hrs: 'B23018_003E',
      worked_35_39hrs: 'B23018_004E',
      worked_40hrs: 'B23018_005E',
      worked_41_48hrs: 'B23018_006E',
      worked_49_59hrs: 'B23018_007E',
      worked_60_plus: 'B23018_008E',
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // TRANSPORTATION & COMMUTE (Layer 5, 9)
  // ══════════════════════════════════════════════════════════════════

  censusACS({
    id: 'census-commute',
    label: 'Census Commute & Transportation',
    layers: [5, 9],
    variables: {
      workers_total: 'B08301_001E',
      drove_alone: 'B08301_003E',
      public_transit: 'B08301_010E',
      walked: 'B08301_019E',
      worked_from_home: 'B08301_021E',
      mean_travel_time: 'B08135_001E',
      no_vehicle: 'B08014_002E',
      one_vehicle: 'B08014_003E',
    },
  }),

  censusACS({
    id: 'census-vehicle-availability',
    label: 'Census Vehicle Availability',
    layers: [5, 6],
    variables: {
      total_occupied_vehicles: 'B25044_001E',
      owner_no_vehicle: 'B25044_003E',
      owner_1_vehicle: 'B25044_004E',
      owner_2_vehicles: 'B25044_005E',
      owner_3_plus: 'B25044_006E',
      renter_no_vehicle: 'B25044_009E',
      renter_1_vehicle: 'B25044_010E',
      renter_2_vehicles: 'B25044_011E',
      renter_3_plus: 'B25044_012E',
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // INTERNET & TECHNOLOGY (Layer 2: Systems, Layer 7)
  // ══════════════════════════════════════════════════════════════════

  censusACS({
    id: 'census-internet',
    label: 'Census Internet & Technology',
    layers: [2, 7],
    variables: {
      total_households_internet: 'B28002_001E',
      with_internet: 'B28002_002E',
      broadband: 'B28002_004E',
      no_internet: 'B28002_013E',
      has_computer: 'B28001_002E',
      has_smartphone_only: 'B28001_005E',
      no_computer: 'B28001_011E',
    },
  }),

  censusACS({
    id: 'census-internet-by-age',
    label: 'Census Internet by Age',
    layers: [2, 7],
    variables: {
      total_hh_internet_age: 'B28005_001E',
      under18_with: 'B28005_003E',
      under18_without: 'B28005_006E',
      age18_64_with: 'B28005_009E',
      age18_64_without: 'B28005_012E',
      age65_plus_with: 'B28005_015E',
      age65_plus_without: 'B28005_018E',
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // FERTILITY & BIRTH (Layer 4, 8)
  // ══════════════════════════════════════════════════════════════════

  censusACS({
    id: 'census-fertility',
    label: 'Census Fertility (Women Who Gave Birth)',
    layers: [4, 8],
    variables: {
      women_15_50: 'B13002_001E',
      gave_birth: 'B13002_002E',
      did_not_give_birth: 'B13002_011E',
      gave_birth_unmarried: 'B13002_006E',
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // POVERTY RATIOS (Layer 1: Legal, Layer 3: Fiscal)
  // ══════════════════════════════════════════════════════════════════

  censusACS({
    id: 'census-poverty-ratio',
    label: 'Census Poverty Ratio Distribution',
    layers: [1, 3],
    variables: {
      total_for_ratio: 'C17002_001E',
      under_50_pct_fpl: 'C17002_002E',
      pct_50_99_fpl: 'C17002_003E',
      pct_100_124_fpl: 'C17002_004E',
      pct_125_149_fpl: 'C17002_005E',
      pct_150_184_fpl: 'C17002_006E',
      pct_185_199_fpl: 'C17002_007E',
      pct_200_plus_fpl: 'C17002_008E',
    },
    transform: (data) => ({
      ...data,
      deep_poverty_pct: data.total_for_ratio > 0
        ? Math.round((data.under_50_pct_fpl / data.total_for_ratio) * 1000) / 10
        : null,
      near_poverty_pct: data.total_for_ratio > 0
        ? Math.round(((data.pct_100_124_fpl + data.pct_125_149_fpl) / data.total_for_ratio) * 1000) / 10
        : null,
    }),
  }),

  // ══════════════════════════════════════════════════════════════════
  // BENEFITS CLIFF INDICATORS (Layer 1, 3, 6)
  // ══════════════════════════════════════════════════════════════════

  censusACS({
    id: 'census-income-by-family-type',
    label: 'Census Income by Family Type',
    layers: [3, 6],
    variables: {
      total_families_income: 'B19126_001E',
      married_median: 'B19126_002E',
      male_hh_no_wife_median: 'B19126_004E',
      female_hh_no_husband_median: 'B19126_006E',
    },
  }),

  censusACS({
    id: 'census-median-income-by-race',
    label: 'Census Median Income by Race',
    layers: [3, 6, 8],
    variables: {
      median_white: 'B19013A_001E',
      median_black: 'B19013B_001E',
      median_aian: 'B19013C_001E',
      median_asian: 'B19013D_001E',
      median_nhpi: 'B19013E_001E',
      median_hispanic: 'B19013I_001E',
      median_two_plus_races: 'B19013G_001E',
    },
  }),
]
