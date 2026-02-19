# NOTES — front-end

Location: `front-end/` (Tailwind + Gulp)

What exists:
- `src/` with templates and components; `theme/` compiled assets; `package.json`, `gulpfile.js`.

Checks & fixes:
- `package.json` script `remove-darkmode` uses `yarn format` — change to `npm run format` or ensure Yarn is intentional. See [front-end/package.json](front-end/package.json#L1-L80).
- `package.json` references `scripts/removeDarkMode.js`, but actual file is `scripts/removeDarkmode.js` (case mismatch on Linux).
- Ensure `gulp-cli` availability (global) or use `npx gulp` to run tasks.

I18n EN/IT status (2026-02-19):
- Active i18n script source is `front-end/src/scripts/lang.js` (not `front-end/scripts/lang.js`).
- Gulp copies from `src/scripts/*.js` to `theme/scripts/*.js`; this is required for runtime language switching.
- `data-i18n` coverage implemented for presentation pages:
	- `front-end/src/pages/index.html`
	- `front-end/src/pages/projects.html`
	- `front-end/src/pages/support.html`
	- `front-end/src/pages/join.html`
	- `front-end/src/pages/contact.html`
- Language preference key: `localStorage.site_lang` (`it` default, `en` optional).
