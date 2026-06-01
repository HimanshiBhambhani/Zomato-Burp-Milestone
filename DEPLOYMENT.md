# Deployment Guide – BURP Restaurant Recommender

## Architecture
```
[User] → [Vercel (Next.js Frontend)] → [Railway (FastAPI Backend)] → [Groq LLM]
```

---

## 1. Deploy Backend on Railway

### Step 1: Push code to GitHub
```bash
cd "/Users/hibhambh/Desktop/Meta-folder/Next Leap/Zomato-Milestone"
git init
git add .
git commit -m "Initial commit - BURP restaurant recommender"
git remote add origin git@github.com:YOUR_USERNAME/burp-restaurant-recommender.git
git push -u origin main
```

### Step 2: Create Railway Project
1. Go to [railway.app](https://railway.app) → Sign in with GitHub
2. Click **"New Project"** → **"Deploy from GitHub Repo"**
3. Select your repo: `burp-restaurant-recommender`
4. Railway will auto-detect the `Dockerfile` and start building

### Step 3: Set Environment Variables on Railway
In Railway Dashboard → Your Service → **Variables** tab, add:

| Variable | Value |
|----------|-------|
| `GROQ_API_KEY` | `your-groq-api-key` |
| `FRONTEND_URL` | `https://your-app.vercel.app` (add after Vercel deploy) |
| `PORT` | `8000` (Railway auto-sets this, usually not needed) |

### Step 4: Set Root Directory (if monorepo)
If Railway deploys the frontend by mistake:
- Go to **Settings** → **Root Directory** → set to `/` (the project root, not `frontend/`)

### Step 5: Get your Railway URL
After deploy succeeds, Railway assigns a public URL like:
```
https://burp-backend-production.up.railway.app
```
Copy this – you'll need it for Vercel.

---

## 2. Deploy Frontend on Vercel

### Step 1: Import to Vercel
1. Go to [vercel.com](https://vercel.com) → Sign in with GitHub
2. Click **"Add New Project"** → Import your repo
3. **Important:** Set **Root Directory** to `frontend`
4. Framework Preset: **Next.js** (auto-detected)
5. Click **Deploy**

### Step 2: Set Environment Variables on Vercel
In Vercel Dashboard → Your Project → **Settings** → **Environment Variables**, add:

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_API_URL` | `https://burp-backend-production.up.railway.app` |

> Replace with your actual Railway URL from Step 1.5

### Step 3: Redeploy
After adding the env var, trigger a redeploy:
- Go to **Deployments** tab → click **"..."** on latest → **Redeploy**

### Step 4: Update Railway CORS
Go back to Railway and update the `FRONTEND_URL` variable:
```
FRONTEND_URL=https://your-app.vercel.app
```

---

## 3. Verify Deployment

1. Visit your Vercel URL (e.g., `https://burp-app.vercel.app`)
2. Try searching for restaurants
3. Check Railway logs if API calls fail

### Health Check
```bash
curl https://your-railway-url.up.railway.app/api/health
```
Should return:
```json
{"status": "ok", "orchestrator_ready": true, "restaurants_loaded": 91}
```

---

## 4. Troubleshooting

| Issue | Fix |
|-------|-----|
| API calls return 500 | Check Railway logs; likely missing `GROQ_API_KEY` |
| CORS errors in browser | Update `FRONTEND_URL` env var on Railway to match Vercel domain |
| Frontend shows no results | Verify `NEXT_PUBLIC_API_URL` is set correctly on Vercel, then redeploy |
| Railway build fails | Check Dockerfile; ensure `data/processed/zomato_clean.csv` is committed |
| "Module not found" on Railway | Ensure `requirements.txt` includes `fastapi` and `uvicorn` |

---

## 5. Cost Estimate

| Service | Plan | Cost |
|---------|------|------|
| Railway | Hobby | ~$5/month (pay-per-use, always-on) |
| Vercel | Free/Hobby | $0 (100GB bandwidth, generous for this app) |
| Groq API | Free tier | $0 (rate limited at ~30 req/min) |

---

## 6. Custom Domain (Optional)

**Vercel:** Settings → Domains → Add `burp.yourdomain.com`
**Railway:** Settings → Networking → Custom Domain → Add `api.burp.yourdomain.com`

---

## File Structure for Deployment
```
/                          ← Railway deploys from here
├── Dockerfile             ← Railway build instructions
├── railway.toml           ← Railway config
├── Procfile               ← Alternative to Dockerfile
├── requirements.txt       ← Python dependencies
├── api_server.py          ← FastAPI entrypoint
├── config.yaml
├── src/                   ← Python backend modules
├── data/processed/        ← Restaurant CSV data
├── prompts/               ← LLM prompt templates
└── frontend/              ← Vercel deploys from here
    ├── vercel.json        ← Vercel config
    ├── next.config.ts     ← Uses NEXT_PUBLIC_API_URL
    ├── package.json
    └── src/               ← React components & pages
```
