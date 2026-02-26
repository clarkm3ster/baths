/**
 * CHARACTER FRAGMENT — Source Registry
 *
 * All seed sources and discovery APIs in one place.
 * Each source exports an array of character objects.
 * API discovery exports functions for finding new source works.
 */

import nonfiction from './nonfiction.mjs'
import journalism from './journalism.mjs'
import caseStudies from './case-studies.mjs'
import oralHistories from './oral-histories.mjs'
import literature from './literature.mjs'
import filmTv from './film-tv.mjs'
import theaterGamesMythology from './theater-games-myth.mjs'

// ── All seed characters ───────────────────────────────────────────────────────

export const SEED_SOURCES = [
  { id: 'nonfiction',               label: 'Nonfiction Books',                   characters: nonfiction },
  { id: 'journalism',               label: 'Investigative Journalism',           characters: journalism },
  { id: 'case-studies',             label: 'Case Studies & Testimony',           characters: caseStudies },
  { id: 'oral-histories',           label: 'Oral Histories & Memoirs',           characters: oralHistories },
  { id: 'literature',               label: 'Literature (Fiction)',               characters: literature },
  { id: 'film-tv',                  label: 'Film, TV & Documentary',             characters: filmTv },
  { id: 'theater-games-mythology',  label: 'Theater, Games, Mythology & Comics', characters: theaterGamesMythology },
]

// ── Statistics ────────────────────────────────────────────────────────────────

export function getSourceStats() {
  const stats = {
    total_characters: 0,
    total_real: 0,
    total_fictional: 0,
    by_source: {},
  }

  for (const source of SEED_SOURCES) {
    const real = source.characters.filter(c => c.real_or_fictional === 'real').length
    const fictional = source.characters.filter(c => c.real_or_fictional === 'fictional').length
    stats.by_source[source.id] = {
      label: source.label,
      total: source.characters.length,
      real,
      fictional,
    }
    stats.total_characters += source.characters.length
    stats.total_real += real
    stats.total_fictional += fictional
  }

  return stats
}

// ── Get all characters flat ───────────────────────────────────────────────────

export function getAllSeedCharacters() {
  const all = []
  for (const source of SEED_SOURCES) {
    for (const character of source.characters) {
      all.push({
        ...character,
        _source_category: source.id,
        _source_label: source.label,
      })
    }
  }
  return all
}

// ── Print registry ────────────────────────────────────────────────────────────

export function printRegistry() {
  const stats = getSourceStats()
  console.log('  Source Registry:')
  for (const [id, info] of Object.entries(stats.by_source)) {
    console.log(`    ${info.label}: ${info.total} characters (${info.real} real, ${info.fictional} fictional)`)
  }
  console.log(`    ──────────────────────────────────────`)
  console.log(`    Total: ${stats.total_characters} characters (${stats.total_real} real, ${stats.total_fictional} fictional)\n`)
}

export default SEED_SOURCES
