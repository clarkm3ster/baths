/**
 * CHARACTER FRAGMENT — Source Works Tracker
 *
 * Tracks every source work discovered — books, films, articles, case studies,
 * oral histories, games, myths. Follows references between works.
 *
 * When a work is cataloged, the tracker:
 * 1. Records the work and its metadata
 * 2. Identifies works it references or is referenced by
 * 3. Queues referenced works for discovery
 * 4. Tracks which works have been fully processed (all characters extracted)
 */

import { readJSON, writeJSON, SOURCE_WORKS_DIR, slugify } from './lib.mjs'
import { join } from 'node:path'

// ── Known reference chains ────────────────────────────────────────────────────
// When we discover work A, we know to look for these related works.

const REFERENCE_CHAINS = {
  'evicted': ['random-family', '$2-a-day', 'there-are-no-children-here', 'gang-leader-for-a-day', 'the-other-america'],
  'random-family': ['evicted', 'invisible-child', 'there-are-no-children-here'],
  'invisible-child': ['random-family', 'evicted', 'there-are-no-children-here'],
  'just-mercy': ['the-new-jim-crow', 'between-the-world-and-me', '13th'],
  'the-new-jim-crow': ['just-mercy', 'are-prisons-obsolete', '13th', 'the-condemnation-of-blackness'],
  'behind-the-beautiful-forevers': ['evicted', 'random-family'],
  'nickel-and-dimed': ['$2-a-day', 'maid', 'hand-to-mouth', 'scratch-beginnings'],
  'the-warmth-of-other-suns': ['the-other-america', 'the-color-of-law', 'caste'],
  'the-color-purple': ['beloved', 'their-eyes-were-watching-god', 'the-bluest-eye'],
  'beloved': ['the-color-purple', 'kindred', 'the-underground-railroad'],
  'native-son': ['invisible-man', 'the-bluest-eye', 'between-the-world-and-me'],
  'the-jungle': ['the-grapes-of-wrath', 'nickel-and-dimed', 'fast-food-nation'],
  'les-miserables': ['oliver-twist', 'a-tale-of-two-cities', 'crime-and-punishment'],
  'the-wire': ['the-corner', 'homicide-a-year-on-the-killing-streets', 'we-own-this-city'],
  'hoop-dreams': ['minding-the-gap', 'dark-days', 'the-interrupters'],
  'making-a-murderer': ['the-staircase', 'the-innocence-files', 'serial'],
  'maus': ['persepolis', 'fun-home', 'march'],
  'angels-in-america': ['the-normal-heart', 'rent', 'pose'],
  'death-of-a-salesman': ['fences', 'glengarry-glen-ross', 'a-raisin-in-the-sun'],
  'a-streetcar-named-desire': ['the-glass-menagerie', 'cat-on-a-hot-tin-roof'],
  'the-handmaids-tale': ['1984', 'brave-new-world', 'the-power'],
  'moonlight': ['the-florida-project', 'beale-street', 'the-last-black-man-in-san-francisco'],
  'parasite': ['roma', 'shoplifters', 'capernaum'],
}

// ── Genre discovery — when we find works in a genre, look for more ────────────

