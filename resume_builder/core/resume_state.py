from typing import Optional, List
from resume_builder.core.resume_schema import ResumeSchema, Skills
class ResumeState:
    def __init__(self):
        self._resume: Optional[ResumeSchema] = None
    def is_initialized(self) -> bool:
        return self._resume is not None
    def set_resume(self, resume: ResumeSchema):
        self._resume = resume
    def get_resume(self) -> ResumeSchema:
        if not self._resume:
            raise RuntimeError("Resume state is not initialized")
        return self._resume
    def update_summary(self, summary: str):
        self.get_resume().summary = summary
    def update_experience(self, experience: List):
        self.get_resume().experience = experience
    def update_projects(self, projects: List):
        self.get_resume().projects = projects
    def update_education(self, education: List):
        self.get_resume().education = education
    def update_skills(self, skills: Skills):
        self.get_resume().skills = skills
    def update_certifications(self, certifications: List[str]):
        self.get_resume().certifications = certifications
    def update_hobbies(self, hobbies: List[str]):
        self.get_resume().hobbies = hobbies
    def update_career_goal(self, goal: str):
        self.get_resume().career_goal = goal
    def clear(self):
        self._resume = None