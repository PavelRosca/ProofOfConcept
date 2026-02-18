# NOTES — front-end

Location: `front-end/` (Tailwind + Gulp)

What exists:
- `src/` with templates and components; `theme/` compiled assets; `package.json`, `gulpfile.js`.

Checks & fixes:
- `package.json` script `remove-darkmode` uses `yarn format` — change to `npm run format` or ensure Yarn is intentional. See [front-end/package.json](front-end/package.json#L1-L80).
- Ensure `gulp-cli` availability (global) or use `npx gulp` to run tasks.
