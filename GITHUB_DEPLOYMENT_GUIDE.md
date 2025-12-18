# GitHub Deployment Guide for AnyLaw

This guide will help you push your code to GitHub and deploy to Railway (backend) and Vercel (frontend).

## Prerequisites

- GitHub account (https://github.com)
- Railway account (https://railway.app)
- Vercel account (https://vercel.com)
- Git installed on your machine

## Step 1: Create GitHub Repository

### Option A: Via GitHub Website (Recommended)

1. Go to https://github.com
2. Click the "+" icon in top right → "New repository"
3. Fill in repository details:
   - **Repository name**: `anylaw-case-database`
   - **Description**: "AnyLaw Case Database Navigator - Browse 8.5M+ legal cases"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README (we already have code)
4. Click "Create repository"

### Option B: Via GitHub CLI (if installed)

```bash
gh repo create anylaw-case-database --public --source=. --remote=origin
```

## Step 2: Initialize Git and Push to GitHub

### 2.1: Initialize Git Repository

```bash
cd "/Users/alexmclaughlin/Desktop/Cursor Projects/AnyLaw"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: separated frontend and backend for deployment"
```

### 2.2: Connect to GitHub

GitHub will show you instructions after creating the repo. Use these commands:

```bash
# Add GitHub remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/anylaw-case-database.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

### Authentication

If prompted for credentials:

**Option 1: Personal Access Token (Recommended)**
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "AnyLaw Deployment"
4. Select scopes: `repo` (full control of private repositories)
5. Generate token and **copy it immediately** (you won't see it again)
6. When prompted for password, paste the token

**Option 2: GitHub CLI**
```bash
gh auth login
```

**Option 3: SSH Keys**
See: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

## Step 3: Deploy Backend to Railway

### 3.1: Create Railway Project

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Click "Configure GitHub App" (first time only)
5. Authorize Railway to access your GitHub account
6. Select your `anylaw-case-database` repository
7. When prompted, configure:
   - **Root Directory**: `backend`
   - **Branch**: `main`

### 3.2: Configure Environment Variables

In Railway project settings → Variables, add:

```
FLASK_ENV=production
CORS_ORIGINS=https://your-frontend-name.vercel.app
PORT=8000
DATA_DIR=/app/backend/data
```

**Note**: You'll update `CORS_ORIGINS` after deploying the frontend.

### 3.3: Wait for Deployment

Railway will:
1. Detect Python app (via `requirements.txt`)
2. Install dependencies
3. Run command from `Procfile`
4. Deploy automatically

### 3.4: Get Your Railway URL

1. Click on your deployment
2. Go to Settings → Networking
3. Click "Generate Domain"
4. Copy your URL (e.g., `anylaw-backend-production.up.railway.app`)

### 3.5: Test Backend

```bash
# Test health endpoint
curl https://your-backend.railway.app/health

# Should return:
# {"status":"healthy","service":"anylaw-backend","version":"1.0.0"}

# Test API
curl https://your-backend.railway.app/api/stats
```

## Step 4: Deploy Frontend to Vercel

### 4.1: Update env.js with Railway URL

First, update your frontend configuration:

```bash
cd frontend

# Edit env.js
# Change the API_URL to your Railway URL
```

Edit `frontend/env.js`:
```javascript
window.ENV = {
    API_URL: 'https://your-backend.railway.app'  // Replace with your actual Railway URL
};
```

**Commit this change:**
```bash
cd "/Users/alexmclaughlin/Desktop/Cursor Projects/AnyLaw"
git add frontend/env.js
git commit -m "Update API URL to Railway backend"
git push origin main
```

### 4.2: Create Vercel Project

1. Go to https://vercel.com
2. Click "Add New..." → "Project"
3. Import your GitHub repository:
   - Click "Import Git Repository"
   - Find `anylaw-case-database`
   - Click "Import"

### 4.3: Configure Vercel Project

On the import screen:

**Framework Preset**: Other

**Root Directory**: 
- Click "Edit"
- Enter: `frontend`
- Click "Continue"

**Build Settings**:
- Build Command: (leave empty)
- Output Directory: `./`
- Install Command: (leave empty)

**Environment Variables**: (Optional, env.js already has the URL)
- Click "Add"
- Key: `API_URL`
- Value: `https://your-backend.railway.app`

Click "Deploy"

### 4.4: Wait for Deployment

Vercel will:
1. Clone your repository
2. Build (in this case, just serve static files)
3. Deploy to CDN
4. Give you a URL

### 4.5: Get Your Vercel URL

After deployment completes:
- You'll see your URL: `https://anylaw-case-database.vercel.app`
- Or a custom one like: `https://anylaw-username.vercel.app`

## Step 5: Update CORS Settings

Now that you have your Vercel URL, update Railway:

1. Go back to Railway project
2. Click on your service
3. Go to Variables
4. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://your-actual-frontend.vercel.app
   ```
5. Click "Update Variables"
6. Railway will automatically redeploy (takes ~2 minutes)

## Step 6: Test Full Application

1. Visit your Vercel URL
2. Dashboard should load with statistics
3. Try these features:
   - ✅ Search for cases
   - ✅ Citation lookup
   - ✅ View case details
   - ✅ Click citations to navigate

### Check Browser Console

Press `F12` or `Cmd+Option+J`:
- No CORS errors
- API calls succeed
- No JavaScript errors

## Step 7: Set Up Automatic Deployments

Good news! Both are already set up:

### Railway
- Automatically redeploys when you push changes to `backend/` folder
- Monitors `main` branch

### Vercel
- Automatically redeploys when you push changes to `frontend/` folder
- Monitors `main` branch
- Also creates preview deployments for pull requests

## Making Updates

### To update your application:

```bash
# Make your changes
git add .
git commit -m "Description of changes"
git push origin main
```

**Railway** will redeploy if `backend/*` changed
**Vercel** will redeploy if `frontend/*` changed

## Custom Domains (Optional)

### Add Custom Domain to Railway

1. Railway Settings → Networking → Custom Domain
2. Enter your domain (e.g., `api.myapp.com`)
3. Update DNS records as shown:
   ```
   CNAME api.myapp.com -> your-app.railway.app
   ```

### Add Custom Domain to Vercel

1. Vercel Settings → Domains
2. Enter your domain (e.g., `myapp.com`)
3. Update DNS records as shown:
   ```
   A @ 76.76.21.21
   CNAME www cname.vercel-dns.com
   ```

### After Adding Custom Domains

Update Railway CORS_ORIGINS:
```
CORS_ORIGINS=https://myapp.com,https://www.myapp.com
```

## Troubleshooting

### CORS Errors

**Symptom**: Browser console shows CORS errors

**Solution**:
1. Check Railway `CORS_ORIGINS` matches Vercel URL exactly
2. No trailing slashes in URLs
3. After changing, wait for Railway to redeploy
4. Hard refresh browser (Cmd+Shift+R / Ctrl+Shift+R)

### API Connection Failed

**Symptom**: Frontend shows "Error loading statistics"

**Solution**:
1. Verify Railway backend is running:
   ```bash
   curl https://your-backend.railway.app/health
   ```
2. Check `frontend/env.js` has correct URL
3. Check Railway logs for errors
4. Verify environment variables are set

### Backend Not Starting

**Symptom**: Railway deployment fails

**Solution**:
1. Check Railway logs (click on deployment)
2. Common issues:
   - Missing dependencies → Check `requirements.txt`
   - Port binding → Railway sets PORT automatically
   - Data path → Check DATA_DIR environment variable
3. Verify `Procfile` is correct:
   ```
   web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120
   ```

### Frontend Not Loading

**Symptom**: Vercel deployment succeeds but site blank

**Solution**:
1. Check Vercel function logs
2. Verify `vercel.json` exists in `frontend/` directory
3. Check browser console for errors
4. Verify root directory is set to `frontend`

### Push Rejected

**Symptom**: Git push fails with authentication error

**Solution**:
1. Use Personal Access Token (not password)
2. Generate at: Settings → Developer settings → Personal access tokens
3. Use token as password when prompted
4. Or use GitHub CLI: `gh auth login`

### Data Files Not Found

**Symptom**: Backend can't find case data

**Solution**:
1. Verify data symlink exists: `ls -la backend/data`
2. If missing, recreate:
   ```bash
   cd backend
   ln -s "../Anylaw sample documents-b" data
   git add data  # May need to force add symlink
   ```
3. Alternative: Copy data to `backend/data/` (not recommended, large files)

## Monitoring

### Railway Monitoring

1. View real-time logs
2. Monitor CPU/Memory/Network usage
3. Set up metrics and alerts
4. Check deployment history

### Vercel Monitoring

1. Analytics (on Pro plan)
2. Real-time function logs
3. Performance insights
4. Error tracking

## GitHub Best Practices

### Branch Protection

1. Go to repo Settings → Branches
2. Add rule for `main`:
   - Require pull request reviews
   - Require status checks to pass
   - Require branches to be up to date

### GitHub Actions (Optional CI/CD)

Create `.github/workflows/test.yml`:

```yaml
name: Test

on: [push, pull_request]

jobs:
  backend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: |
          cd backend
          pip install -r requirements.txt
          python -m pytest  # if you add tests

  frontend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: |
          cd frontend
          # Add frontend tests here
```

## Security Best Practices

### GitHub Security

1. Enable two-factor authentication
2. Use Personal Access Tokens (not passwords)
3. Review authorized OAuth apps regularly
4. Set repository to private if needed

### Environment Variables

1. Never commit `.env` files
2. Use Railway/Vercel dashboards for secrets
3. Rotate tokens periodically
4. Use different tokens for dev/prod

### CORS Configuration

1. Keep `CORS_ORIGINS` restrictive
2. Never use `*` in production
3. Only add trusted domains
4. Verify in Railway dashboard

## Cost Monitoring

### Railway
- Free tier: $5/month credit
- Monitor usage in dashboard
- Set up usage alerts
- Upgrade to Pro if needed ($20/month)

### Vercel
- Free tier: Generous for hobby projects
- Pro: $20/month for commercial use
- Monitor bandwidth and function execution
- Set up usage alerts

## Environment Variables Reference

### Backend (Railway)

```bash
# Required
FLASK_ENV=production
CORS_ORIGINS=https://your-frontend.vercel.app

# Optional (Railway sets PORT automatically)
PORT=8000
DATA_DIR=/app/backend/data
```

### Frontend (Vercel)

Already configured in `env.js`, but can also set:

```bash
API_URL=https://your-backend.railway.app
```

## Useful Commands

```bash
# Check remote URLs
git remote -v

# View commit history
git log --oneline

# Create and switch to new branch
git checkout -b feature-name

# Merge branch
git checkout main
git merge feature-name

# Force update local branch
git fetch origin
git reset --hard origin/main

# View Railway logs
# (in Railway dashboard or use Railway CLI)

# View Vercel logs
# (in Vercel dashboard or use Vercel CLI)
```

## Next Steps

1. ✅ Deploy backend to Railway
2. ✅ Deploy frontend to Vercel
3. ✅ Test full application
4. 📊 Set up monitoring
5. 🎨 Customize styling
6. 🚀 Add new features
7. 📱 Consider mobile app
8. 🤖 Add AI features

## Resources

- **GitHub Docs**: https://docs.github.com
- **Railway Docs**: https://docs.railway.app
- **Vercel Docs**: https://vercel.com/docs
- **Flask Docs**: https://flask.palletsprojects.com
- **Chart.js Docs**: https://www.chartjs.org

## Support

### GitHub Issues
Create issues in your repo for tracking bugs and features

### Railway Support
- Help: https://railway.app/help
- Discord: https://discord.gg/railway

### Vercel Support
- Help: https://vercel.com/support
- Discord: https://vercel.com/discord

---

## Summary

Your deployment process:

1. ✅ Create GitHub repository
2. ✅ Push code to GitHub
3. ✅ Deploy backend to Railway (set root: `backend`)
4. ✅ Deploy frontend to Vercel (set root: `frontend`)
5. ✅ Update CORS with Vercel URL
6. ✅ Test everything
7. 🎉 You're live!

**Total time: ~20-30 minutes**

**Congratulations!** Your AnyLaw application is now deployed and accessible worldwide! 🚀

