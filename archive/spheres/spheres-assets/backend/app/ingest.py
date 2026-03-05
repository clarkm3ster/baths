"""Ingest publicly-owned parcel data from the OpenDataPhilly Carto SQL API."""

import time
import httpx
from sqlalchemy.orm import Session

from app.models import Parcel
from app.scoring import score_parcel, categorize_parcel

CARTO_URL = "https://phl.carto.com/api/v2/sql"

_FIELDS = (
    "parcel_number, location, owner_1, market_value, taxable_land, "
    "taxable_building, exempt_land, exempt_building, category_code, "
    "category_code_description, zoning, total_area, frontage, depth, "
    "exterior_condition, year_built, geographic_ward, zip_code, "
    "ST_Y(the_geom) as lat, ST_X(the_geom) as lng"
)

_WHERE = """
    owner_1 ILIKE 'CITY OF PHILA%%'
    OR owner_1 ILIKE 'PHILADELPHIA HOUSING%%'
    OR owner_1 ILIKE 'PHILA HOUSING%%'
    OR owner_1 = 'PHILADELPHIA LAND BANK'
    OR owner_1 ILIKE 'REDEVELOPMENT AUTH%%'
    OR owner_1 ILIKE 'PHILA REDEVELOPMENT%%'
    OR owner_1 ILIKE 'PHILADELPHIA REDEVELOPMENT%%'
    OR owner_1 ILIKE 'SCHOOL DISTRICT%%'
    OR owner_1 = 'SEPTA'
    OR owner_1 ILIKE 'COMMONWEALTH OF P%%'
    OR owner_1 = 'PENNDOT'
    OR owner_1 ILIKE 'UNITED STATES%%'
    OR owner_1 ILIKE 'FAIRMOUNT PARK%%'
    OR owner_1 ILIKE 'PHILA AUTH%%'
"""

BATCH_SIZE = 5000


def _normalize_agency(owner: str) -> str:
    """Map raw owner_1 string to a normalized agency category."""
    o = (owner or "").upper().strip()
    if "HOUSING" in o:
        return "housing_authority"
    if "LAND BANK" in o:
        return "land_bank"
    if "REDEVELOPMENT" in o:
        return "redevelopment_authority"
    if "SCHOOL" in o:
        return "school_district"
    if o == "SEPTA":
        return "septa"
    if "PENNDOT" in o:
        return "penndot"
    if "COMMONWEALTH" in o:
        return "state"
    if "UNITED STATES" in o:
        return "federal"
    if "FAIRMOUNT" in o:
        return "parks"
    if "PHILA AUTH" in o:
        return "pidc"
    if "CITY OF PHILA" in o:
        return "city"
    return "other"


def _is_vacant(category_code: str, exterior_condition: str) -> bool:
    return category_code in ("6", "12", "13") or exterior_condition in ("6", "7")


def _row_to_parcel(row: dict) -> Parcel:
    owner = row.get("owner_1") or ""
    cat_code = str(row.get("category_code") or "")
    ext_cond = str(row.get("exterior_condition") or "")
    area = float(row.get("total_area") or 0)
    zoning = row.get("zoning") or ""
    frontage = float(row.get("frontage") or 0)

    p = Parcel(
        parcel_number=str(row.get("parcel_number") or ""),
        address=row.get("location") or "",
        lat=row.get("lat"),
        lng=row.get("lng"),
        owner=owner,
        owner_agency=_normalize_agency(owner),
        total_area_sqft=area,
        zoning=zoning,
        category_code=cat_code,
        category_description=row.get("category_code_description") or "",
        frontage=frontage,
        depth=float(row.get("depth") or 0),
        exterior_condition=ext_cond,
        year_built=str(row.get("year_built") or ""),
        geographic_ward=str(row.get("geographic_ward") or ""),
        zip_code=str(row.get("zip_code") or ""),
        market_value=float(row.get("market_value") or 0),
        taxable_land=float(row.get("taxable_land") or 0),
        taxable_building=float(row.get("taxable_building") or 0),
        exempt_land=float(row.get("exempt_land") or 0),
        exempt_building=float(row.get("exempt_building") or 0),
        vacancy_likely=_is_vacant(cat_code, ext_cond),
    )
    p.activation_score = score_parcel(p)
    p.activation_categories = categorize_parcel(p)
    return p


def ingest_parcels(db: Session) -> int:
    """Fetch all publicly-owned parcels from Carto and insert into the DB.

    Returns the number of parcels ingested.
    """
    total = 0
    offset = 0
    client = httpx.Client(timeout=60)

    while True:
        query = (
            f"SELECT {_FIELDS} FROM opa_properties_public "
            f"WHERE {_WHERE} "
            f"ORDER BY parcel_number "
            f"LIMIT {BATCH_SIZE} OFFSET {offset}"
        )
        try:
            resp = client.post(CARTO_URL, data={"q": query})
            resp.raise_for_status()
            data = resp.json()
        except Exception as exc:
            print(f"  Carto API error at offset {offset}: {exc}")
            break

        rows = data.get("rows", [])
        if not rows:
            break

        for row in rows:
            pn = str(row.get("parcel_number") or "")
            if not pn:
                continue
            parcel = _row_to_parcel(row)
            db.merge(parcel)

        db.commit()
        total += len(rows)
        print(f"  Ingested {total} parcels...")

        if len(rows) < BATCH_SIZE:
            break
        offset += BATCH_SIZE
        time.sleep(1)  # rate-limit courtesy

    client.close()
    return total
