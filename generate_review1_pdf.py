from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#888888"))
            self.drawRightString(558, 30, f"Page {self._pageNumber} of {num_pages}")
            self.drawString(54, 30, "RareSense.AI — Review 1")
            self.setStrokeColor(colors.HexColor("#CCCCCC"))
            self.setLineWidth(0.5)
            self.line(54, 40, 558, 40)
            super().showPage()
        super().save()

def build():
    styles = getSampleStyleSheet()
    title = ParagraphStyle('T', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=colors.HexColor("#0D47A1"), spaceAfter=4)
    subtitle = ParagraphStyle('ST', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=14, textColor=colors.HexColor("#1565C0"), spaceAfter=12)
    h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=14, leading=17, textColor=colors.HexColor("#0D47A1"), spaceBefore=14, spaceAfter=6, keepWithNext=True)
    h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=colors.HexColor("#1565C0"), spaceBefore=10, spaceAfter=4, keepWithNext=True)
    body = ParagraphStyle('B', parent=styles['BodyText'], fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#212121"), spaceAfter=6)
    bullet = ParagraphStyle('BL', parent=body, leftIndent=15, firstLineIndent=-10, spaceAfter=3)
    th = ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=colors.white, alignment=1)
    td = ParagraphStyle('TD', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor("#212121"))
    td_bold = ParagraphStyle('TDB', parent=td, fontName='Helvetica-Bold', textColor=colors.HexColor("#0D47A1"))
    note_style = ParagraphStyle('NOTE', parent=body, fontName='Helvetica-Oblique', fontSize=9, leading=12, textColor=colors.HexColor("#616161"), leftIndent=10, rightIndent=10, spaceBefore=4, spaceAfter=4)
    case_note = ParagraphStyle('CASE', parent=body, fontName='Courier', fontSize=9, leading=13, textColor=colors.HexColor("#333333"), leftIndent=10, rightIndent=10, backColor=colors.HexColor("#F5F5F5"), borderPadding=6, spaceBefore=4, spaceAfter=4)

    doc = SimpleDocTemplate("RareSense_AI_Review1.pdf", pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=60)
    s = []

    # ── Title ──
    s.append(Spacer(1, 8))
    s.append(Paragraph("RareSense.AI", title))
    s.append(Paragraph("LLM-Powered Rare Disease Detection from Unstructured Clinical Notes", subtitle))
    s.append(Paragraph("<b>Review 1 — Project Overview, Data Sources & Case Study</b>", ParagraphStyle('rev', parent=body, fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor("#E65100"))))

    meta = [
        [Paragraph("<b>Supervisor:</b> Raj Kumar Sir", body), Paragraph("<b>Date:</b> June 2026", body)],
        [Paragraph("<b>Domain:</b> Health Data Science", body), Paragraph("<b>Syllabus Ref:</b> Project #7 (CareerPulse)", body)]
    ]
    mt = Table(meta, colWidths=[252, 252])
    mt.setStyle(TableStyle([
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('BOTTOMPADDING',(0,0),(-1,-1),3), ('TOPPADDING',(0,0),(-1,-1),3),
        ('LEFTPADDING',(0,0),(-1,-1),0),
        ('LINEBELOW',(0,1),(1,1),1,colors.HexColor("#0D47A1")),
    ]))
    s.append(mt)
    s.append(Spacer(1, 10))

    # ── 1. Problem ──
    s.append(Paragraph("1. Problem Statement", h1))
    s.append(Paragraph(
        "Rare diseases affect over <b>300 million people worldwide</b>. Despite this, the average rare disease "
        "takes <b>7.6 years</b> to diagnose. Patients visit an average of <b>7 specialists</b> before receiving a correct diagnosis. "
        "The root cause: symptoms are scattered across years of clinical notes from different doctors, "
        "and no single physician sees the complete picture. Traditional keyword search fails because doctors use "
        "varied medical terminology for the same condition.", body))

    # ── 2. Solution ──
    s.append(Paragraph("2. Our Solution: RareSense.AI", h1))
    s.append(Paragraph(
        "An AI system that <b>reads all of a patient's clinical notes</b>, extracts symptoms/diagnoses/medications "
        "using Clinical NLP, builds a unified patient timeline, and <b>cross-references the full symptom picture "
        "against 7,000+ rare diseases</b> to flag potential undiagnosed conditions.", body))

    # Architecture flow
    flow_data = [
        [Paragraph("<b>Step</b>", th), Paragraph("<b>Process</b>", th), Paragraph("<b>Technology</b>", th)],
        [Paragraph("1", td_bold), Paragraph("Ingest raw doctor's notes (discharge summaries, progress notes)", td), Paragraph("MIMIC-IV dataset", td)],
        [Paragraph("2", td_bold), Paragraph("Extract symptoms, diagnoses, medications, lab values from free text", td), Paragraph("BioBERT + medSpaCy (NER)", td)],
        [Paragraph("3", td_bold), Paragraph("Build chronological patient health timeline", td), Paragraph("MongoDB Document Store", td)],
        [Paragraph("4", td_bold), Paragraph("Generate patient phenotype embeddings", td), Paragraph("MongoDB Vector Search", td)],
        [Paragraph("5", td_bold), Paragraph("Match against rare disease symptom profiles", td), Paragraph("Orphanet + HPO database", td)],
        [Paragraph("6", td_bold), Paragraph("Display flagged diseases with confidence scores on dashboard", td), Paragraph("React.js Frontend", td)],
    ]
    ft = Table(flow_data, colWidths=[35, 295, 174])
    ft.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#0D47A1")),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor("#CCCCCC")),
        ('BOTTOMPADDING',(0,0),(-1,-1),5), ('TOPPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),5), ('RIGHTPADDING',(0,0),(-1,-1),5),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor("#F5F5F5")]),
    ]))
    s.append(ft)
    s.append(Spacer(1, 8))

    # ── 3. Data Sources ──
    s.append(Paragraph("3. Data Sources", h1))

    s.append(Paragraph("3.1  Patient Data — MIMIC-IV", h2))
    s.append(Paragraph(
        "MIMIC-IV is a <b>free, publicly available</b> dataset of real ICU patient records from "
        "<b>Beth Israel Deaconess Medical Center</b> (a Harvard-affiliated teaching hospital). "
        "Access requires completion of a CITI ethics course (~2-3 hours).", body))

    mimic_data = [
        [Paragraph("<b>Table</b>", th), Paragraph("<b>Contents</b>", th), Paragraph("<b>Usage in Our Project</b>", th)],
        [Paragraph("discharge.csv", td_bold), Paragraph("Free-text discharge summaries written by doctors", td), Paragraph("PRIMARY INPUT — AI reads these notes to extract symptoms", td)],
        [Paragraph("diagnoses_icd.csv", td_bold), Paragraph("ICD-10 diagnosis codes per patient admission", td), Paragraph("Ground truth for validating our AI's predictions", td)],
        [Paragraph("prescriptions.csv", td_bold), Paragraph("All medications prescribed", td), Paragraph("Patient timeline + potential drug interaction flags", td)],
        [Paragraph("labevents.csv", td_bold), Paragraph("Lab test results (blood counts, glucose, etc.)", td), Paragraph("Abnormal labs are symptoms too (e.g., low platelets)", td)],
        [Paragraph("patients.csv", td_bold), Paragraph("Age, gender, demographics", td), Paragraph("Patient profile construction", td)],
    ]
    mimic_t = Table(mimic_data, colWidths=[120, 195, 189])
    mimic_t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#1B5E20")),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor("#CCCCCC")),
        ('BOTTOMPADDING',(0,0),(-1,-1),5), ('TOPPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),5), ('RIGHTPADDING',(0,0),(-1,-1),5),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor("#F5F5F5")]),
    ]))
    s.append(mimic_t)
    s.append(Spacer(1, 8))

    s.append(Paragraph("3.2  Rare Disease Database — Orphanet + HPO", h2))
    rare_data = [
        [Paragraph("<b>Database</b>", th), Paragraph("<b>What It Contains</b>", th), Paragraph("<b>Usage</b>", th)],
        [Paragraph("Orphanet (en_product4.xml)", td_bold), Paragraph("7,000+ rare diseases with associated symptom lists and prevalence", td), Paragraph("The 'answer key' — maps diseases to symptoms", td)],
        [Paragraph("HPO (phenotype.hpoa)", td_bold), Paragraph("Standardized symptom-to-disease mappings (e.g., HP:0000958 = butterfly rash)", td), Paragraph("Bridges free-text symptoms to disease codes", td)],
        [Paragraph("HPO Ontology (hp.obo)", td_bold), Paragraph("Hierarchy of all medical symptom terms", td), Paragraph("Standardizes AI-extracted symptoms into codes", td)],
    ]
    rare_t = Table(rare_data, colWidths=[145, 195, 164])
    rare_t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#B71C1C")),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor("#CCCCCC")),
        ('BOTTOMPADDING',(0,0),(-1,-1),5), ('TOPPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),5), ('RIGHTPADDING',(0,0),(-1,-1),5),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor("#FFF3E0")]),
    ]))
    s.append(rare_t)
    s.append(Spacer(1, 8))

    s.append(Paragraph("3.3  Pre-Trained AI Models (No Training Required)", h2))
    s.append(Paragraph("<bullet>&bull;</bullet><b>BioBERT</b> (dmis-lab/biobert-v1.1) — Pre-trained on PubMed biomedical literature. Understands medical language.", bullet))
    s.append(Paragraph("<bullet>&bull;</bullet><b>medSpaCy</b> — Clinical NLP pipeline for extracting symptoms, medications, and diagnoses from doctor's notes.", bullet))
    s.append(Paragraph("<bullet>&bull;</bullet><b>scispaCy</b> — Scientific entity recognition and medical concept linking.", bullet))

    # ── 4. Case Study ──
    s.append(Paragraph("4. Case Study: How RareSense.AI Detects Lupus", h1))
    s.append(Paragraph(
        "Below is a walkthrough of how the system would process a real-world scenario where a patient visits "
        "multiple doctors over 3 years, and no single doctor catches the underlying rare disease.", body))

    s.append(Paragraph("4.1  Raw Clinical Notes (Input)", h2))
    s.append(Paragraph(
        "<b>Visit 1 — Dermatologist (Jan 2023):</b><br/>"
        "\"28F presents with erythematous malar rash across both cheeks. Reports photosensitivity. "
        "Prescribed topical hydrocortisone. Follow-up in 4 weeks.\"", case_note))
    s.append(Paragraph(
        "<b>Visit 2 — Hematologist (Aug 2023):</b><br/>"
        "\"Patient referred for thrombocytopenia. Platelet count 89,000/uL (normal: 150,000-400,000). "
        "CBC otherwise unremarkable. Monitor and repeat labs in 3 months.\"", case_note))
    s.append(Paragraph(
        "<b>Visit 3 — Nephrologist (Mar 2024):</b><br/>"
        "\"Urinalysis shows proteinuria (2+). eGFR mildly reduced at 72. No prior renal history. "
        "Started ACE inhibitor. Renal biopsy considered if worsening.\"", case_note))
    s.append(Paragraph(
        "<b>Visit 4 — Primary Care (Nov 2024):</b><br/>"
        "\"Patient reports persistent fatigue, arthralgia in bilateral hands and knees. "
        "Attributes to work stress. OTC ibuprofen recommended.\"", case_note))

    s.append(Paragraph(Paragraph("No single doctor above suspected a systemic condition. Each treated their own finding in isolation.", note_style).text, note_style))

    s.append(Paragraph("4.2  AI-Extracted Entities (NLP Output)", h2))
    extract_data = [
        [Paragraph("<b>Visit</b>", th), Paragraph("<b>Extracted Symptoms</b>", th), Paragraph("<b>HPO Code</b>", th)],
        [Paragraph("Visit 1", td_bold), Paragraph("Malar rash (butterfly rash)", td), Paragraph("HP:0025300", td)],
        [Paragraph("Visit 1", td_bold), Paragraph("Photosensitivity", td), Paragraph("HP:0000992", td)],
        [Paragraph("Visit 2", td_bold), Paragraph("Thrombocytopenia (low platelets)", td), Paragraph("HP:0001873", td)],
        [Paragraph("Visit 3", td_bold), Paragraph("Proteinuria (protein in urine)", td), Paragraph("HP:0000790", td)],
        [Paragraph("Visit 3", td_bold), Paragraph("Reduced renal function", td), Paragraph("HP:0012622", td)],
        [Paragraph("Visit 4", td_bold), Paragraph("Chronic fatigue", td), Paragraph("HP:0012432", td)],
        [Paragraph("Visit 4", td_bold), Paragraph("Arthralgia (joint pain)", td), Paragraph("HP:0002829", td)],
    ]
    et = Table(extract_data, colWidths=[60, 260, 184])
    et.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#4A148C")),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor("#CCCCCC")),
        ('BOTTOMPADDING',(0,0),(-1,-1),4), ('TOPPADDING',(0,0),(-1,-1),4),
        ('LEFTPADDING',(0,0),(-1,-1),5), ('RIGHTPADDING',(0,0),(-1,-1),5),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor("#F3E5F5")]),
    ]))
    s.append(et)
    s.append(Spacer(1, 8))

    s.append(Paragraph("4.3  Rare Disease Match (Output)", h2))
    s.append(Paragraph(
        "The system cross-references the 7 extracted phenotypes against the Orphanet/HPO database and returns:", body))

    match_data = [
        [Paragraph("<b>Rank</b>", th), Paragraph("<b>Disease</b>", th), Paragraph("<b>Matched Symptoms</b>", th), Paragraph("<b>Confidence</b>", th)],
        [Paragraph("1", td_bold),
         Paragraph("<b>Systemic Lupus Erythematosus (SLE)</b><br/>ORPHA:536", td),
         Paragraph("Malar rash + Photosensitivity + Thrombocytopenia + Proteinuria + Fatigue + Arthralgia<br/><b>6 / 7 symptoms match</b>", td),
         Paragraph("<b>87%</b>", ParagraphStyle('conf', parent=td, fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor("#1B5E20"), alignment=1))],
        [Paragraph("2", td_bold),
         Paragraph("Antiphospholipid Syndrome<br/>ORPHA:464", td),
         Paragraph("Thrombocytopenia + Proteinuria + Fatigue<br/>3 / 7 symptoms match", td),
         Paragraph("41%", ParagraphStyle('conf2', parent=td, fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor("#E65100"), alignment=1))],
        [Paragraph("3", td_bold),
         Paragraph("Mixed Connective Tissue Disease<br/>ORPHA:809", td),
         Paragraph("Arthralgia + Fatigue + Malar rash<br/>3 / 7 symptoms match", td),
         Paragraph("38%", ParagraphStyle('conf3', parent=td, fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor("#E65100"), alignment=1))],
    ]
    match_t = Table(match_data, colWidths=[40, 150, 230, 84])
    match_t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#B71C1C")),
        ('BACKGROUND',(0,1),(-1,1),colors.HexColor("#E8F5E9")),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor("#CCCCCC")),
        ('BOTTOMPADDING',(0,0),(-1,-1),6), ('TOPPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),5), ('RIGHTPADDING',(0,0),(-1,-1),5),
        ('ROWBACKGROUNDS',(0,2),(-1,-1),[colors.white, colors.HexColor("#FFF3E0")]),
    ]))
    s.append(match_t)
    s.append(Spacer(1, 8))

    s.append(Paragraph(
        "<b>Result:</b> RareSense.AI flags <b>Systemic Lupus Erythematosus (SLE)</b> with 87% confidence. "
        "A condition that would have taken years to diagnose through traditional clinical pathways is "
        "identified in <b>seconds</b> by connecting symptoms from 4 different doctors over 2 years.", body))

    # ── 5. Tech Stack ──
    s.append(Paragraph("5. Technology Stack Summary", h1))
    s.append(Paragraph("<bullet>&bull;</bullet><b>Database:</b> MongoDB (Document Store + Vector Search Index)", bullet))
    s.append(Paragraph("<bullet>&bull;</bullet><b>NLP Engine:</b> BioBERT + medSpaCy + scispaCy", bullet))
    s.append(Paragraph("<bullet>&bull;</bullet><b>Backend:</b> Python (FastAPI)", bullet))
    s.append(Paragraph("<bullet>&bull;</bullet><b>Frontend:</b> React.js (Clinician Dashboard)", bullet))
    s.append(Paragraph("<bullet>&bull;</bullet><b>Patient Data:</b> MIMIC-IV (40,000+ real ICU records)", bullet))
    s.append(Paragraph("<bullet>&bull;</bullet><b>Disease Data:</b> Orphanet (7,000+ rare diseases) + HPO", bullet))

    # ── 6. Next Steps ──
    s.append(Paragraph("6. Next Steps (Post Review 1)", h1))
    s.append(Paragraph("<bullet>&bull;</bullet>Complete MIMIC-IV data access (CITI course + PhysioNet registration)", bullet))
    s.append(Paragraph("<bullet>&bull;</bullet>Download and parse Orphanet XML + HPO annotations", bullet))
    s.append(Paragraph("<bullet>&bull;</bullet>Set up NLP pipeline (medSpaCy + BioBERT) on sample discharge notes", bullet))
    s.append(Paragraph("<bullet>&bull;</bullet>Design MongoDB schema for patient timelines", bullet))
    s.append(Paragraph("<bullet>&bull;</bullet>Build initial matching prototype against top 200 rare diseases", bullet))

    doc.build(s, canvasmaker=NumberedCanvas)
    print("[OK] RareSense_AI_Review1.pdf generated successfully.")

if __name__ == "__main__":
    build()
