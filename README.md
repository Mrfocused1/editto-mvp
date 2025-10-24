# Editto MVP - AI Video Editing Platform

A complete end-to-end MVP for AI-powered video editing using the Editto model. Users upload videos and provide text instructions to edit them.

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌────────────┐
│   Next.js   │─────▶│   FastAPI    │─────▶│   Redis    │
│  Frontend   │      │   Backend    │      │   Queue    │
│  (Vercel)   │      │  (Railway)   │      │ (Railway)  │
└─────────────┘      └──────────────┘      └────────────┘
                             │                     │
                             │                     │
                             ▼                     ▼
                     ┌──────────────┐      ┌────────────┐
                     │ Cloudflare R2│◀─────│   RunPod   │
                     │    Storage   │      │ GPU Worker │
                     └──────────────┘      └────────────┘
```

## 💰 Cost Breakdown

### Monthly Costs (Estimated)

| Service | Cost | Usage |
|---------|------|-------|
| **Vercel** (Frontend) | $0 | Free tier |
| **Railway** (Backend + Redis) | $5/month | Hobby plan |
| **Cloudflare R2** (Storage) | $0 | Free 10GB tier |
| **RunPod** (GPU) | $24-100/month | $0.50/hr, varies by usage |
| **Total** | **$30-105/month** | Depending on video processing volume |

**Light usage (5 videos/day):** ~$30/month
**Medium usage (20 videos/day):** ~$100/month

## 🚀 Setup Guide

### Prerequisites

- GitHub account
- Basic command line knowledge
- Credit card (for RunPod, even on trial)

### Step 1: Sign Up for Services (In Order)

#### 1.1 GitHub
1. Go to [github.com](https://github.com)
2. Sign up for a free account
3. Verify your email

#### 1.2 Vercel (Frontend Hosting)
1. Go to [vercel.com](https://vercel.com)
2. Click "Sign Up" → "Continue with GitHub"
3. Select the Hobby (FREE) plan
4. **Cost:** FREE

#### 1.3 Railway (Backend + Database + Redis)
1. Go to [railway.app](https://railway.app)
2. Click "Login" → "Login with GitHub"
3. You'll get $5 trial credit automatically
4. Add payment method (required, charges start after trial)
5. **Cost:** $5 trial, then $5/month

#### 1.4 Cloudflare (Video Storage)
1. Go to [cloudflare.com](https://cloudflare.com)
2. Sign up for an account
3. In dashboard, go to R2 section
4. Enable R2 (may need to add payment method)
5. Create a bucket named `editto-videos`
6. **Cost:** FREE for 10GB storage

#### 1.5 RunPod (GPU Processing)
1. Go to [runpod.io](https://runpod.io)
2. Sign up for an account
3. Add payment method (required)
4. Add $10-20 credit to start
5. **Cost:** ~$0.50/hour when GPU is running

---

## 📦 Deployment Instructions

### Part 1: Deploy Backend to Railway

#### 1. Create a New GitHub Repository

```bash
cd editto-mvp
git init
git add .
git commit -m "Initial commit"
gh repo create editto-mvp --public --source=. --push
```

Or create manually on GitHub and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/editto-mvp.git
git push -u origin main
```

#### 2. Deploy Backend on Railway

