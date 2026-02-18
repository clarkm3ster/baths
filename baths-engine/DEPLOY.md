# 🏛️ BATHS Game Engine - Docker Deployment

## Quick Start

### 1. Build and Run

```bash
cd baths-engine
docker-compose up -d
```

The game will be available at: **http://localhost:9000**

### 2. Stop

```bash
docker-compose down
```

---

## Deploy to Cloud

### Option A: Railway.app (Easiest)

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `baths` repo
5. Set root directory: `baths-engine`
6. Railway auto-detects Dockerfile
7. Your app will be live with a public URL!

### Option B: DigitalOcean App Platform

1. Go to https://cloud.digitalocean.com/apps
2. Click "Create App"
3. Connect your GitHub repo
4. Select `baths-engine` directory
5. DigitalOcean auto-detects Dockerfile
6. Deploy!

### Option C: Render.com

1. Go to https://render.com
2. New > Web Service
3. Connect repo
4. Root directory: `baths-engine`
5. Build command: `docker build -t baths .`
6. Start command: `docker run -p 9000:9000 baths`

### Option D: Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login and deploy
cd baths-engine
fly launch
fly deploy
```

---

## Environment Variables

None required for basic operation.

For production with real API integration:
- `API_BASE_URL` - Base URL for BATHS backend APIs

---

## What's Included

- ✅ Game engine backend
- ✅ React frontend
- ✅ All dependencies
- ✅ Production build
- ✅ Single container, single port (9000)

---

## Testing Locally

```bash
# Build
docker build -t baths-engine .

# Run
docker run -p 9000:9000 baths-engine

# Open browser
open http://localhost:9000
```

---

Built by Mike @ BATHS with Molty 🏛️
