/**
 * CHARACTER FRAGMENT — API Discovery Engine
 *
 * Discovers NEW source works by querying open APIs:
 * - Open Library (books)
 * - TMDB (films/TV)
 * - Project Gutenberg (free texts)
 * - Internet Archive (everything)
 * - Google Books (metadata)
 *
 * For each discovered work, the engine identifies whether it likely
 * contains characters with documented circumstances.
 */

import { safeFetch, delay, slugify } from '../lib.mjs'

// ── Circumstance search terms ─────────────────────────────────────────────────
// These terms identify works likely to contain dome-buildable characters.

const CIRCUMSTANCE_QUERIES = [
  // Housing
  'homelessness memoir', 'eviction story', 'housing crisis', 'shelter life',
  'public housing novel', 'tenement life',
  // Legal/Criminal
  'wrongful conviction', 'prison memoir', 'incarceration narrative',
  'death row', 'exoneration', 'reentry from prison',
  // Health
  'addiction memoir', 'mental illness narrative', 'disability memoir',
  'chronic illness story', 'AIDS crisis', 'opioid epidemic',
  // Economic
  'poverty in America', 'working poor', 'minimum wage', 'welfare',
  'food stamps narrative', 'debt crisis personal',
  // Migration
  'immigration memoir', 'refugee narrative', 'asylum seeker story',
  'deportation', 'border crossing memoir', 'undocumented immigrant',
  // Child welfare
  'foster care memoir', 'aging out foster care', 'child welfare',
  'orphan narrative', 'child abuse memoir',
  // Environment
  'environmental justice', 'lead poisoning', 'Flint water',
  'toxic exposure memoir', 'environmental racism',
  // War/Veterans
  'veteran PTSD memoir', 'war coming home', 'military family',
  // Systemic
  'social worker case study', 'navigating bureaucracy', 'welfare system',
  'benefits cliff', 'safety net America',
  // Historical
  'slave narrative', 'Great Migration', 'Jim Crow memoir',
  'Japanese internment', 'Trail of Tears', 'reservation life',
  // Gender
  'domestic violence memoir', 'sex trafficking survivor',
  'single mother poverty',
]

// ── Open Library Search ───────────────────────────────────────────────────────

export async function searchOpenLibrary(query, limit = 20) {
  const url = `https://openlibrary.org/search.json?q=${encodeURIComponent(query)}&limit=${limit}&fields=key,title,author_name,first_publish_year,subject,isbn,number_of_pages_median`
  const result = await safeFetch(url, `OpenLibrary: ${query}`)
  if (!result.ok) return { ok: false, source: 'open-library', query, error: result.error }

  const docs = result.data?.docs || []
  return {
    ok: true,
    source: 'open-library',
    query,
    works: docs.map(d => ({
      id: `ol-${d.key?.replace('/works/', '')}`,
      title: d.title,
      authors: d.author_name || [],
      year: d.first_publish_year,
      subjects: (d.subject || []).slice(0, 20),
      pages: d.number_of_pages_median,
      isbn: d.isbn?.[0],
      api_url: `https://openlibrary.org${d.key}.json`,
      source_api: 'Open Library',
    })),
  }
}

// ── TMDB Search (The Movie Database) ──────────────────────────────────────────
// TMDB API v3 requires an API key. We attempt with demo access.

export async function searchTMDB(query, limit = 20) {
  // TMDB requires API key — check environment
  const apiKey = process.env.TMDB_API_KEY
  if (!apiKey) {
    return {
      ok: false,
      source: 'tmdb',
      query,
      error: 'TMDB_API_KEY not set. Get free key at https://www.themoviedb.org/settings/api',
      needs_key: true,
    }
  }

  const url = `https://api.themoviedb.org/3/search/movie?api_key=${apiKey}&query=${encodeURIComponent(query)}&page=1`
  const result = await safeFetch(url, `TMDB: ${query}`)
  if (!result.ok) return { ok: false, source: 'tmdb', query, error: result.error }

  const movies = (result.data?.results || []).slice(0, limit)
  return {
    ok: true,
    source: 'tmdb',
    query,
    works: movies.map(m => ({
      id: `tmdb-${m.id}`,
      title: m.title,
      year: m.release_date?.slice(0, 4),
      overview: m.overview,
      genre_ids: m.genre_ids,
      source_api: 'TMDB',
    })),
  }
}

// ── Project Gutenberg Search ──────────────────────────────────────────────────

export async function searchGutenberg(query, limit = 20) {
  const url = `https://gutendex.com/books/?search=${encodeURIComponent(query)}&page=1`
  const result = await safeFetch(url, `Gutenberg: ${query}`)
  if (!result.ok) return { ok: false, source: 'gutenberg', query, error: result.error }

  const books = (result.data?.results || []).slice(0, limit)
  return {
    ok: true,
    source: 'gutenberg',
    query,
    works: books.map(b => ({
      id: `gut-${b.id}`,
      title: b.title,
      authors: (b.authors || []).map(a => a.name),
      year: b.authors?.[0]?.birth_year ? `c.${b.authors[0].birth_year + 30}` : null,
      subjects: b.subjects || [],
      bookshelves: b.bookshelves || [],
      languages: b.languages || [],
      download_count: b.download_count,
      text_url: b.formats?.['text/plain; charset=utf-8'] || b.formats?.['text/plain'],
      source_api: 'Project Gutenberg',
    })),
  }
}

// ── Internet Archive Search ───────────────────────────────────────────────────

