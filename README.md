# Salvage Cars Business
This project is currently a static HTML site served from `public/`.

## Source of truth
- All live site pages are stored in `public/`.
- Firebase Hosting is configured in `firebase.json` with:
  - `"public": "public"`
- There is no active `web/` build step in the current workflow.

## Directory structure
- `public/index.html` → homepage
- `public/guides/.../index.html` → guide pages
- `public/categories/index.html` → categories landing page
- `public/privacy/index.html` and `public/terms/index.html` → legal placeholders

## Local development workflow
Run commands from the repository root:

1. Start local hosting:
   - `firebase serve --only hosting`
2. Open the local URL shown in terminal (commonly `http://localhost:5000`).
3. Edit HTML files in `public/` and refresh the browser.

## Publishing workflow
When ready to publish:
- `firebase deploy --only hosting`

## Adding new pages
For clean URLs, use folder routes:
- Create `public/your-path/index.html`
- Link to `/your-path` from other pages

Example:
- File: `public/guides/new-guide/index.html`
- URL: `/guides/new-guide`

## Notes
- If a link returns 404, confirm there is a matching file path under `public/`.
- Keep placeholder legal pages updated before production launch.
