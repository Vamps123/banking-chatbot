# Publish the GenAI Banking Support Chatbot

This project is ready for publishing on GitHub and Render.

## 1. Initialize Git (if not already done)

```powershell
cd c:\Users\meet2\OneDrive\Desktop\Gen.ai
git init
git add .
git commit -m "Initial GenAI Banking Support Chatbot implementation"
```

## 2. Create a GitHub repository

1. Create a new repository on GitHub.
2. Add the remote URL:
   ```powershell
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
```
3. Push to GitHub:
   ```powershell
git push -u origin master
```

## 3. Deploy backend and frontend to Render

The repo includes `render.yaml`, which configures:

- A backend Docker web service using `backend/Dockerfile`
- A static site for the frontend from `frontend/dist`

### Current Render dashboard

- Render dashboard: `https://dashboard.render.com/web/srv-d862d337uimc73bt85rg/deploys/dep-d862d3b7uimc73bt860g?r=2026-05-19%4008%3A58%3A57%7E2026-05-19%4009%3A01%3A09`

### Recommended Render setup

1. Sign in to Render.
2. Create a new service from GitHub.
3. Select this repository.
4. Ensure the backend service uses Docker and the `backend/Dockerfile` path.
5. Add the environment variable:
   - `OPENAI_API_KEY` (optional)

## 4. Deploy manually if needed

If Render is unavailable, you can also deploy the backend using Docker on any platform that supports container deployment.

## 5. Verify deployment

When deployed, test the following endpoints:

- `GET /health`
- `POST /chat`
- `POST /upload`

And confirm the frontend loads successfully.
