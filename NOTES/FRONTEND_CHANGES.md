# FRONTEND CHANGES — traceability log

Date: 2026-02-18

Work completed in this iteration:

- Converted homepage to Italian-focused content with clear CTAs for `Iscriviti` and `Sostienici`.
  - File: `front-end/src/pages/index.html`

- Added new primary pages to represent product scope:
 - Added new primary pages to represent product scope (filenames are English; visible text remains Italian):
  - `front-end/src/pages/projects.html` (Progetti)
  - `front-end/src/pages/support.html` (Sostienici)
  - `front-end/src/pages/join.html` (Iscriviti)
  - `front-end/src/pages/contact.html` (Contatti)

- Updated header and footer partials to reflect Italian menu and to include a language toggle.
  - Files: `front-end/src/partials/header.html`, `front-end/src/partials/footer.html`

- Implemented a lightweight client-side language switcher using `data-i18n` attributes.
  - File: `front-end/scripts/lang.js`
  - Behavior: default language `it`; user may toggle to `en`; preference persisted in `localStorage`.

Notes and follow-ups:
- The language switcher is DOM-only. For SEO and server-rendered translations, add server-side i18n or pre-rendered translated pages.
- Forms (`iscriviti`, `contatti`) are frontend templates — backend endpoints must be implemented and CSRF/validation wired (see `back-end/members` and `back-end/donations`).
 - Forms (`join`, `contact`) are frontend templates — backend endpoints must be implemented and CSRF/validation wired (see `back-end/members` and `back-end/donations`).
- Styling reuses existing Tailwind classes; run build (`npm run build`) to produce compiled assets.
