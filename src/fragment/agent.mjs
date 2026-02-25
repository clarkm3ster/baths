#!/usr/bin/env node
/**
 * FRAGMENT AGENT — Autonomous data source discovery & scraper generation
 *
 * This is not a standalone program. It's a PIPELINE that Claude runs.
 *
 * Claude IS the intelligence layer. When Fragment needs to:
 *   - Discover sources → Claude reasons about what exists
 *   - Evaluate a response → Claude classifies the data
 *   - Generate a scraper → Claude writes the code
 *   - Decide what layers a source feeds → Claude makes the call
 *
 * The only external calls are to actual data endpoints being probed/scraped.
 * No Anthropic API. No LLM calls. Claude does the reasoning directly.
 *
 * HOW TO USE:
 *   Claude runs this with a domain:
 *     node src/fragment/agent.mjs "nonprofit services"
 *
 *   The agent handles: probe URLs → test scrapers → register working ones.
 *   Claude provides: the source list, the scraper code, the layer classification.
 *
 *   The source list is passed via a JSON file that Claude writes before running:
 *     data/meta/agent-input/{domain-slug}.json
 *
 * PIPELINE:
 *   1. READ input — load source definitions Claude wrote
 *   2. PROBE — hit every URL, capture response format + sample
 *   3. TEST — execute scraper code against Philadelphia (42101)
 *   4. REGISTER — write passing scrapers to sources/{domain}.mjs
 *   5. REPORT — log everything
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, unlinkSync, readdirSync, copyFileSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { delay, safeFetch, readJSON, writeJSON, stateAbbrev, stateFips, countyFips } from './lib.mjs'

const __dirname = dirname(fileURLToPath(import.meta.url))
const ROOT = join(__dirname, '..', '..')
const SOURCES_DIR = join(__dirname, 'sources')
const DATA = join(ROOT, 'data')
const INPUT_DIR = join(DATA, 'meta', 'agent-input')
const REPORTS_DIR = join(DATA, 'meta', 'agent-runs')

const TEST_FIPS = '42101'
const TEST_COUNTY = 'Philadelphia, PA'
const PROBE_TIMEOUT = 12000

// ── Logging ──────────────────────────────────────────────────────────────────
const P = {
  phase: (n, name) => console.log(`\n${'═'.repeat(64)}\n  PHASE ${n}: ${name}\n${'═'.repeat(64)}`),
  step:  (msg) => console.log(`  > ${msg}`),
  ok:    (msg) => console.log(`  + ${msg}`),
  fail:  (msg) => console.log(`  - ${msg}`),
  info:  (msg) => console.log(`    ${msg}`),
  blank: ()    => console.log(''),
}

// ══════════════════════════════════════════════════════════════════════════════
//  PHASE 1: READ INPUT
// ══════════════════════════════════════════════════════════════════════════════

function readInput(domain) {
  P.phase(1, 'READ INPUT')

  const slug = domain.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-+$/, '')
  const inputPath = join(INPUT_DIR, `${slug}.json`)

  if (!existsSync(inputPath)) {
    P.fail(`No input file found at ${inputPath}`)
    P.info('Claude must write the source definitions before running the agent.')
    P.info(`Expected: data/meta/agent-input/${slug}.json`)
    P.info('Format: { domain, sources: [{ name, label, probe_url, scraper_code, layers, ... }] }')
    return null
  }

  const input = readJSON(inputPath)
  if (!input?.sources?.length) {
    P.fail('Input file has no sources')
    return null
  }

  // Deduplicate against existing registered scrapers
  const existingIds = loadExistingSourceIds()
  const fresh = input.sources.filter(s => !existingIds.has(s.name))
  const dupes = input.sources.length - fresh.length

  P.ok(`Loaded ${input.sources.length} source definitions`)
  if (dupes > 0) P.info(`Filtered ${dupes} already registered`)
  P.ok(`Fresh sources to process: ${fresh.length}`)

  return { ...input, sources: fresh }
}

function loadExistingSourceIds() {
  const ids = new Set()
  for (const file of readdirSync(SOURCES_DIR).filter(f => f.endsWith('.mjs') && f !== 'index.mjs' && f !== 'factories.mjs')) {
    try {
      const content = readFileSync(join(SOURCES_DIR, file), 'utf8')
      for (const m of content.matchAll(/id:\s*['"]([^'"]+)['"]/g)) ids.add(m[1])
    } catch { /* skip */ }
  }
  return ids
}

