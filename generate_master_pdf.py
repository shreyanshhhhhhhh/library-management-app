import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
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
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Times-Roman", 9)
        self.setFillColor(colors.HexColor("#4b5563"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "Azista Space — Written Assessment")
            self.drawRightString(612 - 54, 755, "Shreyansh Pandey | Symbiosis Institute of Technology")
            self.setStrokeColor(colors.HexColor("#9ca3af"))
            self.setLineWidth(0.5)
            self.line(54, 747, 612 - 54, 747)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#9ca3af"))
        self.setLineWidth(0.5)
        self.line(54, 45, 612 - 54, 45)
        
        self.drawString(54, 32, "Technical Written Test Submission — Confidential")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 32, page_text)
        self.restoreState()

def build_pdf():
    pdf_path = r"C:\Users\HP\.gemini\antigravity\scratch\library-management-app\Library_Inventory_Management_Submission.pdf"
    img_dir = r"C:\Users\HP\.gemini\antigravity\scratch\library-management-app\screenshots"
    ticket_dir = os.path.join(img_dir, "ticket_project")
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Pure Academic Black & Grey Palette
    c_black = colors.HexColor("#111827")      # Rich black
    c_dark_grey = colors.HexColor("#374151")  # Dark grey
    c_mid_grey = colors.HexColor("#4b5563")   # Mid grey
    c_light_bg = colors.HexColor("#f3f4f6")   # Soft subtle grey
    c_border = colors.HexColor("#9ca3af")     # Clear border grey
    
    # Standard Academic Typography (Times-Roman / Helvetica Mix)
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=20, leading=24, textColor=c_black, spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=11, leading=15, textColor=c_mid_grey, spaceAfter=10
    )

    part_header_style = ParagraphStyle(
        'PartHeader', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=13, leading=17, textColor=c_black,
        spaceBefore=0, spaceAfter=0, alignment=0
    )
    
    h1_style = ParagraphStyle(
        'SectionH1', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=12, leading=16, textColor=c_black,
        spaceBefore=11, spaceAfter=5, keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'SectionH2', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=10, leading=14, textColor=c_dark_grey,
        spaceBefore=8, spaceAfter=3, keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'DocBody', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=9.5, leading=13.5, textColor=c_black, spaceAfter=4.5
    )

    body_bold = ParagraphStyle('DocBodyBold', parent=body_style, fontName='Times-Bold')
    
    bullet_style = ParagraphStyle(
        'DocBullet', parent=body_style, leftIndent=14, firstLineIndent=-9, spaceAfter=3
    )

    caption_style = ParagraphStyle(
        'DocCaption', parent=styles['Normal'],
        fontName='Times-Italic', fontSize=8.5, leading=11.5, textColor=c_dark_grey,
        alignment=1, spaceBefore=3, spaceAfter=8
    )

    story = []

    # ==================== MAIN HEADER (ACADEMIC FORMAT) ====================
    story.append(Paragraph("Azista Space — Written Assessment", ParagraphStyle('InstHeader', parent=styles['Normal'], fontName='Times-Bold', fontSize=10, textColor=c_dark_grey, spaceAfter=2)))
    story.append(Paragraph("Candidate Technical Assessment Dossier", title_style))
    story.append(Paragraph("Solutions for Question 1 (AI Project & Research Publication) and Question 2 (Library System Design)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_black, spaceBefore=0, spaceAfter=9))

    # Candidate Meta Table (Clean Minimalist Grey)
    meta_data = [
        [
            Paragraph("<b>Candidate Name:</b> Shreyansh Pandey", body_style),
            Paragraph("<b>Institute:</b> Symbiosis Institute of Technology (SIT), Pune", body_style)
        ],
        [
            Paragraph("<b>Program:</b> B.Tech in Artificial Intelligence & Machine Learning", body_style),
            Paragraph("<b>Assessment:</b> Azista Space Technical Hiring Test", body_style)
        ],
        [
            Paragraph("<b>Question 1 (Paper):</b> Accepted at IEEE IConAECC 2026 (Paper ID: 1231)", body_style),
            Paragraph("<b>Question 1 (Code):</b> <a href='https://github.com/shreyanshhhhhhhh/TIcket_agent_BTECH' color='#111827'><u>github.com/shreyanshhhhhhhh/TIcket_agent_BTECH</u></a>", body_style)
        ],
        [
            Paragraph("<b>Question 2 (Live):</b> <a href='https://shreyanshhhhhhhh.github.io/library-management-app/' color='#111827'><u>shreyanshhhhhhhh.github.io/library-management-app</u></a>", body_style),
            Paragraph("<b>Question 2 (Code):</b> <a href='https://github.com/shreyanshhhhhhhh/library-management-app' color='#111827'><u>github.com/shreyanshhhhhhhh/library-management-app</u></a>", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light_bg),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e5e7eb")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # PART 1: QUESTION 1 — AI PROJECT SHOWCASE & PUBLISHED RESEARCH
    # =========================================================================
    part1_bar = Table([[Paragraph("<b>PART 1: QUESTION 1 — AI PROJECT & PUBLISHED RESEARCH WORK</b>", part_header_style)]], colWidths=[504])
    part1_bar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light_bg),
        ('BOX', (0,0), (-1,-1), 1, c_black),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(part1_bar)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1.1 Project Context & Peer-Reviewed Publication", h1_style))
    story.append(Paragraph(
        "<b>Project Title:</b> AI-Powered Intelligent Ticket Routing & Resolution Agent<br/>"
        "<b>Published Research Paper:</b> <i>'Calibrated Escalation for IT Ticket Triage: What the Calibration Distribution Decides'</i><br/>"
        "<b>Authors:</b> Aryan Manoj Waingankar, <b>Shreyansh Pandey</b>, Parth Bagle, Swapnil Samrat, Dr. Madhvi Saxena, Dr. Aditi Saxena (Department of AIML, Symbiosis Institute of Technology, Pune)<br/>"
        "<b>Conference Acceptance:</b> <b>Accepted for Presentation & IEEE Xplore Proceedings at 2026 Indian Conference on Advances in Electrical, Computers, and Communications (IEEE IConAECC 2026, Paper ID: 1231)</b>.<br/>"
        "<b>Repository Link:</b> <a href='https://github.com/shreyanshhhhhhhh/TIcket_agent_BTECH' color='#111827'><u>https://github.com/shreyanshhhhhhhh/TIcket_agent_BTECH</u></a>",
        body_style
    ))
    story.append(Paragraph(
        "<b>Problem Context:</b> Enterprise IT support desks handle large volumes of tickets daily, causing three major practical problems: (1) <i>Misrouting</i> tickets to the wrong technical team; (2) <i>High Mean-Time-To-Resolution (MTTR)</i> caused by manual triage queues; and (3) <i>Repeated Engineering Work</i>, where recurring technical faults are investigated from scratch rather than reusing past verified fixes. In enterprise operations, <b>routing a ticket confidently but incorrectly carries a much higher business cost than asking for human assistance</b>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Core Research Contribution:</b> We built human escalation as a primary, first-class output. The pipeline uses two separately calibrated decision gates: (1) a 0.50 confidence threshold on a fast lexical classifier to decide whether to consult a dense embedding classifier, and (2) a 0.67 cosine-similarity threshold on retrieved historical tickets to decide whether a language model may draft a suggested fix. On our 9-ticket adversarial test set, the retrieval gate resolved <b>9 out of 9 tickets correctly</b> (compared to only 3 of 9 when the gate was removed).",
        body_style
    ))

    # Acceptance Letter Screenshot
    acc_path = os.path.join(ticket_dir, "iconaecc_acceptance_letter.png")
    if os.path.exists(acc_path):
        img_acc = Image(acc_path, width=490, height=275)
        story.append(KeepTogether([
            Paragraph("<b>Figure 1.1: Official IEEE IConAECC 2026 Conference Acceptance Notification (Paper ID: 1231)</b>", h2_style),
            img_acc,
            Paragraph("<i>Official acceptance notification confirming peer-reviewed acceptance of our paper 'Calibrated Escalation for IT Ticket Triage: What the Calibration Distribution Decides' for presentation and publication in IEEE Xplore.</i>", caption_style)
        ]))
    story.append(Spacer(1, 8))

    # Paper Page 1 Screenshot
    p1_path = os.path.join(ticket_dir, "paper_page_1.png")
    if os.path.exists(p1_path):
        img_p1 = Image(p1_path, width=490, height=310)
        story.append(KeepTogether([
            Paragraph("<b>Figure 1.2: Published Research Manuscript (Title, Authors, Abstract & Introduction)</b>", h2_style),
            img_p1,
            Paragraph("<i>Page 1 of the accepted research paper showing author affiliations at Symbiosis Institute of Technology (SIT), Pune, problem definition, abstract, and core contributions.</i>", caption_style)
        ]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("1.2 Functional System Pipeline & Architecture", h1_style))
    story.append(Paragraph(
        "The system pipeline is structured into four sequential stages designed for speed, calibrated reliability, and interpretability:",
        body_style
    ))
    
    q1_layers = [
        ("Tier-1 Lexical Classifier & Cascade Deferral Gate (Threshold = 0.50):",
         "Incoming support tickets first pass through a lightweight TF-IDF logistic regression classifier (1.04 ms median latency). If its top-class probability is >= 0.50, the classification is accepted immediately. If confidence is < 0.50, execution defers to Tier-2."),
        
        ("Tier-2 Dense Semantic Embedding Representation (BGE Embeddings):",
         "For complex or ambiguous tickets, 768-dimensional dense embeddings are generated using <code>bge-base-en-v1.5</code>, followed by logistic regression across the 7 IT categories (Access Management, Application, Database, Infrastructure, Network, Security, Storage). While more compute-intensive (156.4 ms), the cascade saves 8% to 18% overall median latency without accuracy loss."),
        
        ("Vector RAG Retrieval & Calibrated Guardrail Gate (Threshold = 0.67):",
         "The top-5 nearest resolved tickets are retrieved from a vector store using inner-product / cosine distance. If top-1 cosine similarity falls below 0.67, <b>the ticket is escalated to a human specialist and no LLM call is made</b>. Only when similarity >= 0.67 is Gemini allowed to draft an answer based strictly on retrieved resolutions."),
        
        ("Agentic Orchestration & Offline Automation Clustering:",
         "Orchestrated via LangGraph with clear state transitions. In the background, resolved tickets are clustered by resolution text similarity at a 0.80 cutoff to flag candidates for permanent automation.")
    ]
    for l_title, l_desc in q1_layers:
        story.append(Paragraph(f"• <b>{l_title}</b> {l_desc}", bullet_style))
    story.append(Spacer(1, 6))

    # Architecture Block Diagram
    arch_img_path = os.path.join(ticket_dir, "custom_system_block_diagram.png")
    if os.path.exists(arch_img_path):
        img_arch = Image(arch_img_path, width=490, height=310)
        story.append(KeepTogether([
            Paragraph("<b>Figure 1.3: End-to-End System Block Diagram & Dual-Gated Decision Flow</b>", h2_style),
            img_arch,
            Paragraph("<i>System block diagram illustrating the two calibrated escalation gates, embedding generation, RAG knowledge base, LangGraph decision state machine, and auto-resolve vs. human-escalate pathways.</i>", caption_style)
        ]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("1.3 Empirical Evaluation & Benchmarking Results", h1_style))
    story.append(Paragraph(
        "Our paper evaluated the system across multiple benchmarks: synthetic sets, a 14-ticket handwritten benchmark, an adversarial set of vague/slang tickets, an independent blind cross-labelled 108-ticket author set (Cohen's κ = 0.936), and 583 distinct real-world enterprise tickets from Pereira's public dataset:",
        body_style
    ))

    # Model Performance Table from Paper
    m_data = [
        [Paragraph("<b>Model / Pipeline</b>", body_bold), Paragraph("<b>Val Acc</b>", body_bold), Paragraph("<b>Val Macro F1</b>", body_bold), Paragraph("<b>Test Acc</b>", body_bold), Paragraph("<b>Test Macro F1</b>", body_bold)],
        [Paragraph("Baseline: TF-IDF + Naive Bayes", body_style), Paragraph("66.44%", body_style), Paragraph("67.19%", body_style), Paragraph("65.33%", body_style), Paragraph("65.64%", body_style)],
        [Paragraph("<b>Main: Embeddings (MiniLM) + LogReg</b>", body_style), Paragraph("<b>73.15%</b>", body_style), Paragraph("<b>73.43%</b>", body_style), Paragraph("<b>70.00%</b>", body_style), Paragraph("<b>70.26%</b>", body_style)],
        [Paragraph("Embeddings + Support Vector Machine (SVM)", body_style), Paragraph("73.15%", body_style), Paragraph("73.36%", body_style), Paragraph("70.00%", body_style), Paragraph("69.97%", body_style)],
        [Paragraph("5-Fold Cross-Validation (Main Model)", body_style), Paragraph("73.40% ± 0.96%", body_style), Paragraph("73.40% ± 1.10%", body_style), Paragraph("—", body_style), Paragraph("—", body_style)],
        [Paragraph("Zero-Shot Gemini Flash-Lite Baseline", body_style), Paragraph("—", body_style), Paragraph("—", body_style), Paragraph("88.89% (40/45)", body_style), Paragraph("Cannot Abstain")]
    ]
    m_table = Table(m_data, colWidths=[154, 85, 90, 85, 90])
    m_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_light_bg),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
    ]))
    story.append(m_table)
    story.append(Spacer(1, 6))

    # Paper Table III - Operating Points
    story.append(Paragraph("<b>Table 1.2: Operating Points of the Calibrated Dual-Gate Architecture</b>", h2_style))
    op_data = [
        [Paragraph("<b>Pipeline Metric / Operating Quantity</b>", body_bold), Paragraph("<b>Empirical Value (From Research Paper Table III)</b>", body_bold)],
        [Paragraph("Retrieval Gate Threshold (Top-1 Cosine Similarity)", body_style), Paragraph("<b>0.67</b>", body_style)],
        [Paragraph("In-domain tickets proceeding past Retrieval Gate", body_style), Paragraph("<b>175 / 175 (100.0%)</b>", body_style)],
        [Paragraph("Adversarial tickets decided correctly WITH Gate", body_style), Paragraph("<b>9 / 9 (100.0%)</b>", body_style)],
        [Paragraph("Adversarial tickets decided correctly WITHOUT Gate (Unsafe)", body_style), Paragraph("3 / 9 (33.3% — 6 unsafe leaks)", body_style)],
        [Paragraph("Cascade Gate Threshold (Tier-1 Top-Class Probability)", body_style), Paragraph("<b>0.50</b>", body_style)],
        [Paragraph("Tier-1 Median Latency vs. Tier-2 Median Latency", body_style), Paragraph("<b>1.04 ms vs. 156.4 ms (151.0x compute saving)</b>", body_style)],
        [Paragraph("End-to-End Pipeline Latency Reduction via Cascade", body_style), Paragraph("<b>8.2% (Benchmark) to 18.2% (Deployment Distribution)</b>", body_style)]
    ]
    op_table = Table(op_data, colWidths=[240, 264])
    op_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_light_bg),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
    ]))
    story.append(op_table)
    story.append(Spacer(1, 8))

    # Visual Artifacts: Confusion Matrix & Reliability Diagram
    cm_path = os.path.join(ticket_dir, "confusion_matrix.png")
    rel_path = os.path.join(ticket_dir, "reliability_diagram.png")
    if os.path.exists(cm_path) and os.path.exists(rel_path):
        eval_imgs = Table([
            [Image(cm_path, width=245, height=195), Image(rel_path, width=245, height=195)],
            [Paragraph("<b>Figure 1.4: Multi-Class Confusion Matrix (7 Categories)</b>", caption_style),
             Paragraph("<b>Figure 1.5: Empirical Reliability Diagram & Calibration Curve</b>", caption_style)]
        ], colWidths=[252, 252])
        eval_imgs.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(KeepTogether([eval_imgs]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("1.4 Challenges Faced, Debugging Process & Resolutions", h1_style))
    story.append(Paragraph(
        "Four significant technical challenges were identified and systematically resolved during the project:",
        body_style
    ))

    challenges = [
        ("Challenge 1: Category Ambiguity Between Infrastructure & Network",
         "<b>Diagnosis:</b> The confusion matrix revealed that 41% of misclassifications occurred between Infrastructure and Network (e.g., router failovers causing server unreachability). Inspecting embeddings showed high cosine overlap.<br/>"
         "<b>Resolution:</b> Rather than forcing an overconfident wrong label, we calibrated the LangGraph state machine so that ambiguous tickets drop below the 0.50 threshold, triggering immediate escalation to a human engineer along with cross-category diagnostic context."),
        
        ("Challenge 2: Systemic Underconfidence in Softmax Probabilities",
         "<b>Diagnosis:</b> Raw softmax probabilities on valid tickets frequently sat around 0.45 – 0.65, threatening to escalate almost every ticket needlessly.<br/>"
         "<b>Resolution:</b> Constructed an empirical binned calibration reliability curve (Figure 1.5). We proved that the model is <i>systematically underconfident</i>: predictions with 50-60% nominal probability achieve <b>80.65% actual accuracy</b>. Setting the gate at 0.50 allows safe automation while maintaining an 80%+ precision envelope."),
        
        ("Challenge 3: Semantic Drift & OS Noise in Dense Vector Retrieval",
         "<b>Diagnosis:</b> Queries reporting <i>'VPN client crashes on Windows 11'</i> retrieved fixes for <i>'Word document crashes on Windows 11'</i> due to heavy keyword dominance by common OS terms.<br/>"
         "<b>Resolution:</b> Implemented domain-aware metadata pre-filtering in <code>rag_retrieval.py</code>. Candidate vectors in ChromaDB are pre-filtered by predicted category before computing cosine similarity, eliminating cross-domain noise."),
        
        ("Challenge 4: The Transferability Gap on Real-World Data (The Paper's Core Finding)",
         "<b>Diagnosis:</b> When evaluated on 583 real-world user tickets, a classifier trained only on synthetic templates dropped in routing accuracy (19.7% to 50.4%), and 371 misrouted tickets leaked past the drafter.<br/>"
         "<b>Resolution:</b> We demonstrated empirically that <i>the data distribution used to calibrate a component constrains it more than the algorithm chosen</i>. We designed an independent dual-verification gate (both classifier confidence >= 0.50 AND retrieval similarity >= 0.67 required) to strictly prevent unauthorized hallucinations from reaching users.")
    ]
    for c_title, c_desc in challenges:
        story.append(Paragraph(f"• <b>{c_title}</b><br/>{c_desc}", bullet_style))
        story.append(Spacer(1, 3))
    
    story.append(Spacer(1, 12))

    # =========================================================================
    # PART 2: QUESTION 2 — LIBRARY INVENTORY MANAGEMENT SYSTEM
    # =========================================================================
    story.append(PageBreak())
    part2_bar = Table([[Paragraph("<b>PART 2: QUESTION 2 — LIBRARY INVENTORY MANAGEMENT SYSTEM DESIGN</b>", part_header_style)]], colWidths=[504])
    part2_bar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light_bg),
        ('BOX', (0,0), (-1,-1), 1, c_black),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(part2_bar)
    story.append(Spacer(1, 8))

    story.append(Paragraph("2.1 System Architecture & Live Deployment Verification", h1_style))
    story.append(Paragraph(
        "<b>System Name:</b> LibraTrack v1.0 — Enterprise Library Management Application<br/>"
        "<b>Live Deployment URL:</b> <a href='https://shreyanshhhhhhhh.github.io/library-management-app/' color='#111827'><u>https://shreyanshhhhhhhh.github.io/library-management-app/</u></a><br/>"
        "<b>GitHub Source Repository:</b> <a href='https://github.com/shreyanshhhhhhhh/library-management-app' color='#111827'><u>https://github.com/shreyanshhhhhhhh/library-management-app</u></a>",
        body_style
    ))
    story.append(Paragraph(
        "<b>Architectural Foundation:</b> LibraTrack is built as a zero-dependency, high-performance web application utilizing modern ECMAScript 6+ modular patterns, semantic HTML5, and CSS custom design tokens. State persistence is governed by an ACID-compliant client storage engine enforcing relational constraints, foreign-key integrity between transactions and books/members, and auto-incrementing surrogate keys.",
        body_style
    ))
    story.append(Paragraph(
        "The software is hosted permanently on GitHub Pages with 24/7 global CDN distribution, SSL encryption, and continuous availability. Every required feature—adding/deleting books, tracking issued books and inventory, managing fines, and handling multiple physical copies of identical titles—is completely implemented, interactive, and demonstrable.",
        body_style
    ))

    story.append(Paragraph("2.2 Architectural Decisions & Feature Rationale", h1_style))
    story.append(Paragraph(
        "The application architecture directly addresses core operational challenges in physical library administration:",
        body_style
    ))

    q2_features = [
        ("Multi-Copy Inventory Abstraction (Title vs. Physical Unit):",
         "In real-world libraries, an ISBN identifies an intellectual title, while multiple physical copies circulate independently. LibraTrack decouples the title entity from physical copy states. The system dynamically computes: <code>Available Copies = Total Inventory - Currently Active Issues</code>. This enables granular copy-level tracking without catalog duplication."),
        
        ("Differential Role-Based Quota Tiers (Students vs. Faculty):",
         "Patron groups possess distinct operational requirements. The system supports custom borrowing caps: Students (3 books, 14-day loan), Faculty (10 books, extended loan), Staff (5 books), and External Members (2 books). Borrowing limits are hard-enforced at the checkout interface."),
        
        ("Progressive Daily Overdue Fine Engine:",
         "Eliminates manual calculation errors by computing overdue penalties dynamically at ₹2 per calendar day. Fines accrue automatically upon book check-in and are tracked on member balance profiles until settled through supported payment rails (Cash, UPI, Card, or authorized Librarian Waiver)."),
        
        ("Defensive Referential Integrity Enforcement:",
         "Guarantees that database records remain consistent under all conditions: (1) Books cannot be deleted while physical copies are circulating; (2) Total copies cannot be decreased below the number of active issues; (3) Members with outstanding book loans or unsettled fines cannot be deleted; (4) Duplicate issues of the identical title to the same patron are blocked."),
        
        ("High-Throughput Unified Circulation Desk:",
         "A unified split-view interface allows desk operators to issue outgoing books and process returns side-by-side on a single display, minimizing page transitions during peak checkout hours."),
        
        ("Proactive Event Notification System:",
         "Surfaces real-time color-coded alerts: urgent warning notifications for overdue loans, and 48-hour advance reminders for upcoming due dates.")
    ]
    for f_title, f_desc in q2_features:
        story.append(Paragraph(f"• <b>{f_title}</b> {f_desc}", bullet_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("2.3 Matrix of Accounted Scenarios & Defensive Handlings", h1_style))
    
    q2_scenario_data = [
        [Paragraph("<b>Scenario #</b>", body_bold), Paragraph("<b>Operational Scenario & Edge Condition</b>", body_bold), Paragraph("<b>System Behavior & Defensive Handling</b>", body_bold)],
        [Paragraph("SC-01", body_style), Paragraph("Adding a new book to catalog", body_style), Paragraph("Enforces ISBN uniqueness. Rejects duplicates; registers stock count and shelf rack coordinates.", body_style)],
        [Paragraph("SC-02", body_style), Paragraph("Multi-copy book acquisition", body_style), Paragraph("Permits assigning total copies (N >= 1) to an ISBN title. Calculates live availability badges.", body_style)],
        [Paragraph("SC-03", body_style), Paragraph("Editing stock with active loans", body_style), Paragraph("Blocks administrator from decreasing total copies below current circulating count.", body_style)],
        [Paragraph("SC-04", body_style), Paragraph("Attempted deletion of circulating book", body_style), Paragraph("Rejects deletion with an informative toast showing circulating copy count.", body_style)],
        [Paragraph("SC-05", body_style), Paragraph("Member registration & duplicate checks", body_style), Paragraph("Validates unique email address and sets borrowing limits based on institutional tier.", body_style)],
        [Paragraph("SC-06", body_style), Paragraph("Student vs. Faculty differential quotas", body_style), Paragraph("Preconfigures Student cap at 3 books and Faculty cap at 10 books. Enforced at checkout selector.", body_style)],
        [Paragraph("SC-07", body_style), Paragraph("Borrowing limit exhaustion", body_style), Paragraph("Disables member in checkout selector once current issues equal max allowed books.", body_style)],
        [Paragraph("SC-08", body_style), Paragraph("Attempt to issue fully checked-out book", body_style), Paragraph("Books with 0 available copies are marked disabled in selection lists, preventing overselling.", body_style)],
        [Paragraph("SC-09", body_style), Paragraph("Duplicate checkout prevention", body_style), Paragraph("Prevents issuing another copy of the same book to a patron who already holds an active copy.", body_style)],
        [Paragraph("SC-10", body_style), Paragraph("Overdue check-in with penalty", body_style), Paragraph("Calculates days overdue against system date, generates ₹2/day fine, and prompts for payment.", body_style)],
        [Paragraph("SC-11", body_style), Paragraph("Timely return (Zero fine)", body_style), Paragraph("Marks loan as returned on time, restores book copy to available pool with zero fine penalty.", body_style)],
        [Paragraph("SC-12", body_style), Paragraph("Multi-channel fine settlement", body_style), Paragraph("Supports Cash, UPI, Card, and Librarian Waiver. Generates formal payment audit record with payment ID.", body_style)],
        [Paragraph("SC-13", body_style), Paragraph("Borrowing attempt with pending fines", body_style), Paragraph("Displays contextual warning banner showing patron's outstanding balance before proceeding.", body_style)],
        [Paragraph("SC-14", body_style), Paragraph("Deleting member with active obligations", body_style), Paragraph("Strictly prohibits deleting any member profile that holds active loans or unsettled fines.", body_style)],
        [Paragraph("SC-15", body_style), Paragraph("Advance expiration alert (48-hour notice)", body_style), Paragraph("Surfaces notification banner highlighting upcoming due dates before penalties begin accruing.", body_style)],
        [Paragraph("SC-16", body_style), Paragraph("Audit trail & operational reporting", body_style), Paragraph("Maintains immutable historical logs with real-time analytics for genre volume and borrowing frequency.", body_style)]
    ]
    q2_sc_table = Table(q2_scenario_data, colWidths=[45, 185, 274])
    q2_sc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_light_bg),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
    ]))
    story.append(q2_sc_table)
    story.append(Spacer(1, 10))

    # ==================== SECTION 2.4: SCREENSHOTS & FEATURE RENDERS ====================
    story.append(PageBreak())
    story.append(Paragraph("2.4 Feature Renders & Operational Screenshots", h1_style))
    story.append(Paragraph(
        "Screenshots illustrating all primary windows, modals, interactive workflows, and visual reports:",
        body_style
    ))
    story.append(Spacer(1, 5))

    renders = [
        ("01_dashboard.png", "Figure 2.1: Executive Dashboard & Operational KPIs", "Provides metric cards (Total Books, Available Stock, Active Issues, Overdue Count, Member Total, Outstanding Fines), recent circulation feed, and immediate overdue action list."),
        ("02_book_catalog.png", "Figure 2.2: Book Catalog & Multi-Copy Inventory", "Tabular inventory displaying book metadata, ISBN, genre classification, total copies, live available copy badges, and action controls (Inspect, Modify, Remove)."),
        ("03_add_book_modal.png", "Figure 2.3: Book Registration Modal", "Form capturing Title, Author, ISBN, Classification, Publisher, Publication Year, Total Physical Copies, and Shelf Rack Location with field validation."),
        ("04_book_details_modal.png", "Figure 2.4: Deep Book Inspection & Copy-Level Borrower Tracking", "Detailed dialog showing book metadata and a live table of which members currently possess specific copies of this ISBN, including due dates and overdue statuses."),
        ("05_members_management.png", "Figure 2.5: Member Directory & Quota Monitoring", "Directory of library patrons segmented by classification (Student, Faculty, Staff, External) displaying contact details, quota usage (e.g. 1/3), and outstanding liabilities."),
        ("06_add_member_modal.png", "Figure 2.6: Member Registration Modal", "Form for onboarding patrons with contact verification, category assignment, and custom maximum book limits based on institutional tier."),
        ("07_member_details_modal.png", "Figure 2.7: Member Profile & Complete Borrowing Dossier", "Shows member metadata, active borrowing quota utilization, unpaid fine balances, and complete lifetime borrowing and return history."),
        ("08_issue_return_workflow.png", "Figure 2.8: Unified Circulation Desk (Issue & Return)", "Split-screen interface allowing staff to simultaneously execute check-outs and check-ins without switching pages, significantly cutting desk turnaround time."),
        ("09_issue_book_form.png", "Figure 2.9: Validated Book Check-Out Flow", "Demonstrates dynamic validation during checkout: surfaces member quota status, warns of existing fines, and sets borrowing period."),
        ("10_return_fine_calculation.png", "Figure 2.10: Check-In & Automated Overdue Fine Calculation", "Selecting an overdue check-in triggers automatic computation of days overdue and applies penalty according to the standard fine schedule (₹2/day)."),
        ("11_transactions_history.png", "Figure 2.11: Transaction Ledger & Audit Trail", "Filterable audit log documenting every book check-out and check-in with transaction ID, patron, issue date, due date, return date, status, and fine assessment."),
        ("12_fines_management.png", "Figure 2.12: Fines Management & Revenue Tracking", "Dedicated accounts module tracking Total Pending Fines, Total Collected Fines, current fine rate, active overdue accounts, and payment reconciliation history."),
        ("13_pay_fine_modal.png", "Figure 2.13: Multi-Channel Fine Payment Reconciliation", "Modal for settling accrued fines with support for Cash, UPI, Card, or authorized Librarian Waivers, recording payment IDs into financial records."),
        ("14_reports_analytics.png", "Figure 2.14: Administrative Analytics & Visual Reports", "Interactive Chart.js visualizations presenting collection composition by genre, 6-month circulation volume trends, top borrowed titles, and most active patrons."),
        ("15_notifications_panel.png", "Figure 2.15: Proactive Alert & Notification Center", "Top-level notification panel detailing overdue emergencies and advance 48-hour return reminders for desk staff follow-up.")
    ]

    for filename, fig_title, fig_desc in renders:
        img_path = os.path.join(img_dir, filename)
        if os.path.exists(img_path):
            img = Image(img_path, width=490, height=270)
            render_block = [
                Paragraph(f"<b>{fig_title}</b>", h2_style),
                img,
                Paragraph(f"<i>{fig_desc}</i>", caption_style),
                Spacer(1, 6)
            ]
            story.append(KeepTogether(render_block))

    # ==================== SUMMARY & EVALUATION TABLE ====================
    story.append(Spacer(1, 8))
    story.append(Paragraph("2.5 Summary & Direct Access Endpoints", h1_style))
    
    end_data = [
        [Paragraph("<b>Resource</b>", body_bold), Paragraph("<b>Hyperlink / Verification Path</b>", body_bold)],
        [
            Paragraph("Q1 Research Publication (IEEE IConAECC)", body_style),
            Paragraph("Paper ID: 1231 | Presentation at IEEE IConAECC 2026", body_style)
        ],
        [
            Paragraph("Q1 Project GitHub Repository", body_style),
            Paragraph("<a href='https://github.com/shreyanshhhhhhhh/TIcket_agent_BTECH' color='#111827'><u>https://github.com/shreyanshhhhhhhh/TIcket_agent_BTECH</u></a>", body_style)
        ],
        [
            Paragraph("Q2 Live Web Application", body_style),
            Paragraph("<a href='https://shreyanshhhhhhhh.github.io/library-management-app/' color='#111827'><u>https://shreyanshhhhhhhh.github.io/library-management-app/</u></a>", body_style)
        ],
        [
            Paragraph("Q2 Source Code Repository", body_style),
            Paragraph("<a href='https://github.com/shreyanshhhhhhhh/library-management-app' color='#111827'><u>https://github.com/shreyanshhhhhhhh/library-management-app</u></a>", body_style)
        ],
        [
            Paragraph("Instant Interactive Demo", body_style),
            Paragraph("Click <b>Quick Action → Load Sample Data</b> on the live web app.", body_style)
        ]
    ]
    end_table = Table(end_data, colWidths=[160, 344])
    end_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_light_bg),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
    ]))
    story.append(end_table)
    story.append(Spacer(1, 10))
    story.append(Paragraph("<i>Prepared for Azista Space — Written Assessment Evaluation. Candidate: Shreyansh Pandey (Symbiosis Institute of Technology, Pune).</i>", ParagraphStyle('FooterNote', parent=caption_style, alignment=0)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Human-styled Master PDF generated successfully at: {pdf_path}")

if __name__ == '__main__':
    build_pdf()
