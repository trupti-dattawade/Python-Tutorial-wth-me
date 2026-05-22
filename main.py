import os
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

# PDF Libraries
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus.flowables import HRFlowable

# ------------------------------------------
# Load Environment Variables
# ------------------------------------------
load_dotenv()

# ------------------------------------------
# GROQ Configuration
# ------------------------------------------
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "llama-3.1-8b-instant"

# ------------------------------------------
# Supported File Extensions
# ------------------------------------------
SUPPORTED_EXTENSIONS = [
    ".py",
    ".txt",
    ".md",
    ".json",
    ".csv",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".java",
    ".sql",
    ".yaml",
    ".yml"
]


# ------------------------------------------
# Read File
# ------------------------------------------
def read_file(file_path):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            return file.read()

    except Exception as e:

        return f"Error Reading File: {e}"


# ------------------------------------------
# Analyze Folder
# ------------------------------------------
def analyze_folder(folder_path):

    project_data = ""

    for root, dirs, files in os.walk(folder_path):

        for file in files:

            extension = os.path.splitext(file)[1]

            if extension not in SUPPORTED_EXTENSIONS:
                continue

            file_path = os.path.join(root, file)

            print(f"Analyzing: {file_path}")

            content = read_file(file_path)

            # Limit file size
            content = content[:3000]

            project_data += f"""

================================================

FILE NAME:
{file}

FILE LOCATION:
{file_path}

FILE CONTENT:
{content}

================================================

"""

    return project_data


# ------------------------------------------
# Generate Report using GROQ
# ------------------------------------------
def generate_report(project_data):

    prompt = f"""
You are a professional enterprise project documentation specialist.

Analyze the provided project folder files and generate a complete professional project report.

IMPORTANT:
- Generate ONLY project-related report.
- Do NOT mention AI, Agent, KT Agent, Knowledge Transfer Agent.
- Do NOT dump raw code.
- Explain everything professionally.
- Make the report suitable for employee onboarding and project understanding.

The report must contain:

1. Executive Summary
2. Project Overview
3. Project Objective
4. Folder Structure Explanation
5. Important Files and Their Purpose
6. Workflow Explanation
7. Responsibilities and Operational Tasks
8. Setup and Execution Process
9. Dependencies and Technologies Used
10. Pending Tasks and Improvements
11. Best Practices
12. Troubleshooting Guide
13. Recommendations

Formatting Rules:
- Use professional corporate language.
- Use structured headings.
- Use bullet points.
- Explain technical details in simple language.
- Mention important files and locations.
- Keep report clean, readable, and highly professional.

PROJECT FILES:

{project_data}
"""

    response = client.chat.completions.create(

        model=MODEL,

        messages=[
            {
                "role": "system",
                "content": "You are a senior corporate project documentation specialist."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.1,
        max_tokens=4096
    )

    return response.choices[0].message.content


# ------------------------------------------
# Generate Professional PDF
# ------------------------------------------
def generate_pdf(report, folder_path):

    pdf_file = "Project_Report.pdf"

    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=35,
        leftMargin=35,
        topMargin=40,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()

    # --------------------------------------
    # Custom Styles
    # --------------------------------------
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        textColor=colors.white
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading1"],
        fontSize=15,
        leading=20,
        textColor=colors.HexColor("#0B3C5D"),
        spaceBefore=15,
        spaceAfter=10
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["BodyText"],
        fontSize=10,
        leading=18,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#333333")
    )

    elements = []

    # --------------------------------------
    # Header Design
    # --------------------------------------
    header = Table(
        [
            [
                Paragraph(
                    "<font color='white'><b>PROJECT REPORT</b></font>",
                    title_style
                ),
                Paragraph(
                    f"""
                    <font color='white'>
                    Generated Date:<br/>
                    {datetime.now().strftime('%d-%m-%Y %I:%M %p')}
                    </font>
                    """,
                    body_style
                )
            ]
        ],
        colWidths=[350, 150]
    )

    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0B3C5D")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
        ("TOPPADDING", (0, 0), (-1, -1), 18),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
    ]))

    elements.append(header)

    elements.append(Spacer(1, 20))

    # --------------------------------------
    # Project Information Table
    # --------------------------------------
    info_table = Table(
        [
            ["Folder Path", folder_path],
            ["Document Type", "Project Analysis Report"],
            ["Generated For", "Project Understanding & Continuity"],
        ],
        colWidths=[180, 320]
    )

    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#D9EAF4")),
        ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#B5C7D3")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
    ]))

    elements.append(info_table)

    elements.append(Spacer(1, 25))

    elements.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor("#C9D3DD")
        )
    )

    elements.append(Spacer(1, 20))

    # --------------------------------------
    # Report Content
    # --------------------------------------
    lines = report.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Detect headings
        if (
            "Summary" in line or
            "Overview" in line or
            "Objective" in line or
            "Workflow" in line or
            "Responsibilities" in line or
            "Guide" in line or
            "Practices" in line or
            "Dependencies" in line or
            "Recommendations" in line or
            "Tasks" in line
        ):

            elements.append(
                Paragraph(
                    f"<b>{line}</b>",
                    heading_style
                )
            )

        else:

            elements.append(
                Paragraph(
                    line,
                    body_style
                )
            )

        elements.append(Spacer(1, 8))

    # --------------------------------------
    # Footer
    # --------------------------------------
    elements.append(Spacer(1, 30))

    footer = Paragraph(
        """
        <font size=9 color='#666666'>
        Confidential Project Documentation — Internal Use Only
        </font>
        """,
        body_style
    )

    elements.append(footer)

    # Build PDF
    doc.build(elements)

    print("\nProfessional PDF Report Generated Successfully")
    print(f"Saved File: {pdf_file}")


# ------------------------------------------
# Main Function
# ------------------------------------------
def main():

    print("\n========== PROJECT REPORT GENERATOR ==========")

    folder_path = input(
        "\nEnter Project Folder Path: "
    ).strip()

    folder_path = folder_path.replace('"', "")

    # Validate Folder
    if not os.path.exists(folder_path):

        print("\nInvalid Folder Path")
        return

    print("\nScanning Project Files...\n")

    project_data = analyze_folder(folder_path)

    if not project_data:

        print("\nNo Supported Files Found")
        return

    print("\nGenerating Project Report...\n")

    report = generate_report(project_data)

    print("\nCreating Professional PDF...\n")

    generate_pdf(report, folder_path)

    print("\nProject Report Generated Successfully")


# ------------------------------------------
# Run Application
# ------------------------------------------
if __name__ == "__main__":
    main()
