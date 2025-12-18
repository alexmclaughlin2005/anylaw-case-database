# Quick Deploy to GitHub + Railway + Vercel

**Status**: ✅ Local testing complete! Ready to deploy.

## 🚀 Deploy in 3 Commands

### Step 1: Push to GitHub (2 minutes)

```bash
cd "/Users/alexmclaughlin/Desktop/Cursor Projects/AnyLaw"

# Initialize git
git init
git add .
git commit -m "Initial commit: AnyLaw ready for deployment"

# Create repo on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/anylaw-case-database.git
git branch -M main
git push -u origin main
```

**First, create the GitHub repo:**
1. Go to https://github.com/new
2. Name: `anylaw-case-database`
3. Visibility: Your choice
4. **DO NOT** initialize with README
5. Create repository
6. Use the URL in the commands above

---

### Step 2: Deploy Backend to Railway (5 minutes)

1. **Go to**: https://railway.app
2. **Click**: "New Project" → "Deploy from GitHub repo"
3. **Authorize**: GitHub access (first time only)
4. **Select**: `anylaw-case-database`
5. **Configure**:
   - Root Directory: `backend` ⚠️ **IMPORTANT**
   - Click "Deploy"
6. **Add Environment Variables**:
   - Go to Variables tab
   - Add: `FLASK_ENV=production`
   - Add: `CORS_ORIGINS=https://your-app.vercel.app` (update after Vercel)
7. **Generate Domain**:
   - Settings → Networking → Generate Domain
   - Copy your URL: `https://anylaw-xxxxx.railway.app`

**Test it:**
```bash
curl https://your-railway-url.railway.app/health
# Should return: {"status":"healthy",...}
```

---

### Step 3: Deploy Frontend to Vercel (5 minutes)

**First, update the API URL:**

1. Edit `frontend/env.js`:
   ```javascript
   window.ENV = {
       API_URL: 'https://your-actual-railway-url.railway.app'
   };
   ```

2. Commit the change:
   ```bash
   git add frontend/env.js
   git commit -m "Update API URL to Railway backend"
   git push origin main
   ```

**Then deploy:**

1. **Go to**: https://vercel.com
2. **Click**: "Add New..." → "Project"
3. **Import**: Select `anylaw-case-database`
4. **Configure**:
   - Root Directory: `frontend` ⚠️ **IMPORTANT**
   - Framework: Other
   - Build Command: (leave empty)
   - Output Directory: `./`
5. **Click**: "Deploy"
6. **Copy your URL**: `https://anylaw-xxxxx.vercel.app`

---

### Step 4: Update CORS (2 minutes)

1. Go back to **Railway**
2. Click your service → **Variables**
3. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://your-actual-vercel-url.vercel.app
   ```
4. Railway auto-redeploys

---

## ✅ Test Your Deployment

Visit your Vercel URL: `https://your-app.vercel.app`

**Check that:**
- ✅ Dashboard loads with statistics
- ✅ Search works
- ✅ Citation lookup works
- ✅ Case details load
- ✅ No errors in browser console (F12)

---

## 🎉 You're Live!

Your app is now deployed at:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-backend.railway.app`

## 🔄 Making Updates

After deployment, just push to GitHub:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

- Railway auto-deploys if `backend/*` changed
- Vercel auto-deploys if `frontend/*` changed

---

## 📚 Need More Details?

See the complete guide: **[GITHUB_DEPLOYMENT_GUIDE.md](GITHUB_DEPLOYMENT_GUIDE.md)**

---

## 🆘 Quick Troubleshooting

### CORS Error in Browser
→ Update Railway `CORS_ORIGINS` to match your Vercel URL exactly

### Can't Connect to API
→ Check `frontend/env.js` has correct Railway URL

### Railway Deployment Failed
→ Check Railway logs, verify `backend` root directory is set

### Vercel Deployment Failed
→ Check Vercel logs, verify `frontend` root directory is set

---

**Questions?** Check the full guide or Railway/Vercel dashboards for logs.

**Time to deploy: ~15 minutes total** ⚡

