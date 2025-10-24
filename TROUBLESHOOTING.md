# 🔧 Troubleshooting Guide

Common issues and how to fix them.

---

## Frontend Issues

### ❌ Error: "Cannot connect to backend"

**Symptoms:**
- Upload button doesn't work
- Browser console shows CORS errors
- Network requests fail

**Solutions:**

1. **Check backend URL in Vercel:**
   ```bash
   # In Vercel dashboard, verify:
   NEXT_PUBLIC_API_URL=https://your-actual-backend.up.railway.app
   ```

2. **Test backend directly:**
   ```bash
   curl https://your-backend.up.railway.app/health
   # Should return: {"status":"healthy"}
   ```

3. **Check Railway backend is running:**
   - Go to Railway dashboard
   - Check backend service status
   - View recent logs for errors

4. **Verify CORS settings:**
   - In `backend/main.py`, check CORS origins
   - For testing, use `allow_origins=["*"]`
   - For production, use your Vercel domain

---

### ❌ Error: "Failed to upload video"

**Symptoms:**
- Upload fails immediately
- Error message in UI
- No job created

**Solutions:**

1. **Check video file:**
   - File must be a video format (mp4, mov, etc.)
   - Try a different, smaller video first
   - Max size depends on your setup

2. **Check backend logs:**
   ```bash
   # In Railway dashboard, view backend logs
   # Look for upload errors
   ```

3. **Verify R2 credentials:**
   - Check environment variables in Railway
   - Test R2 bucket access manually
   - Ensure bucket name is correct

4. **Check browser console:**
   - Open DevTools (F12)
   - Check Network tab for failed requests
   - Look for specific error messages

---

### ❌ Videos not appearing in gallery

**Symptoms:**
- Upload succeeds
- No videos show in "Your Videos" section
- Gallery shows "No videos yet"

**Solutions:**

1. **Check database connection:**
   ```bash
   # In Railway dashboard
   # Verify PostgreSQL is running
   # Check DATABASE_URL is set
   ```

2. **Test API endpoint:**
   ```bash
   curl https://your-backend.up.railway.app/api/jobs
   # Should return array of jobs (or empty array)
   ```

3. **Check browser console:**
   - Look for JavaScript errors
   - Check Network tab for API call failures

4. **Force refresh:**
   - Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
   - Clear browser cache
   - Try incognito mode

---

## Backend Issues

### ❌ Railway deployment fails

**Symptoms:**
- Build fails
- Deployment crashes
- Service won't start

**Solutions:**

1. **Check root directory:**
   ```
   Railway → Backend Service → Settings → Root Directory
   Should be: /backend
   ```

2. **Verify requirements.txt:**
   ```bash
   # Make sure backend/requirements.txt exists
   # Check for syntax errors
   ```

3. **Check logs:**
   ```
   Railway → Backend Service → Deployments → View Logs
   Look for specific error messages
   ```

4. **Environment variables:**
   ```
   # Ensure all required vars are set:
   - R2_ENDPOINT
   - R2_ACCESS_KEY
   - R2_SECRET_KEY
   - R2_BUCKET_NAME
   - R2_PUBLIC_URL
   - RUNPOD_API_KEY
   - RUNPOD_ENDPOINT_ID
   ```

---

### ❌ Database errors

**Symptoms:**
- "Database connection failed"
- "Table does not exist"
- 500 errors on API calls

**Solutions:**

1. **Verify PostgreSQL is added:**
   ```
   Railway → Project
   Should see: Backend, PostgreSQL, Redis
   ```

2. **Check DATABASE_URL:**
   ```
   Railway → PostgreSQL → Variables
   Copy DATABASE_URL
   Railway → Backend → Variables
   Paste as DATABASE_URL
   ```

3. **Restart services:**
   ```
   Railway → Backend → Restart
   Railway → PostgreSQL → Restart
   ```

4. **Check migrations:**
   - Tables should be created automatically on startup
   - Check backend logs for "CREATE TABLE" statements

---

### ❌ Redis connection issues

**Symptoms:**
- Jobs stuck in pending
- Celery tasks not running
- Redis connection errors in logs

**Solutions:**

1. **Verify Redis is running:**
   ```
   Railway → Redis → Check status
   ```

2. **Check REDIS_URL:**
   ```
   Railway → Redis → Variables → REDIS_URL
   Copy to Backend service variables
   ```

