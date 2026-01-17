from website_builder.core.prompt_processor import PromptProcessor
from website_builder.core.spec_inference import WebsiteSpecInference
from website_builder.core.generator import WebsiteGenerator
from website_builder.core.sanitizer import OutputSanitizer
from website_builder.core.validator import HTMLValidator
from website_builder.core.health_check import HealthCheck
from website_builder.core.llm_client import LLMClient
from website_builder.core.error_handler import (
    PromptValidationError,
    GenerationError,
    ValidationError,
)
from utils.log_manager import LogManager
from utils.logger import log_agent_operation
class WebsiteBuilderAgent:
    def __init__(self):
        self.api_client = LLMClient()
        self.current_html = None
        LogManager.info("WebsiteBuilderAgent initialized", agent="WEBSITE_AGENT")
    @log_agent_operation("WEBSITE_AGENT", "build_website")
    def build(self, prompt: str, modification: str = None):
        LogManager.info("Starting website build process", 
                       agent="WEBSITE_AGENT",
                       details={"prompt_length": len(prompt),
                                "has_modification": bool(modification)})        
        LogManager.audit("website_build_requested",
                        details={"prompt": prompt[:100],
                                 "modification": modification})
        try:
            LogManager.agent_start("WEBSITE_AGENT", "prompt_processing")
            processor = PromptProcessor(prompt, modification or "")           
            if not processor.is_valid():
                LogManager.error("Prompt validation failed", agent="WEBSITE_AGENT",
                               details={"prompt": prompt[:200]})
                raise PromptValidationError("Invalid prompt. Please provide a valid website description.")            
            merged_prompt = processor.merge()
            LogManager.agent_end("WEBSITE_AGENT", "prompt_processing", "SUCCESS",
                               details={"merged_prompt_length": len(merged_prompt)})            
            LogManager.debug(f"Merged prompt: {merged_prompt[:200]}...", 
                            agent="WEBSITE_AGENT")
            LogManager.agent_start("WEBSITE_AGENT", "spec_inference")
            spec = WebsiteSpecInference.infer(merged_prompt)
            LogManager.agent_end("WEBSITE_AGENT", "spec_inference", "SUCCESS",
                               details={"spec_keys": list(spec.keys()) if hasattr(spec, 'keys') else []})
            LogManager.agent_start("WEBSITE_AGENT", "html_generation")
            generator = WebsiteGenerator(self.api_client)
            result = generator.generate(spec)
            LogManager.agent_end("WEBSITE_AGENT", "html_generation", "SUCCESS",
                               details={"result_keys": list(result.keys())})
            raw_output = result.get("html", "")           
            if not raw_output:
                LogManager.error("No HTML output generated", agent="WEBSITE_AGENT",
                               details={"spec": str(spec)[:200]})
                raise GenerationError("No HTML output generated.")           
            LogManager.debug(f"Raw HTML generated: {len(raw_output)} chars", 
                            agent="WEBSITE_AGENT")
            LogManager.agent_start("WEBSITE_AGENT", "html_sanitization")
            clean_html = OutputSanitizer.sanitize(raw_output)
            LogManager.agent_end("WEBSITE_AGENT", "html_sanitization", "SUCCESS",
                               details={"raw_length": len(raw_output),
                                        "clean_length": len(clean_html)})
            if not clean_html:
                LogManager.error("HTML sanitization resulted in empty output", 
                                agent="WEBSITE_AGENT")
                raise GenerationError("HTML sanitization resulted in empty output.")           
            LogManager.debug(f"Sanitized HTML: {len(clean_html)} chars", 
                            agent="WEBSITE_AGENT")
            LogManager.agent_start("WEBSITE_AGENT", "html_validation")
            if not HTMLValidator.is_valid(clean_html):
                LogManager.error("Generated HTML is invalid", agent="WEBSITE_AGENT",
                               details={"html_sample": clean_html[:200]})
                raise ValidationError("Generated HTML is invalid.")
            LogManager.agent_end("WEBSITE_AGENT", "html_validation", "SUCCESS")
            LogManager.agent_start("WEBSITE_AGENT", "health_check")
            if not HealthCheck.run(clean_html):
                LogManager.error("HTML health check failed", agent="WEBSITE_AGENT")
                raise ValidationError("HTML health check failed.")
            LogManager.agent_end("WEBSITE_AGENT", "health_check", "SUCCESS")
            self.current_html = clean_html
            LogManager.info("Website build completed successfully", 
                           agent="WEBSITE_AGENT",
                           details={"html_length": len(clean_html),
                                    "has_css": "style" in clean_html.lower(),
                                    "has_js": "script" in clean_html.lower()})
            LogManager.audit("website_generated",
                           details={"html_length": len(clean_html),
                                    "prompt": prompt[:50]})
            return clean_html
        except PromptValidationError as e:
            LogManager.agent_error("WEBSITE_AGENT", "build_website", e,
                                  details={"error_type": "PromptValidationError"})
            raise ValueError(f"Prompt validation failed: {str(e)}")
        except GenerationError as e:
            LogManager.agent_error("WEBSITE_AGENT", "build_website", e,
                                  details={"error_type": "GenerationError"})
            raise Exception(f"HTML generation failed: {str(e)}")
        except ValidationError as e:
            LogManager.agent_error("WEBSITE_AGENT", "build_website", e,
                                  details={"error_type": "ValidationError"})
            raise Exception(f"HTML validation failed: {str(e)}")
        except Exception as e:
            LogManager.agent_error("WEBSITE_AGENT", "build_website", e,
                                  details={"error_type": "Unknown"})
            raise Exception(f"Website building failed: {str(e)}")
    def get_current_html(self):
        has_html = self.current_html is not None and len(self.current_html) > 0
        LogManager.debug(f"get_current_html: {has_html}", agent="WEBSITE_AGENT")
        return self.current_html
    def has_website(self) -> bool:
        has_website = self.current_html is not None and len(self.current_html) > 0
        LogManager.debug(f"has_website check: {has_website}", agent="WEBSITE_AGENT")
        return has_website