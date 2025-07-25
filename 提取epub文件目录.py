import tkinter as tk
from tkinter import filedialog, messagebox
from ebooklib import epub

def extract_toc(epub_path):
    book = epub.read_epub(epub_path)
    toc = book.get_toc()
    return toc

def save_toc_to_file(toc, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in toc:
            f.write(f"{item.title}\n")

def choose_epub_file():
    epub_file = filedialog.askopenfilename(filetypes=[("EPUB files", "*.epub")])
    if epub_file:
        epub_entry.delete(0, tk.END)
        epub_entry.insert(0, epub_file)

def choose_output_file():
    output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if output_file:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_file)

def extract_and_save():
    epub_path = epub_entry.get()
    output_path = output_entry.get()
    if not epub_path or not output_path:
        messagebox.showwarning("Warning", "Please select both EPUB file and output file.")
        return
    try:
        toc = extract_toc(epub_path)
        save_toc_to_file(toc, output_path)
        messagebox.showinfo("Success", "Table of Contents has been extracted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("EPUB TOC Extractor")

# Create widgets
tk.Label(root, text="EPUB File:").grid(row=0, column=0)
epub_entry = tk.Entry(root, width=50)
epub_entry.grid(row=0, column=1)
tk.Button(root, text="Browse...", command=choose_epub_file).grid(row=0, column=2)

tk.Label(root, text="Output File:").grid(row=1, column=0)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1)
tk.Button(root, text="Browse...", command=choose_output_file).grid(row=1, column=2)

tk.Button(root, text="Extract TOC", command=extract_and_save).grid(row=2, column=1, pady=10)

# Run the main loop
root.mainloop()