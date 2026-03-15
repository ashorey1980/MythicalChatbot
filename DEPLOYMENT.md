# Deployment Guide - Streamlit Cloud

## 🚀 Quick Deployment Steps

### 1. Push to GitHub

Your app is already in the pm-2 repository. Push your changes:

```bash
cd ~/claude-projects/pm-2
git add demo-apps/llm-proxy-tester/
git commit -m "Add Mythical Enterprise Chatbot app"
git push origin master
```

### 2. Deploy to Streamlit Cloud

1. **Go to** [share.streamlit.io](https://share.streamlit.io)

2. **Sign in** with your GitHub account

3. **Click "New app"**

4. **Fill in the deployment settings:**
   - **Repository:** `mulesoft/pm-2`
   - **Branch:** `master`
   - **Main file path:** `demo-apps/llm-proxy-tester/app.py`

5. **Click "Deploy!"**

### 3. Configure Environment Variables (Optional)

If you want to use the ANTHROPIC_API_KEY for summarization features:

1. In Streamlit Cloud dashboard, click on your deployed app
2. Click **⚙️ Settings** → **Secrets**
3. Add:
   ```toml
   ANTHROPIC_API_KEY = "your-api-key-here"
   ```
4. Click **Save**

---

## ✅ Your App Will Be Live At:

`https://[your-app-name].streamlit.app`

---

## 📋 What's Included

- ✅ `app.py` - Main application
- ✅ `requirements.txt` - Python dependencies
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ `.gitignore` - Git ignore rules

---

## 🔧 Post-Deployment

### Custom Domain (Optional)
You can add a custom domain in the Streamlit Cloud settings.

### App Settings
- **Sleep mode:** Apps sleep after inactivity on free tier
- **Reboot:** Settings → Reboot to restart the app
- **Logs:** Settings → Logs to view application logs

---

## 🐛 Troubleshooting

**App won't start?**
- Check logs in Streamlit Cloud dashboard
- Verify `requirements.txt` has all dependencies
- Ensure `app.py` path is correct

**Missing API key?**
- Add `ANTHROPIC_API_KEY` to Secrets (optional)
- The app works without it (just won't use summarization)

---

## 🔄 Updates

To update your deployed app:

```bash
cd ~/claude-projects/pm-2
git add demo-apps/llm-proxy-tester/
git commit -m "Update chatbot app"
git push origin master
```

Streamlit Cloud auto-detects changes and redeploys!

---

## 📱 Sharing

Share your app URL with anyone:
- No authentication required for viewers
- Viewers can use the app immediately
- You control access via GitHub repository permissions