3. **Test connection:**
   ```bash
   # In Railway backend shell:
   python3 -c "import redis; r = redis.from_url('$REDIS_URL'); print(r.ping())"
   # Should print: True
   ```

---

## GPU Worker Issues

### ❌ Docker build fails

**Symptoms:**
- Build hangs or crashes
- "No space left on device"
- Dependency errors

**Solutions:**

1. **Free up disk space:**
   ```bash
   # Clean up Docker
   docker system prune -a

   # Check available space
   df -h
   ```

2. **Build with more resources:**
   ```bash
   # Increase Docker memory (Docker Desktop settings)
   # Set to at least 8GB RAM
   ```

3. **Build without cache:**
   ```bash
   docker build --no-cache -t your-username/editto-worker:latest .
   ```

4. **Check Docker is running:**
   ```bash
   docker --version
   docker ps
   ```

---

### ❌ RunPod endpoint not responding

**Symptoms:**
- Jobs stuck in "processing"
- Timeout errors
- No response from GPU worker

**Solutions:**

1. **Check endpoint status:**
   ```
   RunPod → Serverless → Your Endpoint
   Status should be: Active
   ```

2. **View logs:**
   ```
   RunPod → Endpoint → Logs
   Look for error messages
   ```

3. **Verify environment variables:**
   ```
   RunPod → Endpoint → Configuration
   Check all R2 credentials are set correctly
   ```

4. **Test manually:**
   ```bash
   curl -X POST https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"input":{"video_url":"test","instruction":"test"}}'
   ```

5. **Check worker container:**
   ```
   RunPod → Endpoint → Workers
   Verify at least one worker is running
   ```

---

### ❌ "Image not found" error

**Symptoms:**
- RunPod can't pull Docker image
- Deployment fails with "image not found"

**Solutions:**

1. **Verify image was pushed:**
   ```bash
   docker push your-username/editto-worker:latest
   # Check for success message
   ```

2. **Check image name:**
   ```
   RunPod → Endpoint → Container Image
   Should match: your-username/editto-worker:latest
   ```

3. **Make image public:**
   ```
   Docker Hub → Repository → Settings
   Set visibility to: Public
   ```

4. **Try pulling locally:**
   ```bash
   docker pull your-username/editto-worker:latest
   # Should download successfully
   ```

---

## Storage Issues

### ❌ R2 upload fails

**Symptoms:**
- "Failed to upload to R2"
- 403 Forbidden errors
- Credentials errors

**Solutions:**

1. **Verify credentials:**
   ```
   Cloudflare → R2 → Manage R2 API Tokens
   Check Access Key ID and Secret Key
   ```

2. **Check bucket name:**
   ```
   R2_BUCKET_NAME=editto-videos
   # Must match exact bucket name in Cloudflare
   ```

3. **Verify bucket exists:**
   ```
   Cloudflare → R2
   Should see bucket named "editto-videos"
   ```

4. **Check permissions:**
   ```
   Cloudflare → R2 → API Token
   Permissions should include:
   - Object Read
   - Object Write
   ```

5. **Test with AWS CLI:**
   ```bash
   aws s3 ls \
     --endpoint-url YOUR_R2_ENDPOINT \
     s3://editto-videos
   ```

---

### ❌ Videos not publicly accessible

**Symptoms:**
- Video URLs return 404
- Can't view uploaded videos
- Download fails

**Solutions:**

1. **Enable public access:**
   ```
   Cloudflare → R2 → Bucket → Settings
   Enable: Public Access
   ```

2. **Check public URL:**
   ```
   Cloudflare → R2 → Bucket
   Note the public R2.dev URL
   Update R2_PUBLIC_URL in environment variables
   ```

3. **Verify file was uploaded:**
   ```
   Cloudflare → R2 → Bucket → Browse
   Look for files in original/ and edited/ folders
   ```

---

## Cost Issues

### ❌ Unexpected high costs

**Symptoms:**
- RunPod bill higher than expected
- Railway exceeding $5 credit
- Surprise charges

**Solutions:**

1. **Check RunPod usage:**
   ```
   RunPod → Billing → Usage
   Review GPU hours and costs
   ```

2. **Look for stuck workers:**
   ```
   RunPod → Serverless → Workers
   Check for workers running longer than expected
   Stop any stuck workers
   ```

3. **Review failed jobs:**
   ```
   # Check backend logs for repeated failures
   # Failed jobs still cost GPU time
   ```

4. **Set spending limits:**
   ```
   RunPod → Settings → Billing
   Set maximum spending limit
   Enable alerts at $10, $25, $50
   ```

