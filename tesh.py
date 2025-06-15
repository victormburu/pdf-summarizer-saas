# Remove emoji or special unicode characters not supported by latin-1
import re

def strip_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

# Clean all text blocks for ASCII only
profile = strip_non_ascii(profile)
core_skills = strip_non_ascii(core_skills)
experience = strip_non_ascii(experience)
education = strip_non_ascii(education)
certifications = strip_non_ascii(certifications)
tools = strip_non_ascii(tools)
development = strip_non_ascii(development)
volunteer = strip_non_ascii(volunteer)
interests = strip_non_ascii(interests)
references = strip_non_ascii(references)

# Recreate the PDF with sanitized text
pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

pdf.add_section("Professional Summary", profile)
pdf.add_section("Core Skills", core_skills)
pdf.add_section("Professional Experience", experience)
pdf.add_section("Education", education)
pdf.add_section("Certifications", certifications)
pdf.add_section("Tools & Tech", tools)
pdf.add_section("Professional Development", development)
pdf.add_section("Volunteer Work", volunteer)
pdf.add_section("Personal Interests", interests)
pdf.add_section("References", references)

# Save the final cleaned PDF
pdf_path = "/mnt/data/Teresia_Njeri_Muthoni_Resume.pdf"
pdf.output(pdf_path)

pdf_path
