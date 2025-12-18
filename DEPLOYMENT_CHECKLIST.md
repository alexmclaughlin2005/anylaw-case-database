# 🚀 AnyLaw Deployment Checklist

Use this checklist to deploy your application to production.

## ✅ Pre-Deployment (COMPLETED)

- [x] Backend restructured with API-only Flask app
- [x] Frontend converted to static site with API client
- [x] Local testing successful
- [x] Documentation created
- [x] Deployment configurations ready
- [x] Helper scripts created

## 📝 Deployment Steps

### 1. Create GitHub Repository

- [ ] Go to https://github.com/new
- [ ] Repository name: `anylaw-case-database`
- [ ] Choose visibility (Public or Private)
- [ ] **DO NOT** check "Initialize with README"
- [ ] Click "Create repository"
- [ ] Copy the repository URL

**Your URL will be**: `https://github.com/YOUR_USERNAME/anylaw-case-database.git`

---

### 2. Initialize Git and Push

Run these commands in Terminal:

```bash
cd "/Users/alexmclaughlin/Desktop/Cursor Projects/AnyLaw"

# Initialize git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: AnyLaw separated architecture"

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/anylaw-case-database.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Checklist:**
- [ ] Git initialized
- [ ] Files committed
- [ ] Remote added
- [ ] Pushed to GitHub successfully
- [ ] Verify files on GitHub website

**If prompted for authentication:**
- Use your GitHub Personal Access Token (not password)
- Generate at: Settings → Developer settings → Personal access tokens → Generate new token
- Select scope: `repo`

---

### 3. Deploy Backend to Railway

**Go to**: https://railway.app

- [ ] Click "New Project"
- [ ] Select "Deploy from GitHub repo"
- [ ] Authorize GitHub (if first time)
- [ ] Select `anylaw-case-database` repository
- [ ] **IMPORTANT**: Set Root Directory to `backend`
- [ ] Wait for initial deployment

**Add Environment Variables:**
- [ ] Click on Variables tab
- [ ] Add: `FLASK_ENV` = `production`
- [ ] Add: `CORS_ORIGINS` = `https://temporary-url.vercel.app` (update later)
- [ ] Railway auto-redeploys

**Generate Domain:**
- [ ] Go to Settings → Networking
- [ ] Click "Generate Domain"
- [ ] Copy the URL (e.g., `anylaw-production-abcd.up.railway.app`)

**Test Backend:**
```bash
curl https://YOUR-BACKEND-URL.railway.app/health
```

- [ ] Health check returns: `{"status":"healthy",...}`
- [ ] No errors in Railway logs

**Your Railway URL**: `___________________________________`

---

### 4. Update Frontend Configuration

**Edit** `frontend/env.js`:

```javascript
window.ENV = {
    API_URL: 'https://YOUR-ACTUAL-RAILWAY-URL.railway.app'
};
```

- [ ] Update `API_URL` with your Railway URL
- [ ] Save file

**Commit and Push:**
```bash
git add frontend/env.js
git commit -m "Update API URL to Railway backend"
git push origin main
```

- [ ] Changes committed
- [ ] Pushed to GitHub

---

### 5. Deploy Frontend to Vercel

**Go to**: https://vercel.com

- [ ] Click "Add New..." → "Project"
- [ ] Click "Import Git Repository"
- [ ] Find `anylaw-case-database`
- [ ] Click "Import"

**Configure Project:**
- [ ] Click "Edit" next to Root Directory
- [ ] Enter: `frontend`
- [ ] Framework Preset: `Other`
- [ ] Build Command: (leave empty)
- [ ] Output Directory: `./`
- [ ] Click "Deploy"

**Wait for Deployment:**
- [ ] Deployment completes successfully
- [ ] Copy the Vercel URL (e.g., `anylaw-abc123.vercel.app`)

**Your Vercel URL**: `___________________________________`

---

### 6. Update CORS Configuration

**Back to Railway:**

