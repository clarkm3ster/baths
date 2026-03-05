/**
 * Season 1 — "The North Broad Concourse"
 * 5 episodes mapping the transformation of abandoned BSL infrastructure
 * into Philadelphia's first programmable material environment.
 */

export interface Episode {
  number: number;
  title: string;
  logline: string;
  runtime_minutes: number;
  primary_sphere: string;
  material_systems_featured: string[];
  narrative_arc: string;
  key_moments: string[];
  legacy_mode: string;
}

export interface Season {
  id: string;
  title: string;
  tagline: string;
  location: string;
  episodes: Episode[];
  total_runtime_minutes: number;
  material_systems_deployed: string[];
  production_budget_usd: number;
  crew_size: number;
}

export const SEASON_1: Season = {
  id: "s1",
  title: "The North Broad Concourse",
  tagline: "What happens when a city decides to remember what it buried?",
  location: "N Broad St & W Lehigh Ave — BSL Concourse (below grade)",
  total_runtime_minutes: 245,
  material_systems_deployed: [
    "acoustic_metamaterial",
    "electrochromic_surface",
    "projection_mapping",
    "haptic_surface",
    "phase_change_panel",
    "olfactory_synthesis",
    "shape_memory_element",
  ],
  production_budget_usd: 2_400_000,
  crew_size: 18,
  episodes: [
    {
      number: 1,
      title: "Descent",
      logline:
        "A team descends into the abandoned BSL concourse for the first time in 30 years. The space remembers them before they remember it.",
      runtime_minutes: 48,
      primary_sphere: "nbc-001",
      material_systems_featured: [
        "acoustic_metamaterial",
        "projection_mapping",
      ],
      narrative_arc: "establishing",
      key_moments: [
        "First footstep triggers 7.2-second reverb — space is alive",
        "Projection mapping reveals 1928 tile patterns under decades of grime",
        "Train passes overhead — 4.2mm/s vibration pulse becomes the heartbeat",
        "Acoustic metamaterial test: reverb drops from 7.2s to 1.8s in 25ms",
      ],
      legacy_mode: "research_lab",
    },
    {
      number: 2,
      title: "The Nine Senses",
      logline:
        "Each of the 9 material drivers is installed and tested. The concourse transforms from ruin to instrument.",
      runtime_minutes: 52,
      primary_sphere: "nbc-001",
      material_systems_featured: [
        "electrochromic_surface",
        "haptic_surface",
        "phase_change_panel",
        "olfactory_synthesis",
      ],
      narrative_arc: "rising_action",
      key_moments: [
        "Electrochromic walls shift from institutional white to deep cobalt",
        "Haptic floor tiles map the old rail lines — visitors feel the ghost tracks",
        "Phase-change panels stabilize temperature across 48,000 sqft",
        "Olfactory synthesis: petrichor + machine oil + something unnamed",
      ],
      legacy_mode: "research_lab",
    },
    {
      number: 3,
      title: "First Light",
      logline:
        "The first public performance in the activated SPHERE. 200 people experience a space that reacts to their presence.",
      runtime_minutes: 45,
      primary_sphere: "nbc-001",
      material_systems_featured: [
        "acoustic_metamaterial",
        "electrochromic_surface",
        "projection_mapping",
        "haptic_surface",
        "olfactory_synthesis",
      ],
      narrative_arc: "turning_point",
      key_moments: [
        "Audience enters in silence — reverb makes their breathing audible",
        "Walls shift color in response to crowd density — blue to amber to deep red",
        "Train pulse interrupts the performance — becomes part of it",
        "Standing ovation generates 94dB — acoustic system absorbs to protect",
      ],
      legacy_mode: "public_installation",
    },
    {
      number: 4,
      title: "The Settlement",
      logline:
        "Who owns a programmable environment? The city, the artists, the neighborhood, or the space itself? Legal and financial reckoning.",
      runtime_minutes: 50,
      primary_sphere: "nbc-001",
      material_systems_featured: [
        "shape_memory_element",
        "projection_mapping",
      ],
      narrative_arc: "complication",
      key_moments: [
        "Shape memory elements reconfigure walls — the space argues its own case",
        "Community board meeting projected onto concourse walls at 40ft scale",
        "Revenue model revealed: $180/hr production bookings fund free public hours",
        "First Prevention-Backed Security bond priced against space activation data",
      ],
      legacy_mode: "community_space",
    },
    {
      number: 5,
      title: "Permanence",
      logline:
        "The concourse becomes permanent public infrastructure. The SPHERE doesn't end — it becomes the city's new nervous system.",
      runtime_minutes: 50,
      primary_sphere: "nbc-001",
      material_systems_featured: [
        "acoustic_metamaterial",
        "electrochromic_surface",
        "projection_mapping",
        "haptic_surface",
        "phase_change_panel",
        "olfactory_synthesis",
        "shape_memory_element",
      ],
      narrative_arc: "resolution",
      key_moments: [
        "All 7 deployed material systems running in concert for the first time",
        "24-hour cycle: production dawn → public day → community evening → maintenance night",
        "Second SPHERE site announced — Germantown Rail Yard",
        "Final shot: empty concourse, all systems at rest, train pulse continues",
      ],
      legacy_mode: "living_soundstage",
    },
  ],
};

export function getEpisode(number: number): Episode | undefined {
  return SEASON_1.episodes.find((e) => e.number === number);
}
