import os
import sys
import json
import inspect
import traceback
from datetime import datetime
from pathlib import Path
from enum import Enum
from typing import Any, Dict, Optional
import threading
import time
class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    AUDIT = "AUDIT"  
    PERFORMANCE = "PERFORMANCE"
    AGENT = "AGENT"  
class LogCategory(Enum):
    AGENT = "AGENT"
    UI = "UI"
    API = "API"
    FILE = "FILE"
    DATABASE = "DATABASE"
    SECURITY = "SECURITY"
    PERFORMANCE = "PERFORMANCE"
    AUDIT = "AUDIT"
    ERROR = "ERROR"
    SYSTEM = "SYSTEM"
class CentralLogger:
    _instance = None
    _lock = threading.Lock()
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(CentralLogger, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        self.archive_dir = self.log_dir / "archive"
        self.archive_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file = self.log_dir / f"app_{timestamp}.log"
        self.perf_start_times = {}
        self.log_entries = []
        self.max_entries_memory = 1000
        self._write_header()
        print(f"✅ Centralized Logger Initialized: {self.log_file}")
    def _write_header(self):
        header = {
            "timestamp": self._get_timestamp(),
            "level": "INFO",
            "category": "SYSTEM",
            "module": "LOGGER",
            "message": "=== CENTRALIZED LOGGING SYSTEM STARTED ===",
            "session_id": self._generate_session_id(),
            "system_info": {
                "python_version": sys.version,
                "platform": sys.platform,
                "cwd": str(Path.cwd())
            }
        }  
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(header, default=str) + '\n')
    def _get_timestamp(self) -> str:
        return datetime.now().isoformat()
    def _generate_session_id(self) -> str:
        return datetime.now().strftime("%Y%m%d%H%M%S")
    def _get_caller_info(self):
        try:
            stack = inspect.stack()
            for frame_info in stack[2:]:  
                module = inspect.getmodule(frame_info.frame)
                if module and module.__name__ != __name__:
                    module_name = module.__name__
                    if 'agents' in module_name:
                        agent_name = module_name.split('.')[-1]
                    else:
                        agent_name = module_name.split('.')[-1] if '.' in module_name else module_name
                    return {
                        "module": agent_name.upper(),
                        "function": frame_info.function,
                        "line": frame_info.lineno,
                        "file": Path(frame_info.filename).name
                    }
        except:
            pass
        return {"module": "UNKNOWN", "function": "UNKNOWN", "line": 0, "file": "UNKNOWN"}
    def _write_log(self, log_data: Dict[str, Any]):
        with self._lock:
            self.log_entries.append(log_data)
            if len(self.log_entries) > self.max_entries_memory:
                self.log_entries.pop(0)
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(log_data, default=str) + '\n')
            except Exception as e:
                print(f"⚠️ Failed to write log: {e}")
    def log(self, 
            level: LogLevel, 
            category: LogCategory, 
            message: str,
            details: Optional[Dict[str, Any]] = None,
            agent: Optional[str] = None,
            user_action: Optional[str] = None):
        caller_info = self._get_caller_info()
        log_entry = {
            "timestamp": self._get_timestamp(),
            "level": level.value,
            "category": category.value,
            "module": agent or caller_info["module"],
            "function": caller_info["function"],
            "file": caller_info["file"],
            "line": caller_info["line"],
            "message": message,
            "session_id": self._generate_session_id(),
            "thread_id": threading.get_ident(),
            "user_action": user_action
        }
        if details:
            log_entry["details"] = details
        if level in [LogLevel.ERROR, LogLevel.CRITICAL]:
            log_entry["traceback"] = traceback.format_exc()
        self._write_log(log_entry)
        if level in [LogLevel.ERROR, LogLevel.CRITICAL]:
            print(f"🔴 [{level.value}] {message}")
    def info(self, message: str, category: LogCategory = LogCategory.SYSTEM, **kwargs):
        self.log(LogLevel.INFO, category, message, **kwargs)
    def debug(self, message: str, category: LogCategory = LogCategory.SYSTEM, **kwargs):
        self.log(LogLevel.DEBUG, category, message, **kwargs)
    def warning(self, message: str, category: LogCategory = LogCategory.SYSTEM, **kwargs):
        self.log(LogLevel.WARNING, category, message, **kwargs)
    def error(self, message: str, category: LogCategory = LogCategory.ERROR, **kwargs):
        self.log(LogLevel.ERROR, category, message, **kwargs)
    def critical(self, message: str, category: LogCategory = LogCategory.ERROR, **kwargs):
        self.log(LogLevel.CRITICAL, category, message, **kwargs)
    def audit(self, user_action: str, details: Dict[str, Any] = None):
        self.log(
            LogLevel.AUDIT,
            LogCategory.AUDIT,
            f"User action: {user_action}",
            details=details,
            user_action=user_action
        )
    def agent_start(self, agent_name: str, operation: str, **kwargs):
        self.log(
            LogLevel.AGENT,
            LogCategory.AGENT,
            f"Agent {agent_name} starting: {operation}",
            details={"operation": operation, **kwargs},
            agent=agent_name
        )
    def agent_end(self, agent_name: str, operation: str, status: str, **kwargs):
        self.log(
            LogLevel.AGENT,
            LogCategory.AGENT,
            f"Agent {agent_name} completed: {operation} - Status: {status}",
            details={"operation": operation, "status": status, **kwargs},
            agent=agent_name
        )
    def agent_error(self, agent_name: str, operation: str, error: Exception, **kwargs):
        self.log(
            LogLevel.ERROR,
            LogCategory.AGENT,
            f"Agent {agent_name} error in {operation}: {str(error)}",
            details={"operation": operation, "error": str(error), **kwargs},
            agent=agent_name
        )
    def perf_start(self, operation_id: str):
        self.perf_start_times[operation_id] = time.time()
        self.log(
            LogLevel.PERFORMANCE,
            LogCategory.PERFORMANCE,
            f"Performance tracking started: {operation_id}",
            details={"operation_id": operation_id}
        )
    def perf_end(self, operation_id: str, metadata: Dict[str, Any] = None):
        if operation_id in self.perf_start_times:
            duration = time.time() - self.perf_start_times[operation_id]
            perf_data = {
                "operation_id": operation_id,
                "duration_seconds": round(duration, 3),
                "timestamp": self._get_timestamp()
            }
            if metadata:
                perf_data.update(metadata)
            self.log(
                LogLevel.PERFORMANCE,
                LogCategory.PERFORMANCE,
                f"Performance completed: {operation_id} - Duration: {duration:.3f}s",
                details=perf_data
            )
            del self.perf_start_times[operation_id]
    def get_log_file_path(self) -> Path:
        return self.log_file
    def get_recent_logs(self, count: int = 100) -> list:
        return self.log_entries[-count:] if self.log_entries else []
    def get_logs_by_level(self, level: LogLevel) -> list:
        return [log for log in self.log_entries if log.get("level") == level.value]
    def get_logs_by_agent(self, agent_name: str) -> list:
        return [log for log in self.log_entries if log.get("module") == agent_name.upper()]
    def export_logs(self, output_path: Path = None) -> Path:
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.archive_dir / f"logs_export_{timestamp}.json"
        export_data = {
            "export_timestamp": self._get_timestamp(),
            "log_file": str(self.log_file),
            "total_entries": len(self.log_entries),
            "logs": self.log_entries
        }
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)
        self.info(f"Logs exported to: {output_path}")
        return output_path
    def clear_memory_logs(self):
        with self._lock:
            self.log_entries.clear()
            self.info("Memory log buffer cleared")
    def rotate_log_file(self):
        with self._lock:
            if self.log_file.exists() and self.log_file.stat().st_size > 0:
                archive_name = self.archive_dir / f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
                self.log_file.rename(archive_name)
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                self.log_file = self.log_dir / f"app_{timestamp}.log"
                self._write_header()
                self.info(f"Log file rotated. Archive: {archive_name.name}")
_logger_instance = None
def get_logger() -> CentralLogger:
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = CentralLogger()
    return _logger_instance
def log_agent_operation(agent_name: str, operation: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger()
            func_args = {}
            if args and hasattr(args[0], '__class__'):
                arg_names = list(kwargs.keys())
                for i, arg in enumerate(args[1:], 1):
                    if i-1 < len(arg_names):
                        func_args[arg_names[i-1]] = str(arg)[:100] 
            logger.agent_start(agent_name, operation, 
                             function=func.__name__, 
                             arguments=func_args)
            try:
                result = func(*args, **kwargs)
                logger.agent_end(agent_name, operation, "SUCCESS")
                return result
            except Exception as e:
                logger.agent_error(agent_name, operation, e)
                raise
        return wrapper
    return decorator
def log_user_action(action: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger()
            logger.audit(action)
            return func(*args, **kwargs)
        return wrapper
    return decorator