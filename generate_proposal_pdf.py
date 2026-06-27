import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#555555"))
        if self._pageNumber > 1:
            self.drawString(54, 750, "Project Brief: RareSense.AI")
            self.setStrokeColor(colors.HexColor("#CCCCCC"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 40, page_text)
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.5)
        self.line(54, 52, 558, 52)
        self.restoreState()

def build_pdf(filename="RareSense_AI_Proposal.pdf"):
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('DocTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=colors.HexColor("#0D47A1"), spaceAfter=6)
    subtitle_style = ParagraphStyle('DocSubtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=15, textColor=colors.HexColor("#1565C0"), spaceAfter=15)
    h1_style = ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=colors.HexColor("#0D47A1"), spaceBefore=12, spaceAfter=6, keepWithNext=True)
    body_style = ParagraphStyle('Body', parent=styles['BodyText'], fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#212121"), spaceAfter=8)
    bullet_style = ParagraphStyle('Bullet', parent=body_style, leftIndent=15, firstLineIndent=-10, spaceAfter=4)
    th_style = ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=colors.white, alignment=1)
    td_style = ParagraphStyle('TD', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11, textColor=colors.HexColor("#212121"))
    td_bold = ParagraphStyle('TDB', parent=td_style, fontName='Helvetica-Bold', textColor=colors.HexColor("#0D47A1"))

    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=72)
    story = []

    # ── Title ──
    story.append(Spacer(1, 10))
    story.append(Paragraph("PROJECT PROPOSAL", title_style))
    story.append(Paragraph("RareSense.AI — LLM-Powered Rare Disease Detection from Unstructured Clinical Notes", subtitle_style))

    # ── Metadata ──
    meta = [
        [Paragraph("<b>Supervisor:</b> Raj Kumar Sir", body_style), Paragraph("<b>Syllabus Equivalent:</b> Project #7 (CareerPulse)", body_style)],
        [Paragraph("<b>Domain:</b> Health Data Science (HDS)", body_style), Paragraph("<b>Date:</b> June 2026", body_style)]
    ]
    mt = Table(meta, colWidths=[252, 252])
    mt.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4), ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('LINEBELOW', (0,1), (1,1), 1, colors.HexColor("#0D47A1")),
    ]))
    story.append(mt)
    story.append(Spacer(1, 12))

    # ── 1. Problem Statement ──
    story.append(Paragraph("1. Problem Statement", h1_style))
    story.append(Paragraph(
        "Rare diseases affect over <b>300 million people worldwide</b>, yet the average rare disease takes "
        "<b>7.6 years to diagnose</b>. Patients visit an average of 7 specialists before receiving a correct diagnosis. "
        "The core issue is that symptoms are scattered across years of fragmented clinical notes written by different "
        "doctors, and no single physician sees the complete picture. Traditional keyword-based search systems fail because "
        "doctors use varied terminology (e.g., 'NIDDM' vs 'Type 2 Diabetes' vs 'non-insulin dependent diabetes').",
        body_style
    ))

    # ── 2. Proposed Solution ──
    story.append(Paragraph("2. Proposed Solution: RareSense.AI", h1_style))
    story.append(Paragraph(
        "<b>RareSense.AI</b> is an intelligent diagnostic support system that reads unstructured clinical notes, "
        "extracts medical entities (symptoms, diagnoses, medications, lab values) using Clinical NLP, builds a "
        "patient health timeline, and cross-references it against rare disease databases (OMIM / Orphanet) to flag "
        "potential undiagnosed rare conditions that may have been missed.",
        body_style
    ))

    # ── 3. Architecture ──
    story.append(Paragraph("3. System Architecture", h1_style))
    story.append(Paragraph("<bullet>&bull;</bullet><b>Data Source</b>: MIMIC-IV — a publicly available dataset of real ICU patient records from Beth Israel Deaconess Medical Center (a Harvard-affiliated teaching hospital). Contains 40,000+ patient stays with clinical notes, lab results, medications, and ICD codes.", bullet_style))
    story.append(Paragraph("<bullet>&bull;</bullet><b>Clinical NLP Engine</b>: Uses pre-trained BioBERT and medSpaCy for Named Entity Recognition (NER) to extract symptoms, diagnoses, medications, and lab findings from free-text doctor notes.", bullet_style))
    story.append(Paragraph("<bullet>&bull;</bullet><b>Patient Timeline Builder</b>: Constructs a chronological health timeline per patient in MongoDB, linking extracted entities across multiple clinical encounters over time.", bullet_style))
    story.append(Paragraph("<bullet>&bull;</bullet><b>Rare Disease Matching Engine</b>: Generates phenotype embeddings from the patient timeline using MongoDB Vector Search and calculates semantic similarity against rare disease symptom profiles from the Orphanet and OMIM databases.", bullet_style))
    story.append(Paragraph("<bullet>&bull;</bullet><b>Clinician Dashboard</b>: A React.js interface displaying flagged rare disease candidates with confidence scores, matched symptom evidence, and a visual patient health timeline.", bullet_style))

    # ── 4. Technical Equivalence ──
    story.append(Spacer(1, 8))
    story.append(Paragraph("4. Technical Equivalence to CareerPulse (Project #7)", h1_style))
    story.append(Paragraph(
        "The <b>database schema, algorithmic complexity, and coding deliverables remain 100% equivalent</b> "
        "to the originally assigned CareerPulse project:",
        body_style
    ))

    table_data = [
        [Paragraph("Core Module", th_style), Paragraph("Original: CareerPulse", th_style), Paragraph("Proposed: RareSense.AI", th_style)],
        [Paragraph("Data Ingestion", td_bold),
         Paragraph("Ingests user resumes/portfolios with flexible schemas for varying skills and experiences.", td_style),
         Paragraph("Ingests clinical notes from MIMIC-IV with flexible schemas for varying medical specialties and record formats.", td_style)],
        [Paragraph("Search & Matching", td_bold),
         Paragraph("Recommends job vacancies by matching candidate skill profiles against job criteria.", td_style),
         Paragraph("Matches patient symptom profiles against rare disease criteria using MongoDB Vector Search and clinical embeddings (BioBERT).", td_style)],
        [Paragraph("Activity Tracking", td_bold),
         Paragraph("Tracks course completions, application stages, and user activity over time.", td_style),
         Paragraph("Tracks patient symptoms, medications, and lab results chronologically to build a health timeline.", td_style)],
        [Paragraph("Analytics Dashboard", td_bold),
         Paragraph("Visualizes hiring trends, salary data, and skill progression graphs.", td_style),
         Paragraph("Visualizes rare disease match scores, symptom evidence, and patient health timelines.", td_style)]
    ]

    t = Table(table_data, colWidths=[100, 202, 202])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0D47A1")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'), ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6), ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F5F5F5")]),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # ── 5. Significance ──
    story.append(Paragraph("5. Health Data Science Significance", h1_style))
    story.append(Paragraph(
        "Rare disease diagnostics represents one of the most critical unmet needs in modern clinical informatics. "
        "By applying clinical NLP and semantic vector matching to real-world EHR data, this project demonstrates "
        "advanced health data engineering capabilities and addresses a problem that directly impacts patient lives. "
        "The use of MIMIC-IV (a publicly available clinical dataset from a leading academic medical center) ensures "
        "reproducibility and academic rigor.",
        body_style
    ))

    # ── 6. Tech Stack ──
    story.append(Paragraph("6. Technology Stack", h1_style))
    story.append(Paragraph("<bullet>&bull;</bullet><b>Database</b>: MongoDB (Document Store + Vector Search + Time-Series)", bullet_style))
    story.append(Paragraph("<bullet>&bull;</bullet><b>NLP</b>: BioBERT, medSpaCy, scispaCy (pre-trained clinical models)", bullet_style))
    story.append(Paragraph("<bullet>&bull;</bullet><b>Backend</b>: Python (FastAPI)", bullet_style))
    story.append(Paragraph("<bullet>&bull;</bullet><b>Frontend</b>: React.js", bullet_style))
    story.append(Paragraph("<bullet>&bull;</bullet><b>Data</b>: MIMIC-IV, Orphanet API, OMIM", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] {filename} successfully generated.")

if __name__ == "__main__":
    build_pdf()
