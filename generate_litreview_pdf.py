from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
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
            self.drawString(54, 30, "RareSense.AI — Literature Review")
            self.setStrokeColor(colors.HexColor("#CCCCCC"))
            self.setLineWidth(0.5)
            self.line(54, 40, 558, 40)
            super().showPage()
        super().save()

def build():
    styles = getSampleStyleSheet()
    title = ParagraphStyle('T', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=colors.HexColor("#0D47A1"), spaceAfter=4, alignment=1)
    subtitle = ParagraphStyle('ST', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=14, textColor=colors.HexColor("#1565C0"), spaceAfter=4, alignment=1)
    h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=colors.HexColor("#0D47A1"), spaceBefore=14, spaceAfter=6, keepWithNext=True)
    h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=colors.HexColor("#1565C0"), spaceBefore=10, spaceAfter=4, keepWithNext=True)
    body = ParagraphStyle('B', parent=styles['BodyText'], fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=colors.HexColor("#212121"), spaceAfter=6)
    cite = ParagraphStyle('CITE', parent=body, fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor("#424242"), leftIndent=20, firstLineIndent=-20, spaceAfter=3)
    th = ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.white, alignment=1)
    td = ParagraphStyle('TD', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11, textColor=colors.HexColor("#212121"))
    td_bold = ParagraphStyle('TDB', parent=td, fontName='Helvetica-Bold', textColor=colors.HexColor("#0D47A1"))

    doc = SimpleDocTemplate("RareSense_AI_LiteratureReview.pdf", pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=60)
    s = []

    # ── Title Page ──
    s.append(Spacer(1, 120))
    s.append(Paragraph("LITERATURE REVIEW", title))
    s.append(Spacer(1, 8))
    s.append(Paragraph("RareSense.AI: LLM-Powered Rare Disease Detection<br/>from Unstructured Clinical Notes", subtitle))
    s.append(Spacer(1, 20))
    s.append(Paragraph("Domain: Health Data Science &amp; Clinical Informatics", ParagraphStyle('meta', parent=body, alignment=1, fontSize=10)))
    s.append(Paragraph("Date: June 2026", ParagraphStyle('meta2', parent=body, alignment=1, fontSize=10)))
    s.append(PageBreak())

    # ── Abstract ──
    s.append(Paragraph("Abstract", h1))
    s.append(Paragraph(
        "Rare diseases collectively affect over 300 million individuals worldwide, yet the average time to diagnosis "
        "remains between 4.7 and 7.6 years across regions — a period often termed the <i>diagnostic odyssey</i>. "
        "This literature review surveys the current landscape of computational approaches to rare disease diagnosis, "
        "covering four key areas: (1) the clinical burden of diagnostic delay, (2) advances in clinical Natural Language "
        "Processing (NLP) for Electronic Health Record (EHR) phenotyping, (3) rare disease knowledge bases and phenotype "
        "matching algorithms, and (4) emerging frameworks that integrate large language models with ontological grounding. "
        "The review identifies a critical gap: while individual components (NLP extraction, ontology matching, EHR analysis) "
        "have matured significantly, few systems integrate these into an end-to-end pipeline for rare disease detection "
        "from unstructured clinical text. RareSense.AI is proposed to address this gap.", body))
    s.append(Spacer(1, 4))

    # ── 1. Introduction ──
    s.append(Paragraph("1. Introduction", h1))
    s.append(Paragraph(
        "Rare diseases are defined as conditions affecting fewer than 200,000 individuals in the United States or fewer "
        "than 1 in 2,000 people in Europe. Despite their individual rarity, there are over 7,000 recognized rare diseases, "
        "collectively affecting approximately 3.5–5.9% of the global population (Nguengang Wakap et al., 2020). The "
        "paradox of rare diseases lies in their collective prevalence: while each condition is uncommon, the aggregate "
        "patient population is enormous.", body))
    s.append(Paragraph(
        "The diagnostic journey for rare disease patients is characterized by significant delays. A 2024 Rare Barometer "
        "survey by EURORDIS reported an average diagnostic delay of 4.7 years in Europe, while US-based studies estimate "
        "5 to 7.6 years (EURORDIS, 2024; NORD, 2023). During this period, patients consult an average of 7.3 physicians "
        "and receive 2–3 misdiagnoses before the correct condition is identified (Global Commission on Rare Diseases, 2024). "
        "This diagnostic odyssey imposes substantial clinical, emotional, and financial burdens on patients and healthcare systems.", body))
    s.append(Paragraph(
        "The fundamental challenge is one of <b>information fragmentation</b>. Symptoms of rare diseases often span multiple "
        "organ systems and manifest across different clinical encounters over extended periods. Each specialist documents "
        "their observations independently in unstructured clinical notes, but no single physician — or system — synthesizes "
        "the complete phenotypic picture. This review examines the technological landscape that makes an automated, "
        "NLP-driven approach to rare disease detection both feasible and urgently needed.", body))

    # ── 2. Clinical NLP for EHR Phenotyping ──
    s.append(Paragraph("2. Clinical NLP for EHR Phenotyping", h1))

    s.append(Paragraph("2.1 Evolution of Biomedical Language Models", h2))
    s.append(Paragraph(
        "The application of NLP to clinical text has undergone rapid evolution. Early approaches relied on rule-based "
        "systems such as cTAKES (Savova et al., 2010) and MetaMap (Aronson & Lang, 2010) for concept extraction from "
        "clinical narratives. While effective for structured extraction tasks, these systems struggled with the ambiguity, "
        "abbreviations, and negation patterns inherent in physician-authored text.", body))
    s.append(Paragraph(
        "The introduction of transformer-based language models marked a paradigm shift. <b>BioBERT</b> (Lee et al., 2020), "
        "pre-trained on PubMed abstracts and PMC full-text articles, demonstrated substantial improvements over general-domain "
        "BERT on biomedical NER, relation extraction, and question answering tasks. <b>ClinicalBERT</b> (Huang et al., 2019) "
        "and <b>BioClinicalBERT</b> extended this by pre-training on MIMIC-III clinical notes, achieving superior performance "
        "on clinical outcome prediction and de-identification tasks.", body))
    s.append(Paragraph(
        "More recently, domain-specific models such as <b>PhenoBCBERT</b> and <b>PhenoGPT</b> (2024) have been developed "
        "specifically for phenotype recognition in clinical narratives, demonstrating that task-specific pre-training yields "
        "measurable improvements in extracting Human Phenotype Ontology (HPO) terms from free text (Yang et al., 2024).", body))

    s.append(Paragraph("2.2 Clinical NLP Tools and Pipelines", h2))
    s.append(Paragraph(
        "Several open-source tools have been developed to operationalize clinical NLP for research:", body))

    tools_data = [
        [Paragraph("<b>Tool</b>", th), Paragraph("<b>Developer</b>", th), Paragraph("<b>Key Capabilities</b>", th), Paragraph("<b>Citation</b>", th)],
        [Paragraph("medSpaCy", td_bold), Paragraph("VA / University of Utah", td), Paragraph("Section detection, context (negation/family history), target matching", td), Paragraph("Eyre et al., 2021", td)],
        [Paragraph("scispaCy", td_bold), Paragraph("Allen AI", td), Paragraph("Biomedical NER, entity linking to UMLS/SNOMED", td), Paragraph("Neumann et al., 2019", td)],
        [Paragraph("cTAKES", td_bold), Paragraph("Mayo Clinic / Apache", td), Paragraph("Clinical concept extraction, assertion, relation detection", td), Paragraph("Savova et al., 2010", td)],
        [Paragraph("SemEHR", td_bold), Paragraph("KCL / NIHR", td), Paragraph("Dictionary-based EHR phenotyping, negation handling", td), Paragraph("Wu et al., 2018", td)],
        [Paragraph("RARE-PHENIX", td_bold), Paragraph("Shyr et al.", td), Paragraph("End-to-end rare disease phenotyping: extraction + HPO mapping + ranking", td), Paragraph("Shyr et al., 2026", td)],
    ]
    tt = Table(tools_data, colWidths=[80, 110, 200, 114])
    tt.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#1B5E20")),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor("#CCCCCC")),
        ('BOTTOMPADDING',(0,0),(-1,-1),4), ('TOPPADDING',(0,0),(-1,-1),4),
        ('LEFTPADDING',(0,0),(-1,-1),4), ('RIGHTPADDING',(0,0),(-1,-1),4),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor("#F1F8E9")]),
    ]))
    s.append(tt)
    s.append(Spacer(1, 6))

    s.append(Paragraph("2.3 The Shift from Fine-Tuning to Large Language Models", h2))
    s.append(Paragraph(
        "A significant trend in 2024–2026 has been the shift from fine-tuned BERT-family models toward general-purpose "
        "Large Language Models (LLMs) such as GPT-4 for clinical phenotyping tasks. Shyr et al. (2024) benchmarked LLMs "
        "against fine-tuned BioClinicalBERT models for rare disease phenotype extraction and found that while fine-tuned "
        "models excel on narrow extraction tasks, LLMs provide superior flexibility for complex clinical reasoning, "
        "zero-shot classification, and multi-step diagnostic workflows.", body))
    s.append(Paragraph(
        "However, LLMs introduce challenges including hallucination, inconsistent output formatting, and high computational "
        "cost. Current best practice recommends <b>hybrid pipelines</b> that combine rule-based tools (medSpaCy, SemEHR) "
        "for reliable initial extraction with LLMs for higher-order reasoning and disambiguation (Wu et al., 2024).", body))

    # ── 3. EHR Datasets ──
    s.append(Paragraph("3. EHR Datasets for Clinical NLP Research", h1))

    s.append(Paragraph("3.1 MIMIC-IV and MIMIC-IV-Note", h2))
    s.append(Paragraph(
        "The Medical Information Mart for Intensive Care (MIMIC-IV) is the most widely used publicly available EHR dataset "
        "for clinical NLP research. Developed by the MIT Lab for Computational Physiology and sourced from Beth Israel "
        "Deaconess Medical Center (BIDMC) — a Harvard Medical School teaching affiliate — MIMIC-IV (v3.1, 2024) contains "
        "de-identified records from over 40,000 ICU patient stays, including structured data (diagnoses, labs, prescriptions) "
        "and unstructured clinical notes (Johnson et al., 2023).", body))
    s.append(Paragraph(
        "The <b>MIMIC-IV-Note</b> component provides de-identified free-text clinical notes including discharge summaries, "
        "radiology reports, progress notes, and nursing entries. These notes are linked to structured EHR data via patient "
        "and admission identifiers, enabling multimodal research that bridges free text and tabular clinical data "
        "(Johnson et al., 2023). Access is granted through PhysioNet after completion of the CITI data ethics course.", body))

    s.append(Paragraph("3.2 Relevance to Rare Disease Detection", h2))
    s.append(Paragraph(
        "MIMIC-IV is particularly suitable for rare disease detection research because: (a) discharge summaries contain "
        "rich, longitudinal patient narratives documenting symptoms across multiple encounters; (b) ICD-10 diagnosis codes "
        "provide ground-truth labels for validation; (c) the dataset's scale enables statistical evaluation of detection "
        "algorithms; and (d) its Harvard/MIT provenance ensures academic credibility and reproducibility.", body))

    # ── 4. Rare Disease Knowledge Bases ──
    s.append(Paragraph("4. Rare Disease Knowledge Bases and Ontologies", h1))

    s.append(Paragraph("4.1 Orphanet and the ORPHAcode System", h2))
    s.append(Paragraph(
        "Orphanet, established in 1997 and coordinated by INSERM (France), is the reference portal for rare disease "
        "information worldwide. It maintains a nomenclature of over 7,000 rare diseases, each assigned a unique "
        "ORPHAcode. The Orphanet Rare Disease Ontology (ORDO) provides structured, machine-readable descriptions of "
        "diseases including associated phenotypic features, inheritance patterns, epidemiological data, and therapeutic "
        "information. Orphadata exports (e.g., <i>en_product4.xml</i>) provide disease-phenotype associations in "
        "computable formats suitable for algorithmic matching (Orphanet, 2024).", body))

    s.append(Paragraph("4.2 Human Phenotype Ontology (HPO)", h2))
    s.append(Paragraph(
        "The Human Phenotype Ontology (HPO), maintained by the Monarch Initiative, provides a standardized vocabulary "
        "of over 16,000 phenotypic abnormality terms organized in a directed acyclic graph. Each term (e.g., "
        "HP:0025300 — Malar rash) is linked to associated diseases and genes, enabling computational phenotype matching. "
        "The HPO Annotation file (<i>phenotype.hpoa</i>) contains curated disease-to-phenotype associations covering "
        "over 8,000 diseases, serving as the primary resource for symptom-to-disease mapping in computational "
        "diagnosis tools (Köhler et al., 2021).", body))

    s.append(Paragraph("4.3 HPO-Orphanet Integration (HOOM)", h2))
    s.append(Paragraph(
        "The HPO-Orphanet Ontological Module (HOOM) integrates Orphanet's disease annotations with HPO's phenotypic "
        "vocabulary, providing high-quality, expert-curated links between clinical entities and phenotypic abnormalities. "
        "This integration is critical for computational diagnostic systems that need to bridge free-text clinical "
        "descriptions with standardized disease profiles (INSERM / Orphanet, 2023).", body))

    # ── 5. Computational Diagnosis ──
    s.append(Paragraph("5. Computational Approaches to Rare Disease Diagnosis", h1))

    s.append(Paragraph("5.1 Phenotype Similarity Matching", h2))
    s.append(Paragraph(
        "Traditional computational diagnostic tools operate by comparing a patient's observed phenotypes (encoded as "
        "HPO terms) against known disease phenotype profiles. Systems such as <b>Phenomizer</b>, <b>AMELIE</b>, and "
        "<b>Exomiser</b> compute semantic similarity scores using information-theoretic measures (e.g., Resnik similarity) "
        "over the HPO ontology graph. These tools have demonstrated clinical utility but require phenotypes to be "
        "manually curated by clinicians — a labor-intensive process that limits scalability.", body))

    s.append(Paragraph("5.2 LLM-Agentic Diagnostic Systems", h2))
    s.append(Paragraph(
        "A notable 2025–2026 development is the emergence of LLM-agentic diagnostic frameworks. <b>DeepRare</b> (2025) "
        "employs a multi-agent architecture integrating LLMs with over 40 specialized tools to process heterogeneous "
        "clinical inputs — including free text, HPO terms, and genetic data — and produce ranked diagnostic hypotheses "
        "with transparent, traceable reasoning. This represents a shift from single-model inference to orchestrated, "
        "tool-augmented diagnostic workflows.", body))

    s.append(Paragraph("5.3 End-to-End Phenotyping: RARE-PHENIX", h2))
    s.append(Paragraph(
        "The <b>RARE-PHENIX</b> framework (Shyr et al., 2026) addresses the critical gap between unstructured clinical "
        "text and standardized phenotype codes. Rather than treating extraction, standardization, and ranking as separate "
        "tasks, RARE-PHENIX models the entire workflow as a continuous pipeline: extracting phenotypic features from "
        "clinical notes, mapping them to HPO terms, and ranking them by diagnostic importance. This end-to-end approach "
        "significantly outperforms multi-step methods on rare disease phenotyping benchmarks.", body))

    s.append(Paragraph("5.4 Weakly Supervised Transformers (WEST)", h2))
    s.append(Paragraph(
        "Directly relevant to RareSense.AI is the <b>WEST</b> (WEakly Supervised Transformer) framework developed by "
        "Greco, Cai, and colleagues, published in <i>npj Digital Medicine</i> (February 2026). WEST addresses the "
        "fundamental challenge of rare disease phenotyping: the scarcity of labeled training data. The framework "
        "learns concept-level embeddings from EHR co-occurrence patterns, aggregates them via multi-layer transformers "
        "into patient-level representations, and uses iteratively refined 'silver-standard' labels derived from noisy "
        "EHR data. Validated on rare pulmonary diseases at Boston Children's Hospital, WEST demonstrated improved "
        "phenotype classification, clinically meaningful subphenotype discovery, and enhanced disease progression "
        "prediction (Greco & Cai et al., 2026).", body))

    # ── 6. Temporal Modeling ──
    s.append(Paragraph("5.5 Temporal and Longitudinal Modeling", h2))
    s.append(Paragraph(
        "Because rare diseases present with sparse, long-term phenotypic signals scattered across irregular clinical "
        "visits, temporal modeling is critical. Recent work (2025–2026) has introduced hierarchical set-to-sequence "
        "(HSS) frameworks that capture disease progression across irregular clinical visit intervals, modeling the "
        "evolution of phenotypic patterns over time rather than treating each visit independently. This temporal "
        "dimension is essential for detecting conditions that only become apparent when symptoms are aggregated "
        "across years of clinical encounters.", body))

    # ── 6. Research Gap ──
    s.append(Paragraph("6. Identified Research Gap", h1))
    s.append(Paragraph(
        "While significant progress has been made in individual components — clinical NLP extraction, ontological "
        "standardization, phenotype matching, and temporal modeling — a critical gap persists in the integration of "
        "these components into a <b>unified, end-to-end system</b> that:", body))
    s.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;(a) Ingests raw, unstructured clinical notes directly (not pre-curated HPO terms);", body))
    s.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;(b) Extracts and standardizes medical entities automatically;", body))
    s.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;(c) Constructs a longitudinal patient timeline across multiple encounters;", body))
    s.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;(d) Performs semantic matching against comprehensive rare disease databases; and", body))
    s.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;(e) Presents actionable results through a clinician-facing interface.", body))
    s.append(Paragraph(
        "Most existing tools require clinicians to manually input HPO terms, creating a scalability bottleneck. "
        "Systems that do automate extraction (e.g., RARE-PHENIX) have not been integrated with comprehensive rare "
        "disease matching engines and clinician dashboards. <b>RareSense.AI</b> is proposed to bridge this gap by "
        "combining clinical NLP (BioBERT/medSpaCy), HPO standardization, MongoDB-based temporal storage, vector "
        "similarity matching against Orphanet/HPO, and a React.js clinician dashboard into a single integrated system.", body))

    # ── 7. Comparison ──
    s.append(Paragraph("7. Comparison of Existing Systems", h1))
    comp_data = [
        [Paragraph("<b>System</b>", th), Paragraph("<b>Input</b>", th), Paragraph("<b>NLP</b>", th), Paragraph("<b>Ontology</b>", th), Paragraph("<b>Temporal</b>", th), Paragraph("<b>Dashboard</b>", th)],
        [Paragraph("Phenomizer", td_bold), Paragraph("Manual HPO", td), Paragraph("None", td), Paragraph("HPO", td), Paragraph("No", td), Paragraph("Basic", td)],
        [Paragraph("Exomiser", td_bold), Paragraph("Manual HPO + VCF", td), Paragraph("None", td), Paragraph("HPO + Genomic", td), Paragraph("No", td), Paragraph("Basic", td)],
        [Paragraph("DeepRare", td_bold), Paragraph("Multi-modal", td), Paragraph("LLM-based", td), Paragraph("HPO + OMIM", td), Paragraph("No", td), Paragraph("No", td)],
        [Paragraph("RARE-PHENIX", td_bold), Paragraph("Clinical notes", td), Paragraph("LLM-based", td), Paragraph("HPO", td), Paragraph("No", td), Paragraph("No", td)],
        [Paragraph("WEST (Cai)", td_bold), Paragraph("EHR structured", td), Paragraph("Embedding", td), Paragraph("ICD/EHR", td), Paragraph("Yes", td), Paragraph("No", td)],
        [Paragraph("RareSense.AI", td_bold), Paragraph("Clinical notes", td), Paragraph("BioBERT + medSpaCy", td), Paragraph("HPO + Orphanet", td), Paragraph("Yes", td), Paragraph("Yes", td)],
    ]
    ct = Table(comp_data, colWidths=[80, 80, 95, 95, 60, 60])
    ct.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#0D47A1")),
        ('BACKGROUND',(0,6),(-1,6),colors.HexColor("#E8F5E9")),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor("#CCCCCC")),
        ('BOTTOMPADDING',(0,0),(-1,-1),4), ('TOPPADDING',(0,0),(-1,-1),4),
        ('LEFTPADDING',(0,0),(-1,-1),4), ('RIGHTPADDING',(0,0),(-1,-1),4),
        ('ROWBACKGROUNDS',(0,1),(-1,5),[colors.white, colors.HexColor("#F5F5F5")]),
    ]))
    s.append(ct)
    s.append(Spacer(1, 4))
    s.append(Paragraph(
        "<i>Table: RareSense.AI is the only system that combines automated NLP extraction from raw clinical notes, "
        "dual ontology grounding (HPO + Orphanet), temporal timeline construction, and a clinician-facing dashboard.</i>",
        ParagraphStyle('cap', parent=body, fontName='Helvetica-Oblique', fontSize=8.5, textColor=colors.HexColor("#616161"))))

    # ── 8. References ──
    s.append(Paragraph("8. References", h1))
    refs = [
        "[1] Nguengang Wakap, S., et al. (2020). Estimating cumulative point prevalence of rare diseases. Orphanet Journal of Rare Diseases, 15(1), 171.",
        "[2] EURORDIS (2024). Rare Barometer Survey: The Diagnostic Odyssey in Europe. eurordis.org.",
        "[3] NORD — National Organization for Rare Disorders (2023). Rare Disease Facts and Statistics. rarediseases.org.",
        "[4] Global Commission on Rare Diseases (2024). Ending the Diagnostic Odyssey. globalrarediseasecommission.com.",
        "[5] Lee, J., et al. (2020). BioBERT: a pre-trained biomedical language representation model. Bioinformatics, 36(4), 1234–1240.",
        "[6] Huang, K., et al. (2019). ClinicalBERT: Modeling Clinical Notes and Predicting Hospital Readmission. arXiv:1904.05342.",
        "[7] Yang, S., et al. (2024). PhenoBCBERT and PhenoGPT: Enhanced phenotype recognition in clinical notes. JAMIA, 31(5).",
        "[8] Eyre, H., et al. (2021). Launching into clinical space with medSpaCy. AMIA Annual Symposium Proceedings.",
        "[9] Neumann, M., et al. (2019). ScispaCy: Fast and Robust Models for Biomedical NLP. BioNLP Workshop, ACL.",
        "[10] Savova, G.K., et al. (2010). Mayo clinical Text Analysis and Knowledge Extraction (cTAKES). JAMIA, 17(5), 507–513.",
        "[11] Wu, H., et al. (2018). SemEHR: A general-purpose semantic search system. JAMIA, 25(5), 530–537.",
        "[12] Shyr, C., et al. (2024). Benchmarking LLMs for Rare Disease Phenotype Extraction. arXiv preprint.",
        "[13] Shyr, C., et al. (2026). RARE-PHENIX: End-to-end rare disease phenotyping framework. arXiv preprint.",
        "[14] Johnson, A., et al. (2023). MIMIC-IV, a freely accessible electronic health record dataset. Scientific Data, 10(1), 1.",
        "[15] Johnson, A., et al. (2023). MIMIC-IV-Note: Deidentified free-text clinical notes. PhysioNet.",
        "[16] Köhler, S., et al. (2021). The Human Phenotype Ontology in 2021. Nucleic Acids Research, 49(D1), D1207–D1217.",
        "[17] Orphanet (2024). Orphadata: Free access datasets. orphadata.com.",
        "[18] INSERM / Orphanet (2023). HPO-Orphanet Ontological Module (HOOM). orpha.net.",
        "[19] Greco, K.F., Cai, T., et al. (2026). A weakly supervised transformer for rare disease diagnosis and subphenotyping from EHRs. npj Digital Medicine, 9(1).",
        "[20] DeepRare Consortium (2025). DeepRare: Multi-agent LLM framework for rare disease diagnosis. Nature Methods.",
        "[21] Aronson, A.R. & Lang, F.M. (2010). An overview of MetaMap. JAMIA, 17(3), 229–236.",
        "[22] Aali, M., et al. (2024). A dataset and benchmark for hospital course summarization. PhysioNet.",
    ]
    for r in refs:
        s.append(Paragraph(r, cite))

    doc.build(s, canvasmaker=NumberedCanvas)
    print("[OK] RareSense_AI_LiteratureReview.pdf generated successfully.")

if __name__ == "__main__":
    build()
