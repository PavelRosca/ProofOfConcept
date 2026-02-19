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

---

Date: 2026-02-19

Work completed in this iteration (Presentation Step 1):

- Frozen presentation scope to 5 primary pages:
  - `front-end/src/pages/index.html`
  - `front-end/src/pages/projects.html`
  - `front-end/src/pages/support.html`
  - `front-end/src/pages/join.html`
  - `front-end/src/pages/contact.html`

- Cleaned main navigation to include only the 5 presentation pages.
  - Removed template/demo dropdown links (Career, Integrations, Pricing, Changelogs, etc.).
  - File: `front-end/src/partials/header.html`

- Aligned footer quick links with presentation scope.
  - Added `Sostienici` link for consistency.
  - File: `front-end/src/partials/footer.html`

- Validation:
  - `npm run build` completed successfully.
  - Existing Sass/JSHint warnings remain non-blocking and pre-existing.

---

Date: 2026-02-19

Work completed in this iteration (Presentation Step 2):

- Removed generic template leftovers from homepage.
  - Removed generic "Services", "Reviews" and "Download The Theme" CTA blocks.
  - File: `front-end/src/pages/index.html`

- Removed duplicate generic contact template from contact page.
  - Kept only localized political contact form/section.
  - File: `front-end/src/pages/contact.html`

- Validation:
  - `npm run build` completed successfully.
  - Existing Sass/JSHint warnings remain non-blocking and pre-existing.

---

Date: 2026-02-19

Work completed in this iteration (Presentation Step 3 — EN/IT working):

- Fixed i18n build source path:
  - Added active language switcher in `front-end/src/scripts/lang.js` so Gulp includes it in generated `theme/scripts/lang.js`.
  - Root cause was script location mismatch (`front-end/scripts/lang.js` was outside Gulp source pipeline).

- Extended `data-i18n` coverage to the 5 presentation pages:
  - `front-end/src/pages/index.html`
  - `front-end/src/pages/projects.html`
  - `front-end/src/pages/support.html`
  - `front-end/src/pages/join.html`
  - `front-end/src/pages/contact.html`

- Corrected CTA translation keys:
  - Split `support` intent (`Sostienici`) from `donate now` intent to prevent wrong substitutions in EN/IT.

- Validation:
  - `npm run build` completed successfully after changes.
  - Remaining warnings are pre-existing (`main.js` JSHint + Sass/Tailwind deprecations) and unrelated to i18n behavior.
