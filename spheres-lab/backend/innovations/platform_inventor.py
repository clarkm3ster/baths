"""
SPHERES Innovation Laboratory — Platform Inventor seed innovations and templates.

Domain: platform-invention
Technology platforms for public space activation: IoT sensors, community apps,
digital twins, real-time monitoring, data dashboards, and ML-driven tooling
for Philadelphia's 40,000+ vacant parcels.
"""

# ---------------------------------------------------------------------------
# 6 Seed Innovations
# ---------------------------------------------------------------------------

INNOVATIONS: list[dict] = [
    {
        "title": "Lot Pulse IoT Network",
        "summary": (
            "A mesh network of low-power environmental sensors deployed across "
            "activated parcels measuring soil moisture, air quality (PM2.5, NO2, "
            "ozone), ambient noise, and pedestrian foot traffic in real time."
        ),
        "category": "iot-network",
        "impact_level": 5,
        "feasibility": 3,
        "novelty": 4,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "technology_stack": [
                "LoRaWAN 868/915 MHz mesh radios",
                "ESP32-S3 microcontrollers with solar harvesting",
                "InfluxDB time-series backend",
                "Grafana dashboards",
                "MQTT broker (Mosquitto) for edge-to-cloud relay",
            ],
            "data_sources": [
                "Onboard BME680 air-quality / VOC sensors",
                "Capacitive soil-moisture probes (0-60 cm depth)",
                "PIR + mmWave radar pedestrian counters",
                "OpenDataPhilly parcel geometry (OPA dataset)",
                "PurpleAir community air-quality reference stations",
            ],
            "api_endpoints": [
                "GET  /api/v1/lots/{parcel_id}/readings — latest sensor snapshot",
                "GET  /api/v1/lots/{parcel_id}/history?range=7d — time-series",
                "POST /api/v1/lots/{parcel_id}/alerts — threshold alert config",
                "GET  /api/v1/network/health — mesh connectivity status",
            ],
            "privacy_model": (
                "All sensor data is aggregated at the parcel level; no cameras "
                "or microphones are deployed. Foot traffic counts use anonymous "
                "thermal signatures — no PII is collected or stored. Data is "
                "published under an Open Data Commons PDDL license."
            ),
            "deployment_cost": "$1,200 per node (hardware + install); $80/yr cloud",
        },
        "tags": ["iot", "sensors", "air-quality", "open-data", "lorawan"],
    },
    {
        "title": "Community Voice App",
        "summary": (
            "A bilingual (English/Spanish) mobile app enabling neighbors to "
            "photograph lot conditions, report maintenance issues, propose new "
            "activations, and vote on community priorities via ranked-choice polls."
        ),
        "category": "community-app",
        "impact_level": 5,
        "feasibility": 4,
        "novelty": 3,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "technology_stack": [
                "React Native (iOS + Android) with Expo managed workflow",
                "FastAPI backend on Railway / Render",
                "PostgreSQL + PostGIS for spatial queries",
                "Firebase Cloud Messaging for push notifications",
                "Mapbox GL JS for parcel map overlay",
            ],
            "data_sources": [
                "User-submitted geotagged photos and condition reports",
                "OpenDataPhilly 311 service requests (L&I violations)",
                "City of Philadelphia parcel boundaries via ArcGIS REST",
                "U.S. Census ACS demographic context layers",
                "SPHERES activation registry (spheres-assets API)",
            ],
            "api_endpoints": [
                "POST /api/v1/reports — submit a condition report with photo",
                "GET  /api/v1/reports?bbox=... — reports in bounding box",
                "POST /api/v1/polls — create ranked-choice activation poll",
                "GET  /api/v1/polls/{poll_id}/results — live ranked results",
                "GET  /api/v1/feed/{neighborhood} — neighborhood activity feed",
            ],
            "privacy_model": (
                "Accounts use phone-number verification only; no real names "
                "required. Photos are stripped of EXIF data before storage. "
                "Reports can be submitted anonymously. All poll votes are "
                "encrypted at rest and tallied using an auditable open-source "
                "ranked-choice algorithm."
            ),
            "user_count_target": "15,000 active monthly users within 18 months",
        },
        "tags": ["mobile-app", "community", "voting", "bilingual", "civic-tech"],
    },
    {
        "title": "Digital Twin City Layer",
        "summary": (
            "A real-time 3D digital twin of all 40,000+ vacant parcels rendered "
            "in the browser, overlaying activation status, sensor feeds, and "
            "community sentiment onto a photorealistic CesiumJS city model."
        ),
        "category": "digital-twin",
        "impact_level": 4,
        "feasibility": 2,
        "novelty": 5,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "technology_stack": [
                "CesiumJS + 3D Tiles for terrain and building meshes",
                "Three.js custom overlays for activation visualizations",
                "Deck.gl data layers (heatmaps, arcs, hex bins)",
                "GraphQL federation gateway (Apollo Router)",
                "WebSocket push for live sensor + event streams",
            ],
            "data_sources": [
                "Philadelphia LiDAR point cloud (2023 flight, PASDA)",
                "OpenStreetMap building footprints via Overture Maps",
                "Lot Pulse IoT sensor feeds (see sister innovation)",
                "SPHERES activation status from spheres-assets DB",
                "Philadelphia Office of Property Assessment (OPA) bulk data",
            ],
            "api_endpoints": [
                "GET  /api/v1/twin/tiles/{z}/{x}/{y}.b3dm — 3D tile endpoint",
                "WS   /api/v1/twin/live — WebSocket live parcel event stream",
                "GET  /api/v1/twin/parcels?status=activated — filtered GeoJSON",
                "POST /api/v1/twin/scenarios — save scenario snapshot",
            ],
            "privacy_model": (
                "Building meshes are derived from public LiDAR; no interior "
                "scans. Parcel-level data is public record via OPA. User "
                "scenario snapshots are private by default and shareable via "
                "tokenized links with a 30-day expiry."
            ),
            "integration_points": [
                "spheres-viz — embed twin viewer in SPHERES visualization suite",
                "spheres-brain — feed twin state into decision-support models",
                "spheres-studio — export activation designs as 3D-tile overlays",
            ],
        },
        "tags": ["digital-twin", "3d", "cesium", "geospatial", "real-time"],
    },
    {
        "title": "Space Matching Algorithm",
        "summary": (
            "An ML pipeline that scores every vacant parcel against activation "
            "archetypes (pocket park, urban farm, maker space, etc.) using soil, "
            "sunlight, walkability, demographics, and zoning feature vectors."
        ),
        "category": "ml-platform",
        "impact_level": 4,
        "feasibility": 3,
        "novelty": 5,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "technology_stack": [
                "scikit-learn gradient-boosted classifier (LightGBM)",
                "Feature store in DuckDB (columnar, zero-copy parquet)",
                "MLflow experiment tracking and model registry",
                "FastAPI serving layer with async batch scoring",
                "Shapley (SHAP) explainability reports per recommendation",
            ],
            "data_sources": [
                "USDA Web Soil Survey — soil type and drainage class",
                "Google Solar API — annual solar irradiance per parcel",
                "Walk Score / EPA Smart Location Database — walkability",
                "OpenDataPhilly zoning overlays + L&I permit history",
                "Community Voice App sentiment and poll preference data",
            ],
            "api_endpoints": [
                "GET  /api/v1/match/{parcel_id} — top-5 activation recommendations",
                "POST /api/v1/match/batch — score a list of parcel IDs",
                "GET  /api/v1/match/{parcel_id}/explain — SHAP feature breakdown",
                "POST /api/v1/match/retrain — trigger model retraining pipeline",
            ],
            "privacy_model": (
                "Model features use only public and aggregated data; no "
                "individual-level demographics. Recommendations include a "
                "fairness audit score (demographic parity across council "
                "districts) published with every model version."
            ),
            "deployment_cost": "$350/mo cloud compute (GPU spot instances for retraining)",
        },
        "tags": ["machine-learning", "recommendations", "explainability", "equity"],
    },
    {
        "title": "Activation Dashboard",
        "summary": (
            "A city-wide operational dashboard showing real-time status of every "
            "activated space — maintenance alerts, visitor counts, event "
            "calendars, funding burn rates, and community satisfaction scores."
        ),
        "category": "data-dashboard",
        "impact_level": 4,
        "feasibility": 4,
        "novelty": 3,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "technology_stack": [
                "Next.js 14 with React Server Components",
                "D3.js + Observable Plot for custom charts",
                "MapLibre GL JS with PMTiles vector basemap",
                "tRPC typed API layer over PostgreSQL views",
                "Redis pub/sub for server-sent event (SSE) push",
            ],
            "data_sources": [
                "SPHERES activation registry (spheres-assets)",
                "Lot Pulse IoT sensor aggregates",
                "Community Voice App satisfaction survey results",
                "Philadelphia Land Bank disposition pipeline data",
                "Grant and budget tracking from spheres-legal contracts",
            ],
            "api_endpoints": [
                "GET  /api/v1/dashboard/overview — KPI summary cards",
                "GET  /api/v1/dashboard/map — GeoJSON activation layer",
                "GET  /api/v1/dashboard/timeseries?metric=visitors — chart data",
                "SSE  /api/v1/dashboard/stream — live event push channel",
            ],
            "user_count_target": (
                "200 city staff, 50 partner nonprofits, unlimited public "
                "read-only view via embedded iframe widget"
            ),
            "integration_points": [
                "spheres-brain — pull predictive analytics into dashboard panels",
                "spheres-legal — surface contract milestone and compliance flags",
                "spheres-viz — share chart components with the SPHERES web portal",
            ],
        },
        "tags": ["dashboard", "monitoring", "operations", "next-js", "open-data"],
    },
    {
        "title": "Blockchain Land Registry",
        "summary": (
            "A transparent, append-only stewardship ledger tracking community "
            "parcel custody chains — ownership transfers, stewardship agreements, "
            "maintenance logs, and activation permits — anchored to a public chain."
        ),
        "category": "blockchain-registry",
        "impact_level": 3,
        "feasibility": 2,
        "novelty": 5,
        "time_horizon": "far",
        "status": "approved",
        "details": {
            "technology_stack": [
                "Hyperledger Fabric permissioned network (City + Land Bank nodes)",
                "IPFS content-addressed document store for deed images",
                "Polygon PoS anchoring for public verifiability",
                "Ceramic Network DID-based identity for stewards",
                "React + ethers.js explorer frontend",
            ],
            "data_sources": [
                "Philadelphia Recorder of Deeds — deed transfer records",
                "Philadelphia Land Bank — disposition and side-yard sales",
                "SPHERES stewardship agreements (spheres-legal)",
                "Community Voice App — steward activity attestations",
                "OpenDataPhilly tax delinquency and sheriff sale lists",
            ],
            "api_endpoints": [
                "GET  /api/v1/registry/{parcel_id}/chain — full custody chain",
                "POST /api/v1/registry/{parcel_id}/transfer — record transfer",
                "GET  /api/v1/registry/{parcel_id}/verify — on-chain proof",
                "POST /api/v1/registry/stewardship — log maintenance event",
            ],
            "privacy_model": (
                "Steward identities use decentralized identifiers (DIDs) that "
                "can be linked to real names only by the steward themselves. "
                "Property records mirror existing public deed information. "
                "Maintenance attestations are pseudonymous by default."
            ),
            "deployment_cost": "$5,000 initial Fabric network; $200/mo node hosting",
        },
        "tags": ["blockchain", "land-registry", "transparency", "stewardship", "web3"],
    },
]