const GENRE_EXPANSIONS = {
  'prison-literature': [
    'Orange Is the New Black', 'In the Place of Justice', 'Newjack', 'The Sun Does Shine',
    'Writing My Wrongs', 'Are Prisons Obsolete?', 'Solitary', 'American Prison',
  ],
  'migration-narratives': [
    'Enrique\'s Journey', 'The Distance Between Us', 'Tell Me How It Ends',
    'The Far Away Brothers', 'Lost Children Archive', 'Exit West',
  ],
  'disability-memoirs': [
    'The Diving Bell and the Butterfly', 'Still Alice', 'The Reason I Jump',
    'My Stroke of Insight', 'Look Me in the Eye', 'The Collected Schizophrenias',
  ],
  'addiction-recovery': [
    'Beautiful Boy', 'Tweak', 'Lit', 'Drinking: A Love Story', 'The Night of the Gun',
    'In the Realm of Hungry Ghosts', 'Sober Curious',
  ],
  'foster-care': [
    'Three Little Words', 'A Place Called Home', 'Another Place at the Table',
    'The Lost Children of Wilder', 'Somebody\'s Someone',
  ],
  'indigenous-narratives': [
    'There There', 'The Absolutely True Diary of a Part-Time Indian',
    'Killers of the Flower Moon', 'An Indigenous Peoples\' History of the United States',
    'Heart Berries', 'Braiding Sweetgrass',
  ],
  'appalachian-poverty': [
    'Night Comes to the Cumberlands', 'Hillbilly Elegy', 'Dopesick',
    'What You Are Getting Wrong About Appalachia', 'Ramp Hollow',
  ],
  'domestic-violence': [
    'No Visible Bruises', 'Why Does He Do That?', 'In the Dream House',
    'Behind Closed Doors', 'A Burning',
  ],
}

// ── Load or initialize the tracker ────────────────────────────────────────────

export function loadTracker() {
  const trackerPath = join(SOURCE_WORKS_DIR, 'tracker.json')
  const existing = readJSON(trackerPath)
  if (existing) return existing

  return {
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    version: 0,
    works: {},
    reference_queue: [],
    genre_queue: [],
    genres_discovered: [],
    total_works: 0,
    total_processed: 0,
  }
}

// ── Register a source work ────────────────────────────────────────────────────

export function registerWork(tracker, work) {
  const id = slugify(work.title || work.source_work)

  if (!tracker.works[id]) {
    tracker.works[id] = {
      id,
      title: work.title || work.source_work,
      authors: work.authors || (work.source_author_creator ? [work.source_author_creator] : []),
      year: work.year || work.source_year,
      type: work.type || inferType(work),
      characters_extracted: 0,
      fully_processed: false,
      first_seen: new Date().toISOString(),
      source_api: work.source_api || 'seed',
      dome_potential: work.dome_potential || null,
    }
    tracker.total_works++

    // Queue references
    const refs = REFERENCE_CHAINS[id] || []
    for (const ref of refs) {
      if (!tracker.works[ref] && !tracker.reference_queue.some(r => r.id === ref)) {
        tracker.reference_queue.push({
          id: ref,
          referenced_by: id,
          queued_at: new Date().toISOString(),
          searched: false,
        })
      }
    }
  }

  return tracker.works[id]
}

// ── Register character extraction for a work ──────────────────────────────────

export function registerCharacterForWork(tracker, workTitle, characterName) {
  const id = slugify(workTitle)
  if (tracker.works[id]) {
    tracker.works[id].characters_extracted++
    tracker.works[id].last_character_added = new Date().toISOString()
  }
}

// ── Mark a work as fully processed ────────────────────────────────────────────

export function markWorkProcessed(tracker, workTitle) {
  const id = slugify(workTitle)
  if (tracker.works[id]) {
    tracker.works[id].fully_processed = true
    tracker.works[id].processed_at = new Date().toISOString()
    tracker.total_processed++
  }
}

// ── Discover genre based on existing works ────────────────────────────────────

export function discoverGenres(tracker) {
  const newGenres = []

  for (const [genre, works] of Object.entries(GENRE_EXPANSIONS)) {
    if (tracker.genres_discovered.includes(genre)) continue

    // Check if we have any works that suggest this genre
    const genreWorks = works.map(w => slugify(w))
    const known = genreWorks.filter(w => tracker.works[w])

    if (known.length > 0 || shouldDiscoverGenre(tracker, genre)) {
      tracker.genres_discovered.push(genre)

      // Queue all unknown works in this genre
      for (const work of works) {
        const wid = slugify(work)
        if (!tracker.works[wid] && !tracker.genre_queue.some(g => g.id === wid)) {
          tracker.genre_queue.push({
            id: wid,
            title: work,
            genre,
            queued_at: new Date().toISOString(),
            searched: false,
          })
        }
      }

      newGenres.push({ genre, works_queued: works.length })
    }
  }

  return newGenres
}

