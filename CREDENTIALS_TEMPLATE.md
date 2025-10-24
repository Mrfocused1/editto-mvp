# Credentials Checklist

Use this to keep track of all your credentials. **NEVER commit this file to Git!**

---

## ☁️ Cloudflare R2

```
R2_ENDPOINT: https://_____________________.r2.cloudflarestorage.com
R2_ACCESS_KEY: _____________________________________
R2_SECRET_KEY: _____________________________________
R2_BUCKET_NAME: editto-videos
R2_PUBLIC_URL: https://pub-_____________________.r2.dev
```

**Where to find:**
- Cloudflare Dashboard → R2 → Manage R2 API Tokens
- Public URL: R2 bucket settings → Public Access

---

## 🚂 Railway

```
Backend URL: https://_____________________.up.railway.app
DATABASE_URL: (automatically set by Railway)
REDIS_URL: (automatically set by Railway)
```

**Where to find:**
- Railway project → Backend service → Settings → Domains
- Database/Redis URLs are auto-generated

---

## 🎨 Vercel

```
Frontend URL: https://_____________________.vercel.app
NEXT_PUBLIC_API_URL: (your Railway backend URL)
```

**Where to find:**
- Vercel project → Settings → Domains

---

## 🎮 RunPod

```
RUNPOD_API_KEY: _____________________________________
RUNPOD_ENDPOINT_ID: _____________________________________
```

**Where to find:**
- API Key: RunPod Dashboard → Settings → API Keys
- Endpoint ID: RunPod → Serverless → Your endpoint

---

## 🐳 Docker Hub

```
Docker Username: _____________________________________
Docker Password: _____________________________________
Image Name: _____________________________________/editto-worker:latest
```

**Where to find:**
- hub.docker.com

---

## GitHub

```
Repository URL: https://github.com/_____________________/editto-mvp
```

---

## Quick Reference URLs

- **Frontend (Live Site):** ___________________________________________
- **Backend API Health:** ___________________________________________/health
- **Railway Dashboard:** https://railway.app/project/YOUR_PROJECT_ID
- **Vercel Dashboard:** https://vercel.com/YOUR_USERNAME/editto-mvp
- **RunPod Dashboard:** https://www.runpod.io/console/serverless
- **Cloudflare Dashboard:** https://dash.cloudflare.com/

---

## Environment Variables Setup

### Backend (Railway)

Copy these into Railway → Backend Service → Variables:

```env
R2_ENDPOINT=
R2_ACCESS_KEY=
R2_SECRET_KEY=
R2_BUCKET_NAME=editto-videos
R2_PUBLIC_URL=
RUNPOD_API_KEY=
RUNPOD_ENDPOINT_ID=
```

### Frontend (Vercel)

Copy these into Vercel → Project Settings → Environment Variables:

```env
NEXT_PUBLIC_API_URL=
```

### GPU Worker (RunPod)

Copy these into RunPod → Endpoint → Environment Variables:

```env
R2_ENDPOINT=
R2_ACCESS_KEY=
R2_SECRET_KEY=
R2_BUCKET_NAME=editto-videos
R2_PUBLIC_URL=
```

---

## Security Reminder

🔒 **NEVER:**
- Commit this file to Git
- Share these credentials publicly
- Post them in screenshots or videos
- Store them in unencrypted files

✅ **DO:**
- Use password managers
- Rotate keys periodically
- Keep backups securely
- Use environment variables

---

## Testing Checklist

- [ ] Backend health check works: `curl https://YOUR_BACKEND/health`
- [ ] Frontend loads without errors
- [ ] Can upload a video
- [ ] Video appears in R2 bucket
- [ ] Job status updates correctly
- [ ] GPU worker receives requests
- [ ] No console errors in browser

---

## Monthly Cost Tracking

| Month | Railway | RunPod | Total | Videos Processed |
|-------|---------|--------|-------|------------------|
| Jan   | $5      | $     | $     |                  |
| Feb   | $5      | $     | $     |                  |
| Mar   | $5      | $     | $     |                  |

**Goal:** Keep under $_____ per month

---

## Support Contacts

- Railway Support: help@railway.app
- Vercel Support: support@vercel.com
- RunPod Support: support@runpod.io
- Cloudflare Support: support.cloudflare.com

---

Last Updated: _______________