5. **Check for loops:**
   ```
   # Review backend code for infinite retry loops
   # Check Celery task logs
   ```

---

## Performance Issues

### ❌ Slow video processing

**Symptoms:**
- Videos take > 10 minutes
- GPU usage seems low
- Timeouts

**Solutions:**

1. **Check GPU type:**
   ```
   RunPod → Endpoint → Configuration
   Should be: RTX A6000 or better
   ```

2. **Optimize video size:**
   ```
   # Pre-process videos:
   # - Reduce resolution
   # - Compress before upload
   # - Limit video length
   ```

3. **Check worker resources:**
   ```
   RunPod → Workers → Metrics
   Look for CPU/RAM bottlenecks
   ```

4. **Increase timeout:**
   ```python
   # In backend/tasks.py
   max_attempts = 120  # Increase from 60
   ```

---

### ❌ Frontend loads slowly

**Symptoms:**
- Page takes long to load
- Videos load slowly
- Poor performance

**Solutions:**

1. **Optimize video delivery:**
   ```
   - Enable Cloudflare CDN
   - Compress videos
   - Use video thumbnails
   ```

2. **Check Vercel bandwidth:**
   ```
   Vercel → Project → Usage
   Look for bandwidth limits
   ```

3. **Optimize frontend:**
   ```
   - Enable Next.js Image optimization
   - Lazy load videos
   - Pagination for job list
   ```

---

## Common Error Messages

### "CORS policy: No 'Access-Control-Allow-Origin' header"

**Fix:**
```python
# In backend/main.py, update CORS:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-vercel-app.vercel.app"],  # Specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### "ModuleNotFoundError: No module named 'X'"

**Fix:**
```bash
# Missing Python dependency
# Add to backend/requirements.txt:
package-name==version

# Or for GPU worker:
# Add to gpu-worker/requirements.txt
```

---

### "ECONNREFUSED" or "Connection refused"

**Fix:**
- Service is not running
- Wrong URL
- Firewall blocking connection
- Check service status and logs

---

### "413 Payload Too Large"

**Fix:**
```python
# In backend/main.py, increase limit:
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add this:
from starlette.middleware.base import BaseHTTPMiddleware
app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=lambda request, call_next: call_next(request)
)

# Set max file size in Railway environment:
# MAX_CONTENT_LENGTH=104857600  # 100MB
```

---

## Debugging Checklist

When something goes wrong:

- [ ] Check all service statuses (Railway, Vercel, RunPod)
- [ ] Review logs from each service
- [ ] Verify environment variables are set correctly
- [ ] Test each component individually
- [ ] Check network connectivity
- [ ] Review recent code changes
- [ ] Check for service outages
- [ ] Test in incognito/private browsing
- [ ] Clear cache and cookies
- [ ] Try a different browser
- [ ] Check service status pages
- [ ] Review billing/credit status

---

## Getting Help

### 1. Check Logs First
- Railway: Deployment → Logs
- Vercel: Deployments → Build Logs
- RunPod: Endpoint → Logs
- Browser: DevTools → Console

### 2. Search Documentation
- Railway Docs: docs.railway.app
- Vercel Docs: vercel.com/docs
- RunPod Docs: docs.runpod.io
- FastAPI Docs: fastapi.tiangolo.com

### 3. Community Support
- Railway Discord
- Vercel Discord
- RunPod Discord
- Stack Overflow

### 4. Contact Support
- Railway: help@railway.app
- Vercel: support@vercel.com
- RunPod: support@runpod.io
- Cloudflare: support.cloudflare.com

---

## Prevention Tips

### Before Deploying:
- [ ] Test locally first
- [ ] Verify all credentials
- [ ] Check .env files are not committed
- [ ] Review environment variables
- [ ] Set spending limits
- [ ] Enable monitoring/alerts

### During Operation:
- [ ] Monitor costs daily (first week)
- [ ] Check logs regularly
- [ ] Review error rates
- [ ] Track successful vs failed jobs
- [ ] Monitor storage growth
- [ ] Keep dependencies updated

### Best Practices:
- [ ] Use version control (Git)
- [ ] Document changes
- [ ] Test in development first
- [ ] Have rollback plan
- [ ] Keep backups of configs
- [ ] Monitor uptime

---

**Remember:** 90% of issues are related to:
1. Wrong environment variables
2. Missing credentials
3. Service not running
4. CORS configuration
5. Network/connectivity

Check these first! 🔍