# ---------------------------------------------------------------------------
# 8 Generator Templates
# ---------------------------------------------------------------------------

TEMPLATES: list[dict] = [
    {
        "title": "Neighborhood Mesh WiFi Commons",
        "summary": (
            "Deploy a community-owned mesh WiFi network across activated lots, "
            "providing free broadband while doubling as a data backhaul for IoT "
            "sensors and public kiosk terminals."
        ),
        "category": "connectivity",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [3, 4],
        "details": {
            "technology_stack": [
                "OpenWrt mesh nodes on Ubiquiti hardware",
                "WireGuard VPN tunnels for backhaul encryption",
                "RADIUS auth with optional captive-portal splash page",
            ],
            "data_sources": [
                "FCC broadband availability maps",
                "OpenDataPhilly utility pole locations",
                "SPHERES parcel activation GeoJSON",
            ],
            "api_endpoints": [
                "GET  /api/v1/mesh/status — node uptime and throughput",
                "GET  /api/v1/mesh/coverage — coverage polygon GeoJSON",
            ],
            "privacy_model": (
                "No deep-packet inspection; DNS-over-HTTPS enforced. "
                "Usage logs retained for 24 hours only, then purged."
            ),
            "deployment_cost": "$600 per node; $40/mo backhaul per hub site",
        },
        "tags": ["mesh-wifi", "digital-equity", "connectivity", "open-source"],
    },
    {
        "title": "Participatory Budgeting Engine",
        "summary": (
            "A quadratic-voting platform where residents allocate a virtual "
            "budget across proposed activations, surfacing genuine community "
            "priorities while limiting plutocratic capture."
        ),
        "category": "community-app",
        "time_horizon": "near",
        "impact_range": [4, 5],
        "feasibility_range": [3, 5],
        "novelty_range": [3, 5],
        "details": {
            "technology_stack": [
                "SvelteKit web app with progressive enhancement",
                "PostgreSQL with row-level security per council district",
                "Quadratic voting tally engine (open-source library)",
            ],
            "data_sources": [
                "City Council district boundaries",
                "SPHERES activation cost estimates",
                "Community Voice App demographic opt-in data",
            ],
            "api_endpoints": [
                "POST /api/v1/budget/vote — submit quadratic ballot",
                "GET  /api/v1/budget/results/{round_id} — allocation outcomes",
            ],
            "privacy_model": (
                "Voter identity verified by SMS one-time code; ballots are "
                "stored without link to phone number after verification."
            ),
            "user_count_target": "5,000 voters per budget round",
        },
        "tags": ["participatory-budgeting", "quadratic-voting", "democracy", "civic-tech"],
    },
    {
        "title": "Predictive Blight Early-Warning System",
        "summary": (
            "A time-series forecasting model that predicts which currently "
            "maintained parcels are at risk of falling into blight within "
            "12 months, enabling proactive intervention."
        ),
        "category": "ml-platform",
        "time_horizon": "medium",
        "impact_range": [4, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [4, 5],
        "details": {
            "technology_stack": [
                "Prophet + XGBoost ensemble forecaster",
                "Airflow DAG for weekly batch scoring",
                "PostGIS spatial joins for feature engineering",
            ],
            "data_sources": [
                "OpenDataPhilly L&I code violations (rolling 5-year)",
                "Philadelphia Water Dept. stormwater billing anomalies",
                "Lot Pulse IoT vegetation and soil degradation signals",
                "U.S. Postal Service vacancy indicator data",
            ],
            "api_endpoints": [
                "GET  /api/v1/blight/risk/{parcel_id} — 12-month risk score",
                "GET  /api/v1/blight/hotspots?threshold=0.7 — high-risk cluster GeoJSON",
            ],
            "privacy_model": (
                "Model uses parcel-level public records only. Risk scores "
                "are shared with authorized city staff; public dashboard "
                "shows census-tract aggregates only."
            ),
            "integration_points": [
                "spheres-brain — feed risk scores into decision-support engine",
                "Activation Dashboard — surface early-warning alerts in ops view",
            ],
        },
        "tags": ["prediction", "blight", "early-warning", "time-series", "equity"],
    },
    {
        "title": "Open API Gateway for SPHERES Ecosystem",
        "summary": (
            "A unified API gateway that federates data from all SPHERES services "
            "(assets, legal, studio, viz, brain) into a single developer-friendly "
            "GraphQL endpoint with API-key authentication and rate limiting."
        ),
        "category": "developer-platform",
        "time_horizon": "near",
        "impact_range": [3, 5],
        "feasibility_range": [3, 5],
        "novelty_range": [2, 4],
        "details": {
            "technology_stack": [
                "Apollo Router GraphQL federation gateway",
                "Kong or Tyk API gateway for auth and rate limiting",
                "OpenAPI 3.1 spec auto-generated from FastAPI subgraphs",
            ],
            "data_sources": [
                "spheres-assets activation registry",
                "spheres-legal contract and compliance data",
                "spheres-brain analytics and prediction outputs",
                "Lot Pulse and Community Voice upstream APIs",
            ],
            "api_endpoints": [
                "POST /graphql — federated query endpoint",
                "GET  /api/v1/health — gateway health check",
                "POST /api/v1/keys — developer API key provisioning",
            ],
            "privacy_model": (
                "Tiered access: public (read-only open data), partner "
                "(authenticated write), admin (full mutation). Rate "
                "limited to 1,000 req/min per key."
            ),
            "deployment_cost": "$150/mo managed gateway; free tier for civic hackers",
        },
        "tags": ["api-gateway", "graphql", "developer-experience", "federation"],
    },
    {
        "title": "Augmented Reality Lot Previewer",
        "summary": (
            "A mobile AR experience that lets residents point their phone at a "
            "vacant lot and see a proposed activation rendered in place — pocket "
            "parks, murals, and farm plots overlaid on the real scene."
        ),
        "category": "ar-experience",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [2, 3],
        "novelty_range": [4, 5],
        "details": {
            "technology_stack": [
                "ARCore (Android) + ARKit (iOS) via Unity AR Foundation",
                "Cloud Anchors for persistent, geo-located 3D models",
                "glTF 2.0 activation models exported from spheres-studio",
            ],
            "data_sources": [
                "Space Matching Algorithm top recommendations per parcel",
                "SPHERES design library (3D model catalog)",
                "GPS + visual-inertial odometry for precise placement",
            ],
            "api_endpoints": [
                "GET  /api/v1/ar/models/{parcel_id} — activation 3D asset bundle",
                "POST /api/v1/ar/feedback — user reaction / preference capture",
            ],
            "privacy_model": (
                "Camera frames are processed on-device only; no images are "
                "uploaded. Feedback submissions are anonymized. Location "
                "data is rounded to parcel centroid before storage."
            ),
            "user_count_target": "10,000 AR sessions within first pilot year",
        },
        "tags": ["augmented-reality", "visualization", "community-engagement", "3d"],
    },
    {
        "title": "Event & Programming Scheduler Platform",
        "summary": (
            "A shared calendar and booking engine for activated spaces — "
            "community groups reserve time slots, equipment, and permits "
            "through a self-service portal with automated conflict detection."
        ),
        "category": "community-app",
        "time_horizon": "near",
        "impact_range": [3, 4],
        "feasibility_range": [4, 5],
        "novelty_range": [2, 3],
        "details": {
            "technology_stack": [
                "Django + django-scheduler with CalDAV sync",
                "Stripe Connect for optional booking fee splits",
                "Twilio SMS reminders and confirmation flow",
            ],
            "data_sources": [
                "SPHERES activation registry for available spaces",
                "Philadelphia Parks & Rec permit calendar",
                "Community Voice App event interest surveys",
            ],
            "api_endpoints": [
                "POST /api/v1/bookings — create reservation",
                "GET  /api/v1/bookings?space_id=...&week=... — availability grid",
                "DELETE /api/v1/bookings/{id} — cancel with 48-hr policy",
            ],
            "privacy_model": (
                "Organizer contact info visible to space steward only. "
                "Public calendar shows event title and time; no organizer PII."
            ),
            "user_count_target": "500 bookings/month across 100 activated spaces",
        },
        "tags": ["scheduling", "booking", "events", "community-programming"],
    },
    {
        "title": "Civic Data Lake & Analytics Warehouse",
        "summary": (
            "A managed data lake that ingests, cleans, and joins all SPHERES "
            "operational data with Philadelphia open datasets, providing SQL "
            "access for researchers, journalists, and civic hackers."
        ),
        "category": "data-infrastructure",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [3, 4],
        "novelty_range": [3, 4],
        "details": {
            "technology_stack": [
                "Apache Iceberg tables on S3-compatible object storage",
                "DuckDB + dbt for transformation pipelines",
                "Metabase self-service BI for non-technical users",
            ],
            "data_sources": [
                "All SPHERES service databases (CDC replication)",
                "OpenDataPhilly catalog (100+ datasets, automated ingest)",
                "U.S. Census Bureau ACS and decennial microdata",
                "EPA Toxics Release Inventory and brownfield listings",
            ],
            "api_endpoints": [
                "POST /api/v1/lake/query — SQL query execution (read-only)",
                "GET  /api/v1/lake/catalog — available tables and schemas",
                "GET  /api/v1/lake/lineage/{table} — data lineage graph",
            ],
            "privacy_model": (
                "PII columns are hashed or dropped during ingestion. "
                "Row-level access control enforced per dataset sensitivity tier."
            ),
            "deployment_cost": "$500/mo storage + compute; free query tier for .edu and .org",
        },
        "tags": ["data-lake", "analytics", "open-data", "research", "dbt"],
    },
    {
        "title": "Accessibility & Equity Audit Bot",
        "summary": (
            "An automated compliance scanner that evaluates every activation "
            "proposal against ADA accessibility standards, language-access "
            "requirements, and equity metrics before approval."
        ),
        "category": "compliance-automation",
        "time_horizon": "medium",
        "impact_range": [4, 5],
        "feasibility_range": [3, 4],
        "novelty_range": [3, 5],
        "details": {
            "technology_stack": [
                "Rule engine built on Python Pydantic validators",
                "NLP classifier for proposal text (spaCy + zero-shot)",
                "GitHub Actions integration for CI-style audit reports",
            ],
            "data_sources": [
                "ADA Accessibility Guidelines (ADAAG) checklist database",
                "City of Philadelphia language-access policy thresholds",
                "Census tract demographic and income quintile data",
                "SPHERES activation proposals submitted via Community Voice",
            ],
            "api_endpoints": [
                "POST /api/v1/audit/run — submit proposal for audit",
                "GET  /api/v1/audit/{audit_id}/report — structured findings",
                "GET  /api/v1/audit/stats — citywide equity score trends",
            ],
            "privacy_model": (
                "Audit reports reference parcel and proposal IDs only. "
                "Demographic data used in aggregate; no individual records."
            ),
            "integration_points": [
                "spheres-legal — block non-compliant proposals from execution",
                "Activation Dashboard — surface equity scores in KPI panels",
            ],
        },
        "tags": ["accessibility", "equity", "compliance", "automation", "ada"],
    },
]
