export interface Episode {
  number: number;
  slug: string;
  genre: string;
  genre_color: string;
  title: string;
  subtitle: string;
  location: string;
  coordinates: { lat: number; lng: number };
  mapPosition: { x: number; y: number }; // SVG coordinates on Philly map
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
  {
    number: 1,
    slug: 'floating-theater',
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
      'The pier had been rotting for thirty years. Seagulls nested in the pylons. The city had forgotten it existed. Then one morning, a stage appeared on the water — and the river started telling stories.',
    description:
      'A floating amphitheater built on rehabilitated pier pylons, featuring a retractable stage that rises from the Delaware River. Performances happen at sunset. The audience sits on terraced seating carved from reclaimed shipping containers. When the show ends, the stage descends, and the pier becomes a public fishing dock at dawn.',
    stats: {
      cost_low: 280000,
      cost_high: 420000,
      timeline: '14 months',
      permanence_pct: 72,
      permanent_elements: [
        'Pier rehabilitation',
        'Terraced seating',
        'Solar lighting grid',
      ],
      jobs_created: 34,
      people_served: 12000,
    },
  },
  {
    number: 2,
    slug: 'seed-cathedral',
    genre: 'Solarpunk',
    genre_color: '#00C853',
    title: 'The Seed Cathedral',
    subtitle: 'Growing tomorrow from the cracks in today',
    location: 'Vacant Lot, 2300 Block of North Broad Street',
    coordinates: { lat: 39.9782, lng: -75.1556 },
    mapPosition: { x: 220, y: 130 },
    palette: {
      primary: '#00C853',
      secondary: '#1B5E20',
      dark: '#0A1F0D',
      accent: '#69F0AE',
    },
    opening_text:
      'The lot had been empty since 1987. Needles in the grass. A chain-link fence with a padlock nobody had the key to. Then someone planted a single tomato seed in a crack in the sidewalk — and the cathedral began to grow.',
    description:
      'A vertical farm and community greenhouse built inside a tensile fabric structure shaped like a Gothic cathedral. Translucent ETFE panels filter sunlight into prismatic color. Automated hydroponic towers grow 40 varieties of produce distributed free to neighbors within a 10-block radius. Evening programming includes cooking classes, seed-saving workshops, and solstice celebrations.',
    stats: {
      cost_low: 350000,
      cost_high: 520000,
      timeline: '18 months',
      permanence_pct: 85,
      permanent_elements: [
        'Foundation & utilities',
        'Hydroponic infrastructure',
        'Rainwater collection',
      ],
      jobs_created: 28,
      people_served: 8500,
    },
  },
  {
    number: 3,
    slug: 'echo-chamber',
    genre: 'Noir',
    genre_color: '#FF6B6B',
    title: 'The Echo Chamber',
    subtitle: 'The city speaks if you know how to listen',
    location: 'Abandoned Subway Ventilation Shaft, Spring Garden',
    coordinates: { lat: 39.9615, lng: -75.1580 },
    mapPosition: { x: 230, y: 195 },
    palette: {
      primary: '#FF6B6B',
      secondary: '#8B0000',
      dark: '#1A0A0A',
      accent: '#FF9E9E',
    },
    opening_text:
      'Detective work starts with listening. The ventilation shaft had been sealed since 1971. But if you pressed your ear to the grate on Callowhill Street, you could hear the ghost trains. Someone decided to amplify them.',
    description:
      'An underground sound installation and oral history archive built inside a decommissioned subway ventilation shaft. Visitors descend a spiral staircase into a 40-foot chamber where directional speakers play layered recordings: oral histories from the neighborhood, field recordings of the city, and original compositions that respond to the weather above. A noir-inspired cocktail bar operates on weekends in the upper chamber.',
    stats: {
      cost_low: 190000,
      cost_high: 310000,
      timeline: '11 months',
      permanence_pct: 90,
      permanent_elements: [
        'Structural reinforcement',
        'Sound system',
        'Spiral staircase',
        'Climate control',
      ],
      jobs_created: 18,
      people_served: 6200,
    },
  },
  {
    number: 4,
    slug: 'night-market',
    genre: 'Cyberpunk',
    genre_color: '#00E5FF',
    title: 'The Night Market',
    subtitle: 'Commerce after dark, under neon rain',
    location: 'Vacant Industrial Lot, Kensington & Lehigh',
    coordinates: { lat: 39.9923, lng: -75.1321 },
    mapPosition: { x: 290, y: 85 },
    palette: {
      primary: '#00E5FF',
      secondary: '#006064',
      dark: '#0A1215',
      accent: '#84FFFF',
    },
    opening_text:
      'After the last factory closed, the lot became a dumping ground. Shopping carts. Mattresses. A broken neon sign that still flickered OPEN on rainy nights. They kept the sign. They kept the rain. They just added a market.',
    description:
      'A covered night market with retractable transparent roof panels, programmable LED architecture, and 30 micro-vendor stalls. The market operates Thursday through Sunday from 6PM to 2AM. Vendors rotate monthly through a lottery system favoring first-time entrepreneurs. Rain sensors trigger a choreographed light show across the roof panels. A maker space operates during daytime hours.',
    stats: {
      cost_low: 410000,
      cost_high: 580000,
      timeline: '16 months',
      permanence_pct: 78,
      permanent_elements: [
        'Utility infrastructure',
        'Structural frame',
        'LED grid',
        'Maker space buildout',
      ],
      jobs_created: 65,
      people_served: 22000,
    },
  },
  {
    number: 5,
    slug: 'memory-palace',
    genre: 'Gothic Romance',
    genre_color: '#E040FB',
    title: 'The Memory Palace',
    subtitle: 'Where every wall holds a story of someone who loved this place',
    location: 'Vacant Rowhouse Block, Strawberry Mansion',
    coordinates: { lat: 39.9868, lng: -75.1812 },
    mapPosition: { x: 165, y: 100 },
    palette: {
      primary: '#E040FB',
      secondary: '#6A1B9A',
      dark: '#150A1A',
      accent: '#EA80FC',
    },
    opening_text:
      'Five rowhouses in a row, all empty. But the wallpaper remembered. Roses in the parlor. A child\'s handprint in the plaster of the second floor. Love letters found between the joists. They didn\'t demolish the memories — they made a museum of them.',
    description:
      'A connected series of five formerly vacant rowhouses transformed into an immersive memory museum. Each house represents a decade (1950s-1990s) of the neighborhood\'s history, reconstructed from oral histories and donated artifacts. Visitors walk through living rooms, kitchens, and bedrooms frozen in time. The final house is empty — a blank canvas where visitors record their own memories on the walls.',
    stats: {
      cost_low: 520000,
      cost_high: 780000,
      timeline: '24 months',
      permanence_pct: 95,
      permanent_elements: [
        'Structural renovation',
        'Museum buildout',
        'HVAC systems',
        'Archive storage',
      ],
      jobs_created: 22,
      people_served: 15000,
    },
  },
  {
    number: 6,
    slug: 'feral-garden',
    genre: 'Eco-Horror',
    genre_color: '#76FF03',
    title: 'The Feral Garden',
    subtitle: 'Nature does not ask permission',
    location: 'Former Gas Station Site, Point Breeze',
    coordinates: { lat: 39.9318, lng: -75.1780 },
    mapPosition: { x: 185, y: 315 },
    palette: {
      primary: '#76FF03',
      secondary: '#33691E',
      dark: '#0D1A05',
      accent: '#B2FF59',
    },
    opening_text:
      'The gas station had been leaking since 1994. The soil was poisoned. Nothing was supposed to grow there. But mycorrhizal networks don\'t read EPA reports. The fungi came first. Then the flowers. Then the things that eat flowers.',
    description:
      'A bioremediation garden and ecological research station built on a former brownfield site. Specially selected hyperaccumulator plants draw heavy metals from contaminated soil while mycoremediation networks break down petroleum compounds. The garden is deliberately "wild" — no mowing, no manicuring. A raised boardwalk allows visitors to observe without disturbing. Night tours feature bioluminescent fungi installations. Soil testing stations let visitors track the remediation in real time.',
    stats: {
      cost_low: 160000,
      cost_high: 240000,
      timeline: '8 months',
      permanence_pct: 88,
      permanent_elements: [
        'Soil remediation',
        'Boardwalk',
        'Research station',
        'Bioswale system',
      ],
      jobs_created: 12,
      people_served: 4800,
    },
  },
  {
    number: 7,
    slug: 'time-capsule',
    genre: 'Science Fiction',
    genre_color: '#448AFF',
    title: 'The Time Capsule',
    subtitle: 'Messages to a future we may never see',
    location: 'Decommissioned Water Tower, Manayunk',
    coordinates: { lat: 40.0265, lng: -75.2253 },
    mapPosition: { x: 65, y: 40 },
    palette: {
      primary: '#448AFF',
      secondary: '#1A237E',
      dark: '#0A0D1A',
      accent: '#82B1FF',
    },
    opening_text:
      'The water tower hadn\'t held water since 2003. It held pigeons. It held graffiti. It held the memory of a neighborhood that used to make things. Then someone asked: what if it held the future instead?',
    description:
      'A decommissioned water tower converted into a vertical public archive and observatory. The ground floor houses a "letter to the future" station where visitors write messages sealed in archival tubes and stored in the tower walls. The mid-level features an augmented reality timeline showing the neighborhood\'s past and projected futures. The top level is an open-air observatory with telescopes and a 360-degree view of the Schuylkill Valley.',
    stats: {
      cost_low: 380000,
      cost_high: 540000,
      timeline: '20 months',
      permanence_pct: 92,
      permanent_elements: [
        'Tower restoration',
        'Observatory deck',
        'Archive system',
        'Elevator installation',
      ],
      jobs_created: 16,
      people_served: 9200,
    },
  },
  {
    number: 8,
    slug: 'ghost-kitchen',
    genre: 'Comedy',
    genre_color: '#FFD740',
    title: 'The Ghost Kitchen',
    subtitle: 'Grandma\'s recipes never die. They just need a new stove.',
    location: 'Vacant Commercial Strip, Germantown Avenue',
    coordinates: { lat: 40.0342, lng: -75.1720 },
    mapPosition: { x: 175, y: 25 },
    palette: {
      primary: '#FFD740',
      secondary: '#F57F17',
      dark: '#1A1505',
      accent: '#FFE57F',
    },
    opening_text:
      'The storefront had been empty for six years. The awning still said "CHECKS CASHED." But Doris from across the street remembered when it was a bakery. She still had the recipe for the cinnamon rolls. She just needed an oven.',
    description:
      'A rotating community kitchen and food incubator occupying a renovated commercial storefront. Each month, a different neighborhood cook takes over the kitchen to develop and sell their signature dish. A commercial-grade kitchen, dining room for 40, and takeout window operate on a sliding-scale pricing model. Retired cooks mentor aspiring food entrepreneurs. A recipe archive preserves neighborhood food traditions in print and video.',
    stats: {
      cost_low: 220000,
      cost_high: 340000,
      timeline: '10 months',
      permanence_pct: 82,
      permanent_elements: [
        'Commercial kitchen',
        'Dining buildout',
        'Recipe archive system',
      ],
      jobs_created: 42,
      people_served: 18000,
    },
  },
  {
    number: 9,
    slug: 'dream-machine',
    genre: 'Surrealism',
    genre_color: '#FF6E40',
    title: 'The Dream Machine',
    subtitle: 'Close your eyes and build what you see',
    location: 'Vacant Lot Under I-95 Overpass, South Philadelphia',
    coordinates: { lat: 39.9285, lng: -75.1465 },
    mapPosition: { x: 310, y: 335 },
    palette: {
      primary: '#FF6E40',
      secondary: '#BF360C',
      dark: '#1A0F0A',
      accent: '#FFAB91',
    },
    opening_text:
      'Under the highway, the rain doesn\'t fall straight. It spirals. Truckers honk their horns and the echoes make chords. Someone hung a mirror from the overpass and the sky appeared underground. That was the first installation. The rest followed like dreams.',
    description:
      'An outdoor sculpture park and interactive art installation occupying the dead space beneath an I-95 overpass. Large-scale kinetic sculptures respond to traffic vibrations overhead. Sound installations transform highway noise into ambient music. A children\'s imagination workshop operates on weekends, where kids design sculptures that are then fabricated by local metalworkers. Rain channels are sculpted to create waterfalls during storms.',
    stats: {
      cost_low: 150000,
      cost_high: 260000,
      timeline: '9 months',
      permanence_pct: 70,
      permanent_elements: [
        'Ground treatment',
        'Electrical infrastructure',
        'Drainage sculpture',
      ],
      jobs_created: 20,
      people_served: 11000,
    },
  },
  {
    number: 10,
    slug: 'last-library',
    genre: 'Post-Apocalyptic Hope',
    genre_color: '#FFAB40',
    title: 'The Last Library',
    subtitle: 'In the ruins, someone saved the books',
    location: 'Burned-Out Church, West Philadelphia',
    coordinates: { lat: 39.9565, lng: -75.2184 },
    mapPosition: { x: 85, y: 210 },
    palette: {
      primary: '#FFAB40',
      secondary: '#E65100',
      dark: '#1A1005',
      accent: '#FFD180',
    },
    opening_text:
      'The church burned in 2019. The congregation scattered. But the basement survived — and so did the books someone had been quietly storing there for years. Thousands of them. A secret library, waiting for readers who would come after the fire.',
    description:
      'A community library and reading sanctuary built inside the restored shell of a fire-damaged church. The original stone walls remain exposed, with new steel and glass insertions creating reading nooks at multiple levels. A book-sharing network connects 20 Little Free Libraries across West Philadelphia. The basement houses a rare book preservation workshop. The bell tower is converted into a writing residency studio for local authors.',
    stats: {
      cost_low: 480000,
      cost_high: 720000,
      timeline: '22 months',
      permanence_pct: 94,
      permanent_elements: [
        'Structural restoration',
        'Climate-controlled archive',
        'Writing studio',
        'Book network infrastructure',
      ],
      jobs_created: 26,
      people_served: 14000,
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
