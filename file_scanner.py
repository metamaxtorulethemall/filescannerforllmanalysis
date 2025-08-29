import os
import json
from pathlib import Path
from tkinter import Tk, filedialog, messagebox
from tqdm import tqdm  # Für den Fortschrittsbalken

def scan_folder(root_folder):
    """Scannt den ausgewählten Ordner rekursiv und zeigt den Fortschritt an."""
    output = []
    root_path = Path(root_folder)
    files = list(root_path.rglob("*"))  # Alle Dateien und Ordner sammeln
    file_count = sum(1 for f in files if f.is_file())

    print(f"Scanne {file_count} Dateien in {root_folder}...")

    for file in tqdm(files, desc="Fortschritt", unit="Datei"):
        if file.is_file():
            output.append({
                "Path": str(file),
                "Name": file.name,
                "SizeKB": round(file.stat().st_size / 1024, 2),
                "LastModified": file.stat().st_mtime,
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
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Wähle den übergeordneten Ordner aus")
    if not folder_path:
        messagebox.showerror("Fehler", "Kein Ordner ausgewählt!")
        return

    # JSON-Dateipfad festlegen
    output_path = os.path.join(folder_path, "file_structure.json")

    # Scannen und speichern
    try:
        print("Starte Scan...")
        data = scan_folder(folder_path)
        save_json(data, output_path)
        print("\nScan abgeschlossen!")
        messagebox.showinfo(
            "Erfolg",
            f"Scan abgeschlossen!\n{len(data)} Dateien gescannt.\n\n"
            f"Die JSON-Datei wurde gespeichert unter:\n{output_path}"
        )
    except Exception as e:
        messagebox.showerror("Fehler", f"Etwas ist schiefgelaufen: {e}")

if __name__ == "__main__":
    # Installiere tqdm falls nicht vorhanden (nur einmalig nötig)
    try:
        from tqdm import tqdm
    except ImportError:
        print("Installiere 'tqdm' für den Fortschrittsbalken...")
        os.system("pip install tqdm")
        from tqdm import tqdm
    main()
