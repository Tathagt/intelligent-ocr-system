# 🚀 Deployment Guide

Complete guide to deploy the Intelligent OCR System to production.

## 📋 Prerequisites

- GitHub account
- Railway account (or Render/Vercel)
- Streamlit Cloud account

## 🎯 Deployment Options

### Option 1: Railway (Recommended for Backend)

#### Step 1: Deploy Backend to Railway

1. **Sign up/Login to Railway**
   - Go to https://railway.app
   - Sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `intelligent-ocr-system`

3. **Configure Service**
   - Railway auto-detects `railway.json`
   - Set environment variables (if needed):
     - `PORT`: 8000 (auto-set by Railway)
   
4. **Deploy**
   - Railway will build and deploy automatically
   - Wait for deployment to complete (~5-10 minutes)
   - Copy the generated URL (e.g., `https://your-app.railway.app`)

5. **Verify Deployment**
   - Visit `https://your-app.railway.app/`
   - Should see: `{"message": "Intelligent OCR API", "status": "running"}`
   - Check API docs: `https://your-app.railway.app/docs`

#### Step 2: Deploy Frontend to Streamlit Cloud

1. **Sign up/Login to Streamlit Cloud**
   - Go to https://streamlit.io/cloud
   - Sign in with GitHub

2. **Create New App**
   - Click "New app"
   - Repository: `Tathagt/intelligent-ocr-system`
   - Branch: `main`
   - Main file path: `frontend/app.py`

3. **Configure App**
   - Click "Advanced settings"
   - Add Python version: `3.10`
   - No secrets needed for basic deployment

4. **Update API URL**
   - Before deploying, update the default API URL in `frontend/app.py`
   - Or users can enter it in the sidebar after deployment

5. **Deploy**
   - Click "Deploy!"
   - Wait for deployment (~3-5 minutes)
   - Your app will be live at `https://your-app.streamlit.app`

---

### Option 2: Render (Alternative for Backend)

#### Deploy Backend to Render

1. **Sign up/Login to Render**
   - Go to https://render.com
   - Sign in with GitHub

2. **Create Web Service**
   - Click "New" → "Web Service"
   - Connect GitHub repository
   - Select `intelligent-ocr-system`

3. **Configure Service**
   - Name: `ocr-backend`
   - Environment: `Python 3`
   - Build Command: `cd backend && pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment
   - Copy the URL

---

### Option 3: Vercel (Alternative for Backend)

#### Deploy Backend to Vercel

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Create `vercel.json`**
   ```json
   {
     "builds": [
       {
         "src": "backend/main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "backend/main.py"
       }
     ]
   }
   ```

3. **Deploy**
   ```bash
   vercel --prod
   ```

---

## 🔧 Configuration

### Environment Variables

#### Backend (Optional)
- `PORT`: Server port (auto-set by platforms)
- `WORKERS`: Number of workers (default: 1)
- `LOG_LEVEL`: Logging level (default: info)

#### Frontend
- Update API URL in sidebar or hardcode in `app.py`:
  ```python
  api_url = st.text_input(
      "Backend API URL",
      value="https://your-backend-url.railway.app",  # Update this
      help="Enter the backend API URL"
  )
  ```

---

## ✅ Post-Deployment Checklist

### Backend
- [ ] API is accessible at root endpoint
- [ ] `/health` endpoint returns healthy status
- [ ] `/docs` shows Swagger UI
- [ ] Can upload and process test image
- [ ] CORS is properly configured

### Frontend
- [ ] App loads without errors
- [ ] Can connect to backend API
- [ ] File upload works
- [ ] Processing returns results
- [ ] All tabs display correctly

---

## 🧪 Testing Deployment

### Test Backend API

```bash
# Health check
curl https://your-backend-url.railway.app/health

# Test with sample image
curl -X POST "https://your-backend-url.railway.app/api/process-document" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_image.jpg"
```

### Test Frontend

1. Visit your Streamlit app URL
2. Upload a test document image
3. Click "Process Document"
4. Verify all results display correctly

---

## 🐛 Troubleshooting

### Backend Issues

**Problem: Build fails on Railway**
- Check logs in Railway dashboard
- Ensure all dependencies in `requirements.txt`
- Verify Python version compatibility

**Problem: API returns 500 errors**
- Check application logs
- Verify spaCy model downloaded
- Check memory limits (OCR is memory-intensive)

**Problem: Slow processing**
- Increase instance size on Railway
- Consider adding Redis caching
- Optimize image preprocessing

### Frontend Issues

**Problem: Cannot connect to backend**
- Verify backend URL is correct
- Check CORS configuration
- Ensure backend is running

**Problem: Upload fails**
- Check file size limits
- Verify file type is supported
- Check backend logs for errors

---

## 📊 Monitoring

### Railway Dashboard
- View logs in real-time
- Monitor CPU/Memory usage
- Check request metrics

### Streamlit Cloud
- View app analytics
- Monitor user sessions
- Check error logs

---

## 🔒 Security Best Practices

1. **API Security**
   - Add rate limiting
   - Implement authentication (for production)
   - Validate file uploads

2. **Environment Variables**
   - Never commit secrets to Git
   - Use platform secret management
   - Rotate keys regularly

3. **CORS Configuration**
   - Restrict origins in production
   - Update `allow_origins` in `main.py`

---

## 💰 Cost Estimates

### Railway (Backend)
- **Hobby Plan**: $5/month
- Includes: 500 hours, 512MB RAM, 1GB storage
- Sufficient for demo/testing

### Streamlit Cloud (Frontend)
- **Free Tier**: Unlimited public apps
- Includes: 1GB RAM, community support
- Perfect for this project

### Total: ~$5/month for full deployment

---

## 🚀 Production Optimization

### Backend
- Add Redis for caching
- Implement request queuing
- Use CDN for static assets
- Add monitoring (Sentry, DataDog)

### Frontend
- Add loading states
- Implement error boundaries
- Add analytics (Google Analytics)
- Optimize image uploads

---

## 📞 Support

If you encounter issues:
1. Check logs in platform dashboard
2. Review error messages
3. Test locally first
4. Check GitHub Issues

---

**Deployment completed! 🎉**

Your OCR system is now live and ready for the SPAZORLABS internship submission!
