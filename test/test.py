import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from glu import process_glu_file_qbd

class GLUViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GLU Viewer")
        
        self.selected_file = None
        self.json_data = None
        self.exported_files = []

        self.file_label = tk.Label(root, text="Select a .glu file:")
        self.file_label.pack()

        self.file_entry = tk.Entry(root, width=50, state='disabled')
        self.file_entry.pack(side=tk.TOP, padx=5)

        self.export_one_button = tk.Button(root, text="Export a single .glu", command=self.export_one)
        self.export_one_button.pack(side=tk.TOP)

        self.json_text = tk.Text(root, height=20, width=80)
        self.json_text.pack(pady=10)

    def export_one(self):
        self.selected_file = filedialog.askopenfilename(filetypes=[("GLU files", "*.glu")])
        self.file_entry.config(state='normal')
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, self.selected_file)
        self.file_entry.config(state='disabled')

        if self.selected_file:
            self.json_data = self.load_glu_data(self.selected_file)
            self.json_text.delete('1.0', tk.END)
            self.json_text.insert(tk.END, json.dumps(self.json_data, indent=4))

    def view_json(self):
        if self.selected_file:
            try:
                self.json_data = self.load_glu_data(self.selected_file)
                self.json_text.delete('1.0', tk.END)
                self.json_text.insert(tk.END, json.dumps(self.json_data, indent=4))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load JSON data: {e}")

    def load_glu_data(self, file_path):
        with open(file_path, 'rb') as f:
            first_bytes = f.read(8)
        if b'GLUE' in first_bytes:
            process_glu_file_qbd(file_path, isall=None)
            with open(f"{os.path.splitext(file_path)[0]}/{os.path.splitext(os.path.basename(file_path))[0]}.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            raise ValueError("The selected file isn't valid .glu file")

if __name__ == "__main__":
    root = tk.Tk()
    app = GLUViewerApp(root)
    root.mainloop()
