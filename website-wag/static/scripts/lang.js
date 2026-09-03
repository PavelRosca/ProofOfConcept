// Client-side language switcher (IT / EN)
(function () {
  "use strict";

  const DEFAULT_LANG = "it";
  const SUPPORTED_LANGS = ["it", "en"];

  function getLangFromPath(pathname) {
    const segments = pathname.split("/").filter(Boolean);
    const maybeLang = segments.length ? segments[0] : "";
    return SUPPORTED_LANGS.includes(maybeLang) ? maybeLang : DEFAULT_LANG;
  }

  function buildLocalizedPath(targetLang, pathname) {
    const segments = pathname.split("/").filter(Boolean);
    if (segments.length && SUPPORTED_LANGS.includes(segments[0])) {
      segments.shift();
    }

    if (targetLang === "en") {
      return `/en/${segments.join("/")}${segments.length ? "/" : ""}`;
    }

    return `/${segments.join("/")}${segments.length ? "/" : ""}`;
  }

  function setLanguageState(lang) {
    document.documentElement.lang = lang;
    localStorage.setItem("site_lang", lang);
    document.cookie = `django_language=${lang}; path=/; max-age=31536000; SameSite=Lax`;

    document.querySelectorAll("[data-lang]").forEach(function (btn) {
      btn.classList.toggle("font-semibold", btn.dataset.lang === lang);
    });
  }

  function applyTranslations(lang) {
    // Text content is rendered server-side per locale (request.LANGUAGE_CODE);
    // this just keeps the lang attribute, cookie, and toggle button in sync.
    setLanguageState(lang === "en" ? "en" : "it");
  }

  // Expose for external calls (e.g. admin custom scripts)
  window.applyTranslations = applyTranslations;
  window.getCurrentSiteLang = function () { return getLangFromPath(window.location.pathname); };

  document.addEventListener("DOMContentLoaded", function () {
    const currentLang = getLangFromPath(window.location.pathname);
    document.cookie = `django_language=${currentLang}; path=/; max-age=31536000; SameSite=Lax`;
    applyTranslations(currentLang);

    // Event delegation — survives DOM re-renders
    document.addEventListener("click", function (e) {
      const btn = e.target.closest("[data-lang]");
      if (!btn) return;

      e.preventDefault();
      const targetLang = btn.dataset.lang === "en" ? "en" : "it";
      setLanguageState(targetLang);

      const nextPath = buildLocalizedPath(targetLang, window.location.pathname);
      const nextUrl = `${nextPath}${window.location.search}${window.location.hash}`;

      if (nextUrl !== `${window.location.pathname}${window.location.search}${window.location.hash}`) {
        window.location.assign(nextUrl);
      } else {
        applyTranslations(targetLang);
      }
    });

    // Re-apply translations when DOM mutates (Wagtail editor may re-render parts)
    const observer = new MutationObserver(function () {
      clearTimeout(window.__langObserverTimeout);
      window.__langObserverTimeout = setTimeout(function () {
        applyTranslations(window.getCurrentSiteLang());
      }, 50);
    });
    observer.observe(document.body, { childList: true, subtree: true, attributes: true });
  });
})();
