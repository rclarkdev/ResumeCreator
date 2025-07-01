##Interactive Resume Builder (Python CLI Tool)
A simple and interactive command-line tool written in Python to help professionals—especially software engineers—create polished, HTML-based resumes. The tool guides you through each resume section, collects your data, and generates a clean, styled resume.html file that you can easily open or share.

##Features
Interactive prompts for comprehensive resume sections:

Contact Information

Professional Summary / Objective (optional)

Skills (spell-corrected and grouped as bullet points)

Work Experience (with multi-line responsibilities and skills per role)

Education

Optional Certifications and Projects

Ability to load and edit existing resumes from an HTML file, with in-place editing of all sections

Clean, professional resume layout with responsive HTML/CSS styling

Omits empty fields or sections for a clean final look

Saves resume as a standalone resume.html file, ready to open in any browser

##Requirements
Python 3.7 or higher

TextBlob library for spell correction

BeautifulSoup4 for parsing existing HTML resumes

You can install dependencies via:

bash
Copy
Edit
pip install textblob beautifulsoup4

##Installation & Usage

Clone the repository and run the script:

bash
Copy
Edit
git clone https://github.com/yourusername/resume-builder.git
cd resume-builder
python resume_builder.py
Choose to create a new resume or edit an existing resume HTML file

Follow the interactive prompts to enter or update your information

Your resume will be saved as resume.html in the current directory

##Notes

When entering skills, you can add multiple comma-separated skills per line; the tool will spell-check and organize them into bullet groups.

Work experience entries support detailed bullet points and associated skills per job.

Optional sections like Certifications and Projects can be skipped if you don’t have entries.

Editing existing resumes requires the input HTML to follow the tool’s specific markup structure (see generate_html function for reference).

📄License
MIT License
