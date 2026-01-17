from typing import Optional, Literal
from study_buddy.core.input_handler import validate_inputs
from study_buddy.core.context_builder import build_study_context
from study_buddy.pipelines.explain import run_explain_pipeline
from study_buddy.pipelines.summarize import run_summary_pipeline
from study_buddy.pipelines.quiz import run_quiz_pipeline
from study_buddy.utils.errors import StudyBuddyError
from utils.log_manager import LogManager
from utils.logger import log_agent_operation
StudyAction = Literal["EXPLAIN", "SUMMARIZE", "QUIZ"]
class StudyBuddyAgent:
    def __init__(self):
        LogManager.info("StudyBuddyAgent initialized", agent="STUDY_BUDDY")
    @log_agent_operation("STUDY_BUDDY", "run_study_action")
    def run(
        self,
        action: StudyAction,
        prompt: Optional[str] = None,
        pdf_path: Optional[str] = None,
    ) -> str:
        LogManager.info(f"StudyBuddy action requested: {action}", 
                       agent="STUDY_BUDDY",
                       details={"prompt_length": len(prompt) if prompt else 0,
                                "pdf_path": pdf_path})
        try:
            input_mode = validate_inputs(prompt, pdf_path)
            LogManager.debug(f"Input validation completed: {input_mode}", 
                           agent="STUDY_BUDDY")
        except Exception as e:
            LogManager.agent_error("STUDY_BUDDY", "input_validation", e)
            raise
        if pdf_path:
            input_mode = "PDF_ONLY"
            prompt = ""
            LogManager.info("PDF detected, switching to PDF_ONLY mode", 
                           agent="STUDY_BUDDY",
                           details={"pdf_path": pdf_path})
        try:
            LogManager.agent_start("STUDY_BUDDY", "context_building")
            study_context = build_study_context(
                input_mode=input_mode,
                prompt=prompt or "",
                pdf_path=pdf_path or "",
            )
            LogManager.agent_end("STUDY_BUDDY", "context_building", "SUCCESS",
                               details={"context_length": len(study_context)})
        except Exception as e:
            LogManager.agent_error("STUDY_BUDDY", "context_building", e)
            raise
        LogManager.audit(f"study_buddy_{action.lower()}", 
                        details={"action": action, 
                                 "input_mode": input_mode})
        try:
            if action == "EXPLAIN":
                LogManager.agent_start("STUDY_BUDDY", "explain_pipeline")
                result = run_explain_pipeline(study_context)
                LogManager.agent_end("STUDY_BUDDY", "explain_pipeline", "SUCCESS",
                                   details={"result_length": len(result)})
                return result
            if action == "SUMMARIZE":
                LogManager.agent_start("STUDY_BUDDY", "summarize_pipeline")
                result = run_summary_pipeline(study_context)
                LogManager.agent_end("STUDY_BUDDY", "summarize_pipeline", "SUCCESS",
                                   details={"result_length": len(result)})
                return result
            if action == "QUIZ":
                LogManager.agent_start("STUDY_BUDDY", "quiz_pipeline")
                result = run_quiz_pipeline(study_context)
                LogManager.agent_end("STUDY_BUDDY", "quiz_pipeline", "SUCCESS",
                                   details={"result_length": len(result)})
                return result
            error_msg = f"Unsupported StudyBuddy action: {action}"
            LogManager.error(error_msg, agent="STUDY_BUDDY")
            raise StudyBuddyError(error_msg)
        except Exception as e:
            LogManager.agent_error("STUDY_BUDDY", f"{action.lower()}_pipeline", e,
                                  details={"study_context_length": len(study_context)})
            raise