from resume_builder.core.resume_agent import ResumeAgent
from resume_builder.core.resume_validator import ResumeValidator
from resume_builder.renderer.docx_renderer import DocxRenderer
from utils.log_manager import LogManager
from utils.logger import log_agent_operation
import os
class ResumeBuilderAgent:
    def __init__(self):
        self.validator = ResumeValidator()
        self.renderer = DocxRenderer()
        self.current_resume = None
        LogManager.info("ResumeBuilderAgent initialized", agent="RESUME_AGENT")
    @log_agent_operation("RESUME_AGENT", "build_resume")
    def build_resume(self, data: dict):
        LogManager.info(f"Building resume with {len(data)} data fields", 
                       agent="RESUME_AGENT", 
                       details={"data_fields": list(data.keys())})       
        prompt = self._dict_to_prompt(data)       
        LogManager.debug(f"Converted data to prompt: {prompt[:200]}...", 
                        agent="RESUME_AGENT")
        try:
            LogManager.agent_start("RESUME_AGENT", "llm_generation")
            resume = ResumeAgent.generate_from_prompt(prompt)
            LogManager.agent_end("RESUME_AGENT", "llm_generation", "SUCCESS")           
            LogManager.info("LLM resume generation completed", 
                           agent="RESUME_AGENT",
                           details={"resume_length": len(str(resume))})
            LogManager.agent_start("RESUME_AGENT", "resume_validation")
            validated = self.validator.validate(resume)
            self.current_resume = validated
            LogManager.agent_end("RESUME_AGENT", "resume_validation", "SUCCESS")           
            LogManager.info("Resume validation completed", 
                           agent="RESUME_AGENT",
                           details={"has_header": bool(validated.header.name),
                                    "experience_count": len(validated.experience),
                                    "education_count": len(validated.education)})
            output_path = "generated_resume.docx"
            LogManager.file_operation("render_docx", output_path, "RESUME_AGENT")           
            output_path = self.renderer.render(validated, output_path=output_path)
            LogManager.file_operation("save_docx", output_path, "RESUME_AGENT", 
                                     details={"file_size": os.path.getsize(output_path) 
                                             if os.path.exists(output_path) else 0})
            resume_text = self._resume_to_text(validated)
            LogManager.info("Resume build completed successfully", 
                           agent="RESUME_AGENT",
                           details={"output_path": output_path,
                                    "resume_text_length": len(resume_text)})
            return {
                "resume_text": resume_text,
                "file_path": output_path,
                "resume_object": validated
            }
        except Exception as e:
            LogManager.agent_error("RESUME_AGENT", "build_resume", e,
                                  details={"data_keys": list(data.keys())})
            raise Exception(f"Resume generation failed: {str(e)}")
    def _dict_to_prompt(self, data: dict) -> str:
        LogManager.debug(f"Converting dict to prompt: {len(data)} items", 
                        agent="RESUME_AGENT")
        parts = []
        for key, value in data.items():
            if value:
                parts.append(f"{key}: {value}")
        result = "\n".join(parts)
        LogManager.debug(f"Generated prompt length: {len(result)}", 
                        agent="RESUME_AGENT")
        return result
    def _resume_to_text(self, resume) -> str:
        LogManager.debug("Converting resume object to text", 
                        agent="RESUME_AGENT")
        lines = []
        if resume.header.name:
            lines.append(f"Name: {resume.header.name}")
            LogManager.audit("resume_generated", 
                           details={"name": resume.header.name})
        if resume.header.email:
            lines.append(f"Email: {resume.header.email}")
        if resume.header.phone:
            lines.append(f"Phone: {resume.header.phone}")
        if resume.header.address:
            lines.append(f"Location: {resume.header.address}")
        lines.append("")
        if resume.summary:
            lines.append("PROFESSIONAL SUMMARY")
            lines.append(resume.summary)
            lines.append("")
            LogManager.debug(f"Added summary: {len(resume.summary)} chars", 
                           agent="RESUME_AGENT")
        if resume.experience:
            lines.append("EXPERIENCE")
            for exp in resume.experience:
                lines.append(f"{exp.role} at {exp.company}")
                if exp.dates:
                    lines.append(f"  {exp.dates}")
                for bullet in exp.bullets:
                    lines.append(f"  • {bullet}")
                lines.append("")
            LogManager.info(f"Added {len(resume.experience)} experience entries", 
                           agent="RESUME_AGENT")
        if resume.education:
            lines.append("EDUCATION")
            for edu in resume.education:
                lines.append(f"{edu.degree} - {edu.institution}")
                if edu.year:
                    lines.append(f"  {edu.year}")
                lines.append("")
            LogManager.info(f"Added {len(resume.education)} education entries", 
                           agent="RESUME_AGENT")
        if any([resume.skills.programming_languages, resume.skills.frameworks_libraries,
                resume.skills.tools_technologies, resume.skills.methodologies]):
            lines.append("SKILLS")
            if resume.skills.programming_languages:
                lines.append(f"  Languages: {', '.join(resume.skills.programming_languages)}")
            if resume.skills.frameworks_libraries:
                lines.append(f"  Frameworks: {', '.join(resume.skills.frameworks_libraries)}")
            if resume.skills.tools_technologies:
                lines.append(f"  Tools: {', '.join(resume.skills.tools_technologies)}")
            LogManager.debug("Added skills section", agent="RESUME_AGENT")
        result = "\n".join(lines)
        LogManager.info(f"Converted resume to text: {len(result)} chars", 
                       agent="RESUME_AGENT")
        return result
    def get_current_resume(self):
        LogManager.debug("Retrieving current resume", agent="RESUME_AGENT")
        return self.current_resume
    def export_to_docx(self, resume, output_path: str):
        LogManager.file_operation("export_docx", output_path, "RESUME_AGENT")  
        result = self.renderer.render(resume, output_path=output_path)
        if os.path.exists(output_path):
            LogManager.info(f"Resume exported to {output_path}", 
                           agent="RESUME_AGENT",
                           details={"file_size": os.path.getsize(output_path)})
        else:
            LogManager.error(f"Export failed: {output_path} not created", 
                            agent="RESUME_AGENT")
        return result