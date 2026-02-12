/** Narrative data types for the domes-viz cinematic scroll experience. */

export interface NarrativeSection {
  id: string;
  act: string;
  headline: string;
  subline?: string;
  background: "dark" | "mid" | "light";
  sections?: string[];
  marcusStops?: MarcusStop[];
  stats?: AnimatedStat[];
  keyStats?: KeyStat[];
  world?: WorldEmbed;
  ctas?: CTA[];
}

export interface MarcusStop {
  time: string;
  description: string;
}

export interface AnimatedStat {
  value: number;
  prefix: string;
  suffix: string;
  label: string;
}

export interface KeyStat {
  value: string;
  label: string;
}

export interface WorldEmbed {
  worldId: "renaissance" | "broken-capitol" | "personal-dome";
  overlayText: string;
  buttonText: string;
}

export interface CTA {
  label: string;
  href: string;
  description: string;
}
