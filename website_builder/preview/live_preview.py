import webbrowser
from website_builder.preview.temp_site_manager import TempSiteManager
class LivePreview:
    @staticmethod
    def open(html: str):
        manager = TempSiteManager()
        path = manager.write(html)
        webbrowser.open(f"file://{path}")