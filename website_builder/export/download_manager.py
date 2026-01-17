from tkinter import filedialog
class DownloadManager:
    @staticmethod
    def download(html: str):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html")],
        )
        if not file_path:
            return
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)