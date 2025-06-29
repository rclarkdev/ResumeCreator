import os
from textblob import TextBlob

def get_input(prompt):
    return input(f"{prompt.strip()} ").strip()

def collect_contact_info():
    print("\n--- Contact Information ---")
    return {
        "name": get_input("Full Name:"),
        "email": get_input("Email Address:"),
        "phone": get_input("Phone Number:"),
        "location": get_input("Location (City, State):"),
        "linkedin": get_input("LinkedIn URL (optional):"),
        "github": get_input("GitHub URL (optional):")
    }

def collect_summary():
    print("\n--- Professional Summary / Objective ---")
    skip = get_input("Would you like to skip the summary section? (yes/no):")
    if skip.lower() == 'yes':
        return ""
    return get_input("Enter a brief summary or career objective:")

def collect_skills():
    print("\n--- Skills ---")
    print("Enter your skills as comma-separated lists.")
    print("Each list will appear as a bullet point.")
    print("Type 'done' when finished.\n")

    skill_groups = []

    while True:
        raw_input = get_input("Enter skills (or type 'done' to finish):")
        if raw_input.lower() == 'done':
            break

        # Split and correct individual skills
        corrected = []
        for skill in raw_input.split(','):
            skill = skill.strip()
            if skill:
                corrected_skill = str(TextBlob(skill).correct())
                corrected.append(corrected_skill)

        if corrected:
            skill_groups.append(', '.join(corrected))

    print("\n✅ Final Skill Groups (as bullet points):")
    for group in skill_groups:
        print(f" - {group}")

    return skill_groups

def collect_experience():
    print("\n--- Work Experience ---")
    experiences = []

    while True:
        print("\nEnter details for a new job:")
        job = {
            "job_title": get_input("Job Title:"),
            "company": get_input("Company Name:"),
            "location": get_input("Location (City, State):"),
            "start_date": get_input("Start Date (e.g., Jan 2020):"),
            "end_date": get_input("End Date (or 'Present'):"),
            "bullets": [],
            "skills": []
        }

        # Add job description bullets
        print("\nEnter bullet points describing your responsibilities and achievements:")
        while True:
            bullet = get_input("Add a bullet (or type 'done' to finish):")
            if bullet.lower() == 'done':
                break
            job["bullets"].append(bullet)

        # Add skills for this job
        print("\nNow add any specific skills or technologies used in this role:")
        while True:
            skill = get_input("Add a skill used in this job (or type 'done' to finish):")
            if skill.lower() == 'done':
                break
            job["skills"].append(skill)

        experiences.append(job)

        # Ask if user wants to add another job
        more = get_input("Would you like to add another job? (yes/no):")
        if more.lower() != 'yes':
            break

    return experiences


def collect_education():
    print("\n--- Education ---")
    education = []
    while True:
        school = {
            "degree": get_input("Degree (e.g., B.S. in Computer Science):"),
            "institution": get_input("University/College Name:"),
            "location": get_input("Location (City, State):"),
            "graduation_year": get_input("Graduation Year:")
        }
        education.append(school)
        more = get_input("Would you like to add another degree? (yes/no):")
        if more.lower() != 'yes':
            break
    return education

def collect_certifications():
    print("\n--- Certifications ---")
    certs = []
    use = get_input("Would you like to add any certifications? (yes/no):")
    if use.lower() != 'yes':
        return certs
    while True:
        cert = get_input("Enter a certification (or type 'done' to finish):")
        if cert.lower() == 'done':
            break
        if cert:
            certs.append(cert)
    return certs

def collect_projects():
    print("\n--- Projects ---")
    projects = []
    use = get_input("Would you like to add any projects? (yes/no):")
    if use.lower() != 'yes':
        return projects
    while True:
        name = get_input("Project Name (or type 'done' to finish):")
        if name.lower() == 'done':
            break
        description = get_input("Brief Description:")
        tech_stack = get_input("Technologies Used:")
        projects.append({
            "name": name,
            "description": description,
            "tech_stack": tech_stack
        })
    return projects

def generate_html(resume):
    contact = resume['contact_info']
    summary = resume['summary']
    skills = resume['skills']
    experience = resume['experience']
    education = resume['education']
    certifications = resume['certifications']
    projects = resume['projects']

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{contact['name']} - Resume</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #f7f7f7;
            color: #333;
        }}
        .container {{
            background: #fff;
            padding: 30px;
            border-radius: 10px;
            max-width: 900px;
            margin: auto;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1, h2 {{
            color: #2c3e50;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        ul {{
            padding-left: 20px;
        }}
        .job, .edu, .project {{
            margin-bottom: 15px;
        }}
        .job-title, .degree {{
            font-weight: bold;
        }}
        .info {{
            font-style: italic;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{contact['name']}</h1>
        <p>{contact['location']} | {contact['email']} | {contact['phone']}</p>
        <p>{' | '.join(filter(None, [contact.get('linkedin', '').strip(), contact.get('github', '').strip()]))}</p>

        <div class="section">
            <h2>Professional Summary</h2>
            <p>{summary}</p>
        </div>

        <div class="section">
            <h2>Skills</h2>
            <ul>
                {''.join(f"<li>{skill}</li>" for skill in skills)}
            </ul>
        </div>

        <div class="section">
            <h2>Work Experience</h2>
            {''.join(f"""
            <div class='job'>
                <div class='job-title'>{job['job_title']} - {job['company']}</div>
                <div class='info'>{job['location']} | {job['start_date']} - {job['end_date']}</div>
                <ul>{''.join(f"<li>{bullet}</li>" for bullet in job['bullets'])}</ul>
                <p><strong>Skills:</strong> {', '.join(job['skills'])}</p>
            </div>
            """ for job in experience)}
        </div>

        <div class="section">
            <h2>Education</h2>
            {''.join(f"""
            <div class='edu'>
                <div class='degree'>{edu['degree']}</div>
                <div class='info'>{edu['institution']}, {edu['location']} ({edu['graduation_year']})</div>
            </div>
            """ for edu in education)}
        </div>
"""

    # Optional: Certifications
    if certifications:
        html += f"""
        <div class="section">
            <h2>Certifications</h2>
            <ul>
                {''.join(f"<li>{cert}</li>" for cert in certifications)}
            </ul>
        </div>
"""

    # Optional: Projects
    if projects:
        html += f"""
        <div class="section">
            <h2>Projects</h2>
            {''.join(f"""
            <div class='project'>
                <div class='project-title'><strong>{proj['name']}</strong></div>
                <p>{proj['description']}</p>
                <p><em>Tech: {proj['tech_stack']}</em></p>
            </div>
            """ for proj in projects)}
        </div>
"""

    html += """
    </div>
</body>
</html>
"""
    return html


def save_html(content, filename="resume.html"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n✅ Resume saved as {filename}")

def main():
    print("Welcome to the Resume Generator!\n")
    resume_data = {
        "contact_info": collect_contact_info(),
        "summary": collect_summary(),
        "skills": collect_skills(),
        "experience": collect_experience(),
        "education": collect_education(),
        "certifications": collect_certifications(),
        "projects": collect_projects()
    }

    html_resume = generate_html(resume_data)
    save_html(html_resume)

if __name__ == "__main__":
    main()
