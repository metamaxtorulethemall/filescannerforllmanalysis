import os
import json
from pathlib import Path
from tkinter import Tk, filedialog, messagebox

def scan_folder(root_folder):
    """Scannt den ausgewählten Ordner rekursiv und erstellt eine JSON-Struktur."""
    output = []
    root_path = Path(root_folder)

    for file in root_path.rglob("*"):
        if file.is_file():
            output.append({
                "Path": str(file),
                "Name": file.name,
                "SizeKB": round(file.stat().st_size / 1024, 2),
                "LastModified": file.stat().st_mtime,  # Unix-Timestamp
                "Extension": file.suffix
            })

    return output

def save_json(data, output_path):
    """Speichert die Daten als JSON-Datei."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    # GUI: Ordnerauswahl
    root = Tk()
    root.withdraw()  # Verstecke Hauptfenster
    folder_path = filedialog.askdirectory(title="Wähle den übergeordneten Ordner aus")
    if not folder_path:
        messagebox.showerror("Fehler", "Kein Ordner ausgewählt!")
        return

    # JSON-Dateipfad festlegen
    output_path = os.path.join(folder_path, "file_structure.json")

    # Scannen und speichern
    try:
        data = scan_folder(folder_path)
        save_json(data, output_path)
        messagebox.showinfo(
            "Erfolg",
            f"Scan abgeschlossen! Die JSON-Datei wurde gespeichert unter:\n{output_path}"
        )
    except Exception as e:
        messagebox.showerror("Fehler", f"Etwas ist schiefgelaufen: {e}")

if __name__ == "__main__":
    main()
