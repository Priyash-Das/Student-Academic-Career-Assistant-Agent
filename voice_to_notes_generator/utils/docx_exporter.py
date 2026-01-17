from docx import Document
def export_notes_to_docx(notes: str, output_path: str):
    doc = Document()
    for line in notes.split("\n"):
        doc.add_paragraph(line)
    doc.save(output_path)