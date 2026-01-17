class StudyBuddyError(Exception):
    pass
class InputValidationError(StudyBuddyError):
    pass
class ContextBuildError(StudyBuddyError):
    pass
class LLMCallError(StudyBuddyError):
    pass
class PipelineError(StudyBuddyError):
    pass