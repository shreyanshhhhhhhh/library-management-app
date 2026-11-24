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
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "Azista Space — Written Test | Question 2: Library Inventory Management")
            self.drawRightString(612 - 54, 755, "LibraTrack")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 747, 612 - 54, 747)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 612 - 54, 45)
        
        self.drawString(54, 32, "Confidential — Candidate Response Submission")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 32, page_text)
        self.restoreState()

def build_pdf():
    pdf_path = r"C:\Users\HP\.gemini\antigravity\scratch\library-management-app\Library_Inventory_Management_Submission.pdf"
    img_dir = r"C:\Users\HP\.gemini\antigravity\scratch\library-management-app\screenshots"
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    primary = colors.HexColor("#1e3a8a")     # Deep navy blue
    secondary = colors.HexColor("#4f46e5")   # Indigo
    dark = colors.HexColor("#0f172a")        # Slate 900
    gray_txt = colors.HexColor("#475569")    # Slate 600
    light_bg = colors.HexColor("#f8fafc")    # Slate 50
    border_col = colors.HexColor("#cbd5e1")  # Slate 300
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=gray_txt,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=secondary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=dark,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'DocBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    caption_style = ParagraphStyle(
        'DocCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=gray_txt,
        alignment=1,
        spaceBefore=3,
        spaceAfter=10
    )
    
    link_style = ParagraphStyle(
        'DocLink',
        parent=body_style,
        textColor=secondary
    )

    story = []

    # ==================== COVER / HEADER BANNER ====================
    story.append(Paragraph("Azista Space — Written Test Submission", ParagraphStyle('TopBadge', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=secondary, spaceAfter=4)))
    story.append(Paragraph("Question 2: Library Inventory Management", title_style))
    story.append(Paragraph("Application Design, Architecture, Feature Rationale, and Use-Case Specification", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary, spaceBefore=0, spaceAfter=14))

    # Meta Info Card
    meta_data = [
        [
            Paragraph("<b>Candidate Assignment:</b> Written Test Evaluation", body_style),
            Paragraph("<b>Target System:</b> LibraTrack v1.0", body_style)
        ],
        [
            Paragraph("<b>Live Demo:</b> <a href='https://shreyanshhhhhhhh.github.io/library-management-app/' color='#4f46e5'><u>https://shreyanshhhhhhhh.github.io/library-management-app/</u></a>", body_style),
            Paragraph("<b>GitHub Repo:</b> <a href='https://github.com/shreyanshhhhhhhh/library-management-app' color='#4f46e5'><u>shreyanshhhhhhhh/library-management-app</u></a>", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # ==================== EXECUTIVE SUMMARY ====================
    story.append(Paragraph("1. Executive Summary & Architecture", h1_style))
    story.append(Paragraph(
        "<b>LibraTrack</b> is a responsive, web-based single-page application (SPA) engineered to address the complete operational lifecycle of modern academic, public, and institutional libraries. Designed with a modular, event-driven client architecture, the system provides real-time state synchronization across catalog management, multi-copy inventory control, borrower membership tiers, circulation desk workflows (issues/returns), automated penalty calculations, and administrative analytics.",
        body_style
    ))
    story.append(Paragraph(
        "The system has been completely implemented and hosted live on a persistent public cloud platform (GitHub Pages). Every core requirement specified in the test guidelines—adding and deleting books, tracking issued books and inventory, calculating and managing fines, and handling multiple physical copies per ISBN title—has been comprehensively implemented, tested, and validated against standard institutional operational edge cases.",
        body_style
    ))
    
    # Tech Stack Highlights Table
    tech_data = [
        [Paragraph("<b>Component</b>", body_bold), Paragraph("<b>Technology / Implementation Details</b>", body_bold)],
        [Paragraph("Frontend UI / Layout", body_style), Paragraph("HTML5 Semantic Architecture, Modern CSS3 with Custom Design Tokens (Flexbox & CSS Grid)", body_style)],
        [Paragraph("Client Architecture", body_style), Paragraph("Vanilla ECMAScript 6+ with modular controller pattern, zero heavy framework overhead", body_style)],
        [Paragraph("Data Persistence", body_style), Paragraph("Structured Client-Side Storage Schema with relational constraints, auto-increment keys, and foreign-key integrity", body_style)],
        [Paragraph("Analytics & Data Viz", body_style), Paragraph("Chart.js v4.4 integration rendering responsive doughnut & multi-series transaction bar charts", body_style)],
        [Paragraph("Deployment & Availability", body_style), Paragraph("Continuous Deployment via GitHub Pages (SSL secured, 24/7 uptime, 0-maintenance)", body_style)]
    ]
    tech_table = Table(tech_data, colWidths=[130, 374])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('TEXTCOLOR', (0,0), (-1,0), dark),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 0.5, border_col),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_col),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 14))

    # ==================== SECTION 2: REASONING BEHIND CHOICE OF FEATURES ====================
    story.append(Paragraph("2. Architectural Decisions & Feature Rationale", h1_style))
    story.append(Paragraph(
        "Every feature incorporated into LibraTrack was selected based on the daily workflow friction encountered by library administrative staff, librarians, and patrons. The rationale behind key design decisions is outlined below:",
        body_style
    ))
    
    features = [
        ("Multi-Copy Inventory Model (Abstract Title vs. Physical Copy):",
         "A prevalent failure mode in naive library software is treating a book record as a single entity with a binary 'available/issued' state. In real institutions, a library holds multiple copies (e.g., 5 copies of Cormen's <i>Algorithms</i>). LibraTrack distinguishes between Title Metadata (ISBN, Title, Author, Genre) and Copy Circulation. The system dynamically computes <code>Available Copies = Total Copies - Currently Active Issues</code>. This ensures exact availability reporting without duplicate catalog bloat."),
        
        ("Role-Based Borrowing Quotas & Tier Limits:",
         "Students, faculty, staff, and external members have fundamentally different borrowing needs. Faculty frequently require up to 10 research texts with extended loan periods, whereas students are limited to 3 books. Enforcing hard borrowing caps directly at the transaction creation level prevents collection monopolization and promotes equitable access."),
        
        ("Automated, Progressive Daily Fine Engine:",
         "Manual fine tracking leads to disputes, human calculation errors, and revenue leakage. LibraTrack features an automatic fine engine calibrated at ₹2/day for each day past the due date. Overdue durations are dynamically updated on the dashboard in real-time, calculated upon book check-in, and linked to member profiles until reconciled via cash, card, UPI, or an authorized librarian waiver."),
        
        ("Circulation Integrity Constraints (Preventing Invalid States):",
         "To guarantee database consistency, key defensive safeguards were built: (1) Books cannot be deleted if any copy is currently in circulation; (2) Total copies cannot be edited below the number of active issues; (3) A member cannot borrow two copies of the identical ISBN concurrently; (4) Members cannot be deleted while holding active loans or unsettled fines."),
        
        ("Unified Circulation Desk (Side-by-Side Issue & Return):",
         "Librarians constantly switch between checking out books for departing patrons and receiving returns from incoming patrons. Providing a single split-view circulation screen reduces navigation overhead and streamlines high-traffic front-desk operations."),
        
        ("Proactive Notification & Alert System:",
         "Rather than waiting for manual audits, the system scans active loans and surfaces color-coded notification pills: high-priority alerts for books already overdue, and advance reminders for loans due within 48 hours.")
    ]

    for title, desc in features:
        story.append(Paragraph(f"• <b>{title}</b> {desc}", bullet_style))
    
    story.append(Spacer(1, 14))

    # ==================== SECTION 3: COMPREHENSIVE USE-CASE & SCENARIO CATALOG ====================
    story.append(Paragraph("3. Matrix of Scenarios Accounted For in the Design", h1_style))
    story.append(Paragraph(
        "To ensure robust operation under edge conditions, the software accounts for 16 primary operational scenarios across catalog, member, circulation, and administrative workflows:",
        body_style
    ))

    scenario_data = [
        [Paragraph("<b>Scenario #</b>", body_bold), Paragraph("<b>Operational Scenario & Edge Condition</b>", body_bold), Paragraph("<b>System Behavior & Defensive Handling</b>", body_bold)],
        [
            Paragraph("SC-01", body_style),
            Paragraph("Adding a new book to catalog", body_style),
            Paragraph("Enforces ISBN uniqueness. Rejects duplicate ISBNs with alert; sets initial stock and shelf location.", body_style)
        ],
        [
            Paragraph("SC-02", body_style),
            Paragraph("Multi-copy book acquisition", body_style),
            Paragraph("Permits assigning total copies (N >= 1) to a single ISBN title. Displays live availability counter.", body_style)
        ],
        [
            Paragraph("SC-03", body_style),
            Paragraph("Editing book copies with active issues", body_style),
            Paragraph("Blocks admin from reducing copies below the number of active loans to prevent negative availability.", body_style)
        ],
        [
            Paragraph("SC-04", body_style),
            Paragraph("Attempted deletion of circulating book", body_style),
            Paragraph("Rejects deletion with an informative toast message showing exactly how many copies are still checked out.", body_style)
        ],
        [
            Paragraph("SC-05", body_style),
            Paragraph("Member registration & duplicate checks", body_style),
            Paragraph("Validates unique email address and sets configurable borrowing quotas based on member category.", body_style)
        ],
        [
            Paragraph("SC-06", body_style),
            Paragraph("Student vs. Faculty differential quotas", body_style),
            Paragraph("Preconfigures Student cap at 3 books and Faculty cap at 10 books. Enforces cap at issue dropdown.", body_style)
        ],
        [
            Paragraph("SC-07", body_style),
            Paragraph("Borrowing limit exhaustion", body_style),
            Paragraph("Disables member in the checkout selector once current issues equal max allowed books.", body_style)
        ],
        [
            Paragraph("SC-08", body_style),
            Paragraph("Attempt to issue fully checked-out book", body_style),
            Paragraph("Books with 0 available copies are marked disabled in selection lists, preventing overselling.", body_style)
        ],
        [
            Paragraph("SC-09", body_style),
            Paragraph("Duplicate checkout prevention", body_style),
            Paragraph("Prevents issuing another copy of the same book to a patron who already holds an active copy.", body_style)
        ],
        [
            Paragraph("SC-10", body_style),
            Paragraph("Overdue check-in with penalty", body_style),
            Paragraph("Calculates days overdue against system date, generates ₹2/day fine, and prompts for payment reconciliation.", body_style)
        ],
        [
            Paragraph("SC-11", body_style),
            Paragraph("Timely return (Zero fine)", body_style),
            Paragraph("Marks loan as returned on time, restores book copy to available inventory pool with zero fine penalty.", body_style)
        ],
        [
            Paragraph("SC-12", body_style),
            Paragraph("Multi-channel fine settlement", body_style),
            Paragraph("Supports Cash, UPI, Card, and Librarian Waiver. Generates formal payment audit record with payment ID.", body_style)
        ],
        [
            Paragraph("SC-13", body_style),
            Paragraph("Borrowing attempt with pending fines", body_style),
            Paragraph("Displays contextual warning banner showing patron's outstanding balance before proceeding with new loan.", body_style)
        ],
        [
            Paragraph("SC-14", body_style),
            Paragraph("Deleting member with active obligations", body_style),
            Paragraph("Strictly prohibits deleting any member profile that holds active loans or unsettled fines.", body_style)
        ],
        [
            Paragraph("SC-15", body_style),
            Paragraph("Advance expiration alert (48-hour notice)", body_style),
            Paragraph("Surfaces notification banner highlighting upcoming due dates before penalties begin accruing.", body_style)
        ],
        [
            Paragraph("SC-16", body_style),
            Paragraph("Audit trail & operational reporting", body_style),
            Paragraph("Maintains immutable historical logs with real-time analytics for genre volume and borrowing frequency.", body_style)
        ]
    ]

    sc_table = Table(scenario_data, colWidths=[45, 185, 274])
    sc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('TEXTCOLOR', (0,0), (-1,0), dark),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BOX', (0,0), (-1,-1), 0.5, border_col),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_col),
    ]))
    story.append(sc_table)
    story.append(Spacer(1, 14))

    # ==================== SECTION 4: SCREENSHOTS & FEATURE RENDERS ====================
    story.append(PageBreak())
    story.append(Paragraph("4. Feature Walkthrough & System Renders", h1_style))
    story.append(Paragraph(
        "Below are high-resolution captures of the live application demonstrating each window, modal, interactive state, and report view in strict accordance with the evaluation criteria:",
        body_style
    ))
    story.append(Spacer(1, 6))

    renders = [
        ("01_dashboard.png", "Figure 1: Executive Dashboard", "Displays high-level operational KPIs (Total Books, Available Stock, Active Issues, Overdue Count, Member Total, Outstanding Fines), recent circulation feed, and immediate overdue action list."),
        ("02_book_catalog.png", "Figure 2: Book Catalog & Multi-Copy Inventory", "Tabular view displaying book metadata, ISBN, genre classification, total copies, live available copy badges, and action controls (Inspect, Modify, Remove)."),
        ("03_add_book_modal.png", "Figure 3: Book Registration Modal", "Form capturing Title, Author, ISBN, Classification, Publisher, Publication Year, Total Physical Copies, and Shelf Rack Location with field validation."),
        ("04_book_details_modal.png", "Figure 4: Deep Book Inspection & Copy Tracking", "Detailed dialog showing book metadata and a live table of which members currently possess specific copies of this ISBN, including due dates and overdue statuses."),
        ("05_members_management.png", "Figure 5: Member Directory & Quota Monitoring", "Directory of library patrons segmented by classification (Student, Faculty, Staff, External) displaying contact details, quota usage (e.g. 1/3), and outstanding liabilities."),
        ("06_add_member_modal.png", "Figure 6: Member Registration Modal", "Form for onboarding patrons with contact verification, category assignment, and custom maximum book limits based on institutional tier."),
        ("07_member_details_modal.png", "Figure 7: Member Profile & Complete Borrowing Dossier", "Shows member metadata, active borrowing quota utilization, unpaid fine balances, and complete lifetime borrowing and return history."),
        ("08_issue_return_workflow.png", "Figure 8: Unified Circulation Desk (Issue & Return)", "Split-screen interface allowing staff to simultaneously execute check-outs and check-ins without switching pages, significantly cutting desk turnaround time."),
        ("09_issue_book_form.png", "Figure 9: Validated Book Check-Out Flow", "Demonstrates dynamic validation during checkout: surfaces member quota status, warns of existing fines, and sets borrowing period."),
        ("10_return_fine_calculation.png", "Figure 10: Check-In & Automated Overdue Fine Calculation", "Selecting an overdue check-in triggers automatic computation of days overdue and applies penalty according to the standard fine schedule (₹2/day)."),
        ("11_transactions_history.png", "Figure 11: Transaction Ledger & Audit Trail", "Filterable audit log documenting every book check-out and check-in with transaction ID, patron, issue date, due date, return date, status, and fine assessment."),
        ("12_fines_management.png", "Figure 12: Fines Management & Revenue Tracking", "Dedicated accounts module tracking Total Pending Fines, Total Collected Fines, current fine rate, active overdue accounts, and payment reconciliation history."),
        ("13_pay_fine_modal.png", "Figure 13: Multi-Channel Fine Payment Reconciliation", "Modal for settling accrued fines with support for Cash, UPI, Card, or authorized Librarian Waivers, recording payment IDs into financial records."),
        ("14_reports_analytics.png", "Figure 14: Administrative Analytics & Visual Reports", "Interactive Chart.js visualizations presenting collection composition by genre, 6-month circulation volume trends, top borrowed titles, and most active patrons."),
        ("15_notifications_panel.png", "Figure 15: Proactive Alert & Notification Center", "Top-level notification panel detailing overdue emergencies and advance 48-hour return reminders for desk staff follow-up.")
    ]

    for filename, fig_title, fig_desc in renders:
        img_path = os.path.join(img_dir, filename)
        if os.path.exists(img_path):
            img = Image(img_path, width=490, height=270)
            render_block = [
                Paragraph(f"<b>{fig_title}</b>", h2_style),
                img,
                Paragraph(f"<i>{fig_desc}</i>", caption_style),
                Spacer(1, 8)
            ]
            story.append(KeepTogether(render_block))
        else:
            story.append(Paragraph(f"[Missing Image: {filename}]", caption_style))

    # ==================== SECTION 5: CONCLUSION & VERIFICATION ====================
    story.append(Spacer(1, 10))
    story.append(Paragraph("5. Live Verification & Evaluation Summary", h1_style))
    story.append(Paragraph(
        "All features demonstrated in this report are live and publicly accessible. Evaluators are invited to test the interactive workflow in real time:",
        body_style
    ))
    
    verify_data = [
        [Paragraph("<b>Resource</b>", body_bold), Paragraph("<b>Hyperlink / Access Point</b>", body_bold)],
        [
            Paragraph("Live Web Application", body_style),
            Paragraph("<a href='https://shreyanshhhhhhhh.github.io/library-management-app/' color='#4f46e5'><u>https://shreyanshhhhhhhh.github.io/library-management-app/</u></a>", body_style)
        ],
        [
            Paragraph("Source Code Repository", body_style),
            Paragraph("<a href='https://github.com/shreyanshhhhhhhh/library-management-app' color='#4f46e5'><u>https://github.com/shreyanshhhhhhhh/library-management-app</u></a>", body_style)
        ],
        [
            Paragraph("One-Click Demo Loading", body_style),
            Paragraph("Click <b>Quick Action → Load Sample Data</b> on the web app to populate test state.", body_style)
        ]
    ]
    verify_table = Table(verify_data, colWidths=[150, 354])
    verify_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 0.5, border_col),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_col),
    ]))
    story.append(verify_table)
    story.append(Spacer(1, 15))
    story.append(Paragraph("<i>Prepared for Azista Space — Written Assessment Evaluation. All rights reserved.</i>", ParagraphStyle('FooterNote', parent=caption_style, alignment=0)))

    # Build Document with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {pdf_path}")

if __name__ == '__main__':
    build_pdf()
