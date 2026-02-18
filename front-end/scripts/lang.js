// Simple client-side language switcher (IT / EN)
(function () {
  const translations = {
    it: {
      'nav.home': 'Home',
      'nav.projects': 'Progetti',
      'nav.support': 'Sostienici',
      'nav.join': 'Iscriviti',
      'nav.contact': 'Contatti',
      'nav.signup': 'Iscriviti',
      'cta.join': 'Iscriviti',
      'cta.support': 'Dona ora',
      'actions.viewProjects': 'Vedi tutti i progetti',
      'footer.about': 'Siamo un movimento dedicato al sostegno delle famiglie e alla partecipazione civica. Trasparenza, solidarietà, responsabilità.',
      'footer.socials': 'Social',
      'footer.links': 'Link rapidi',
      'footer.contact': 'Sede & Contatti'
    },
    en: {
      'nav.home': 'Home',
      'nav.projects': 'Projects',
      'nav.support': 'Support us',
      'nav.join': 'Join',
      'nav.contact': 'Contact',
      'nav.signup': 'Join',
      'cta.join': 'Join',
      'cta.support': 'Donate now',
      'actions.viewProjects': 'View all projects',
      'footer.about': 'We are a movement supporting families and civic participation. Transparency, solidarity, responsibility.',
      'footer.socials': 'Social',
      'footer.links': 'Quick links',
      'footer.contact': 'Location & Contact'
    }
  };

  function applyTranslations(lang) {
    document.querySelectorAll('[data-i18n]').forEach((el) => {
      const key = el.getAttribute('data-i18n');
      const txt = (translations[lang] && translations[lang][key]) || '';
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT') {
        el.setAttribute('placeholder', txt);
      } else {
        el.textContent = txt;
      }
    });
    document.documentElement.lang = lang === 'it' ? 'it' : 'en';
    localStorage.setItem('site_lang', lang);
  }

  document.addEventListener('DOMContentLoaded', function () {
    const saved = localStorage.getItem('site_lang') || 'it';
    applyTranslations(saved);

    const itBtn = document.getElementById('lang-it');
    const enBtn = document.getElementById('lang-en');
    if (itBtn) itBtn.addEventListener('click', () => applyTranslations('it'));
    if (enBtn) enBtn.addEventListener('click', () => applyTranslations('en'));
  });
})();
