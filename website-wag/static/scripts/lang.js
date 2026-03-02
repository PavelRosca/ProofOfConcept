// Client-side language switcher (IT / EN)
(function () {
  "use strict";

  const translations = {
    it: {
      "nav.home": "Home",
      "nav.projects": "Progetti",
      "nav.support": "Sostienici",
      "nav.join": "Iscriviti",
      "nav.contact": "Contatti",
      "nav.signup": "Iscriviti",

      "cta.join": "Iscriviti",
      "cta.supportUs": "Sostienici",
      "cta.donateNow": "Dona ora",
      "actions.viewProjects": "Vedi tutti i progetti",

      "home.hero.title": "Per le famiglie, per il futuro — Un paese più forte insieme",
      "home.hero.subtitle": "Sosteniamo politiche concrete per la famiglia, il lavoro e la solidarietà. Partecipa, iscriviti, dona: costruisci con noi un futuro più sicuro per i tuoi cari.",
      "home.mission.title": "La nostra missione",
      "home.mission.text": "Promuovere politiche che mettano al centro la famiglia, il lavoro dignitoso e la coesione sociale. Trasparenza, responsabilità e partecipazione civica guidano ogni nostra iniziativa.",
      "home.values.family.title": "Sostegno alle famiglie",
      "home.values.family.text": "Misure concrete per la cura, l'istruzione e il benessere dei nuclei familiari.",
      "home.values.civic.title": "Partecipazione civica",
      "home.values.civic.text": "Coinvolgiamo i cittadini nelle scelte locali e nazionali, favorendo trasparenza e dialogo.",
      "home.values.work.title": "Economia e lavoro",
      "home.values.work.text": "Sosteniamo politiche per l'occupazione, le piccole imprese e il lavoro stabile.",
      "home.featured.title": "Progetti in evidenza",
      "home.featured.text": "Iniziative locali e nazionali pensate per migliorare la vita quotidiana delle famiglie.",
      "home.featured.card1.title": "Centro di supporto familiare",
      "home.featured.card1.text": "Servizi locali per la cura dei bambini e supporto alle famiglie in difficoltà.",
      "home.featured.card2.title": "Borse lavoro giovanili",
      "home.featured.card2.text": "Programmi di inserimento per giovani e formazione professionale.",
      "home.featured.card3.title": "Rete di volontariato",
      "home.featured.card3.text": "Coordinamento nazionale di volontari per servizi sociali e assistenza.",
      "home.cta.title": "Sostieni il nostro lavoro",
      "home.cta.text": "Con il tuo contributo possiamo ampliare i servizi e raggiungere più famiglie. Ogni donazione conta.",

      "projects.page.title": "Progetti",
      "projects.page.intro": "Elenco delle iniziative e dei progetti in corso, divisi per regione e settore.",
      "projects.card1.title": "Centro di supporto familiare — NORD-01",
      "projects.card1.text": "Progetto pilota per servizi di sostegno alla genitorialità.",
      "projects.card2.title": "Borse lavoro per giovani — CENTRO-02",
      "projects.card2.text": "Formazione e inserimento nel mondo del lavoro.",

      "support.page.title": "Sostienici",
      "support.page.intro": "Come sostenere le nostre attività: donazioni singole, ricorrenti e volontariato.",
      "support.card1.title": "Donazione singola",
      "support.card1.text": "Scegli l'importo e sostieni un progetto locale.",
      "support.card2.title": "Donazione ricorrente",
      "support.card2.text": "Sostegno continuativo per progetti a lungo termine.",
      "support.card2.cta": "Sostieni mensilmente",
      "support.card3.title": "Volontariato",
      "support.card3.text": "Partecipa alle iniziative locali come volontario.",

      "join.page.title": "Iscriviti",
      "join.page.intro": "Diventa membro: compila il modulo per ricevere informazioni e partecipare alle attività locali.",
      "join.form.name": "Nome e Cognome",
      "join.form.email": "Email",
      "join.form.region": "Regione",
      "join.form.regionPlaceholder": "Seleziona regione",
      "join.form.submit": "Invia iscrizione",

      "contact.page.title": "Contatti",
      "contact.page.intro": "Per informazioni, collaborazioni o segnalazioni, contattaci.",
      "contact.form.name": "Nome",
      "contact.form.email": "Email",
      "contact.form.message": "Messaggio",
      "contact.form.submit": "Invia messaggio",

      "footer.about": "Siamo un movimento dedicato al sostegno delle famiglie e alla partecipazione civica. Trasparenza, solidarietà, responsabilità.",
      "footer.socials": "Social",
      "footer.links": "Link rapidi",
      "footer.contact": "Sede & Contatti"
    },
    en: {
      "nav.home": "Home",
      "nav.projects": "Projects",
      "nav.support": "Support us",
      "nav.join": "Join",
      "nav.contact": "Contact",
      "nav.signup": "Join",

      "cta.join": "Join",
      "cta.supportUs": "Support us",
      "cta.donateNow": "Donate now",
      "actions.viewProjects": "View all projects",

      "home.hero.title": "For families, for the future — A stronger country together",
      "home.hero.subtitle": "We support concrete policies for family, work and solidarity. Participate, join, donate: build a safer future for your loved ones with us.",
      "home.mission.title": "Our mission",
      "home.mission.text": "To promote policies that put families, dignified work and social cohesion first. Transparency, responsibility and civic participation guide every initiative.",
      "home.values.family.title": "Family support",
      "home.values.family.text": "Concrete measures for care, education and wellbeing of families.",
      "home.values.civic.title": "Civic participation",
      "home.values.civic.text": "We involve citizens in local and national decisions, promoting transparency and dialogue.",
      "home.values.work.title": "Economy and work",
      "home.values.work.text": "We support policies for employment, small businesses and stable jobs.",
      "home.featured.title": "Featured projects",
      "home.featured.text": "Local and national initiatives designed to improve families' daily life.",
      "home.featured.card1.title": "Family support center",
      "home.featured.card1.text": "Local services for childcare and support for families in need.",
      "home.featured.card2.title": "Youth work scholarships",
      "home.featured.card2.text": "Entry programs for young people and vocational training.",
      "home.featured.card3.title": "Volunteer network",
      "home.featured.card3.text": "National coordination of volunteers for social services and assistance.",
      "home.cta.title": "Support our work",
      "home.cta.text": "With your contribution we can expand services and reach more families. Every donation matters.",

      "projects.page.title": "Projects",
      "projects.page.intro": "List of ongoing initiatives and projects, divided by region and sector.",
      "projects.card1.title": "Family support center — NORTH-01",
      "projects.card1.text": "Pilot project for parenting support services.",
      "projects.card2.title": "Youth work scholarships — CENTER-02",
      "projects.card2.text": "Training and job placement initiatives.",

      "support.page.title": "Support us",
      "support.page.intro": "How to support our activities: one-time donations, recurring donations and volunteering.",
      "support.card1.title": "One-time donation",
      "support.card1.text": "Choose an amount and support a local project.",
      "support.card2.title": "Recurring donation",
      "support.card2.text": "Ongoing support for long-term projects.",
      "support.card2.cta": "Support monthly",
      "support.card3.title": "Volunteering",
      "support.card3.text": "Take part in local initiatives as a volunteer.",

      "join.page.title": "Join",
      "join.page.intro": "Become a member: fill in the form to receive information and take part in local activities.",
      "join.form.name": "Full name",
      "join.form.email": "Email",
      "join.form.region": "Region",
      "join.form.regionPlaceholder": "Select region",
      "join.form.submit": "Submit registration",

      "contact.page.title": "Contact",
      "contact.page.intro": "For information, collaborations or reports, contact us.",
      "contact.form.name": "Name",
      "contact.form.email": "Email",
      "contact.form.message": "Message",
      "contact.form.submit": "Send message",

      "footer.about": "We are a movement supporting families and civic participation. Transparency, solidarity, responsibility.",
      "footer.socials": "Social",
      "footer.links": "Quick links",
      "footer.contact": "Location & Contact"
    }
  };

  function applyTranslations(lang) {
    document.querySelectorAll("[data-i18n]").forEach(function (element) {
      const skipTranslation = element.getAttribute("data-i18n-skip");
      if (skipTranslation !== null && skipTranslation !== "false") {
        return;
      }

      const key = element.getAttribute("data-i18n");
      const text = translations[lang] && translations[lang][key];
      if (!text) {
        return;
      }

      const targetAttribute = element.getAttribute("data-i18n-attr");
      if (targetAttribute) {
        element.setAttribute(targetAttribute, text);
      } else {
        element.textContent = text;
      }
    });

    document.documentElement.lang = lang === "it" ? "it" : "en";
    localStorage.setItem("site_lang", lang);

    const itButton = document.getElementById("lang-it");
    const enButton = document.getElementById("lang-en");
    if (itButton && enButton) {
      if (lang === "it") {
        itButton.classList.add("font-semibold");
        enButton.classList.remove("font-semibold");
      } else {
        enButton.classList.add("font-semibold");
        itButton.classList.remove("font-semibold");
      }
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    const savedLanguage = localStorage.getItem("site_lang") || "it";
    applyTranslations(savedLanguage);

    const itButton = document.getElementById("lang-it");
    const enButton = document.getElementById("lang-en");

    if (itButton) {
      itButton.addEventListener("click", function () {
        applyTranslations("it");
      });
    }

    if (enButton) {
      enButton.addEventListener("click", function () {
        applyTranslations("en");
      });
    }
  });
})();
