/**
 * ENTITY RESOLVER — Collective Goods
 *
 * Resolves: What is this person's share of collective spending?
 *
 * Defense, courts, police, fire, infrastructure, etc.
 * These are allocated per-capita — everyone gets the same share
 * regardless of income.
 *
 * Where fragment data provides local spending, use it.
 * Otherwise fall back to national/state averages.
 */

import { getNum } from '../fragments.mjs'
import {
  FEDERAL_COLLECTIVE, STATE_COLLECTIVE, LOCAL_COLLECTIVE,
} from '../reference.mjs'

export default {
  id: 'collective',
  fields: [
    'defense_per_capita_share', 'veterans_affairs_per_capita',
    'federal_law_enforcement_intel_share', 'diplomacy_foreign_affairs_share',
    'fed_infrastructure_share', 'fed_public_health_share',
    'fed_environment_share', 'fed_courts_share',
    'fed_general_govt_share', 'fed_interest_on_debt_share',
    'state_police_corrections_share', 'state_infrastructure_share',
    'state_courts_share', 'state_public_health_share',
    'state_parks_environment_share', 'state_general_govt_share',
    'local_police_share', 'local_fire_ems_share',
    'local_roads_share', 'local_water_sewer_share',
    'local_parks_rec_share', 'local_library_share',
    'local_general_govt_share', 'total_collective_allocated',
  ],

  resolve(profile, county, fragments) {
    // Federal collective is the same everywhere — national per-capita
    const result = { ...FEDERAL_COLLECTIVE }

    // State collective — use state averages (could be enhanced with Census of Governments data)
    Object.assign(result, STATE_COLLECTIVE)

    // Local collective — try to derive from fragment data, fall back to averages
    const localSpending = { ...LOCAL_COLLECTIVE }

    // If we have census population for the county, we could scale
    // For now, use national averages as baseline
    Object.assign(result, localSpending)

    // ── Total ────────────────────────────────────────────────
    result.total_collective_allocated = 0
    for (const [key, val] of Object.entries(result)) {
      if (key !== 'total_collective_allocated' && typeof val === 'number') {
        result.total_collective_allocated += val
      }
    }

    return result
  },
}
