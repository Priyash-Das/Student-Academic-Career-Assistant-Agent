import tkinter as tk
import sys
import os
from ui.main_window import MainWindow
from supervisor.supervisor_agent import SupervisorAgent
from utils.log_manager import LogManager
LogManager.info("Application starting", agent="SYSTEM")
sys.path.append(os.path.abspath("."))
def main():
    root = tk.Tk()
    root.title("Student Academic & Career Assistant Agent")
    root.geometry("1200x800")
    LogManager.ui_event("app_started", "MainWindow")
    supervisor = SupervisorAgent()
    MainWindow(root, supervisor)
    root.mainloop()
    LogManager.info("Application shutting down", agent="SYSTEM")
if __name__ == "__main__":
    main()