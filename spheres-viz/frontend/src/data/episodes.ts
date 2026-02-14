export interface Episode {
  number: number;
  slug: string;
  genre: string;
  genre_color: string;
  title: string;
  subtitle: string;
  location: string;
  coordinates: { lat: number; lng: number };
  mapPosition: { x: number; y: number };
  palette: {
    primary: string;
    secondary: string;
    dark: string;
    accent: string;
  };
  opening_text: string;
  description: string;
  stats: {
    cost_low: number;
    cost_high: number;
    timeline: string;
    permanence_pct: number;
    permanent_elements: string[];
    jobs_created: number;
    people_served: number;
  };
}

export const EPISODES: Episode[] = [
  // ─── EPISODE 1: WATERFRONT ──────────────────────────────────────────
  {
    number: 1,
    slug: 'waterfront',
    genre: 'Magical Realism',
    genre_color: '#7B68EE',
    title: 'The Floating Theater',
    subtitle: 'Where the river remembers how to dream',
    location: 'Pier 68, Delaware River Waterfront',
    coordinates: { lat: 39.9126, lng: -75.1382 },
    mapPosition: { x: 365, y: 340 },
    palette: {
      primary: '#7B68EE',
      secondary: '#4B0082',
      dark: '#0D0B1A',
      accent: '#B8A9FF',
    },
    opening_text:
      'The pier had been rotting for thirty years. Seagulls nested in the pylons. The city had forgotten it existed. Then one morning, a stage appeared on the water \u2014 and the river started telling stories.',
    description:
      'A floating amphitheater built on rehabilitated pier pylons, featuring a retractable stage that rises from the Delaware River. Performances happen at sunset. The audience sits on terraced seating carved from reclaimed shipping containers. Water reflections dance across the stage lights. When the show ends, the stage descends, and the pier becomes a public fishing dock at dawn.',
    stats: {
      cost_low: 280000,
      cost_high: 420000,
      timeline: '14 months',
      permanence_pct: 72,
      permanent_elements: [
        'Dock rehabilitation',
        'Permanent lighting grid',
        'Waterfront public access',
      ],
      jobs_created: 34,
      people_served: 12000,
    },
  },

  // ─── EPISODE 2: CINEMA GARDEN ───────────────────────────────────────
  {
    number: 2,
    slug: 'cinema-garden',
    genre: 'Documentary',
    genre_color: '#00C853',
    title: 'The Cinema Garden',
    subtitle: 'A screen glows where nothing grew',
    location: 'Vacant Lot, Kensington',
    coordinates: { lat: 39.9923, lng: -75.1321 },
    mapPosition: { x: 290, y: 85 },
    palette: {
      primary: '#00C853',
      secondary: '#1B5E20',
      dark: '#0A1F0D',
      accent: '#69F0AE',
    },
    opening_text:
      'The lot had been empty since 1987. Needles in the grass. A chain-link fence with a padlock nobody had the key to. Then someone hung a screen on the old factory wall, planted garden beds between the rows of chairs, and strung lights from pole to pole. The neighborhood came to watch. They stayed to grow.',
    description:
      'An outdoor cinema and community garden occupying a full city block. A permanent screening wall anchors the north end, with tiered seating descending through raised garden beds bursting with vegetables and native flowers. String lights crisscross overhead. At dusk the screen glows and the neighborhood gathers \u2014 documentaries about the city, films made by local kids, cooking shows featuring produce grown ten feet from the audience.',
    stats: {
      cost_low: 180000,
      cost_high: 290000,
      timeline: '10 months',
      permanence_pct: 85,
      permanent_elements: [
        'Raised garden beds',
        'Screening wall',
        'Irrigation system',
      ],
      jobs_created: 22,
      people_served: 8500,
    },
  },

  // ─── EPISODE 3: ROOFTOP ────────────────────────────────────────────
  {
    number: 3,
    slug: 'rooftop',
    genre: 'Action',
    genre_color: '#FF6B6B',
    title: 'The Sky Park',
    subtitle: 'Above the city, the rules change',
    location: 'Vacant Rooftop, Chinatown',
    coordinates: { lat: 39.9550, lng: -75.1556 },
    mapPosition: { x: 250, y: 205 },
    palette: {
      primary: '#FF6B6B',
      secondary: '#8B0000',
      dark: '#1A0A0A',
      accent: '#FF9E9E',
    },
    opening_text:
      'The parking garage had been half-empty for a decade. The top three levels hadn\u2019t seen a car in years. Pigeons owned it. Then someone brought a half-pipe up in pieces and a DJ booth that ran on solar. Word spread. The sky park was born.',
    description:
      'A rooftop skatepark and music venue built atop a decommissioned parking structure. Concrete bowls, quarter-pipes, and rails share the rooftop with a solar-powered DJ booth and graffiti art walls on rotating commission. Views of the city skyline in every direction. Skateboard and music lessons during the day, DJ sets and competitions at sunset.',
    stats: {
      cost_low: 210000,
      cost_high: 340000,
      timeline: '12 months',
      permanence_pct: 90,
      permanent_elements: [
        'Skatepark structures',
        'Sound system housing',
        'Safety railings & ADA ramp',
      ],
      jobs_created: 18,
      people_served: 9500,
    },
  },

  // ─── EPISODE 4: ALLEY ──────────────────────────────────────────────
  {
    number: 4,
    slug: 'alley',
    genre: 'Mystery',
    genre_color: '#E040FB',
    title: 'The Light Alley',
    subtitle: 'Follow the projections and find what the city hides',
    location: 'Service Alley, Old City',
    coordinates: { lat: 39.9505, lng: -75.1445 },
    mapPosition: { x: 310, y: 225 },
    palette: {
      primary: '#E040FB',
      secondary: '#6A1B9A',
      dark: '#150A1A',
      accent: '#EA80FC',
    },
    opening_text:
      'Nobody walked the alley. Dumpsters. Grease traps. A fire escape to nowhere. Then one night the walls lit up. Projections crawled across the brick \u2014 patterns, faces, the history of every building the alley served. People followed the light. They found art.',
    description:
      'A narrow service alley between two blocks of Old City restaurants, transformed into a permanent projection-mapped art corridor. Weather-protected projectors cast rotating installations across the brick walls. Embedded ground lighting guides visitors through. Local artists submit work quarterly. The alley that nobody used becomes the shortcut everyone takes.',
    stats: {
      cost_low: 120000,
      cost_high: 195000,
      timeline: '7 months',
      permanence_pct: 80,
      permanent_elements: [
        'Projection hardware',
        'Gallery wall surfaces',
        'Embedded ground lighting',
      ],
      jobs_created: 14,
      people_served: 16000,
    },
  },

  // ─── EPISODE 5: SOUND GARDEN ───────────────────────────────────────
  {
    number: 5,
    slug: 'sound-garden',
    genre: 'Fantasy',
    genre_color: '#00E5FF',
    title: 'The Sound Garden',
    subtitle: 'Where wind and bronze remember every song',
    location: 'Clearing, FDR Park',
    coordinates: { lat: 39.9050, lng: -75.1780 },
    mapPosition: { x: 185, y: 385 },
    palette: {
      primary: '#00E5FF',
      secondary: '#006064',
      dark: '#0A1215',
      accent: '#84FFFF',
    },
    opening_text:
      'The clearing in FDR Park had been mowed and forgotten for forty years. Then someone placed a bronze harp where the wind hit hardest. It played all night. They added another. And another. Now the park sings.',
    description:
      'A garden of acoustic sculptures and wind instruments scattered through a wooded clearing. Bronze aeolian harps sing in the breeze. Whisper dishes let visitors talk across 100 feet of garden. Winding accessible paths connect listening stations where you can sit and hear layers of natural and sculpted sound. At the center, a meditation circle built from reclaimed Wissahickon stone.',
    stats: {
      cost_low: 160000,
      cost_high: 250000,
      timeline: '9 months',
      permanence_pct: 92,
      permanent_elements: [
        'Bronze sound sculptures',
        'Accessible pathway network',
        'Meditation circle & benches',
      ],
      jobs_created: 12,
      people_served: 7200,
    },
  },

  // ─── EPISODE 6: UNDERPASS ──────────────────────────────────────────
  {
    number: 6,
    slug: 'underpass',
    genre: 'Adventure',
    genre_color: '#76FF03',
    title: 'The Vertical Playground',
    subtitle: 'Climbing the pillars that hold the highway up',
    location: 'Under I-95, South Philadelphia',
    coordinates: { lat: 39.9285, lng: -75.1465 },
    mapPosition: { x: 310, y: 335 },
    palette: {
      primary: '#76FF03',
      secondary: '#33691E',
      dark: '#0D1A05',
      accent: '#B2FF59',
    },
    opening_text:
      'Under I-95, nobody looked up. The concrete pillars held a highway and nothing else. Graffiti. Broken glass. A place you walked through fast. Then someone bolted climbing holds to the pillars. Colored them like candy. Added lights. Now kids hang from the highway and it feels safe instead of threatening.',
    description:
      'A bouldering park and youth recreation center built into the dead space beneath the I-95 overpass. Professional-grade climbing walls wrap the massive concrete highway pillars, with colored holds arranged in routes from beginner to advanced. Proper LED lighting transforms the underpass from threatening to inviting. Crash pads and safety matting cover the ground. A youth program operates daily with free equipment.',
    stats: {
      cost_low: 190000,
      cost_high: 310000,
      timeline: '11 months',
      permanence_pct: 88,
      permanent_elements: [
        'Climbing walls on pillars',
        'Ground surfacing & matting',
        'LED lighting rig',
      ],
      jobs_created: 20,
      people_served: 11000,
    },
  },

  // ─── EPISODE 7: NIGHT MARKET ───────────────────────────────────────
  {
    number: 7,
    slug: 'night-market',
    genre: 'Ensemble Comedy',
    genre_color: '#FFD740',
    title: 'The Night Market',
    subtitle: 'Broad Street after dark, under string lights and steam',
    location: 'Broad Street at Erie, North Philadelphia',
    coordinates: { lat: 39.9868, lng: -75.1556 },
    mapPosition: { x: 220, y: 95 },
    palette: {
      primary: '#FFD740',
      secondary: '#F57F17',
      dark: '#1A1505',
      accent: '#FFE57F',
    },
    opening_text:
      'Broad Street was wide enough for a market. Everyone knew it. Nobody did it. Then one Thursday night in June, twenty folding tables appeared, each one a different kitchen. Steam rose. Music played. Strangers argued about the best empanada. The comedy of a city feeding itself began.',
    description:
      'A weekly night market occupying four blocks of North Broad Street, operating Thursday through Saturday from 6PM to midnight. Dozens of food stalls line both sides of the boulevard, string lights crisscrossing overhead. A music stage anchors one end. The smell of grilling meat mixes with cumbia and jazz. Steam rises into the string lights. Crowds weave between stalls arguing about who has the best plate.',
    stats: {
      cost_low: 340000,
      cost_high: 480000,
      timeline: '13 months',
      permanence_pct: 75,
      permanent_elements: [
        'Vendor electrical hookups',
        'Market pavilion structure',
        'String-light infrastructure',
      ],
      jobs_created: 65,
      people_served: 22000,
    },
  },

  // ─── EPISODE 8: WINTER VILLAGE ─────────────────────────────────────
  {
    number: 8,
    slug: 'winter-village',
    genre: 'Romance',
    genre_color: '#448AFF',
    title: 'The Winter Village',
    subtitle: 'When the city freezes, this place warms',
    location: 'Dilworth Park, City Hall',
    coordinates: { lat: 39.9526, lng: -75.1639 },
    mapPosition: { x: 215, y: 218 },
    palette: {
      primary: '#448AFF',
      secondary: '#1A237E',
      dark: '#0A0D1A',
      accent: '#82B1FF',
    },
    opening_text:
      'Every city has a place where people fall in love in winter. Philadelphia\u2019s was supposed to be City Hall. But the plaza was empty and the wind was brutal. Then someone added cabins, an ice rink, and hot chocolate that cost a dollar. December changed.',
    description:
      'A seasonal winter village occupying the plaza at City Hall, running November through February. An ice rink wraps around the building\u2019s base. Heated wooden cabins house pop-up shops and craft vendors. A central pavilion serves hot drinks on a sliding scale. Fairy lights drape every surface. The cold becomes the reason to come, not the reason to stay home.',
    stats: {
      cost_low: 280000,
      cost_high: 420000,
      timeline: '8 months (seasonal)',
      permanence_pct: 70,
      permanent_elements: [
        'Ice rink plumbing & refrigeration',
        'Power & lighting infrastructure',
        'Heated gathering pavilion',
      ],
      jobs_created: 48,
      people_served: 35000,
    },
  },

  // ─── EPISODE 9: GLOW CORRIDOR ─────────────────────────────────────
  {
    number: 9,
    slug: 'glow-corridor',
    genre: 'Thriller',
    genre_color: '#FF6E40',
    title: 'The Glow Corridor',
    subtitle: 'A mile of light cutting through the dark',
    location: 'Schuylkill Banks, West Philadelphia',
    coordinates: { lat: 39.9565, lng: -75.1850 },
    mapPosition: { x: 155, y: 200 },
    palette: {
      primary: '#FF6E40',
      secondary: '#BF360C',
      dark: '#1A0F0A',
      accent: '#FFAB91',
    },
    opening_text:
      'The riverbank trail went dark at sunset. Runners stopped coming. The path belonged to shadows. Then a mile of solar-powered LED strips appeared overnight, embedded in the pavement like a landing strip. The corridor glowed. The runners returned. They brought everyone.',
    description:
      'A mile-long illuminated fitness and recreation corridor along the Schuylkill Banks. Solar-powered LED path lighting transforms an underused riverbank trail into a safe nighttime destination. Fitness stations dot the route. Rest shelters with solar-charged USB ports offer refuge. At night the corridor pulses with a slow color cycle, visible from both bridges \u2014 a river of light through the dark city.',
    stats: {
      cost_low: 240000,
      cost_high: 380000,
      timeline: '10 months',
      permanence_pct: 93,
      permanent_elements: [
        'Solar LED path lighting',
        'Fitness stations',
        'Rest shelters & seating',
      ],
      jobs_created: 16,
      people_served: 18000,
    },
  },

  // ─── EPISODE 10: RECOVERY GARDEN ───────────────────────────────────
  {
    number: 10,
    slug: 'quiet-garden',
    genre: 'Quiet Drama',
    genre_color: '#FFAB40',
    title: 'The Recovery Garden',
    subtitle: 'Healing grows in the quietest places',
    location: 'Vacant Block, West Philadelphia',
    coordinates: { lat: 39.9565, lng: -75.2184 },
    mapPosition: { x: 85, y: 210 },
    palette: {
      primary: '#FFAB40',
      secondary: '#E65100',
      dark: '#1A1005',
      accent: '#FFD180',
    },
    opening_text:
      'The block had lost three houses to abandonment and one to fire. The lots merged into a single field of rubble and ragweed. Then a woman from the recovery center on the corner planted a Japanese maple in the center. She built a path around it. Then a bench. Then a water feature. The garden grew the way recovery does \u2014 slowly, deliberately, with no part wasted.',
    description:
      'A contemplative garden and counseling space occupying an entire city block. A central water feature anchors a labyrinth of winding stone paths through native plantings. Benches sit in alcoves under mature trees. A small counseling pavilion offers free sessions twice a week. The garden is intentionally quiet \u2014 no amplified sound, no events, no programming after dark. This is the sphere that exists only for stillness.',
    stats: {
      cost_low: 220000,
      cost_high: 350000,
      timeline: '12 months',
      permanence_pct: 100,
      permanent_elements: [
        'The entire garden stays',
        'Water feature',
        'Winding stone paths',
        'Counseling pavilion',
        'Every bench, every tree, every stone',
      ],
      jobs_created: 14,
      people_served: 6000,
    },
  },
];

export function getAggregateStats(episodes: Episode[]) {
  return {
    totalCostLow: episodes.reduce((sum, e) => sum + e.stats.cost_low, 0),
    totalCostHigh: episodes.reduce((sum, e) => sum + e.stats.cost_high, 0),
    totalJobs: episodes.reduce((sum, e) => sum + e.stats.jobs_created, 0),
    totalPeopleServed: episodes.reduce(
      (sum, e) => sum + e.stats.people_served,
      0,
    ),
    avgPermanence: Math.round(
      episodes.reduce((sum, e) => sum + e.stats.permanence_pct, 0) /
        episodes.length,
    ),
  };
}
