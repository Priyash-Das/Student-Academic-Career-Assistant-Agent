import json
import random
from resume_builder.config.prompts import RESUME_SCHEMA_INSTRUCTION
from resume_builder.llm.llm_router import LLMRouter
from resume_builder.core.resume_schema import ResumeSchema, Header, ExperienceItem, ProjectItem, EducationItem, Skills
from resume_builder.core.resume_validator import ResumeValidator
class ResumeAgent:
    @classmethod
    def generate_demo_resume(cls) -> ResumeSchema:
        return cls._generate_fallback_demo_resume()
    @classmethod
    def generate_from_prompt(cls, user_prompt: str) -> ResumeSchema:
        if not user_prompt or not user_prompt.strip():
            return cls._generate_fallback_demo_resume()
        combined_prompt = f"""
        {RESUME_SCHEMA_INSTRUCTION}
        
        USER INFORMATION:
        {user_prompt}
        
        IMPORTANT:
        1. If the user provides specific information (name, education, experience, etc.), use it
        2. If not enough information is provided, use realistic placeholder data
        3. Always return valid JSON
        """
        try:
            raw_output = LLMRouter.generate_resume(combined_prompt)
            cleaned_output = cls._clean_llm_output(raw_output)
            parsed = json.loads(cleaned_output)
            resume = ResumeSchema.from_dict(parsed)
            return ResumeValidator.validate(resume)
        except Exception as e:
            print(f"LLM generation failed: {e}")
            try:
                return cls._extract_from_prompt(user_prompt)
            except:
                return cls._generate_fallback_demo_resume()
    @classmethod
    def _clean_llm_output(cls, raw_output: str) -> str:
        import re
        cleaned = raw_output.strip()
        cleaned = re.sub(r'^```json\s*', '', cleaned)
        cleaned = re.sub(r'^```\s*', '', cleaned)
        cleaned = re.sub(r'\s*```$', '', cleaned)
        json_pattern = r'(\{.*\}|\[.*\])'
        matches = re.findall(json_pattern, cleaned, re.DOTALL)
        if matches:
            cleaned = max(matches, key=len)
        return cleaned.strip()
    @classmethod
    def _extract_from_prompt(cls, prompt: str) -> ResumeSchema:
        prompt_lower = prompt.lower()
        resume = ResumeSchema()
        import re
        name_match = re.search(r'for\s+([A-Z][a-z]+\s+[A-Z][a-z]+)', prompt)
        if name_match:
            resume.header.name = name_match.group(1)
        else:
            resume.header.name = "John Doe"
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', prompt)
        if email_match:
            resume.header.email = email_match.group(0)
        else:
            resume.header.email = f"{resume.header.name.lower().replace(' ', '.')}@example.com"
        if any(word in prompt_lower for word in ['university', 'college', 'institute', 'bachelor', 'master', 'degree']):
            edu_patterns = [
                r'([BM]\.?Tech|Bachelor|Master|PhD).*?(?:in|at).*?([A-Z][a-zA-Z\s]+(?:University|Institute|College))',
                r'([A-Z][a-zA-Z\s]+(?:University|Institute|College)).*?([\d\.]+)\s*(?:CGPA|GPA)',
            ]
            for pattern in edu_patterns:
                match = re.search(pattern, prompt, re.IGNORECASE)
                if match:
                    degree = match.group(1) if match.lastindex >= 1 else "Bachelor's Degree"
                    institution = match.group(2) if match.lastindex >= 2 else "University"
                    resume.education.append(EducationItem(
                        degree=degree,
                        institution=institution,
                        year="",
                        details=[]
                    ))
                    break
        skill_categories = {
            'programming_languages': ['python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin', 'typescript', 'html', 'css', 'sql'],
            'frameworks_libraries': ['react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'laravel', 'bootstrap', 'tailwind', 'jquery'],
            'tools_technologies': ['git', 'github', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'mongodb', 'mysql', 'postgresql', 'redis', 'jenkins', 'figma'],
            'methodologies': ['agile', 'scrum', 'kanban', 'waterfall', 'ci/cd', 'tdd', 'bdd', 'devops']
        }
        for category, skills in skill_categories.items():
            found_skills = []
            for skill in skills:
                if skill in prompt_lower:
                    display_name = skill.upper() if skill in ['aws', 'gcp', 'ci/cd', 'tdd', 'bdd'] else skill.title()
                    found_skills.append(display_name)
            if found_skills:
                setattr(resume.skills, category, found_skills)
        if not any([resume.skills.programming_languages, resume.skills.frameworks_libraries, 
                   resume.skills.tools_technologies, resume.skills.methodologies]):
            resume.skills = Skills(
                programming_languages=["Python", "JavaScript"],
                frameworks_libraries=["React", "Node.js"],
                tools_technologies=["Git", "Docker"],
                methodologies=["Agile", "Scrum"]
            )
        resume.summary = f"Experienced professional with strong technical skills. {prompt[:100]}..."
        return resume
    @classmethod
    def _generate_fallback_demo_resume(cls) -> ResumeSchema:
        first_names = ["John", "Jane", "Alex", "Sarah", "Michael", "Emily", "David", "Jessica"]
        last_names = ["Doe", "Smith", "Johnson", "Williams", "Brown", "Davis", "Wilson", "Taylor"]
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        resume = ResumeSchema()
        resume.header.name = name
        resume.header.address = "123 Main Street, City, State 12345"
        resume.header.phone = f"({random.randint(200, 999)}) 555-{random.randint(1000, 9999)}"
        resume.header.email = f"{name.lower().replace(' ', '.')}@example.com"
        resume.header.linkedin = f"linkedin.com/in/{name.lower().replace(' ', '')}"
        resume.header.github = f"github.com/{name.lower().replace(' ', '')}"
        resume.summary = f"Results-driven Software Engineer with {random.randint(2, 8)}+ years of experience in full-stack development. Proven track record of building scalable applications. Strong expertise in Python, JavaScript, and cloud technologies. Seeking to leverage technical skills at a forward-thinking tech company."
        companies = ["Tech Innovations Inc.", "Digital Solutions LLC", "Cloud Systems Corp", "Data Dynamics Ltd"]
        roles = ["Senior Software Engineer", "Software Developer", "Full Stack Engineer", "DevOps Engineer"]
        resume.experience.append(ExperienceItem(
            role=random.choice(roles),
            company=random.choice(companies),
            location=random.choice(["San Francisco, CA", "New York, NY", "Austin, TX", "Seattle, WA"]),
            dates=f"{random.choice(['Jan', 'Feb', 'Mar'])} 2021 – Present",
            bullets=[
                f"Led development of scalable microservices serving {random.randint(100, 1000)}K+ daily active users",
                f"Mentored {random.randint(2, 5)} junior developers and established coding best practices",
                f"Reduced system latency by {random.randint(20, 60)}% through performance optimization",
                f"Implemented CI/CD pipeline improving deployment frequency by {random.randint(40, 80)}%"
            ]
        ))
        resume.projects.append(ProjectItem(
            title="E-Commerce Platform",
            tech="React, Node.js, MongoDB, Stripe API",
            bullets=[
                "Developed full-stack platform with payment processing and inventory management",
                "Implemented JWT-based authentication securing user data",
                f"Achieved 99.{random.randint(5, 9)}% uptime through load balancing and caching"
            ]
        ))
        universities = ["University of Technology", "State University", "Tech Institute", "City College"]
        resume.education.append(EducationItem(
            degree="Bachelor of Science in Computer Science",
            institution=random.choice(universities),
            year=f"Graduated {random.choice(['May', 'December'])} 20{random.randint(18, 22)}",
            details=[
                f"GPA: {random.randint(3, 4)}.{random.randint(0, 9)}/4.0",
                "Relevant Coursework: Data Structures, Algorithms, Database Systems, Software Engineering",
                "Awards: Dean's List, Outstanding Student Award"
            ]
        ))
        resume.skills = Skills(
            programming_languages=["Python", "JavaScript", "Java", "SQL", "TypeScript"],
            frameworks_libraries=["React", "Node.js", "Express", "Django", "Spring Boot"],
            tools_technologies=["Git", "Docker", "AWS", "MongoDB", "PostgreSQL", "Jenkins"],
            methodologies=["Agile", "Scrum", "CI/CD", "TDD", "DevOps"]
        )
        resume.certifications = [
            f"AWS Certified Solutions Architect ({random.randint(2020, 2023)})",
            f"Professional Scrum Master I ({random.randint(2020, 2023)})",
            f"Google Cloud Professional ({random.randint(2020, 2023)})"
        ]
        hobbies = ["Open Source Contribution", "Hiking", "Photography", "Reading Tech Blogs", 
                  "Playing Guitar", "Traveling", "Cooking", "Yoga"]
        resume.hobbies = random.sample(hobbies, random.randint(2, 4))
        return resume