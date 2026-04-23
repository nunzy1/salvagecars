# Salvage Cars Business
This project uses `web/` as the single source of truth for the site.

## Source of truth and sync process
- `web/` contains the Next.js application code and assets.
- Firebase Hosting is configured to use `web` as its source in `firebase.json`.
- The old root `public/` folder was removed and should not be recreated.
- When running Firebase locally or deploying, Firebase builds from `web/` and serves generated output from `.firebase/salvage-cars-business/hosting` (build artifact).

## Development workflow
Run all commands from the repository root unless noted.

1. Install dependencies (first time or after dependency changes):
   - `npm --prefix web install`
2. Run the Next.js development server:
   - `npm --prefix web run dev`
   - Open `http://localhost:3000`
3. Validate production build:
   - `npm --prefix web run build`

## Local Firebase preview (deployment-like check)
Use this to verify what Hosting will serve:

1. Start local hosting preview:
   - `firebase serve`
2. Open:
   - `http://localhost:5002`

## Publish workflow
When ready to publish:

- `firebase deploy --only hosting`

## Notes
- Make content/style/code changes under `web/` (for example `web/app` and `web/public`).
- If Next reports another dev server is already running, stop the existing process before starting a new one.
