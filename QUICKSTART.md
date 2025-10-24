# 🚀 Quick Start Guide for Beginners

This guide will walk you through getting your Editto MVP running in **under 1 hour**.

## Prerequisites

- [ ] GitHub account
- [ ] Credit card (for RunPod)
- [ ] $15-20 budget for initial testing

---

## Phase 1: Sign Up (15 minutes)

### Do these in order:

1. **GitHub** → github.com → Sign up → FREE
2. **Vercel** → vercel.com → Sign up with GitHub → FREE
3. **Railway** → railway.app → Sign up with GitHub → $5 trial
4. **Cloudflare** → cloudflare.com → Sign up → Go to R2 → Create bucket "editto-videos" → FREE
5. **RunPod** → runpod.io → Sign up → Add $10-20 credit → Pay per use

**Total time:** 15 minutes
**Money spent:** $10-20 (RunPod credit only)

---

## Phase 2: Get Your Credentials (10 minutes)

### Cloudflare R2:

1. In Cloudflare dashboard → R2
2. Click "Manage R2 API Tokens"
3. Create token → Copy Access Key ID, Secret Key, and Endpoint URL
4. Note your bucket name: `editto-videos`

### RunPod:

1. In RunPod dashboard → Settings
2. Create API Key → Copy it
3. Keep this for later (we'll get the Endpoint ID after deployment)

**Save these somewhere safe!**

---

## Phase 3: Deploy Backend (15 minutes)

### On Your Computer:

```bash
# Navigate to the project folder
cd editto-mvp

# Initialize git
git init
git add .
git commit -m "Initial commit"

# Create GitHub repo (if you have GitHub CLI)
gh repo create editto-mvp --public --source=. --push

# Or push manually:
# 1. Create repo on GitHub website
# 2. git remote add origin https://github.com/YOUR_USERNAME/editto-mvp.git
# 3. git push -u origin main
```

### On Railway:

1. Go to railway.app dashboard
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `editto-mvp`
4. Click "+ New" → "Database" → "PostgreSQL"
5. Click "+ New" → "Database" → "Redis"
6. Click on the backend service
7. Settings → Root Directory → Set to `/backend`
8. Settings → Environment Variables → Add:

```
R2_ENDPOINT=https://YOUR_ID.r2.cloudflarestorage.com
R2_ACCESS_KEY=your_access_key
R2_SECRET_KEY=your_secret_key
R2_BUCKET_NAME=editto-videos
R2_PUBLIC_URL=https://pub-YOUR_ID.r2.dev
RUNPOD_API_KEY=your_key_here
RUNPOD_ENDPOINT_ID=we_will_set_this_later
```

9. Copy your Railway backend URL (e.g., `editto-backend.up.railway.app`)

---

## Phase 4: Deploy Frontend (10 minutes)

### On Vercel:

1. Go to vercel.com dashboard
2. Click "Add New" → "Project"
3. Import `editto-mvp` from GitHub
4. Configure:
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`
5. Environment Variables → Add:

```
NEXT_PUBLIC_API_URL=https://your-railway-backend-url.up.railway.app
```

6. Click "Deploy"
7. Wait for deployment (2-3 minutes)
8. Copy your Vercel URL (e.g., `editto-mvp.vercel.app`)

---

## Phase 5: Setup GPU Worker (20 minutes)

### Build Docker Image (on your computer):

```bash
# Install Docker first if you haven't
# Download from docker.com

# Login to Docker Hub
docker login

# Build and push
cd gpu-worker

# Edit build.sh - change DOCKER_USERNAME to yours
# Then run:
chmod +x build.sh
./build.sh
```

This will take 10-15 minutes to build and push.

### Create RunPod Endpoint:

1. Go to runpod.io → Serverless
2. Click "New Endpoint"
3. Configure:
   - Name: `editto-worker`
   - Select: **RTX A6000 (48GB)**
   - Container Image: `your-dockerhub-username/editto-worker:latest`
   - Container Disk: 20GB
   - Env Variables:
     ```
     R2_ENDPOINT=https://YOUR_ID.r2.cloudflarestorage.com
     R2_ACCESS_KEY=your_access_key
     R2_SECRET_KEY=your_secret_key
     R2_BUCKET_NAME=editto-videos
     R2_PUBLIC_URL=https://pub-YOUR_ID.r2.dev
     ```
4. Deploy
5. Copy the **Endpoint ID**

### Update Railway:

1. Go back to Railway backend
2. Update environment variable:
   ```
   RUNPOD_ENDPOINT_ID=your_actual_endpoint_id
   ```

---

## Phase 6: Test It! (5 minutes)

1. Go to your Vercel URL
2. Upload a short test video (keep it under 10MB)
3. Enter instruction: "make it black and white"
4. Click "Upload & Edit Video"
5. Watch the "Your Videos" section
6. Refresh after 30 seconds to see status

**Note:** The GPU worker currently has placeholder code. It won't actually edit the video yet - you need to implement the Editto inference code.

---

## What You've Built

✅ Frontend hosted on Vercel (FREE)
✅ Backend API on Railway ($5/month)
✅ Database on Railway (included)
✅ Redis queue on Railway (included)
✅ Video storage on Cloudflare R2 (FREE up to 10GB)
✅ GPU processing on RunPod ($0.50/hour when running)

---

## Next Steps

### Immediate:

1. **Test with a real video** - Upload and check status
2. **Monitor costs** - Check RunPod dashboard
3. **Verify storage** - Check videos appear in R2 bucket

### Soon:

1. **Implement actual Editto inference** - The GPU worker currently just copies the video
2. **Add authentication** - So not everyone can use your GPU
3. **Set usage limits** - Protect against abuse
4. **Improve UI** - Make it prettier

### Before Going Public:

1. ✅ Implement real video editing (Editto model)
2. ✅ Add user authentication
3. ✅ Add rate limiting
4. ✅ Set up monitoring
5. ✅ Test thoroughly
6. ✅ Add terms of service

---

## Cost Reminders

- **RunPod charges per second** of GPU use
- A 4-minute video processing = $0.03 (at $0.50/hour)
- 100 videos/day = ~$3/day = $90/month
- **Set up spending limits in RunPod!**

---

## Troubleshooting

### "Backend not responding"
- Check Railway backend is running
- Visit `https://your-backend.railway.app/health`
- Check environment variables are set

### "Video upload fails"
- Check R2 credentials
- Verify bucket name is correct
- Check bucket has public access

### "Docker build fails"
- Ensure Docker is installed and running
- Check you have enough disk space (need ~10GB)
- Try: `docker system prune -a` to free space

### "RunPod endpoint not working"
- Check container logs in RunPod dashboard
- Verify environment variables are set
- Check image was pushed to Docker Hub successfully

---

## Need Help?

1. Check the main README.md for detailed troubleshooting
2. Check service-specific documentation:
   - Railway: docs.railway.app
   - Vercel: vercel.com/docs
   - RunPod: docs.runpod.io
3. Review Editto repo: github.com/EzioBy/Ditto

---

## Success Checklist

- [ ] All services signed up
- [ ] Backend deployed on Railway
- [ ] Frontend deployed on Vercel
- [ ] GPU worker image built and pushed
- [ ] RunPod endpoint created
- [ ] All environment variables set
- [ ] Test video uploaded successfully
- [ ] Can see video in "Your Videos" section

---

**Congratulations!** You've deployed a complete AI video editing platform! 🎉

Start with test videos, monitor your costs, and improve incrementally. You've got this! 💪