- [ ] Go to your Railway project
- [ ] Click Variables
- [ ] Update `CORS_ORIGINS` to: `https://YOUR-ACTUAL-VERCEL-URL.vercel.app`
- [ ] Wait for auto-redeploy (~2 minutes)

---

### 7. Final Testing

**Visit your Vercel URL** and test:

- [ ] Dashboard loads
- [ ] Statistics display correctly
- [ ] Charts render
- [ ] Search works
- [ ] Citation lookup works
- [ ] Case details load
- [ ] Citations are clickable
- [ ] Navigation works

**Browser Console Check** (Press F12):
- [ ] No CORS errors
- [ ] No JavaScript errors
- [ ] API calls succeed (check Network tab)

**Test API Directly:**
```bash
# Stats
curl https://YOUR-BACKEND.railway.app/api/stats

# Search
curl https://YOUR-BACKEND.railway.app/api/search?q=test

# Jurisdictions
curl https://YOUR-BACKEND.railway.app/api/jurisdictions
```

- [ ] All endpoints return data
- [ ] No errors

---

## 🎉 Deployment Complete!

### Your Live URLs

**Frontend**: `https://___________________________________`

**Backend**: `https://___________________________________`

### Share Your Work

Your application is now live and accessible worldwide! Share it:

- [ ] Test on mobile devices
- [ ] Share with colleagues
- [ ] Add to portfolio
- [ ] Tweet about it!

---

## 🔄 Future Updates

To update your deployed application:

```bash
# Make your changes
git add .
git commit -m "Description of changes"
git push origin main
```

- Railway auto-deploys if `backend/` files changed
- Vercel auto-deploys if `frontend/` files changed

---

## 📊 Monitor Your Deployment

### Railway Monitoring

- [ ] Check Railway dashboard
- [ ] View deployment logs
- [ ] Monitor resource usage
- [ ] Set up usage alerts (if needed)

### Vercel Monitoring

- [ ] Check Vercel dashboard
- [ ] View deployment logs
- [ ] Monitor analytics (Pro plan)
- [ ] Check performance insights

---

## 💰 Cost Tracking

### Current Plan

- **Railway**: Free tier ($5/month credit)
- **Vercel**: Free tier
- **GitHub**: Free

**Total Cost**: $0/month (within free tier limits)

### Monitor Usage

- [ ] Set up Railway usage alerts
- [ ] Monitor Vercel bandwidth
- [ ] Track function executions
- [ ] Upgrade if needed

---

## 🆘 Troubleshooting

### Common Issues

**CORS Error**
- ✓ Verify CORS_ORIGINS matches Vercel URL exactly
- ✓ No trailing slashes
- ✓ Hard refresh browser (Cmd+Shift+R)

**API Connection Failed**
- ✓ Check frontend/env.js has correct Railway URL
- ✓ Verify Railway backend is running (/health)
- ✓ Check Railway logs for errors

**Deployment Failed**
- ✓ Check logs in Railway/Vercel dashboard
- ✓ Verify root directories are set correctly
- ✓ Check environment variables

---

## 📚 Resources

- **Full Deployment Guide**: [GITHUB_DEPLOYMENT_GUIDE.md](GITHUB_DEPLOYMENT_GUIDE.md)
- **Quick Commands**: [DEPLOY_COMMANDS.txt](DEPLOY_COMMANDS.txt)
- **Local Development**: [LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md)

---

## ✅ Success Criteria

Your deployment is successful when:

- [x] Code pushed to GitHub
- [x] Backend deployed to Railway
- [x] Frontend deployed to Vercel
- [x] CORS configured correctly
- [x] All features work in production
- [x] No errors in browser console
- [x] Mobile responsive
- [x] Fast load times

---

## 🎓 Next Steps

After deployment:

- [ ] Add custom domain (optional)
- [ ] Set up monitoring
- [ ] Add analytics
- [ ] Implement new features
- [ ] Gather user feedback
- [ ] Optimize performance

---

**Status**: Ready to Deploy! 🚀

**Estimated Time**: 15-20 minutes

**Difficulty**: Easy (we've done all the hard work!)

---

Good luck! You've got this! 💪

