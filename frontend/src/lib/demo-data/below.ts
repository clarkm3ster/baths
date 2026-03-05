/**
 * BELOW — Environmental baseline and research layers for the
 * North Broad Concourse (the founding SPHERE).
 *
 * "BELOW" refers to both the physical location (below Broad Street)
 * and the research program studying what happens when you make
 * abandoned infrastructure programmable.
 */

export interface EnvironmentalBaseline {
  location: string;
  depth_ft: number;
  area_sqft: number;
  temperature: { mean_f: number; range_f: number; source: string };
  humidity: { mean_pct: number; range_pct: number; source: string };
  acoustics: {
    reverb_time_s: number;
    ambient_db: number;
    train_pulse_db: number;
    train_frequency_s: number;
  };
  vibration: {
    baseline_mm_s: number;
    train_peak_mm_s: number;
    train_interval_s: number;
    source: string;
  };
  air_quality: {
    pm25: number;
    co2_ppm: number;
    radon_pci_l: number;
    ventilation_cfm: number;
  };
  structural: {
    ceiling_height_ft: number;
    column_spacing_ft: number;
    floor_material: string;
    wall_material: string;
    load_bearing_psf: number;
  };
}

export const BASELINE: EnvironmentalBaseline = {
  location: "N Broad St & W Lehigh Ave — BSL Concourse Level",
  depth_ft: 35,
  area_sqft: 48000,
  temperature: {
    mean_f: 58,
    range_f: 2,
    source: "Underground thermal mass — constant year-round",
  },
  humidity: {
    mean_pct: 97,
    range_pct: 6,
    source: "Groundwater seepage + condensation on concrete",
  },
  acoustics: {
    reverb_time_s: 7.2,
    ambient_db: 32,
    train_pulse_db: 78,
    train_frequency_s: 90,
  },
  vibration: {
    baseline_mm_s: 0.05,
    train_peak_mm_s: 4.2,
    train_interval_s: 90,
    source: "BSL northbound/southbound — Lehigh Station",
  },
  air_quality: {
    pm25: 8.2,
    co2_ppm: 620,
    radon_pci_l: 2.1,
    ventilation_cfm: 12000,
  },
  structural: {
    ceiling_height_ft: 14,
    column_spacing_ft: 25,
    floor_material: "Poured concrete (1928)",
    wall_material: "Glazed tile over reinforced concrete",
    load_bearing_psf: 250,
  },
};

// ── Research layers ─────────────────────────────────────────────

export interface ResearchLayer {
  id: string;
  title: string;
  domain: string;
  question: string;
  methodology: string;
  current_findings: string;
  material_systems_involved: string[];
  status: "active" | "planned" | "completed";
}

export const RESEARCH_LAYERS: ResearchLayer[] = [
  {
    id: "rl-001",
    title: "Acoustic Memory",
    domain: "psychoacoustics",
    question:
      "Does a 7.2-second reverb tail create measurably different emotional responses than a 1.8s controlled tail?",
    methodology:
      "A/B exposure with galvanic skin response, self-report, and behavioral tracking across 200 participants",
    current_findings:
      "Natural reverb correlates with 23% higher reported 'awe' scores. Controlled reverb preferred for speech intelligibility tasks.",
    material_systems_involved: ["acoustic_metamaterial"],
    status: "active",
  },
  {
    id: "rl-002",
    title: "Chromatic Wayfinding",
    domain: "spatial cognition",
    question:
      "Can electrochromic wall color gradients replace traditional signage for navigation in underground spaces?",
    methodology:
      "Maze navigation study with color-only vs signage-only vs combined conditions",
    current_findings:
      "Color gradients reduced wayfinding time by 31% vs signage alone. Participants with color vision deficiency navigated using brightness gradients.",
    material_systems_involved: ["electrochromic_surface"],
    status: "active",
  },
  {
    id: "rl-003",
    title: "Haptic Ghost Infrastructure",
    domain: "embodied cognition",
    question:
      "When floor tiles vibrate to trace former rail lines, does physical awareness of buried infrastructure change civic attachment?",
    methodology:
      "Pre/post survey with haptic-on vs haptic-off conditions, 6-month longitudinal follow-up",
    current_findings:
      "Preliminary: haptic condition participants 2.4x more likely to attend community meetings about the concourse's future.",
    material_systems_involved: ["haptic_surface"],
    status: "active",
  },
  {
    id: "rl-004",
    title: "Thermal Comfort in Constant Environments",
    domain: "building science",
    question:
      "Does maintaining 58°F feel different than 72°F when humidity is 97%? What is the true comfort band underground?",
    methodology:
      "Phase-change panel manipulation across 54-68°F range with comfort voting",
    current_findings:
      "Optimal comfort at 62°F / 85% RH — not the 72°F/45% office standard. Underground spaces have fundamentally different comfort physics.",
    material_systems_involved: ["phase_change_panel"],
    status: "active",
  },
  {
    id: "rl-005",
    title: "Olfactory Place Identity",
    domain: "environmental psychology",
    question:
      "Can a synthesized scent signature create place attachment comparable to naturally occurring smells?",
    methodology:
      "Scent association study: petrichor + machine oil + ozone blend vs neutral vs surface-level city smells",
    current_findings:
      "The concourse's natural scent profile (concrete dust + groundwater + electrical ozone) rated as 'memorable' by 89% of first-time visitors.",
    material_systems_involved: ["olfactory_synthesis"],
    status: "planned",
  },
];

export function getResearchLayer(id: string): ResearchLayer | undefined {
  return RESEARCH_LAYERS.find((r) => r.id === id);
}