// ══════════════════════════════════════════════════════════════════════════════
//  PHASE 2: PROBE
// ══════════════════════════════════════════════════════════════════════════════

async function probe(sources) {
  P.phase(2, 'PROBE')
  P.step(`Probing ${sources.length} URLs...`)

  const results = []

  for (const source of sources) {
    if (!source.probe_url) {
      P.fail(`${source.name}: no probe_url — skipping probe`)
      results.push({ ...source, probe_ok: false, probe_error: 'No probe URL' })
      continue
    }

    process.stdout.write(`  > ${source.name}... `)

    try {
      const controller = new AbortController()
      const timeout = setTimeout(() => controller.abort(), PROBE_TIMEOUT)
      const res = await fetch(source.probe_url, {
        signal: controller.signal,
        headers: { 'User-Agent': 'BATHS-Fragment/1.0' },
      })
      clearTimeout(timeout)

      const status = res.status
      const contentType = res.headers.get('content-type') || ''
      const body = await res.text()

      let format = 'unknown'
      let parsed = null
      if (body.trimStart().startsWith('{') || body.trimStart().startsWith('[')) {
        try { parsed = JSON.parse(body); format = Array.isArray(parsed) ? 'json_array' : 'json_object' } catch { format = 'json_malformed' }
      } else if (contentType.includes('csv') || contentType.includes('text/plain')) {
        format = 'csv'
      } else if (contentType.includes('html')) {
        format = 'html'
      } else if (contentType.includes('xml')) {
        format = 'xml'
      }

      const ok = status < 400 && (format === 'json_array' || format === 'json_object')
      console.log(ok ? `OK (${format}, HTTP ${status})` : `SKIP (HTTP ${status}, ${format})`)

      results.push({
        ...source,
        probe_ok: ok,
        probe_status: status,
        probe_format: format,
        probe_sample: body.slice(0, 2000),
        probe_parsed: parsed,
        probe_error: ok ? null : `HTTP ${status} / ${format}`,
      })
    } catch (err) {
      console.log(`ERROR (${err.message.slice(0, 50)})`)
      results.push({ ...source, probe_ok: false, probe_error: err.message })
    }

    await delay(300)
  }

  const okCount = results.filter(r => r.probe_ok).length
  P.blank()
  P.ok(`Probed: ${results.length} | Reachable: ${okCount} | Unreachable: ${results.length - okCount}`)
  return results
}

// ══════════════════════════════════════════════════════════════════════════════
//  PHASE 3: TEST
// ══════════════════════════════════════════════════════════════════════════════

async function testScrapers(sources) {
  P.phase(3, 'TEST')

  // Only test sources that have scraper_code
  const testable = sources.filter(s => s.scraper_code)
  P.step(`Testing ${testable.length} scrapers against ${TEST_FIPS} (${TEST_COUNTY})...`)

  if (testable.length === 0) {
    P.info('No scrapers with code to test')
    return []
  }

  // Determine which factories/helpers the code needs
  const allCode = testable.map(s => s.scraper_code).join('\n')
  const factories = new Set()
  const helpers = new Set()
  for (const name of ['restJSON', 'sodaAPI', 'censusACS', 'censusSubject', 'blsSeries', 'femaAPI', 'usaSpend', 'treasuryAPI']) {
    if (allCode.includes(name)) factories.add(name)
  }
  for (const name of ['stateAbbrev', 'stateFips', 'countyFips']) {
    if (allCode.includes(name)) helpers.add(name)
  }

  const ts = Date.now()
  const tmpFile = join(SOURCES_DIR, `.tmp-agent-${ts}.mjs`)

  const moduleCode = [
    factories.size > 0 ? `import { ${[...factories].join(', ')} } from './factories.mjs'` : '',
    helpers.size > 0 ? `import { ${[...helpers].join(', ')} } from '../lib.mjs'` : '',
    '',
    'export default [',
    testable.map(s => `  ${s.scraper_code}`).join(',\n\n'),
    ']',
    '',
  ].filter(l => l !== undefined).join('\n')

  writeFileSync(tmpFile, moduleCode, 'utf8')

  const results = []
  try {
    const mod = await import(`file://${tmpFile}?t=${ts}`)
    const scrapers = mod.default

    if (!Array.isArray(scrapers)) {
      P.fail('Temp module did not export an array')
      return results
    }

    P.ok(`Loaded ${scrapers.length} scrapers`)

    for (let i = 0; i < scrapers.length; i++) {
      const scraper = scrapers[i]
      const source = testable[i]
      const id = scraper?.id || source?.name || `unknown-${i}`

      process.stdout.write(`  > ${id}... `)

      try {
        const result = await scraper.scrape(TEST_FIPS)
        if (result.ok && result.data && JSON.stringify(result.data).length > 5) {
          const size = JSON.stringify(result.data).length
          console.log(`PASS (${size} bytes)`)
          results.push({ id, status: 'pass', data_size: size, data_preview: JSON.stringify(result.data).slice(0, 300), source })
        } else {
          console.log(`FAIL (${result.error || 'empty data'})`)
          results.push({ id, status: 'fail', reason: result.error || 'Empty', source })
        }
      } catch (err) {
        console.log(`ERROR (${err.message.slice(0, 60)})`)
        results.push({ id, status: 'error', reason: err.message, source })
      }

      await delay(500)
    }
  } catch (err) {
    P.fail(`Module load failed: ${err.message}`)
    // Dump the module for debugging
    P.info('Generated module:')
    console.log(moduleCode.split('\n').slice(0, 20).join('\n'))
    console.log('...')
  } finally {
    try { unlinkSync(tmpFile) } catch { /* ok */ }
  }

  const passed = results.filter(r => r.status === 'pass').length
  P.blank()
  P.ok(`Passed: ${passed} | Failed: ${results.length - passed}`)
  return results
}