1. Go to [railway.app](https://railway.app) dashboard
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your `editto-mvp` repository
4. Railway will detect the backend service automatically

#### 3. Add PostgreSQL Database

1. In your Railway project, click "+ New"
2. Select "Database" → "Add PostgreSQL"
3. Railway will automatically set the `DATABASE_URL` environment variable

#### 4. Add Redis

1. Click "+ New" again
2. Select "Database" → "Add Redis"
3. Railway will automatically set the `REDIS_URL` environment variable

#### 5. Configure Backend Environment Variables

In Railway backend service settings, add these variables:

```env
# Cloudflare R2 (get from Cloudflare dashboard)
R2_ENDPOINT=https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com
R2_ACCESS_KEY=your_r2_access_key
R2_SECRET_KEY=your_r2_secret_key
R2_BUCKET_NAME=editto-videos
R2_PUBLIC_URL=https://your-r2-public-url.com

# RunPod API (we'll set this later)
RUNPOD_API_KEY=your_key_here
RUNPOD_ENDPOINT_ID=your_endpoint_id_here
```

#### 6. Set Root Directory

1. In Railway backend service settings
2. Go to "Settings" → "Root Directory"
3. Set to `/backend`
4. Save changes

#### 7. Get Backend URL

- Railway will provide a public URL like `https://editto-backend.up.railway.app`
- Copy this URL for the frontend configuration

---

### Part 2: Deploy Frontend to Vercel

#### 1. Deploy to Vercel

```bash
cd frontend
npm install
```

Then deploy:
1. Go to [vercel.com](https://vercel.com) dashboard
2. Click "Add New" → "Project"
3. Import your `editto-mvp` repository
4. Configure:
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `.next`

#### 2. Add Environment Variables

In Vercel project settings, add:

```env
NEXT_PUBLIC_API_URL=https://your-railway-backend-url.up.railway.app
```

Replace with your actual Railway backend URL.

#### 3. Deploy

- Click "Deploy"
- Vercel will build and deploy your frontend
- You'll get a URL like `https://editto-mvp.vercel.app`

---

### Part 3: Setup GPU Worker on RunPod

#### 1. Build Docker Image

First, install Docker on your local machine, then:

```bash
cd gpu-worker

# Login to Docker Hub
docker login

# Update build.sh with your Docker Hub username
# Then build and push
chmod +x build.sh
./build.sh
```

This will create and push an image like `your-username/editto-worker:latest`

#### 2. Create RunPod Serverless Endpoint

1. Go to [RunPod Serverless](https://www.runpod.io/console/serverless)
2. Click "New Endpoint"
3. Configure:
   - **Name:** editto-worker
   - **GPU Type:** RTX A6000 (48GB)
   - **Container Image:** `your-username/editto-worker:latest`
   - **Container Disk:** 20GB minimum
   - **Environment Variables:**
     ```
     R2_ENDPOINT=https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com
     R2_ACCESS_KEY=your_r2_access_key
     R2_SECRET_KEY=your_r2_secret_key
     R2_BUCKET_NAME=editto-videos
     R2_PUBLIC_URL=https://your-r2-public-url.com
     ```

4. Click "Deploy"

#### 3. Get Endpoint Credentials

- After deployment, you'll get:
  - **Endpoint ID:** (e.g., `abc123def456`)
  - **API Key:** Generate in RunPod settings

#### 4. Update Railway Backend

Go back to Railway and update these environment variables:

```env
RUNPOD_API_KEY=your_runpod_api_key
RUNPOD_ENDPOINT_ID=your_runpod_endpoint_id
```

---

### Part 4: Configure Cloudflare R2

#### 1. Create R2 Bucket

1. In Cloudflare dashboard, go to R2
2. Create bucket named `editto-videos`
3. Enable public access

#### 2. Get API Credentials

1. Go to "Manage R2 API Tokens"
2. Create new token with "Object Read & Write" permissions
3. Copy:
   - Access Key ID
   - Secret Access Key
   - Endpoint URL

#### 3. Setup Public Domain (Optional but Recommended)

1. In R2 bucket settings, go to "Settings" → "Public Access"
2. Enable public access
3. You can:
   - Use the default R2.dev domain
   - Or connect a custom domain

---

## 🧪 Testing Your MVP

### 1. Test Locally (Optional)

#### Backend:
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python main.py
```

#### Frontend:
```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with backend URL
npm run dev
```

Visit `http://localhost:3000`

### 2. Test Production

1. Visit your Vercel URL
2. Upload a short test video (< 10MB recommended)
3. Enter an instruction like "make it black and white"
4. Click "Upload & Edit Video"
5. Check the "Your Videos" section for status
6. Refresh page to see updates (polls every 10 seconds)

---

## 🐛 Troubleshooting

### Backend Issues

**Problem:** Backend won't start on Railway

**Solution:**
- Check that root directory is set to `/backend`
- Verify all environment variables are set
- Check Railway logs for errors

**Problem:** Database connection errors

**Solution:**
- Ensure PostgreSQL is added to project
- Check `DATABASE_URL` is set automatically
- Restart the backend service

### Frontend Issues

**Problem:** Can't connect to backend

**Solution:**
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check CORS is enabled in backend
- Test backend health endpoint: `https://your-backend.railway.app/health`

### GPU Worker Issues

**Problem:** Docker build fails

**Solution:**
- Ensure you have enough disk space
- Check Docker is installed and running
- Try building with `--no-cache` flag

**Problem:** RunPod endpoint times out

**Solution:**
- Check GPU worker logs in RunPod dashboard
- Verify environment variables are set
- Increase timeout in `backend/tasks.py`

### Storage Issues

**Problem:** Videos not uploading to R2

**Solution:**
- Verify R2 credentials in environment variables
- Check bucket name is correct
- Ensure bucket has public access enabled

---

## 📊 Monitoring Costs

### RunPod
- Dashboard shows real-time GPU usage
- Charges accumulate per second of GPU time
- Set up spending limits in settings

### Railway
- Dashboard shows resource usage
- $5/month includes $5 credit
- Additional usage billed separately

### Cloudflare R2
- Free tier: 10GB storage, 1M Class A operations, 10M Class B operations
- Monitor usage in R2 dashboard
- No egress fees (huge savings!)

---

## 🔄 What's Next?

### Current MVP Limitations

1. **GPU Worker is Placeholder:** The handler.py currently just copies the video. You need to implement actual Editto inference.
2. **No Authentication:** Anyone can use your site. Add auth before going public.
3. **No Usage Limits:** Add rate limiting to prevent abuse.
4. **Basic UI:** Consider improving the design and UX.

### Recommended Improvements

1. **Implement Editto Inference:**
   - Download model weights
   - Add actual video processing code in `gpu-worker/handler.py`
   - Test with various editing instructions

2. **Add User Authentication:**
   - Use NextAuth.js or Clerk
   - Track users and their videos
   - Add usage quotas

3. **Improve Job Management:**
   - Add webhook notifications when videos are ready
   - Email notifications
   - Better error handling and retry logic

4. **Optimize Costs:**
   - Cache popular edits
   - Batch multiple small jobs
   - Auto-scale GPU workers

5. **Enhanced UI:**
   - Real-time progress updates
   - Video preview/trim before upload
   - Gallery with filters and search

---

## 📝 Important Notes

### Security

- Never commit `.env` files to Git
- Keep API keys secret
- Add rate limiting before going public
- Implement user authentication

### Production Checklist

- [ ] Change CORS origins from `*` to specific domains
- [ ] Add authentication
- [ ] Set up monitoring and alerts
- [ ] Add usage analytics
- [ ] Implement rate limiting
- [ ] Add Terms of Service and Privacy Policy
- [ ] Test with various video formats and sizes
- [ ] Set up automated backups
- [ ] Add error tracking (e.g., Sentry)
- [ ] Optimize video compression

---

## 🆘 Getting Help

1. **Editto Issues:** Check the [Editto GitHub](https://github.com/EzioBy/Ditto)
2. **Deployment Issues:** Railway and Vercel have excellent docs
3. **General Questions:** Open an issue in this repository

---

## 📄 License

This project is provided as-is for educational purposes. The Editto model has its own license - please review the [Editto repository](https://github.com/EzioBy/Ditto) for terms.

---

## 🎉 Congratulations!

You now have a complete AI video editing platform! Start small, test thoroughly, and scale as you grow.

Remember to monitor your costs, especially GPU usage on RunPod. Start with short videos and low traffic until you're confident in your setup.

Good luck with your MVP! 🚀
