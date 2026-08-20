# SalvageCars.com
A static HTML site served from `public/` and hosted on Firebase.

## Repository Structure

```
salvagecars/
├── docs/                          # Internal project documentation (not deployed)
│   ├── repository-architecture.html
│   └── site-structure-user-nav.html
├── public/                        # All files deployed to Firebase Hosting
│   ├── index.html                 # Homepage
│   ├── guides/                    # Buying guides
│   ├── states/                    # State Guidance Center (index.html)
│   ├── vision/                    # Vision page
│   ├── architecture/              # Architecture page
│   ├── privacy/                   # Privacy Policy
│   ├── terms/                     # Terms of Service
│   └── assets/                    # Shared assets (css/, js/, images/)
├── firebase.json
├── .firebaserc
├── .firebaseignore
└── .gitignore
```

## Local Development
Run from the repository root:
1. `firebase serve --only hosting`
2. Open the local URL shown in terminal (commonly `http://localhost:5000`).
3. Edit HTML files in `public/` and refresh the browser.

## Publishing
- `firebase deploy --only hosting`

## Adding New Pages
For clean URLs, use folder routes:
- Create `public/your-path/index.html`
- Link to `/your-path` from other pages

Example:
- File: `public/guides/new-guide/index.html`
- URL: `/guides/new-guide`

## Notes
- Files in `docs/` are internal documents and are not deployed.
- If a link returns 404, confirm there is a matching file path under `public/`.
- Keep placeholder legal pages updated before production launch.
