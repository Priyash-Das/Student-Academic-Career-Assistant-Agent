import os
import shutil
import tempfile
from website_builder.config.settings import DEFAULT_HTML_FILENAME
class TempSiteManager:
    _active_dirs = []
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="website_builder_")
        self.file_path = os.path.join(self.temp_dir, DEFAULT_HTML_FILENAME)
        TempSiteManager._active_dirs.append(self.temp_dir)
    def write(self, html: str) -> str:
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(html)
        return self.file_path
    @classmethod
    def cleanup_all(cls):
        for d in cls._active_dirs:
            if os.path.exists(d):
                shutil.rmtree(d, ignore_errors=True)
        cls._active_dirs.clear()