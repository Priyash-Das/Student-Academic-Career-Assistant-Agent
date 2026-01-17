from resume_builder.core.resume_schema import (
    ResumeSchema,
    ExperienceItem,
    ProjectItem,
    EducationItem,
    Skills
)
class ResumeValidator:
    @staticmethod
    def _clean_list(items):
        return [item for item in items if item]
    @staticmethod
    def _clean_bullets(bullets):
        return [b.strip() for b in bullets if isinstance(b, str) and b.strip()]
    @classmethod
    def validate(cls, resume: ResumeSchema) -> ResumeSchema:
        resume.header.name = resume.header.name.strip()
        resume.header.address = resume.header.address.strip()
        resume.header.phone = resume.header.phone.strip()
        resume.header.email = resume.header.email.strip()
        resume.header.linkedin = resume.header.linkedin.strip()
        resume.header.github = resume.header.github.strip()
        resume.summary = resume.summary.strip()
        cleaned_experience = []
        for exp in resume.experience:
            exp.role = exp.role.strip()
            exp.company = exp.company.strip()
            exp.location = exp.location.strip()
            exp.dates = exp.dates.strip()
            exp.bullets = cls._clean_bullets(exp.bullets)
            if exp.role or exp.company or exp.bullets:
                cleaned_experience.append(exp)
        resume.experience = cleaned_experience
        cleaned_projects = []
        for proj in resume.projects:
            proj.title = proj.title.strip()
            proj.tech = proj.tech.strip()
            proj.bullets = cls._clean_bullets(proj.bullets)
            if proj.title or proj.bullets:
                cleaned_projects.append(proj)
        resume.projects = cleaned_projects
        cleaned_education = []
        for edu in resume.education:
            edu.degree = edu.degree.strip()
            edu.institution = edu.institution.strip()
            edu.year = edu.year.strip()
            edu.details = cls._clean_bullets(edu.details)
            if edu.degree or edu.institution:
                cleaned_education.append(edu)
        resume.education = cleaned_education
        resume.skills.programming_languages = cls._clean_list(resume.skills.programming_languages)
        resume.skills.frameworks_libraries = cls._clean_list(resume.skills.frameworks_libraries)
        resume.skills.tools_technologies = cls._clean_list(resume.skills.tools_technologies)
        resume.skills.methodologies = cls._clean_list(resume.skills.methodologies)
        resume.certifications = cls._clean_list(resume.certifications)
        resume.hobbies = cls._clean_list(resume.hobbies)
        resume.career_goal = resume.career_goal.strip()
        return resume