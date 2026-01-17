from utils.logger import get_logger, LogLevel, LogCategory
from typing import Optional, Dict, Any
class LogManager:  
    @staticmethod
    def info(message: str, agent: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        """Log INFO level"""
        get_logger().info(message, agent=agent, details=details)    
    @staticmethod
    def error(message: str, agent: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        """Log ERROR level"""
        get_logger().error(message, agent=agent, details=details)    
    @staticmethod
    def warning(message: str, agent: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        """Log WARNING level"""
        get_logger().warning(message, agent=agent, details=details)    
    @staticmethod
    def debug(message: str, agent: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        """Log DEBUG level"""
        get_logger().debug(message, agent=agent, details=details)    
    @staticmethod
    def audit(user_action: str, details: Optional[Dict[str, Any]] = None):
        """Log user action"""
        get_logger().audit(user_action, details)    
    @staticmethod
    def agent_start(agent_name: str, operation: str, **kwargs):
        """Log agent operation start"""
        get_logger().agent_start(agent_name, operation, **kwargs)    
    @staticmethod
    def agent_end(agent_name: str, operation: str, status: str = "SUCCESS", **kwargs):
        """Log agent operation end"""
        get_logger().agent_end(agent_name, operation, status, **kwargs)   
    @staticmethod
    def agent_error(agent_name: str, operation: str, error: Exception, **kwargs):
        """Log agent error"""
        get_logger().agent_error(agent_name, operation, error, **kwargs)    
    @staticmethod
    def file_operation(operation: str, file_path: str, agent: Optional[str] = None, 
                      success: bool = True, details: Optional[Dict[str, Any]] = None):
        """Log file operations"""
        message = f"File {operation}: {file_path} - {'SUCCESS' if success else 'FAILED'}"
        level = LogLevel.INFO if success else LogLevel.ERROR
        category = LogCategory.FILE        
        details = details or {}
        details.update({
            "file_path": file_path,
            "operation": operation,
            "success": success
        })        
        get_logger().log(level, category, message, details=details, agent=agent)    
    @staticmethod
    def api_call(api_name: str, endpoint: str, status: str, 
                agent: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        """Log API calls"""
        message = f"API {api_name}: {endpoint} - Status: {status}"
        level = LogLevel.INFO if status == "SUCCESS" else LogLevel.ERROR
        category = LogCategory.API       
        details = details or {}
        details.update({
            "api_name": api_name,
            "endpoint": endpoint,
            "status": status
        })       
        get_logger().log(level, category, message, details=details, agent=agent)   
    @staticmethod
    def ui_event(event: str, component: str, user_action: Optional[str] = None,
                details: Optional[Dict[str, Any]] = None):
        """Log UI events"""
        message = f"UI Event: {component}.{event}"
        if user_action:
            message += f" - Action: {user_action}"
        details = details or {}
        details.update({
            "event": event,
            "component": component,
            "user_action": user_action
        })
        get_logger().log(LogLevel.INFO, LogCategory.UI, message, details=details, agent="UI")
    @staticmethod
    def get_current_log_file() -> str:
        """Get path to current log file"""
        return str(get_logger().get_log_file_path())
    @staticmethod
    def export_logs(output_path: Optional[str] = None) -> str:
        """Export logs to file"""
        from pathlib import Path
        if output_path:
            path = Path(output_path)
        else:
            path = None
        export_path = get_logger().export_logs(path)
        return str(export_path)
    @staticmethod
    def get_recent_logs(count: int = 50) -> list:
        """Get recent log entries"""
        return get_logger().get_recent_logs(count)