// ══════════════════════════════════════════════════════════════════════════════
//  PHASE 4: REGISTER
// ══════════════════════════════════════════════════════════════════════════════

function register(testResults, domain, allSources) {
  P.phase(4, 'REGISTER')

  const passed = testResults.filter(r => r.status === 'pass')
  if (passed.length === 0) {
    P.info('No scrapers passed — nothing to register')
    return null
  }

  const slug = domain.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-+$/, '')
  const filename = `${slug}.mjs`
  const filepath = join(SOURCES_DIR, filename)

  // Determine imports
  const allCode = passed.map(r => r.source.scraper_code).join('\n')
  const factories = new Set()
  const helpers = new Set()
  for (const name of ['restJSON', 'sodaAPI', 'censusACS', 'censusSubject', 'blsSeries', 'femaAPI', 'usaSpend', 'treasuryAPI']) {
    if (allCode.includes(name)) factories.add(name)
  }
  for (const name of ['stateAbbrev', 'stateFips', 'countyFips']) {
    if (allCode.includes(name)) helpers.add(name)
  }

  const now = new Date().toISOString()
  const fileContent = `/**
 * FRAGMENT — ${domain} (auto-generated)
 *
 * Generated by Fragment Agent on ${now}
 * Domain: "${domain}"
 * Tested: ${testResults.length} scrapers
 * Passed: ${passed.length} scrapers
 */

${factories.size > 0 ? `import { ${[...factories].join(', ')} } from './factories.mjs'` : ''}
${helpers.size > 0 ? `import { ${[...helpers].join(', ')} } from '../lib.mjs'` : ''}

export default [
${passed.map(r => `\n  ${r.source.scraper_code},`).join('\n')}
]
`

  writeFileSync(filepath, fileContent, 'utf8')
  P.ok(`Wrote ${filename} (${passed.length} scrapers)`)

  // Update index.mjs
  const indexPath = join(SOURCES_DIR, 'index.mjs')
  let indexContent = readFileSync(indexPath, 'utf8')
  const importName = slug.replace(/-./g, m => m[1].toUpperCase()) + 'Sources'
  const importLine = `import ${importName} from './${filename}'`

  if (!indexContent.includes(importLine)) {
    const lastImportEnd = indexContent.lastIndexOf('\nimport ')
    const insertAt = indexContent.indexOf('\n', lastImportEnd + 1) + 1
    indexContent = indexContent.slice(0, insertAt) + importLine + '\n' + indexContent.slice(insertAt)

    const allSourcesClose = indexContent.indexOf('\n]', indexContent.indexOf('const ALL_SOURCES'))
    if (allSourcesClose !== -1) {
      indexContent = indexContent.slice(0, allSourcesClose) + `\n  ...${importName},` + indexContent.slice(allSourcesClose)
    }

    writeFileSync(indexPath, indexContent, 'utf8')
    P.ok(`Updated index.mjs`)
  }

  // Log gaps
  const gapSources = allSources.filter(s => !passed.find(p => p.id === s.name))
  if (gapSources.length > 0) {
    const gapLog = join(DATA, 'meta', 'gaps.json')
    const existing = readJSON(gapLog) || { gaps: [], last_updated: null }
    const gapMap = new Map(existing.gaps.map(g => [g.source, g]))
    for (const g of gapSources) {
      gapMap.set(g.name, {
        source: g.name, label: g.label, description: g.description,
        type: g.type, access: g.access, layers: g.layers,
        probe_url: g.probe_url, probe_ok: g.probe_ok ?? false,
        reason: g.probe_error || g.note || 'Test failed',
        domain, logged_at: now,
      })
    }
    writeJSON(gapLog, { gaps: Array.from(gapMap.values()), last_updated: now, total: gapMap.size })
    P.ok(`Logged ${gapSources.length} gaps`)
  }

  return filepath
}

