from docx import Document
from docx.shared import Pt, Cm
import os

OUTPUT_DIR = "/home/user/ProofOfConcept/rapoarte_1_4"

def set_margins(doc):
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(2.5)

def create_doc(filename, role_title, name, p1, p2, p3):
    doc = Document()
    set_margins(doc)

    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(12)

    # Title
    title = doc.add_paragraph()
    run = title.add_run(f"{role_title} – {name}")
    run.bold = True
    run.font.size = Pt(12)
    title.paragraph_format.space_after = Pt(10)

    # P1
    p = doc.add_paragraph()
    r1 = p.add_run("P1: ")
    r1.bold = True
    r1.font.size = Pt(12)
    r2 = p.add_run(p1)
    r2.font.size = Pt(12)
    p.paragraph_format.space_after = Pt(6)

    # P2
    p = doc.add_paragraph()
    r1 = p.add_run("P2: ")
    r1.bold = True
    r1.font.size = Pt(12)
    r2 = p.add_run(p2)
    r2.font.size = Pt(12)
    p.paragraph_format.space_after = Pt(6)

    # P3
    p = doc.add_paragraph()
    r1 = p.add_run("P3: ")
    r1.bold = True
    r1.font.size = Pt(12)
    r2 = p.add_run(p3)
    r2.font.size = Pt(12)
    p.paragraph_format.space_after = Pt(6)

    path = os.path.join(OUTPUT_DIR, filename)
    doc.save(path)
    print(f"  Salvat: {filename}")


# ─── 1. CERCETĂTOR — Alex Bere ────────────────────────────────────────────────
create_doc(
    filename="Cercetator_1_4_Alex_Bere.docx",
    role_title="Cercetător în informatică / Supervizor / Head of R&D",
    name="Alex Bere",
    p1=(
        "Definirea cadrului metodologic de evaluare a performanței sistemului integrat și stabilirea "
        "indicatorilor per subsistem. Inițierea cercetării soluțiilor de încărcare solară: necesar "
        "energetic, variabile meteorologice și criterii de dimensionare. Supervizarea distribuirii "
        "sarcinilor de evaluare între membrii echipei."
    ),
    p2=(
        "Supervizarea evaluării componentei AI pentru detecția panourilor și a anomaliilor termice, "
        "inclusiv validarea metricilor de acuratețe. Coordonarea analizei energetice a platformelor "
        "mobile în condiții meteorologice variate și integrarea rezultatelor într-un model unitar."
    ),
    p3=(
        "Coordonarea sintezei transversale a performanței sistemului și formularea ajustărilor "
        "recomandate la nivelul algoritmilor AI și al specificațiilor de echipamente. Validarea "
        "raportului tehnic al subactivității 1.4 și a direcțiilor de continuare."
    )
)

# ─── 2. EXPERT BACK-END — Gangoș George ──────────────────────────────────────
create_doc(
    filename="Expert_BackEnd_1_4_Gangos_George.docx",
    role_title="Expert în Back-End Development",
    name="Gangoș George",
    p1=(
        "Definirea indicatorilor de performanță pentru platforma software: timpi de răspuns API, "
        "debit de interogări și comportamentul fondului de conexiuni. Analiza interogărilor cu risc "
        "de degradare, pornind de la arhitectura documentată în subactivitatea 1.3."
    ),
    p2=(
        "Evaluarea performanței platformei în condiții de sarcină realistă și identificarea "
        "pârghiilor de optimizare: absența cache-ului și a compresiei HTTP. Analiza metricilor "
        "componentei AI integrate în fluxul backend: latența inferenței și debitul de procesare."
    ),
    p3=(
        "Documentarea recomandărilor de optimizare a platformei software și contribuție la "
        "ajustările specificațiilor de echipamente privind infrastructura server pentru execuția "
        "accelerată a modelelor AI — CPU față de GPU cu TensorRT."
    )
)

# ─── 3. EXPERT DRONE & AR — Pavel Rosca ──────────────────────────────────────
create_doc(
    filename="Expert_Drone_AR_1_4_Pavel_Rosca.docx",
    role_title="Expert în drone și realitate augmentată",
    name="Pavel Rosca",
    p1=(
        "Cercetarea soluțiilor de încărcare autonomă solară pentru platforma aeriană: specificații "
        "tehnice ale stațiilor de andocare comerciale compatibile cu DJI Matrice, necesar energetic "
        "al dronei și timpi de reîncărcare în funcție de condițiile meteo."
    ),
    p2=(
        "Evaluarea autonomiei de zbor în condiții meteorologice variate: impactul vântului și al "
        "temperaturilor scăzute. Analiza performanței fluxurilor de comunicare — telemetrie MQTT, "
        "latența comenzilor, video WebRTC — și documentarea scenariilor de încărcare solară aplicabile."
    ),
    p3=(
        "Documentarea fezabilității soluțiilor de andocare solară pe un parc de 1 MW și contribuție "
        "la ajustările specificațiilor: numărul optim de stații de andocare și validarea bilanțului "
        "energetic din raportul 1.4."
    )
)

# ─── 4. EXPERT DB & BIG DATA — Alexandru Indries ─────────────────────────────
create_doc(
    filename="Expert_Db_Big_Data_1_4_Alexandru_Indries.docx",
    role_title="Expert în big data și baze de date",
    name="Alexandru Indries",
    p1=(
        "Proiectarea cadrului de colectare a datelor de performanță: metrici de telemetrie, "
        "indicatori AI și consum energetic al platformelor mobile. Analiza volumelor de date "
        "generate în operare continuă și a cerințelor de stocare pentru un parc de 1 MW."
    ),
    p2=(
        "Implementarea mecanismelor de colectare și agregare a metricilor de performanță și "
        "evaluarea consistenței datelor de telemetrie. Analiza modelelor de date: eficiența "
        "indexurilor, interogările cu cost ridicat și comportamentul fondului de conexiuni."
    ),
    p3=(
        "Validarea consistenței datelor de consum energetic și generarea analizei de performanță "
        "pe baza metricilor colectate. Contribuție la bilanțul energetic al scenariilor de încărcare "
        "solară prin structurarea datelor de referință privind producția parcurilor fotovoltaice."
    )
)

# ─── 5. EXPERT SECURITATE CIBERNETICĂ — Vlad Botis ───────────────────────────
create_doc(
    filename="Expert_Securitate_Cibernetica_1_4_Vlad_Botis.docx",
    role_title="Expert în securitate cibernetică",
    name="Vlad Botis",
    p1=(
        "Evaluarea overhead-ului mecanismelor de securitate din subactivitatea 1.3 asupra "
        "performanței sistemului: cost computațional JWT, argon2id, bcrypt și interogările de "
        "autentificare per cerere. Documentarea relației dintre securitate și bugetul de "
        "performanță per subsistem."
    ),
    p2=(
        "Benchmarking-ul overhead-ului de securitate: impactul middleware-ului de autentificare, "
        "al validării datelor de intrare și al logging-ului structurat. Estimarea overhead-ului "
        "activării TLS pe canalele necriptate identificate în 1.3 și a impactului asupra latenței."
    ),
    p3=(
        "Documentarea compromisurilor acceptabile dintre securitate și performanță per subsistem. "
        "Contribuție la ajustările specificațiilor de echipamente din perspectiva securității și "
        "validarea secțiunilor din raportul 1.4 privind relația performanță–securitate."
    )
)

print("\nToate fișierele au fost generate cu succes.")
