# MaxLikes API - Render Deployment

Complete deployment package for MaxLikes API on Render with Flask backend and Gunicorn.

## 📁 Project Structure

```
render/
├── app.py                 # Main Flask application
├── like_pb2.py            # Protobuf definitions
├── like_count_pb2.py      # Protobuf definitions
├── uid_generator_pb2.py   # Protobuf definitions
├── token_ind.json         # India server tokens (5,497 tokens)
├── token_br.json          # Brazil/US/SAC/NA tokens
├── token_bd.json          # Bangladesh tokens
├── Procfile               # Render startup command
├── requirements.txt       # Python dependencies (includes gunicorn)
└── README.md              # This file
```

## 🚀 Quick Deploy to Render

### Step 1: Prepare Your Repository

1. Push this `render` folder to GitHub, GitLab, or Bitbucket
2. Ensure all files are in the repository

### Step 2: Create Web Service on Render

1. Go to [render.com](https://render.com) and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your repository
4. Configure the service:

**Basic Settings:**
- **Name**: `maxlikes-api` (or your choice)
- **Region**: Choose closest to your users
- **Branch**: `main` (or your branch)
- **Root Directory**: `render` (if deploying from subdirectory)
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120`
  - Note: If you have a Procfile, Render will use it automatically

**Instance Type:**
- **Free** tier works, but has limitations (spins down after inactivity)
- **Starter** or higher recommended for production use

5. Click **"Create Web Service"**

### Step 3: Configure Environment Variables (CRITICAL!)

After creating the service:

1. Go to your service dashboard
2. Click **"Environment"** tab in left sidebar
3. Add the following environment variables:

#### Required Variables:

**SECRET_KEY**
- Generate using: `python -c 'import os; print(os.urandom(24).hex())'`
- Example: `a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4`
- Click **"Add Environment Variable"**

**ADMIN_PASSWORD**
- Your custom password for admin panel
- Example: `YourSecurePassword123`
- Click **"Add Environment Variable"**

4. Click **"Save Changes"**
5. Render will automatically redeploy with new environment variables

## 📱 Using Your Deployed App

After deployment, you'll get a URL like: `https://maxlikes-api.onrender.com`

### Frontend Pages:

- **Home (IND Server)**: `https://your-service.onrender.com/`
  - Requires login with ADMIN_PASSWORD
  - Simple interface to send likes to IND server

- **Admin Panel**: `https://your-service.onrender.com/admin`
  - Full-featured admin panel
  - Test all servers (IND, BR, US, SAC, NA, BD)
  - Monitor API statistics

### API Endpoints:

**Send Likes**
```
GET /like?uid={UID}&server_name={SERVER}&key=gst&like={OPTIONAL}
```

**Parameters:**
- `uid` - User ID (required)
- `server_name` - Server region: IND, BR, US, SAC, NA, BD (required)
- `key` - Must be "gst" (required)
- `like` - Number of tokens or "max" (optional, defaults to all tokens)

**Examples:**
```bash
curl "https://your-service.onrender.com/like?uid=1366626557&server_name=IND&key=gst"
curl "https://your-service.onrender.com/like?uid=1366626557&server_name=IND&key=gst&like=500"
curl "https://your-service.onrender.com/like?uid=1366626557&server_name=IND&key=gst&like=max"
```

## 🔧 Render vs Vercel Differences

### Why Render?

1. **Always-On Server** - Unlike Vercel's serverless, Render provides a persistent server
2. **No Cold Starts** - Faster response times for production use
3. **Better for Long-Running Requests** - No 10-second timeout limit
4. **Persistent Connections** - Better for complex API operations

### Configuration Differences:

- **Gunicorn** - Production-grade WSGI server (added to requirements.txt)
- **Procfile** - Defines startup command for Render
- **Workers** - Configured for 4 workers to handle concurrent requests
- **Timeout** - Set to 120 seconds for longer operations

## 🐛 Troubleshooting

### "Application Error" on Render
**Solution**: Check the logs (Dashboard → Logs tab) and ensure environment variables are set

### Service keeps spinning down (Free tier)
**Solution**: Free tier spins down after 15 minutes of inactivity. Upgrade to Starter ($7/month) for always-on

### Deployment failed
**Solution**: Check build logs for errors. Common issues:
- Missing dependencies in requirements.txt
- Syntax errors in app.py
- Missing environment variables

### Login not working
**Solution**: Verify ADMIN_PASSWORD is set in Environment tab, then redeploy

## 📊 Token Configuration

Current setup:
- **IND Server**: 5,497 real tokens
- **BR/US/SAC/NA Server**: 2 placeholder tokens (update if needed)
- **BD Server**: 2 placeholder tokens (update if needed)

To update tokens:
1. Edit the respective JSON files locally
2. Commit and push to Git
3. Render will auto-deploy the changes

## 🔄 Updating Your Deployment

### Automatic Deployments:
1. Make changes to your code
2. Commit and push to your Git repository
3. Render automatically detects changes and redeploys

### Manual Deployments:
1. Go to your service dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

### Viewing Logs:
- Real-time logs available in **"Logs"** tab
- Great for debugging and monitoring

## 💡 Render Best Practices

- **Use Starter tier or higher** for production (no spin-down)
- **Enable auto-deploy** from main branch
- **Monitor logs** regularly for errors
- **Set up custom domain** for professional URLs
- **Use health check endpoint** (Render auto-pings your service)

## 🔐 Security Features

✅ Password-protected admin panel  
✅ Secure session management  
✅ Environment variables for sensitive data  
✅ Password hashing with werkzeug  
✅ HTTPS by default on Render  
✅ Gunicorn production server  

## 📈 Monitoring & Performance

### Monitoring:
- **Logs**: Real-time logging in dashboard
- **Metrics**: CPU, Memory usage available in dashboard
- **Alerts**: Set up email notifications for service issues

### Performance:
- **Workers**: 4 workers handle concurrent requests
- **Timeout**: 120 seconds for long operations
- **Scaling**: Easy to scale up with higher-tier plans

## 🆓 Free Tier Limitations

- **Spin down** after 15 minutes of inactivity (90 second restart)
- **750 hours/month** of usage
- **Shared CPU** and **512 MB RAM**
- **100 GB bandwidth/month**

**For production**: Consider Starter plan ($7/month) for:
- Always-on service
- More resources
- Better performance

## 🌐 Custom Domain Setup

1. Go to your service dashboard
2. Click **"Settings"** tab
3. Scroll to **"Custom Domain"**
4. Add your domain and configure DNS
5. Render provides free SSL certificates

## 📄 License

This project is provided as-is for deployment purposes.