// ══════════════════════════════════════════════════════════════════════════════
//  PHASE 5: REPORT
// ══════════════════════════════════════════════════════════════════════════════

function report(domain, input, probed, testResults, registeredFile) {
  P.phase(5, 'REPORT')

  const passed = testResults.filter(r => r.status === 'pass')
  const failed = testResults.filter(r => r.status !== 'pass')
  const unreachable = probed.filter(p => !p.probe_ok)

  const summary = {
    domain,
    timestamp: new Date().toISOString(),
    stats: {
      sources_defined: input?.sources?.length || 0,
      urls_probed: probed.length,
      reachable: probed.filter(p => p.probe_ok).length,
      scrapers_tested: testResults.length,
      scrapers_passed: passed.length,
      scrapers_failed: failed.length,
      gaps_logged: unreachable.length + failed.length,
    },
    registered_file: registeredFile,
    passed: passed.map(r => ({ id: r.id, data_size: r.data_size, preview: r.data_preview })),
    failed: failed.map(r => ({ id: r.id, reason: r.reason })),
    unreachable: unreachable.map(u => ({ name: u.name, error: u.probe_error, type: u.type, access: u.access })),
  }

  mkdirSync(REPORTS_DIR, { recursive: true })
  const slug = domain.toLowerCase().replace(/[^a-z0-9]+/g, '-')
  const reportPath = join(REPORTS_DIR, `${slug}-${Date.now()}.json`)
  writeJSON(reportPath, summary)

  console.log(`
  Domain:          "${domain}"
  Sources defined: ${summary.stats.sources_defined}
  URLs probed:     ${summary.stats.urls_probed}
  Reachable:       ${summary.stats.reachable}
  Scrapers tested: ${summary.stats.scrapers_tested}
  Passed:          ${summary.stats.scrapers_passed}
  Failed:          ${summary.stats.scrapers_failed}
  Gaps:            ${summary.stats.gaps_logged}
  Registered:      ${registeredFile || 'none'}
  Report:          ${reportPath}`)

  if (passed.length > 0) {
    console.log('\n  Working scrapers:')
    for (const r of passed) console.log(`    + ${r.id} (${r.data_size} bytes)`)
  }
  if (unreachable.length > 0) {
    console.log('\n  Unreachable / gated:')
    for (const u of unreachable) console.log(`    - ${u.name}: ${u.error}`)
  }
  console.log('')

  return summary
}

// ══════════════════════════════════════════════════════════════════════════════
//  MAIN
// ══════════════════════════════════════════════════════════════════════════════

async function run(domain) {
  console.log('\n╔══════════════════════════════════════════════════════════════╗')
  console.log('║              FRAGMENT AGENT — Source Discovery               ║')
  console.log('╚══════════════════════════════════════════════════════════════╝')
  console.log(`\n  Domain: "${domain}"`)
  console.log(`  Test:   ${TEST_FIPS} (${TEST_COUNTY})`)

  const input = readInput(domain)
  if (!input) return { stats: { scrapers_passed: 0 } }

  const probed = await probe(input.sources)
  const testResults = await testScrapers(probed)
  const registeredFile = register(testResults, domain, input.sources)
  return report(domain, input, probed, testResults, registeredFile)
}

const domain = process.argv[2]
if (!domain) {
  console.error('Usage: node src/fragment/agent.mjs "<domain>"')
  console.error('  Claude writes source definitions to data/meta/agent-input/{domain}.json first.')
  process.exit(1)
}

run(domain).then(s => process.exit(s.stats?.scrapers_passed > 0 ? 0 : 1)).catch(err => { console.error('FATAL:', err); process.exit(1) })