function shouldDiscoverGenre(tracker, genre) {
  // Discover a genre if we have characters with matching circumstances
  const genreCircumstances = {
    'prison-literature': ['incarcerated', 'formerly_incarcerated', 'wrongly_convicted'],
    'migration-narratives': ['immigrant', 'refugee', 'asylum_seeker', 'undocumented'],
    'disability-memoirs': ['disability', 'chronic_illness', 'mental_illness'],
    'addiction-recovery': ['addiction'],
    'foster-care': ['foster_care'],
    'indigenous-narratives': ['indigenous'],
    'appalachian-poverty': ['poverty', 'deep_poverty', 'environmental_exposure'],
    'domestic-violence': ['domestic_violence'],
  }

  // Always discover all genres (they all matter)
  return true
}

// ── Infer work type ───────────────────────────────────────────────────────────

function inferType(work) {
  if (work.source_api === 'TMDB') return 'film'
  if (work.source_api === 'Project Gutenberg') return 'book'
  if (work.media_type === 'movies') return 'film'
  if (work.media_type === 'texts') return 'book'
  if (work.media_type === 'audio') return 'audio'
  return 'book'
}

// ── Save the tracker ──────────────────────────────────────────────────────────

export function saveTracker(tracker) {
  tracker.updated_at = new Date().toISOString()
  tracker.version++
  writeJSON(join(SOURCE_WORKS_DIR, 'tracker.json'), tracker)

  // Write reference queue
  const unresolvedRefs = tracker.reference_queue.filter(r => !r.searched)
  writeJSON(join(SOURCE_WORKS_DIR, 'reference-queue.json'), {
    updated_at: new Date().toISOString(),
    total: tracker.reference_queue.length,
    unresolved: unresolvedRefs.length,
    queue: unresolvedRefs,
  })

  // Write genre queue
  const unresolvedGenres = tracker.genre_queue.filter(g => !g.searched)
  writeJSON(join(SOURCE_WORKS_DIR, 'genre-queue.json'), {
    updated_at: new Date().toISOString(),
    genres_discovered: tracker.genres_discovered,
    total_queued: tracker.genre_queue.length,
    unresolved: unresolvedGenres.length,
    queue: unresolvedGenres,
  })

  // Write per-type catalogs
  const byType = {}
  for (const work of Object.values(tracker.works)) {
    const type = work.type || 'unknown'
    if (!byType[type]) byType[type] = []
    byType[type].push(work)
  }

  for (const [type, works] of Object.entries(byType)) {
    writeJSON(join(SOURCE_WORKS_DIR, `works-${type}.json`), {
      type,
      count: works.length,
      works: works.sort((a, b) => b.characters_extracted - a.characters_extracted),
    })
  }
}

// ── Tracker stats ─────────────────────────────────────────────────────────────

export function trackerStats(tracker) {
  const works = Object.values(tracker.works)
  return {
    total_works: works.length,
    processed: works.filter(w => w.fully_processed).length,
    unprocessed: works.filter(w => !w.fully_processed).length,
    total_characters_extracted: works.reduce((s, w) => s + w.characters_extracted, 0),
    reference_queue: tracker.reference_queue.filter(r => !r.searched).length,
    genre_queue: tracker.genre_queue.filter(g => !g.searched).length,
    genres_discovered: tracker.genres_discovered.length,
    by_type: Object.entries(
      works.reduce((acc, w) => { acc[w.type || 'unknown'] = (acc[w.type || 'unknown'] || 0) + 1; return acc }, {})
    ).sort((a, b) => b[1] - a[1]),
  }
}
