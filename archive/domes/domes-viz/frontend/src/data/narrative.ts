import type { NarrativeSection } from "./types";

/**
 * NARRATIVE_SECTIONS
 *
 * The complete cinematic scroll narrative for domes.cc.
 * Six acts that move from darkness to light, from brokenness to architecture,
 * from one man's impossible day to a national transformation.
 */
export const NARRATIVE_SECTIONS: NarrativeSection[] = [
  // ──────────────────────────────────────────────────────────────
  // OPENING — Black screen. One sentence. The hook.
  // ──────────────────────────────────────────────────────────────
  {
    id: "opening",
    act: "opening",
    headline: "The government spends $79,000 a year on Marcus.",
    subline: "Nothing gets better.",
    background: "dark",
  },

  // ──────────────────────────────────────────────────────────────
  // ACT 1 — THE PROMISE
  // What government was supposed to be. The dome as metaphor.
  // ──────────────────────────────────────────────────────────────
  {
    id: "promise",
    act: "promise",
    headline: "The Promise",
    background: "dark",
    sections: [
      "The Capitol dome was designed to shelter democracy.",
      "What if government had a dome designed to shelter you?",
      "Not a building. A system. A personal infrastructure that wraps around one person and coordinates everything.",
      "We call it a Dome.",
    ],
    keyStats: [
      { value: "6", label: "systems" },
      { value: "0", label: "coordination" },
    ],
    world: {
      worldId: "renaissance",
      overlayText: "This is what government was supposed to feel like.",
      buttonText: "Enter the Dome",
    },
  },

  // ──────────────────────────────────────────────────────────────
  // ACT 2 — THE REALITY
  // Marcus's day. Six stops. Six failures. One broken system.
  // ──────────────────────────────────────────────────────────────
  {
    id: "reality",
    act: "reality",
    headline: "The Reality",
    background: "dark",
    marcusStops: [
      {
        time: "6:40 AM",
        description:
          "Medicaid office. Take a number. Wait 3 hours. Wrong form.",
      },
      {
        time: "10:15 AM",
        description:
          "Housing authority. Different number. Different wait. Different form.",
      },
      {
        time: "1:00 PM",
        description:
          "Child welfare check-in. 'We need your housing verification.' (Still waiting.)",
      },
      {
        time: "2:30 PM",
        description:
          "Workforce development. 'Do you have your Medicaid card?' (Still processing.)",
      },
      {
        time: "4:00 PM",
        description:
          "Probation office. 'Why did you miss your workforce appointment?' (You were here.)",
      },
      {
        time: "5:30 PM",
        description:
          "Back home. Nothing accomplished. $79,000 spent. Try again tomorrow.",
      },
    ],
    keyStats: [
      { value: "$79,000", label: "per year spent" },
      { value: "6", label: "agencies" },
      { value: "0", label: "coordination" },
      { value: "0", label: "improvement" },
    ],
    world: {
      worldId: "broken-capitol",
      overlayText: "This is what it became.",
      buttonText: "See the Wreckage",
    },
  },

  // ──────────────────────────────────────────────────────────────
  // ACT 3 — THE VISION
  // From darkness to light. What Marcus's life looks like with a Dome.
  // ──────────────────────────────────────────────────────────────
  {
    id: "vision",
    act: "vision",
    headline: "The Vision",
    background: "mid",
    sections: [
      "What if Marcus had a Dome?",
      "One entry point. One coordinator. One record.",
      "His coordinator sees everything: his health needs, his housing situation, his kids' school records, his job training progress.",
      "No more six stops. No more six waits. No more falling through the cracks.",
      "Cost drops from $79,000 to $31,000.",
      "And outcomes actually improve.",
    ],
    keyStats: [
      { value: "$31,000", label: "per year" },
      { value: "1", label: "coordinator" },
      { value: "1", label: "record" },
      { value: "Real", label: "improvement" },
    ],
    world: {
      worldId: "personal-dome",
      overlayText: "This is what we're building.",
      buttonText: "Enter the Vision",
    },
  },

  // ──────────────────────────────────────────────────────────────
  // ACT 4 — THE MATH
  // Clean. White. Numbers that speak for themselves.
  // ──────────────────────────────────────────────────────────────
  {
    id: "math",
    act: "math",
    headline: "The Math",
    background: "light",
    stats: [
      {
        value: 48000,
        prefix: "$",
        suffix: "",
        label: "saved per person per year",
      },
      {
        value: 10000,
        prefix: "",
        suffix: "",
        label: "people in one state pilot",
      },
      {
        value: 480,
        prefix: "$",
        suffix: "M",
        label: "saved per year, one state",
      },
      {
        value: 94,
        prefix: "$",
        suffix: "B",
        label: "saved nationally per year",
      },
    ],
    sections: [
      "Scale it. 10,000 people \u00D7 $48,000 in savings = $480 million per year. In one state.",
      "National scale: $94 billion per year.",
      "Not by spending more. By spending smarter.",
      "Not by adding programs. By connecting them.",
    ],
  },

  // ──────────────────────────────────────────────────────────────
  // ACT 5 — THE CALL
  // The ask. The architecture exists. Help build it.
  // ──────────────────────────────────────────────────────────────
  {
    id: "call",
    act: "call",
    headline: "Build the Dome.",
    subline:
      "The architecture exists. The math works. The technology is ready.",
    background: "light",
    ctas: [
      {
        label: "See the Data",
        href: "/data",
        description: "Explore the government data constellation",
      },
      {
        label: "Build a Profile",
        href: "/profile",
        description: "See how a Dome works for one person",
      },
      {
        label: "Design an Architecture",
        href: "/architect",
        description: "Design the coordination system",
      },
      {
        label: "Join Us",
        href: "#join",
        description: "Help build the Dome",
      },
    ],
  },
];
