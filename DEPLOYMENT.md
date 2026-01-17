# 🚀 Deployment Guide

This guide covers deploying the Loan Approval Prediction System to various platforms.

## 🌐 Backend Deployment Options

### 1. Heroku (Recommended)

```bash
# Install Heroku CLI and login
heroku login

# Create Heroku app
heroku create your-loan-app-backend

# Add Python buildpack
heroku buildpacks:set heroku/python

# Deploy
git subtree push --prefix backend heroku main
```

**Heroku Configuration:**
- Add `Procfile` in backend: `web: python app.py`
- Set environment variables if needed
- Update CORS origins for production

### 2. Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### 3. PythonAnywhere

1. Upload backend files
2. Create virtual environment
3. Install requirements
4. Configure WSGI file
5. Set up web app

## 🎨 Frontend Deployment Options

### 1. Netlify (Recommended)

```bash
# Build the project
cd frontend
npm run build

# Deploy to Netlify
# Drag and drop the 'build' folder to Netlify
```

**Netlify Configuration:**
- Build command: `npm run build`
- Publish directory: `build`
- Update API base URL in `src/api.js`

### 2. Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel
```

### 3. GitHub Pages

```bash
# Install gh-pages
npm install --save-dev gh-pages

# Add to package.json scripts:
"homepage": "https://yourusername.github.io/loan-approval-prediction-system",
"predeploy": "npm run build",
"deploy": "gh-pages -d build"

# Deploy
npm run deploy
```

## 🔧 Production Configuration

### Backend Changes for Production

1. **Update CORS origins** in `app.py`:
```python
CORS(app, origins=["https://your-frontend-domain.com"])
```

2. **Environment variables**:
```python
import os
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
PORT = int(os.environ.get('PORT', 5000))
```

3. **Production WSGI server**:
```bash
pip install gunicorn
gunicorn app:app
```

### Frontend Changes for Production

1. **Update API base URL** in `src/api.js`:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-backend-domain.com';
```

2. **Environment variables** (`.env.production`):
```
REACT_APP_API_URL=https://your-backend-domain.com
```

## 📊 Monitoring and Analytics

### Backend Monitoring
- Add logging with Python `logging` module
- Use services like Sentry for error tracking
- Monitor API performance with tools like New Relic

### Frontend Analytics
- Add Google Analytics
- Monitor user interactions
- Track prediction success rates

## 🔒 Security Considerations

### Backend Security
- Add rate limiting with `flask-limiter`
- Implement API authentication if needed
- Validate all input data
- Use HTTPS in production

### Frontend Security
- Sanitize user inputs
- Use HTTPS
- Implement Content Security Policy (CSP)

## 🧪 Testing in Production

### Backend Testing
```bash
# Test API endpoints
curl -X POST https://your-backend-domain.com/predict \
  -H "Content-Type: application/json" \
  -d '{"Gender":"Male","Married":"Yes",...}'
```

### Frontend Testing
- Test all form validations
- Verify API connectivity
- Check responsive design
- Test error handling

## 📈 Performance Optimization

### Backend Optimization
- Use caching for model predictions
- Optimize model loading
- Use connection pooling for databases

### Frontend Optimization
- Code splitting with React.lazy()
- Image optimization
- Bundle size optimization
- CDN for static assets

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{secrets.HEROKU_API_KEY}}
          heroku_app_name: "your-loan-app-backend"
          heroku_email: "your-email@example.com"
          appdir: "backend"

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Netlify
        uses: nwtgck/actions-netlify@v1.2
        with:
          publish-dir: './frontend/build'
          production-branch: main
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

## 🎯 Deployment Checklist

### Pre-deployment
- [ ] Test locally with production build
- [ ] Update API URLs for production
- [ ] Set up environment variables
- [ ] Configure CORS properly
- [ ] Test all API endpoints
- [ ] Verify model files are included

### Post-deployment
- [ ] Test live application
- [ ] Monitor error logs
- [ ] Check performance metrics
- [ ] Verify SSL certificates
- [ ] Test from different devices/browsers

## 🆘 Troubleshooting

### Common Issues

1. **CORS Errors**: Update CORS configuration in backend
2. **API Connection Failed**: Check API URL and network connectivity
3. **Model Loading Errors**: Ensure model files are properly deployed
4. **Build Failures**: Check Node.js/Python versions and dependencies

### Debug Commands

```bash
# Check backend logs
heroku logs --tail -a your-app-name

# Test API connectivity
curl -I https://your-backend-domain.com/

# Check frontend build
npm run build && serve -s build
```

---

**Your loan approval system is ready for production deployment! 🚀**