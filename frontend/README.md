# SupportIQ Frontend

A React + Vite customer-support dashboard for the AI Customer Support System.

## Features

- Responsive SaaS dashboard layout
- Live chat wired to the FastAPI `POST /chat` endpoint
- Backend health badge wired to `GET /health`
- Ticket, FAQ, analytics, and settings views
- Explicit demo labeling for sample tickets, FAQs, and dashboard metrics
- Configurable API base URL for local development and production

## Project structure

```text
frontend/
├── .env.example
├── index.html
├── package.json
├── vite.config.js
└── src/
    ├── App.jsx
    ├── index.css
    └── main.jsx
```

## Local setup in the existing project

Run from the project root:

```powershell
cd frontend
npm install
npm run dev
```

Start the backend separately from the project root:

```powershell
python -m uvicorn src.api.main:app --reload
```

Open `http://localhost:5173`. Vite proxies `/api/health` to `http://127.0.0.1:8000/health` and `/api/chat` to `http://127.0.0.1:8000/chat`.

## Production API URL

Set `VITE_API_BASE_URL` in the hosting provider's environment variables to the **HTTPS base URL** of your FastAPI service, for example:

```text
VITE_API_BASE_URL=https://api.example.com
```

Then the frontend calls `https://api.example.com/health` and `https://api.example.com/chat`. Rebuild/redeploy the frontend after changing this variable.

The Vite proxy is for local development only. For a separately hosted HTTPS frontend, do not point the browser directly to an HTTP EC2 API endpoint: browsers may block mixed content. Set up HTTPS for the API and configure FastAPI CORS to allow the frontend origin.

## Deploy to AWS Amplify Hosting

Recommended for this project because the FastAPI backend is already on AWS EC2. Amplify hosts the React/Vite static frontend separately and provides managed builds, CDN delivery, and HTTPS.

Because the full project is a monorepo (backend at the repository root and frontend in `frontend/`), copy `amplify.monorepo.yml.example` to `amplify.yml` at the ROOT of the full Git repository. In the Amplify console, connect that repository and select the monorepo app root `frontend` (Amplify should set `AMPLIFY_MONOREPO_APP_ROOT=frontend`). AWS documents this monorepo configuration in its [Amplify Hosting guide](https://docs.aws.amazon.com/amplify/latest/userguide/monorepo-configuration.html).

For a separate Git repository whose root is the frontend itself, use the included `amplify.yml` directly.

Build settings for the frontend are:

- App root: `frontend`
- Build command: `npm ci && npm run build` (or `npm install && npm run build` if there is no lockfile yet)
- Output/publish directory: `dist`
- Environment variable: `VITE_API_BASE_URL=https://your-https-api-domain`

Amplify provides HTTPS and CDN delivery for the static frontend. The FastAPI backend remains a separate service, such as your EC2 Docker container.

## Important implementation notes

- Ticket records and dashboard analytics in this starter are sample/demo UI data; they are not fetched from a ticket or analytics backend endpoint.
- FAQ details in the knowledge-base page are display examples. The live chat is the part connected to your FastAPI API.
- Never store Groq/OpenAI secret keys in frontend variables. Any `VITE_*` variable is compiled into browser-visible code.
- Before real users access the API, add authentication, authorization, rate limiting, HTTPS, and strict CORS rules.
