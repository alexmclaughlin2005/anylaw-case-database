# GitLab Deployment Guide for AnyLaw

This guide will help you push your code to GitLab and deploy to Railway (backend) and Vercel (frontend).

## Prerequisites

- GitLab account
- Railway account (https://railway.app)
- Vercel account (https://vercel.com)
- Git installed on your machine

## Step 1: Initialize Git Repository

```bash
cd "/Users/alexmclaughlin/Desktop/Cursor Projects/AnyLaw"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: separated frontend and backend for deployment"
```

## Step 2: Create GitLab Repository

1. Go to https://gitlab.com
2. Click "New Project" → "Create blank project"
3. Fill in project details:
   - Project name: `anylaw-case-database`
   - Visibility: Private (or Public based on your preference)
4. Click "Create project"

## Step 3: Push to GitLab

GitLab will show you instructions, but here's the typical flow:

```bash
# Add GitLab remote (replace USERNAME and PROJECT with your values)
git remote add origin https://gitlab.com/USERNAME/anylaw-case-database.git

# Push to GitLab
git branch -M main
git push -u origin main
```

If you encounter authentication issues:
1. Generate a Personal Access Token in GitLab:
   - Go to Settings → Access Tokens
   - Create token with `write_repository` scope
2. Use the token as your password when prompted

## Step 4: Deploy Backend to Railway

### 4.1: Create Railway Project

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo" (or GitLab if available)
4. If GitLab isn't available, select "Deploy from GitLab"
5. Authorize Railway to access your GitLab account
6. Select your `anylaw-case-database` repository
7. When prompted for root directory, enter: `backend`

### 4.2: Configure Environment Variables

In Railway project settings, add these environment variables:

```
FLASK_ENV=production
CORS_ORIGINS=https://your-frontend-name.vercel.app
PORT=8000
```

**Note**: You'll update `CORS_ORIGINS` after deploying the frontend.

### 4.3: Deploy

1. Railway will automatically detect the Python app and deploy
2. Wait for deployment to complete
3. Note your Railway URL (e.g., `https://anylaw-backend-production.up.railway.app`)

### 4.4: Test Backend

Visit your Railway URL + `/health`:
```
https://your-backend.railway.app/health
```

You should see:
```json
{
  "status": "healthy",
  "service": "anylaw-backend",
  "version": "1.0.0"
}
```

## Step 5: Deploy Frontend to Vercel

### 5.1: Create Vercel Project

1. Go to https://vercel.com
2. Click "Add New..." → "Project"
3. Import your GitLab repository
4. Configure project:
   - **Framework Preset**: Other
   - **Root Directory**: `frontend`
   - **Build Command**: (leave empty for static site)
   - **Output Directory**: `./`

### 5.2: Configure Environment Variables

In Vercel project settings, add environment variable:

1. Go to Settings → Environment Variables
2. Add variable:
   - **Key**: `API_URL`
   - **Value**: `https://your-backend.railway.app` (your Railway URL)

### 5.3: Update env.js

Before deploying, you need to update the frontend's `env.js` file to use the environment variable:

Create a build script or manually update `frontend/env.js`:

```javascript
window.ENV = {
    API_URL: 'YOUR_RAILWAY_URL_HERE'
};
```

Or create `frontend/build-env.sh`:

```bash
#!/bin/bash
# This will be run during Vercel build
echo "window.ENV = { API_URL: '$API_URL' };" > env.js
```

Then in Vercel settings:
- **Build Command**: `chmod +x build-env.sh && ./build-env.sh`

### 5.4: Deploy

1. Click "Deploy"
2. Wait for deployment to complete
3. Note your Vercel URL (e.g., `https://anylaw.vercel.app`)

## Step 6: Update CORS Settings

Now that you have your Vercel URL:

1. Go back to Railway project
2. Update `CORS_ORIGINS` environment variable:
   ```
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```
3. Railway will automatically redeploy

## Step 7: Test Full Application

1. Visit your Vercel URL
2. The dashboard should load with statistics
3. Try searching for cases
4. Try the citation lookup feature
5. View a case detail page

## Troubleshooting

### CORS Errors

If you see CORS errors in the browser console:

1. Check that `CORS_ORIGINS` in Railway matches your Vercel URL exactly
2. Make sure there are no trailing slashes
3. Redeploy Railway after changes

### API Connection Issues

If frontend can't connect to backend:

1. Check that `env.js` has the correct Railway URL
2. Make sure Railway backend is running (check `/health` endpoint)
3. Check browser console for exact error messages
4. Verify Railway URL in Vercel environment variables

### Backend Not Starting

If Railway deployment fails:

1. Check Railway logs
2. Verify `requirements.txt` has all dependencies
3. Ensure `Procfile` is correct
4. Check that `data` symlink works or copy data files

### Frontend Not Loading

If Vercel deployment succeeds but site doesn't work:

1. Check Vercel function logs
2. Verify `vercel.json` configuration
3. Ensure all HTML files are present
4. Check browser console for errors

## Continuous Deployment

Both Railway and Vercel support automatic deployments:

### Railway (Backend)
- Automatically deploys when you push to `main` branch
- Only redeploys if files in `backend/` directory change

### Vercel (Frontend)
- Automatically deploys when you push to `main` branch
- Only redeploys if files in `frontend/` directory change

## Making Updates

To update your application:

```bash
# Make your changes
git add .
git commit -m "Description of changes"
git push origin main
```

Both Railway and Vercel will automatically detect changes and redeploy.

## Custom Domains (Optional)

### Railway
1. Go to Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

### Vercel
1. Go to Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

## Environment Variables Reference

### Backend (Railway)
```
FLASK_ENV=production
CORS_ORIGINS=https://your-frontend.vercel.app
DATA_DIR=/app/data
PORT=8000
```

### Frontend (Vercel)
```
API_URL=https://your-backend.railway.app
```

## Security Considerations

1. Never commit `.env` files with real credentials
2. Use environment variables for all sensitive data
3. Keep CORS_ORIGINS restrictive (don't use `*` in production)
4. Enable HTTPS on both platforms (enabled by default)
5. Consider adding rate limiting to backend
6. Review Railway and Vercel security settings

## Cost Considerations

### Railway
- Free tier: $5/month of usage (usually sufficient for development)
- Paid: Pay for what you use
- Monitor usage in Railway dashboard

### Vercel
- Free tier: Generous limits for personal projects
- Paid: Starts at $20/month for Pro features
- Bandwidth and serverless function execution limits apply

## Monitoring

### Railway
- View logs in real-time
- Monitor CPU/Memory usage
- Set up alerts for downtime

### Vercel
- Analytics available in dashboard
- Real-time function logs
- Performance monitoring

## Backup Strategy

1. GitLab repository is your source of truth
2. Keep local backups of data files
3. Consider exporting Railway database backups if you add a database later
4. Use GitLab's built-in backup features

## Next Steps

1. Set up custom domain names
2. Add analytics (Google Analytics, Plausible, etc.)
3. Implement caching strategies
4. Add rate limiting
5. Set up monitoring and alerts
6. Consider adding a CDN for static assets
7. Implement user authentication if needed

## Support

- Railway: https://railway.app/help
- Vercel: https://vercel.com/support
- GitLab: https://docs.gitlab.com/

---

**Congratulations!** Your AnyLaw application is now deployed and accessible worldwide! 🎉

