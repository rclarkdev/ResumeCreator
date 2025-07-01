import os
from textblob import TextBlob
from bs4 import BeautifulSoup

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

from bs4 import BeautifulSoup

from bs4 import BeautifulSoup
import os

def load_existing_resume(filename):
    if not os.path.exists(filename):
        print(f"❌ File '{filename}' not found.")
        return None

    with open(filename, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    container = soup.find("div", class_="container")

    # --- Contact Info ---
    name = container.find("h1").get_text(strip=True)

    # The next two <p> tags hold location/email/phone and optional links
    info_paragraphs = container.find_all("p", limit=2)
    location_email_phone = info_paragraphs[0].get_text(strip=True)
    contact_parts = [part.strip() for part in location_email_phone.split('|')]
    location = contact_parts[0] if len(contact_parts) > 0 else ""
    email = contact_parts[1] if len(contact_parts) > 1 else ""
    phone = contact_parts[2] if len(contact_parts) > 2 else ""

    linkedin = ""
    github = ""

    if len(info_paragraphs) > 1:
        links = [link.strip() for link in info_paragraphs[1].get_text(strip=True).split('|')]
        for link in links:
            if "linkedin.com" in link:
                linkedin = link
            elif "github.com" in link:
                github = link

    # --- Professional Summary ---
    summary_section = container.find("h2", string="Professional Summary")
    summary = ""
    if summary_section:
        summary_paragraph = summary_section.find_next("p")
        if summary_paragraph:
            summary = summary_paragraph.get_text(strip=True)

    # --- Skills ---
    skills = []
    skills_section = container.find("h2", string="Skills")
    if skills_section:
        ul = skills_section.find_next("ul")
        if ul:
            skills = [li.get_text(strip=True) for li in ul.find_all("li")]

    # --- Work Experience ---
    experience = []
    experience_section = container.find("h2", string="Work Experience")
    if experience_section:
        job_divs = experience_section.find_all_next("div", class_="job")
        for job_div in job_divs:
            title_line = job_div.find("div", class_="job-title").get_text(strip=True)
            info_line = job_div.find("div", class_="info").get_text(strip=True)

            # Extract title and company
            if " - " in title_line:
                job_title, company = map(str.strip, title_line.split(" - ", 1))
            else:
                job_title = title_line
                company = ""

            # Extract location and dates
            if "|" in info_line:
                location_part, date_range = map(str.strip, info_line.split("|", 1))
                if " - " in date_range:
                    start_date, end_date = map(str.strip, date_range.split(" - ", 1))
                else:
                    start_date = date_range
                    end_date = ""
                location = location_part
            else:
                location = info_line
                start_date = ""
                end_date = ""

            # Extract bullet points
            bullets = []
            ul = job_div.find("ul")
            if ul:
                bullets = [li.get_text(strip=True) for li in ul.find_all("li")]

            # Extract skills (optional)
            skills_list = []
            skills_p = job_div.find("p")
            if skills_p and "Skills:" in skills_p.get_text():
                skill_text = skills_p.get_text().replace("Skills:", "").strip()
                if skill_text:
                    skills_list = [s.strip() for s in skill_text.split(",")]

            experience.append({
                "job_title": job_title,
                "company": company,
                "location": location,
                "start_date": start_date,
                "end_date": end_date,
                "bullets": bullets,
                "skills": skills_list
            })

    # --- Education ---
    education = []
    education_section = container.find("h2", string="Education")
    if education_section:
        edu_divs = education_section.find_all_next("div", class_="edu")
        for edu_div in edu_divs:
            degree = edu_div.find("div", class_="degree").get_text(strip=True)
            info = edu_div.find("div", class_="info").get_text(strip=True)
            institution = location = grad_year = ""

            # Parse something like "University of Utah, Salt Lake City, UT (2012)"
            if "(" in info and ")" in info:
                pre_paren, grad_year = info.rsplit("(", 1)
                grad_year = grad_year.replace(")", "").strip()
                if ", " in pre_paren:
                    parts = pre_paren.split(", ")
                    institution = parts[0].strip()
                    location = ", ".join(parts[1:]).strip()
                else:
                    institution = pre_paren.strip()
            else:
                institution = info.strip()

            education.append({
                "degree": degree,
                "institution": institution,
                "location": location,
                "graduation_year": grad_year
            })

    return {
        "contact_info": {
            "name": name,
            "location": location,
            "email": email,
            "phone": phone,
            "linkedin": linkedin,
            "github": github
        },
        "summary": summary,
        "skills": skills,
        "experience": experience,
        "education": education,
        "certifications": [],  # still not parsed from HTML
        "projects": []          # still not parsed from HTML
    }

def review_section(section_name, existing_value, collect_function):
    print(f"\n--- {section_name} ---")
    
    # Display current value nicely depending on type
    if isinstance(existing_value, list):
        if not existing_value:
            print("[None]")
        else:
            if section_name == "Skills":
                for i, group in enumerate(existing_value, 1):
                    print(f"{i}. {group}")
            elif section_name == "Work Experience":
                for i, job in enumerate(existing_value, 1):
                    print(f"{i}. {job['job_title']} at {job['company']} ({job['start_date']} - {job['end_date']})")
            elif section_name == "Education":
                for i, edu in enumerate(existing_value, 1):
                    print(f"{i}. {edu['degree']} at {edu['institution']} ({edu['graduation_year']})")
            elif section_name == "Certifications" or section_name == "Projects":
                for i, item in enumerate(existing_value, 1):
                    if section_name == "Projects":
                        print(f"{i}. {item['name']} - {item['description']}")
                    else:
                        print(f"{i}. {item}")
            else:
                print(existing_value)
    elif isinstance(existing_value, dict):
        for k,v in existing_value.items():
            print(f"{k.title()}: {v}")
    else:
        print(existing_value if existing_value else "[None]")

    choice = get_input(f"Do you want to edit the {section_name}? (yes/no):")
    if choice.lower() == "yes":
        return collect_function()
    else:
        print(f"Skipping {section_name}...\n")
        return existing_value


def edit_skills(skills):
    answer = get_input("Do you want to edit the Skills? (yes/no):")
    if answer.lower() != "yes":
        return skills
    
    print("Current Skills:")
    for i, group in enumerate(skills, 1):
        print(f"{i}. {group}")
    
    # For simplicity, let's re-collect all skills (you can implement fine editing if you want)
    return collect_skills()

def edit_experience(experience):
    print("\n--- Work Experience ---")

    while True:
        # Display current experience entries
        if not experience:
            print("[No work experience entered yet]")
        else:
            for i, job in enumerate(experience, 1):
                print(f"{i}. {job['job_title']} at {job['company']} ({job['start_date']} - {job['end_date']})")

        print("\nOptions:")
        print(" - Enter a number to view/edit a job")
        print(" - Type 'add' to add a new job")
        print(" - Type 'delete' to delete a job")
        print(" - Type 'done' when finished")

        action = get_input("Your choice:")

        if action.lower() == "done":
            break
        elif action.lower() == "add":
            print("\nAdding a new job:")
            new_job = collect_single_job()
            experience.append(new_job)
        elif action.lower() == "delete":
            index = get_input("Enter the number of the job to delete:")
            if index.isdigit() and 1 <= int(index) <= len(experience):
                deleted = experience.pop(int(index) - 1)
                print(f"Deleted: {deleted['job_title']} at {deleted['company']}")
            else:
                print("❌ Invalid job number.")
        elif action.isdigit():
            index = int(action) - 1
            if 0 <= index < len(experience):
                job = experience[index]
                print(f"\n--- Editing Job {index + 1}: {job['job_title']} at {job['company']} ---")
                print(f"Location: {job['location']}")
                print(f"Dates: {job['start_date']} - {job['end_date']}")
                print("Responsibilities:")
                for b in job["bullets"]:
                    print(f" - {b}")
                print("Skills: " + ", ".join(job["skills"]))

                choice = get_input("Do you want to edit this job? (yes/no):")
                if choice.lower() == "yes":
                    experience[index] = collect_single_job()
            else:
                print("❌ Invalid job number.")
        else:
            print("❌ Unrecognized command.")
    return experience

def collect_single_job():
    print("\nEnter details for the job:")
    job = {
        "job_title": get_input("Job Title:"),
        "company": get_input("Company Name:"),
        "location": get_input("Location (City, State):"),
        "start_date": get_input("Start Date (e.g., Jan 2020):"),
        "end_date": get_input("End Date (or 'Present'):"),

        "bullets": [],
        "skills": []
    }

    print("\nEnter bullet points describing your responsibilities and achievements:")
    while True:
        bullet = get_input("Add a bullet (or type 'done' to finish):")
        if bullet.lower() == 'done':
            break
        job["bullets"].append(bullet)

    print("\nNow add any specific skills or technologies used in this role:")
    while True:
        skill = get_input("Add a skill used in this job (or type 'done' to finish):")
        if skill.lower() == 'done':
            break
        job["skills"].append(skill)

    return job

# Similar functions for education, projects, etc.

def edit_resume_sections(resume):
    # Contact Info needs a custom collector that returns a dict
    resume['contact_info'] = review_section("Contact Information", resume.get('contact_info', {}), collect_contact_info)
    
    resume['summary'] = review_section("Professional Summary", resume.get('summary', ''), collect_summary)
    
    resume['skills'] = review_section("Skills", resume.get('skills', []), collect_skills)
    
    resume['experience'] = review_section("Work Experience", resume.get('experience', []), lambda: edit_experience(resume['experience']))
    
    resume['education'] = review_section("Education", resume.get('education', []), collect_education)
    
    resume['certifications'] = review_section("Certifications", resume.get('certifications', []), collect_certifications)
    
    resume['projects'] = review_section("Projects", resume.get('projects', []), collect_projects)
    
    return resume

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
        .header-info {{
            text-align: center;
            margin-bottom: 30px;
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
        <div class="header-info">
            <h1>{contact['name']}</h1>
            <p>{contact['location']} | {contact['email']} | {contact['phone']}</p>
            <p>{' | '.join(filter(None, [contact.get('linkedin', '').strip(), contact.get('github', '').strip()]))}</p>
        </div>

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
                {f"<p><strong>Skills:</strong> {', '.join(job['skills'])}</p>" if job['skills'] else ""}
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

    if certifications:
        html += f"""
        <div class="section">
            <h2>Certifications</h2>
            <ul>
                {''.join(f"<li>{cert}</li>" for cert in certifications)}
            </ul>
        </div>
"""

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

    choice = get_input("Would you like to (1) create a new resume or (2) edit an existing resume? Enter 1 or 2:")
    
    if choice == '2':
        filename = get_input("Enter the filename of the resume to load (include .html extension):")
        resume_data = load_existing_resume(filename)
        if resume_data is None:
            print("Failed to load resume. Starting fresh.")
            resume_data = {
                "contact_info": {},
                "summary": "",
                "skills": [],
                "experience": [],
                "education": [],
                "certifications": [],
                "projects": []
            }
        else:
            # Now allow user to edit each section interactively
            resume_data = edit_resume_sections(resume_data)
    else:
        # New resume flow — collect everything from scratch
        resume_data = {
            "contact_info": collect_contact_info(),
            "summary": collect_summary(),
            "skills": collect_skills(),
            "experience": collect_experience(),
            "education": collect_education(),
            "certifications": collect_certifications(),
            "projects": collect_projects()
        }

    # Generate and save resume
    html_resume = generate_html(resume_data)
    save_html(html_resume)


if __name__ == "__main__":
    main()