export async function searchInternetArchive(query, limit = 20) {
  const url = `https://archive.org/advancedsearch.php?q=${encodeURIComponent(query)}&fl[]=identifier&fl[]=title&fl[]=creator&fl[]=date&fl[]=description&fl[]=subject&fl[]=mediatype&sort[]=downloads+desc&rows=${limit}&page=1&output=json`
  const result = await safeFetch(url, `InternetArchive: ${query}`)
  if (!result.ok) return { ok: false, source: 'internet-archive', query, error: result.error }

  const docs = result.data?.response?.docs || []
  return {
    ok: true,
    source: 'internet-archive',
    query,
    works: docs.map(d => ({
      id: `ia-${d.identifier}`,
      title: d.title,
      authors: Array.isArray(d.creator) ? d.creator : d.creator ? [d.creator] : [],
      year: d.date?.slice(0, 4),
      subjects: Array.isArray(d.subject) ? d.subject.slice(0, 20) : d.subject ? [d.subject] : [],
      media_type: d.mediatype,
      description: typeof d.description === 'string' ? d.description.slice(0, 300) : null,
      url: `https://archive.org/details/${d.identifier}`,
      source_api: 'Internet Archive',
    })),
  }
}

// ── Run discovery sweep ───────────────────────────────────────────────────────
// Queries all APIs with circumstance-based search terms.

export async function runDiscoverySweep(options = {}) {
  const limit = options.queriesPerSweep || 5
  const delayMs = options.delayMs || 500

  // Pick queries to run this sweep (rotate through the list)
  const stateFile = options.stateFile
  let queryIndex = 0
  if (stateFile) {
    try {
      const { readJSON } = await import('../lib.mjs')
      const state = readJSON(stateFile)
      queryIndex = state?.nextQueryIndex || 0
    } catch { /* start from 0 */ }
  }

  const queries = CIRCUMSTANCE_QUERIES.slice(queryIndex, queryIndex + limit)
  if (queries.length === 0) return { ok: true, works: [], nextQueryIndex: 0 }

  const allWorks = []
  const errors = []

  for (const query of queries) {
    // Query Open Library and Gutenberg (no API key needed)
    const [olResult, gutResult] = await Promise.all([
      searchOpenLibrary(query, 10),
      searchGutenberg(query, 5),
    ])

    if (olResult.ok) allWorks.push(...olResult.works)
    else errors.push(olResult)

    if (gutResult.ok) allWorks.push(...gutResult.works)
    else errors.push(gutResult)

    // Internet Archive (rate limit friendly)
    await delay(delayMs)
    const iaResult = await searchInternetArchive(query, 5)
    if (iaResult.ok) allWorks.push(...iaResult.works)
    else errors.push(iaResult)

    // TMDB if key available
    if (process.env.TMDB_API_KEY) {
      await delay(delayMs)
      const tmdbResult = await searchTMDB(query, 5)
      if (tmdbResult.ok) allWorks.push(...tmdbResult.works)
      else errors.push(tmdbResult)
    }

    await delay(delayMs)
  }

  // Deduplicate by title similarity
  const seen = new Set()
  const unique = allWorks.filter(w => {
    const key = slugify(w.title || '')
    if (seen.has(key)) return false
    seen.add(key)
    return true
  })

  return {
    ok: true,
    works: unique,
    queries_run: queries.length,
    nextQueryIndex: queryIndex + limit >= CIRCUMSTANCE_QUERIES.length ? 0 : queryIndex + limit,
    errors: errors.length > 0 ? errors : undefined,
  }
}

// ── Score a discovered work for dome-buildability ─────────────────────────────
// Higher score = more likely to contain dome-buildable characters.

export function scoreWorkForDomePotential(work) {
  let score = 0
  const signals = []

  const text = [
    work.title || '',
    ...(work.subjects || []),
    ...(work.bookshelves || []),
    work.overview || '',
    work.description || '',
  ].join(' ').toLowerCase()

  const domeSigns = [
    { term: 'poverty', weight: 3 },
    { term: 'homeless', weight: 3 },
    { term: 'prison', weight: 3 },
    { term: 'incarcerat', weight: 3 },
    { term: 'welfare', weight: 2 },
    { term: 'evict', weight: 3 },
    { term: 'addict', weight: 2 },
    { term: 'refugee', weight: 3 },
    { term: 'immigra', weight: 2 },
    { term: 'slave', weight: 3 },
    { term: 'disabil', weight: 2 },
    { term: 'mental health', weight: 2 },
    { term: 'foster care', weight: 3 },
    { term: 'domestic violence', weight: 3 },
    { term: 'memoir', weight: 2 },
    { term: 'case stud', weight: 2 },
    { term: 'social work', weight: 2 },
    { term: 'oral histor', weight: 2 },
    { term: 'testimony', weight: 2 },
    { term: 'investigat', weight: 1 },
    { term: 'nonfiction', weight: 1 },
    { term: 'biography', weight: 1 },
    { term: 'death row', weight: 3 },
    { term: 'wrongful', weight: 3 },
    { term: 'inequality', weight: 1 },
    { term: 'injustice', weight: 2 },
  ]

  for (const { term, weight } of domeSigns) {
    if (text.includes(term)) {
      score += weight
      signals.push(term)
    }
  }

  return {
    score,
    signals,
    potential: score >= 6 ? 'high' : score >= 3 ? 'medium' : 'low',
  }
}

export { CIRCUMSTANCE_QUERIES }
