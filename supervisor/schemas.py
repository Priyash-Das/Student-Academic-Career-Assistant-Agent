from dataclasses import dataclass
from typing import Dict, Any, Optional, Literal
from uuid import uuid4
import uuid
import time
AgentName = Literal[
    "CHAT",
    "STUDY_BUDDY",
    "VOICE_NOTES",
    "RESUME",
    "WEBSITE"
]
IntentType = Literal[
    "CHAT",
    "STUDY_EXPLAIN",
    "STUDY_SUMMARIZE",
    "STUDY_QUIZ",
    "VOICE_TRANSCRIBE",
    "VOICE_NOTES",
    "VOICE_QA",
    "RESUME_BUILD",
    "WEBSITE_BUILD"
]
@dataclass
class AgentMessage:
    trace_id: str
    source_agent: str
    target_agent: AgentName
    intent: IntentType
    payload: Dict[str, Any]
    constraints: Dict[str, Any]
def new_trace_id() -> str:
    return str(uuid4())
@dataclass(frozen=True)
class A2AEnvelope:
    trace_id: str
    agent_name: str
    action: str
    payload: Dict[str, Any]
    session_id: Optional[str]
    timestamp: float
    @staticmethod
    def create(agent_name: str, action: str, payload: Dict[str, Any], session_id: Optional[str] = None):
        return A2AEnvelope(
            trace_id=str(uuid.uuid4()),
            agent_name=agent_name,
            action=action,
            payload=payload,
            session_id=session_id,
            timestamp=time.time(),
        )