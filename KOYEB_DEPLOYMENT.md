# Deploy to Koyeb - Step-by-Step Guide

## Overview

Koyeb is perfect for your URL Shortener! It offers:
- ✅ Free tier with fast deployments
- ✅ Global edge network
- ✅ Auto-scaling
- ✅ Git-based deployments
- ✅ Built-in SSL

---

## Prerequisites

1. GitHub account with your repository
2. Koyeb account (free): [koyeb.com](https://www.koyeb.com)
3. Supabase & Redis Cloud URLs ready

---

## Step 1: Push to GitHub

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Deploy URL Shortener to Koyeb"

# Create repository on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/url-shortener.git
git push -u origin main
```

---

## Step 2: Create Koyeb Account

1. Go to [app.koyeb.com](https://app.koyeb.com)
2. Sign up with GitHub
3. Verify your email

---

## Step 3: Deploy Your App

### Create New Web Service

1. Click **"Create Web Service"**
2. Select **"GitHub"**
3. Connect your GitHub account (if not already)
4. Select your `url-shortener` repository
5. Choose branch: `main`

### Configure Build Settings

**Builder:** Buildpack

Koyeb will auto-detect Python. If not:
- **Builder:** Dockerfile (or Buildpack)
- **Build command:** (leave empty, auto-detected)

### Configure Deployment

- **App name:** `url-shortener`
- **Region:** Choose closest to you (e.g., Washington, Frankfurt)
- **Instance type:** Free (Nano)

**Port Configuration:**
- **Port:** `8501` (Streamlit port)

**Start Command:**
```bash
sh start.sh
```

---

## Step 4: Add Environment Variables

Click **"Advanced"** → **"Environment variables"**

Add these variables:

```bash
DATABASE_URL=postgresql://postgres.xxx:password@aws-xxx.pooler.supabase.com:6543/postgres
REDIS_HOST=redis-xxxxx.redislabs.com
REDIS_PORT=17479
REDIS_PASSWORD=your_redis_password
SECRET_KEY=your-django-secret-key-here
DEBUG=False
ALLOWED_HOSTS=.koyeb.app
SHORT_URL_DOMAIN=https://url-shortener-YOUR_KOYEB_ID.koyeb.app
USE_DUMMY_CACHE=False
API_BASE_URL=http://localhost:8000
PORT=8501
```

**Generate a new SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Step 5: Deploy

1. Click **"Deploy"**
2. Wait for build to complete (~2-3 minutes)
3. Check **"Logs"** tab for any errors

---

## Step 6: Access Your App

Once deployed, your app will be available at:

```
https://url-shortener-YOUR_KOYEB_ID.koyeb.app
```

**Test it:**
1. Visit the URL
2. You should see the Streamlit UI
3. Try creating a short URL
4. Verify the redirect works

---

## Update SHORT_URL_DOMAIN

After deployment, update your environment variable:

1. Go to Koyeb dashboard → Your service
2. Click **"Settings"** → **"Environment variables"**
3. Update `SHORT_URL_DOMAIN` with your actual Koyeb URL:
   ```
   SHORT_URL_DOMAIN=https://url-shortener-abc123.koyeb.app
   ```
4. Save and redeploy

---

## Custom Domain (Optional)

### Add Your Domain

1. In Koyeb dashboard, go to your service
2. Click **"Settings"** → **"Domains"**
3. Click **"Add domain"**
4. Enter your domain: `shortener.yourdomain.com`

### Configure DNS

Add these records to your domain DNS:

**CNAME Record:**
```
Type: CNAME
Name: shortener
Value: url-shortener-YOUR_KOYEB_ID.koyeb.app
```

### Update Environment Variables

```bash
ALLOWED_HOSTS=.koyeb.app,yourdomain.com
SHORT_URL_DOMAIN=https://shortener.yourdomain.com
```

Koyeb will automatically provision SSL certificate! 🔒

---

## Monitoring & Logs

### View Logs

1. Koyeb Dashboard → Your service
2. Click **"Logs"** tab
3. View real-time logs

### Check Metrics

- CPU usage
- Memory usage
- Request count
- Response time

All available in the **"Metrics"** tab.

---

## Auto-Deploy on Git Push

Koyeb automatically redeploys when you push to GitHub:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main

# Koyeb will auto-deploy! 🚀
```

---

## Troubleshooting

### Build Failed

**Check logs:**
- Go to "Build" tab
- Look for error messages
- Common issues:
  - Missing dependencies in `requirements.txt`
  - Syntax errors in code

**Fix:**
```bash
# Test locally first
pip install -r requirements.txt
python manage.py check
streamlit run streamlit_app.py
```

### Application Error

**"Connection refused":**
- Verify `API_BASE_URL=http://localhost:8000`
- Check Django started in logs

**"Database connection failed":**
- Verify `DATABASE_URL` is correct
- Test Supabase connection locally

**"Port already in use":**
- Ensure `PORT=8501` in environment variables
- Check `start.sh` uses correct ports

### Performance Issues

**App is slow:**
- Upgrade to larger instance (paid)
- Check Redis Cloud connection
- Optimize database queries

---

## Scaling (Optional)

### Upgrade Instance

Free tier limitations:
- 512 MB RAM
- Shared CPU
- May sleep after inactivity

To upgrade:
1. Settings → Instance type
2. Choose **Micro** or **Small**
3. Pricing starts at ~$5/month

### Configure Auto-scaling

1. Settings → Scaling
2. Set min/max instances
3. Configure scaling rules

---

## Cost

| Plan | Price | Resources |
|------|-------|-----------|
| **Free** | $0 | 512MB RAM, Shared CPU |
| **Micro** | ~$5/mo | 1GB RAM, 0.5 CPU |
| **Small** | ~$10/mo | 2GB RAM, 1 CPU |

**Recommendation:** Start with free tier, upgrade if needed.

---

## Security Checklist

Before going live:

- [ ] Changed `DEBUG=False`
- [ ] Generated new `SECRET_KEY`
- [ ] Set secure `ALLOWED_HOSTS`
- [ ] Using HTTPS (automatic with Koyeb)
- [ ] Environment variables set (not hardcoded)
- [ ] `.env` file not in repository

---

## Next Steps

1. ✅ Deploy to Koyeb
2. ✅ Test all features
3. ✅ Share your short URL service!
4. (Optional) Add custom domain
5. (Optional) Set up monitoring

---

## Useful Commands

**View service status:**
```bash
# Via Koyeb CLI (optional)
koyeb services list
koyeb services logs url-shortener
```

**Redeploy:**
- Push to GitHub, or
- Click "Redeploy" in Koyeb dashboard

---

## Support

**Koyeb Docs:** [koyeb.com/docs](https://www.koyeb.com/docs)

**Common Issues:**
- Build errors → Check requirements.txt
- Runtime errors → Check logs tab
- Connection issues → Verify environment variables

---

## Your App is Ready! 🚀

**Live URL:** `https://url-shortener-xxxxx.koyeb.app`

Features working:
- ✅ URL shortening
- ✅ QR code generation
- ✅ Click analytics
- ✅ Custom codes
- ✅ Expiry dates
- ✅ Beautiful UI

**Deployment time:** ~5 minutes  
**Cost:** FREE 🎉
