# Premium Railway Ops Dashboard (Vercel Demo)

Self-contained portfolio dashboard for premium Indian Railways operational intelligence.

## Local run

```bash
npm install
npm run dev
```

## Vercel deployment (free tier)

1. Push `vercel-next-dashboard/` to GitHub.
2. In Vercel, import the repo.
3. Set root directory to `vercel-next-dashboard`.
4. Deploy directly (no environment variables required).

## Architecture

- Next.js App Router
- TailwindCSS
- Recharts
- Framer Motion
- Static local mock operational dataset
- Lightweight client-side simulation (~7s updates)

## Notes

- No external API calls.
- No backend ingestion dependency.
- No websocket or streaming infrastructure.
- Designed for recruiter demos and screenshot quality.
