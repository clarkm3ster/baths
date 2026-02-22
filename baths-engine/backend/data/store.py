"""
BATHS Data Store — SQLite accumulation backbone.

Every scrape writes here. Data only grows. The games read from the richest
available dataset: scraped data when it exists, seed data as floor.

Tables:
  provisions     — legal provisions from eCFR / Federal Register
  cost_points    — cost data from CMS, HUD, Vera, HCUP, published research
  gov_systems    — federal/state/local data systems
  system_links   — connections (and gaps) between systems
  parcels        — Philadelphia parcel records
  enrichments    — cross-references discovered by enrichment engine
  scrape_runs    — log of every scrape (what, when, how many records)
"""

import sqlite3
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DB_DIR = Path(os.environ.get("BATHS_DATA_DIR", Path(__file__).parent / "db"))
DB_PATH = DB_DIR / "baths_data.sqlite"

SCHEMA = """
CREATE TABLE IF NOT EXISTS provisions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    cfr_title       INTEGER NOT NULL,
    cfr_part        INTEGER,
    cfr_section     TEXT,
    citation        TEXT NOT NULL,
    title_text      TEXT NOT NULL,
    body            TEXT,
    authority       TEXT,
    source_url      TEXT,
    dome_dimension  TEXT,
    tags            TEXT,           -- JSON array
    effective_date  TEXT,
    scraped_at      TEXT NOT NULL,
    UNIQUE(citation)
);

CREATE TABLE IF NOT EXISTS cost_points (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    category        TEXT NOT NULL,   -- healthcare, incarceration, shelter, emergency, education, fragmentation
    metric          TEXT NOT NULL,
    value           REAL NOT NULL,
    unit            TEXT NOT NULL,   -- $/month, $/year, $/visit, $/day
    geography       TEXT,            -- national, state, city
    population      TEXT,            -- medicaid, medicare, general, homeless, incarcerated
    source          TEXT NOT NULL,
    source_year     INTEGER,
    source_url      TEXT,
    scraped_at      TEXT NOT NULL,
    UNIQUE(category, metric, geography, population, source_year)
);

CREATE TABLE IF NOT EXISTS gov_systems (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    system_code     TEXT NOT NULL UNIQUE,
    name            TEXT NOT NULL,
    agency          TEXT NOT NULL,
    level           TEXT NOT NULL,   -- federal, state, local
    domain          TEXT NOT NULL,   -- health, income, housing, justice, education, food, employment
    data_fields     TEXT,            -- JSON array of field names
    population_served TEXT,
    annual_records  INTEGER,
    api_endpoint    TEXT,
    consent_required TEXT,           -- none, individual, agency, statutory
    scraped_at      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS system_links (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source_system   TEXT NOT NULL,
    target_system   TEXT NOT NULL,
    link_type       TEXT NOT NULL,   -- active, possible, blocked, one-way
    mechanism       TEXT,            -- API, batch, manual, MOU, statutory
    latency         TEXT,            -- realtime, daily, weekly, monthly, none
    consent_barrier TEXT,
    legal_authority TEXT,
    scraped_at      TEXT NOT NULL,
    UNIQUE(source_system, target_system)
);

CREATE TABLE IF NOT EXISTS parcels (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    parcel_id       TEXT NOT NULL UNIQUE,
    address         TEXT,
    owner           TEXT,
    zoning          TEXT,
    land_area_sqft  REAL,
    improvement_val REAL,
    land_val        REAL,
    total_val       REAL,
    vacant          INTEGER,        -- 0 or 1
    lat             REAL,
    lon             REAL,
    neighborhood    TEXT,
    council_district INTEGER,
    extra           TEXT,           -- JSON for additional fields
    scraped_at      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS enrichments (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    enrichment_type TEXT NOT NULL,   -- cross_ref, conflict, opportunity, pattern, gap
    source_table    TEXT NOT NULL,
    source_id       INTEGER NOT NULL,
    target_table    TEXT,
    target_id       INTEGER,
    description     TEXT NOT NULL,
    confidence      REAL,           -- 0.0 to 1.0
    data            TEXT,           -- JSON payload
    discovered_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS scrape_runs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    engine          TEXT NOT NULL,   -- legal, costs, systems, parcels
    source          TEXT NOT NULL,   -- ecfr, federalregister, cms, hud, opendataphilly
    started_at      TEXT NOT NULL,
    completed_at    TEXT,
    records_added   INTEGER DEFAULT 0,
    records_updated INTEGER DEFAULT 0,
    status          TEXT DEFAULT 'running',  -- running, completed, failed
    error           TEXT
);

CREATE INDEX IF NOT EXISTS idx_provisions_dome ON provisions(dome_dimension);
CREATE INDEX IF NOT EXISTS idx_provisions_cfr ON provisions(cfr_title, cfr_part);
CREATE INDEX IF NOT EXISTS idx_cost_category ON cost_points(category);
CREATE INDEX IF NOT EXISTS idx_cost_population ON cost_points(population);
CREATE INDEX IF NOT EXISTS idx_systems_domain ON gov_systems(domain);
CREATE INDEX IF NOT EXISTS idx_system_links_source ON system_links(source_system);
CREATE INDEX IF NOT EXISTS idx_parcels_zoning ON parcels(zoning);
CREATE INDEX IF NOT EXISTS idx_parcels_vacant ON parcels(vacant);
CREATE INDEX IF NOT EXISTS idx_parcels_neighborhood ON parcels(neighborhood);
CREATE INDEX IF NOT EXISTS idx_enrichments_type ON enrichments(enrichment_type);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class DataStore:
    """Thread-safe SQLite store. One instance per process."""

    def __init__(self, db_path: str | Path | None = None):
        self.db_path = Path(db_path) if db_path else DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._conn.executescript(SCHEMA)
        self._conn.commit()

    # ── Provisions ──────────────────────────────────────────────────────

    def upsert_provision(self, **kwargs) -> int:
        kwargs.setdefault("scraped_at", _now())
        kwargs.setdefault("effective_date", None)
        if isinstance(kwargs.get("tags"), list):
            kwargs["tags"] = json.dumps(kwargs["tags"])
        try:
            cur = self._conn.execute("""
                INSERT INTO provisions (cfr_title, cfr_part, cfr_section, citation,
                    title_text, body, authority, source_url, dome_dimension, tags,
                    effective_date, scraped_at)
                VALUES (:cfr_title, :cfr_part, :cfr_section, :citation,
                    :title_text, :body, :authority, :source_url, :dome_dimension, :tags,
                    :effective_date, :scraped_at)
                ON CONFLICT(citation) DO UPDATE SET
                    body=excluded.body, authority=excluded.authority,
                    source_url=excluded.source_url, dome_dimension=excluded.dome_dimension,
                    tags=excluded.tags, scraped_at=excluded.scraped_at
            """, kwargs)
            self._conn.commit()
            return cur.lastrowid
        except Exception:
            self._conn.rollback()
            raise

    def get_provisions(self, dome_dimension: str | None = None,
                       cfr_title: int | None = None, limit: int = 100) -> list[dict]:
        sql = "SELECT * FROM provisions WHERE 1=1"
        params = []
        if dome_dimension:
            sql += " AND dome_dimension = ?"
            params.append(dome_dimension)
        if cfr_title:
            sql += " AND cfr_title = ?"
            params.append(cfr_title)
        sql += " ORDER BY scraped_at DESC LIMIT ?"
        params.append(limit)
        rows = self._conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def provision_count(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM provisions").fetchone()[0]

    # ── Cost Points ─────────────────────────────────────────────────────

    def upsert_cost_point(self, **kwargs) -> int:
        kwargs.setdefault("scraped_at", _now())
        try:
            cur = self._conn.execute("""
                INSERT INTO cost_points (category, metric, value, unit, geography,
                    population, source, source_year, source_url, scraped_at)
                VALUES (:category, :metric, :value, :unit, :geography,
                    :population, :source, :source_year, :source_url, :scraped_at)
                ON CONFLICT(category, metric, geography, population, source_year) DO UPDATE SET
                    value=excluded.value, unit=excluded.unit, source=excluded.source,
                    source_url=excluded.source_url, scraped_at=excluded.scraped_at
            """, kwargs)
            self._conn.commit()
            return cur.lastrowid
        except Exception:
            self._conn.rollback()
            raise

    def get_costs(self, category: str | None = None,
                  population: str | None = None, limit: int = 200) -> list[dict]:
        sql = "SELECT * FROM cost_points WHERE 1=1"
        params = []
        if category:
            sql += " AND category = ?"
            params.append(category)
        if population:
            sql += " AND population = ?"
            params.append(population)
        sql += " ORDER BY source_year DESC, scraped_at DESC LIMIT ?"
        params.append(limit)
        rows = self._conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def cost_count(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM cost_points").fetchone()[0]

    # ── Government Systems ──────────────────────────────────────────────

    def upsert_system(self, **kwargs) -> int:
        kwargs.setdefault("scraped_at", _now())
        if isinstance(kwargs.get("data_fields"), list):
            kwargs["data_fields"] = json.dumps(kwargs["data_fields"])
        try:
            cur = self._conn.execute("""
                INSERT INTO gov_systems (system_code, name, agency, level, domain,
                    data_fields, population_served, annual_records, api_endpoint,
                    consent_required, scraped_at)
                VALUES (:system_code, :name, :agency, :level, :domain,
                    :data_fields, :population_served, :annual_records, :api_endpoint,
                    :consent_required, :scraped_at)
                ON CONFLICT(system_code) DO UPDATE SET
                    name=excluded.name, data_fields=excluded.data_fields,
                    api_endpoint=excluded.api_endpoint, scraped_at=excluded.scraped_at
            """, kwargs)
            self._conn.commit()
            return cur.lastrowid
        except Exception:
            self._conn.rollback()
            raise

    def get_systems(self, domain: str | None = None, level: str | None = None,
                    limit: int = 100) -> list[dict]:
        sql = "SELECT * FROM gov_systems WHERE 1=1"
        params = []
        if domain:
            sql += " AND domain = ?"
            params.append(domain)
        if level:
            sql += " AND level = ?"
            params.append(level)
        sql += " ORDER BY agency, name LIMIT ?"
        params.append(limit)
        rows = self._conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def get_system_links(self, system_code: str | None = None,
                         link_type: str | None = None, limit: int = 500) -> list[dict]:
        sql = "SELECT * FROM system_links WHERE 1=1"
        params = []
        if system_code:
            sql += " AND (source_system = ? OR target_system = ?)"
            params.extend([system_code, system_code])
        if link_type:
            sql += " AND link_type = ?"
            params.append(link_type)
        sql += " LIMIT ?"
        params.append(limit)
        rows = self._conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def system_count(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM gov_systems").fetchone()[0]

    def link_count(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM system_links").fetchone()[0]

    # ── System Links ────────────────────────────────────────────────────

    def upsert_system_link(self, **kwargs) -> int:
        kwargs.setdefault("scraped_at", _now())
        try:
            cur = self._conn.execute("""
                INSERT INTO system_links (source_system, target_system, link_type,
                    mechanism, latency, consent_barrier, legal_authority, scraped_at)
                VALUES (:source_system, :target_system, :link_type,
                    :mechanism, :latency, :consent_barrier, :legal_authority, :scraped_at)
                ON CONFLICT(source_system, target_system) DO UPDATE SET
                    link_type=excluded.link_type, mechanism=excluded.mechanism,
                    latency=excluded.latency, scraped_at=excluded.scraped_at
            """, kwargs)
            self._conn.commit()
            return cur.lastrowid
        except Exception:
            self._conn.rollback()
            raise

    # ── Parcels ─────────────────────────────────────────────────────────

    def upsert_parcel(self, **kwargs) -> int:
        kwargs.setdefault("scraped_at", _now())
        if isinstance(kwargs.get("extra"), dict):
            kwargs["extra"] = json.dumps(kwargs["extra"])
        try:
            cur = self._conn.execute("""
                INSERT INTO parcels (parcel_id, address, owner, zoning, land_area_sqft,
                    improvement_val, land_val, total_val, vacant, lat, lon,
                    neighborhood, council_district, extra, scraped_at)
                VALUES (:parcel_id, :address, :owner, :zoning, :land_area_sqft,
                    :improvement_val, :land_val, :total_val, :vacant, :lat, :lon,
                    :neighborhood, :council_district, :extra, :scraped_at)
                ON CONFLICT(parcel_id) DO UPDATE SET
                    owner=excluded.owner, zoning=excluded.zoning,
                    total_val=excluded.total_val, vacant=excluded.vacant,
                    extra=excluded.extra, scraped_at=excluded.scraped_at
            """, kwargs)
            self._conn.commit()
            return cur.lastrowid
        except Exception:
            self._conn.rollback()
            raise

    def get_parcels(self, zoning: str | None = None, vacant: bool | None = None,
                    neighborhood: str | None = None, limit: int = 200) -> list[dict]:
        sql = "SELECT * FROM parcels WHERE 1=1"
        params = []
        if zoning:
            sql += " AND zoning LIKE ?"
            params.append(f"%{zoning}%")
        if vacant is not None:
            sql += " AND vacant = ?"
            params.append(1 if vacant else 0)
        if neighborhood:
            sql += " AND neighborhood = ?"
            params.append(neighborhood)
        sql += " ORDER BY total_val DESC LIMIT ?"
        params.append(limit)
        rows = self._conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def parcel_count(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM parcels").fetchone()[0]

    # ── Enrichments ─────────────────────────────────────────────────────

    def add_enrichment(self, **kwargs) -> int:
        kwargs.setdefault("discovered_at", _now())
        if isinstance(kwargs.get("data"), dict):
            kwargs["data"] = json.dumps(kwargs["data"])
        cur = self._conn.execute("""
            INSERT INTO enrichments (enrichment_type, source_table, source_id,
                target_table, target_id, description, confidence, data, discovered_at)
            VALUES (:enrichment_type, :source_table, :source_id,
                :target_table, :target_id, :description, :confidence, :data, :discovered_at)
        """, kwargs)
        self._conn.commit()
        return cur.lastrowid

    def get_enrichments(self, enrichment_type: str | None = None,
                        limit: int = 100) -> list[dict]:
        sql = "SELECT * FROM enrichments WHERE 1=1"
        params = []
        if enrichment_type:
            sql += " AND enrichment_type = ?"
            params.append(enrichment_type)
        sql += " ORDER BY discovered_at DESC LIMIT ?"
        params.append(limit)
        rows = self._conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def enrichment_count(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM enrichments").fetchone()[0]

    # ── Scrape Runs ─────────────────────────────────────────────────────

    def start_scrape_run(self, engine: str, source: str) -> int:
        cur = self._conn.execute("""
            INSERT INTO scrape_runs (engine, source, started_at, status)
            VALUES (?, ?, ?, 'running')
        """, (engine, source, _now()))
        self._conn.commit()
        return cur.lastrowid

    def complete_scrape_run(self, run_id: int, records_added: int = 0,
                            records_updated: int = 0, error: str | None = None):
        status = "failed" if error else "completed"
        self._conn.execute("""
            UPDATE scrape_runs SET completed_at=?, records_added=?,
                records_updated=?, status=?, error=?
            WHERE id=?
        """, (_now(), records_added, records_updated, status, error, run_id))
        self._conn.commit()

    def get_scrape_history(self, engine: str | None = None, limit: int = 50) -> list[dict]:
        sql = "SELECT * FROM scrape_runs WHERE 1=1"
        params = []
        if engine:
            sql += " AND engine = ?"
            params.append(engine)
        sql += " ORDER BY started_at DESC LIMIT ?"
        params.append(limit)
        rows = self._conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def last_scrape(self, engine: str, source: str) -> dict | None:
        row = self._conn.execute("""
            SELECT * FROM scrape_runs WHERE engine=? AND source=? AND status='completed'
            ORDER BY completed_at DESC LIMIT 1
        """, (engine, source)).fetchone()
        return dict(row) if row else None

    # ── Stats ───────────────────────────────────────────────────────────

    def stats(self) -> dict:
        return {
            "provisions": self.provision_count(),
            "cost_points": self.cost_count(),
            "gov_systems": self.system_count(),
            "system_links": self.link_count(),
            "parcels": self.parcel_count(),
            "enrichments": self.enrichment_count(),
            "total_scrape_runs": self._conn.execute(
                "SELECT COUNT(*) FROM scrape_runs"
            ).fetchone()[0],
            "successful_scrapes": self._conn.execute(
                "SELECT COUNT(*) FROM scrape_runs WHERE status='completed'"
            ).fetchone()[0],
            "db_size_mb": round(os.path.getsize(self.db_path) / (1024 * 1024), 2)
                if self.db_path.exists() else 0,
        }

    def close(self):
        self._conn.close()


# Module-level singleton
_store: DataStore | None = None

def get_store() -> DataStore:
    global _store
    if _store is None:
        _store = DataStore()
    return _store
