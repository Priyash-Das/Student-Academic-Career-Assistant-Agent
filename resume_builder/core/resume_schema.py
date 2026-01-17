from dataclasses import dataclass, field
from typing import List, Dict, Optional
@dataclass
class Header:
    name: str = ""
    address: str = ""
    phone: str = ""
    email: str = ""
    linkedin: str = ""
    github: str = ""
@dataclass
class ExperienceItem:
    role: str = ""
    company: str = ""
    location: str = ""
    dates: str = ""
    bullets: List[str] = field(default_factory=list)
@dataclass
class ProjectItem:
    title: str = ""
    tech: str = ""
    bullets: List[str] = field(default_factory=list)
@dataclass
class EducationItem:
    degree: str = ""
    institution: str = ""
    year: str = ""
    details: List[str] = field(default_factory=list)
@dataclass
class Skills:
    programming_languages: List[str] = field(default_factory=list)
    frameworks_libraries: List[str] = field(default_factory=list)
    tools_technologies: List[str] = field(default_factory=list)
    methodologies: List[str] = field(default_factory=list)
@dataclass
class ResumeSchema:
    header: Header = field(default_factory=Header)
    summary: str = ""
    experience: List[ExperienceItem] = field(default_factory=list)
    projects: List[ProjectItem] = field(default_factory=list)
    education: List[EducationItem] = field(default_factory=list)
    skills: Skills = field(default_factory=Skills)
    certifications: List[str] = field(default_factory=list)
    hobbies: List[str] = field(default_factory=list)
    career_goal: str = "" 
    def to_dict(self) -> Dict:
        return {
            "header": {
                "name": self.header.name,
                "address": self.header.address,
                "phone": self.header.phone,
                "email": self.header.email,
                "linkedin": self.header.linkedin,
                "github": self.header.github,
            },
            "summary": self.summary,
            "experience": [{
                "role": exp.role,
                "company": exp.company,
                "location": exp.location,
                "dates": exp.dates,
                "bullets": exp.bullets
            } for exp in self.experience],
            "projects": [{
                "title": proj.title,
                "tech": proj.tech,
                "bullets": proj.bullets
            } for proj in self.projects],
            "education": [{
                "degree": edu.degree,
                "institution": edu.institution,
                "year": edu.year,
                "details": edu.details
            } for edu in self.education],
            "skills": {
                "programming_languages": self.skills.programming_languages,
                "frameworks_libraries": self.skills.frameworks_libraries,
                "tools_technologies": self.skills.tools_technologies,
                "methodologies": self.skills.methodologies
            },
            "certifications": self.certifications,
            "hobbies": self.hobbies,
            "career_goal": self.career_goal
        }
    @classmethod
    def from_dict(cls, data: Dict):
        resume = cls()
        header_data = data.get("header", {})
        resume.header = Header(
            name=header_data.get("name", ""),
            address=header_data.get("address", ""),
            phone=header_data.get("phone", ""),
            email=header_data.get("email", ""),
            linkedin=header_data.get("linkedin", ""),
            github=header_data.get("github", "")
        )
        resume.summary = data.get("summary", "")
        for exp_data in data.get("experience", []):
            resume.experience.append(ExperienceItem(
                role=exp_data.get("role", ""),
                company=exp_data.get("company", ""),
                location=exp_data.get("location", ""),
                dates=exp_data.get("dates", ""),
                bullets=exp_data.get("bullets", [])
            ))
        for proj_data in data.get("projects", []):
            resume.projects.append(ProjectItem(
                title=proj_data.get("title", ""),
                tech=proj_data.get("tech", ""),
                bullets=proj_data.get("bullets", [])
            ))
        for edu_data in data.get("education", []):
            resume.education.append(EducationItem(
                degree=edu_data.get("degree", ""),
                institution=edu_data.get("institution", ""),
                year=edu_data.get("year", ""),
                details=edu_data.get("details", [])
            ))
        skills_data = data.get("skills", {})
        resume.skills = Skills(
            programming_languages=skills_data.get("programming_languages", []),
            frameworks_libraries=skills_data.get("frameworks_libraries", []),
            tools_technologies=skills_data.get("tools_technologies", []),
            methodologies=skills_data.get("methodologies", [])
        )
        resume.certifications = data.get("certifications", [])
        resume.hobbies = data.get("hobbies", [])
        resume.career_goal = data.get("career_goal", "")
        return resume