/**
 * TALENT AGENT — Production-specific matching from the unified pool
 *
 * The pool is unified. The matching is production-specific.
 *
 * For a DOME production:  match practitioners whose dome_layers overlap the production's needs
 * For a SPHERE production: match practitioners whose sphere_layers overlap the production's needs
 *
 * A landscape architect appears in both. The matcher doesn't care.
 * It scores based on layer overlap, discipline relevance, and diversity of perspective.
 */

import { loadPool } from './pool.mjs'
import { readJSON, INDEX_DIR } from './lib.mjs'
import { join } from 'node:path'

/**
 * Match talent for a DOME production
 * @param {number[]} layers — dome layers the production needs help with
 * @param {object} opts — { limit, disciplines, includeTypes }
 */
export function matchForDome(layers, opts = {}) {
  return matchFor('dome', layers, opts)
}

/**
 * Match talent for a SPHERE production
 * @param {number[]} layers — sphere layers the production needs help with
 * @param {object} opts — { limit, disciplines, includeTypes }
 */
export function matchForSphere(layers, opts = {}) {
  return matchFor('sphere', layers, opts)
}

function matchFor(productionType, layers, opts = {}) {
  const { limit = 50, disciplines = null, includeTypes = ['real', 'fictional'] } = opts
  const pool = loadPool()

  const scored = pool
    .filter(p => includeTypes.includes(p.type))
    .map(p => {
      const layerField = productionType === 'dome' ? p.dome_layers : p.sphere_layers
      const relevanceField = productionType === 'dome' ? p.dome_relevance : p.sphere_relevance

      // Score: how many requested layers does this practitioner cover?
      const overlap = layers.filter(l => layerField.includes(l))
      if (overlap.length === 0) return null

      const layerScore = overlap.length / layers.length
      const breadthScore = layerField.length / (productionType === 'dome' ? 12 : 10)
      const disciplineMatch = disciplines
        ? (p.disciplines.some(d => disciplines.includes(d)) ? 1 : 0.3)
        : 1

      const score = (layerScore * 0.6) + (breadthScore * 0.2) + (disciplineMatch * 0.2)

      return {
        id: p.id,
        name: p.name,
        type: p.type,
        discipline: p.discipline,
        practice: p.practice,
        approach: p.approach,
        why_instructive: p.why_instructive,
        layers_covered: overlap,
        relevance: Object.fromEntries(overlap.map(l => [l, relevanceField[l] || ''])),
        score: Math.round(score * 1000) / 1000,
        // Fictional extras
        source_work: p.source_work,
        source_medium: p.source_medium,
      }
    })
    .filter(Boolean)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)

  return {
    production_type: productionType,
    layers_requested: layers,
    matches: scored,
    total_matched: scored.length,
    pool_size: pool.length,
    matched_at: new Date().toISOString(),
  }
}
