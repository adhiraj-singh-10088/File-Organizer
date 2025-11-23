import os
import shutil
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

CONFIG_FILE = "settings.json"

#Logic 
extensions = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Setup_Files": [".exe", ".msi", ".dmg"]
}

def generate_unique_name(folder_path, filename):
    file_path = os.path.join(folder_path, filename)
    if not os.path.exists(file_path):
        return filename
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = f"{base}({counter}){extension}"
    while os.path.exists(os.path.join(folder_path, new_filename)):
        counter += 1
        new_filename = f"{base}({counter}){extension}"
    return new_filename

#Settings Manager
def load_settings():
    defaults = {"source": "", "dest": ""}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return defaults

def save_settings(source, dest):
    data = {"source": source, "dest": dest}
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error saving: {e}")


#GUI
def select_source():
    path = filedialog.askdirectory()
    if path:
        entry_source.delete(0, tk.END)
        entry_source.insert(0, path)
        save_settings(entry_source.get(), entry_dest.get())

def select_dest():
    path = filedialog.askdirectory()
    if path:
        entry_dest.delete(0, tk.END)
        entry_dest.insert(0, path)
        save_settings(entry_source.get(), entry_dest.get())

def start_organizing():
    source_folder = entry_source.get()
    dest_folder = entry_dest.get()
    
    #Validating
    if not source_folder or not os.path.exists(source_folder):
        messagebox.showerror("Error", "Source folder does not exist.")
        return
    if not dest_folder or not os.path.exists(dest_folder):
        messagebox.showerror("Error", "Destination folder does not exist.")
        return

    #Saving paths before running
    save_settings(source_folder, dest_folder)

    #1.Preparation
    all_items = os.listdir(source_folder)
    #Ignoring folders
    files_to_move = [f for f in all_items if os.path.isfile(os.path.join(source_folder, f))]
    total_files = len(files_to_move)

    if total_files == 0:
        messagebox.showinfo("Info", "No files found in Source!")
        return

    #2.Setup UI
    lbl_status.config(text=f"Moving {total_files} files...", fg="blue")
    btn_run.config(state=tk.DISABLED)
    progress_bar['maximum'] = total_files
    progress_bar['value'] = 0
    root.update_idletasks() 

    #3.Loop
    try:
        count = 0
        for filename in files_to_move:
            #Source path --> where the file is from
            original_path = os.path.join(source_folder, filename)
            _, ext = os.path.splitext(filename)
            
            found_category = False
            target_subfolder = "Others" #Default

            #Determining category
            for folder_name, ext_list in extensions.items():
                if ext.lower() in ext_list:
                    target_subfolder = folder_name
                    found_category = True
                    break
            
            #Destination path --> where the file is going
            #Logic: Destination / Category / Filename
            final_category_path = os.path.join(dest_folder, target_subfolder)
            
            if not os.path.exists(final_category_path):
                os.makedirs(final_category_path)

            safe_name = generate_unique_name(final_category_path, filename)
            final_path = os.path.join(final_category_path, safe_name)
            
            shutil.move(original_path, final_path)

            #Update Progress
            count += 1
            progress_bar['value'] = count
            root.update_idletasks()
            
        lbl_status.config(text="Success! Files moved.", fg="green")
        messagebox.showinfo("Done", f"Moved {total_files} files to Destination.")
        
    except Exception as e:
        lbl_status.config(text=f"Error: {str(e)}", fg="red")
    finally:
        btn_run.config(state=tk.NORMAL)


#GUI Setup
root = tk.Tk()
root.title("File Organizer Pro")
root.geometry("450x400")

tk.Label(root, text="File Organizer", font=("Arial", 16, "bold")).pack(pady=10)

#Source Block
tk.Label(root, text="1. Select Source Folder (Messy):", anchor="w").pack(fill="x", padx=20)
frame_src = tk.Frame(root)
frame_src.pack(pady=5)
entry_source = tk.Entry(frame_src, width=35)
entry_source.pack(side=tk.LEFT, padx=5)
tk.Button(frame_src, text="Browse", command=select_source).pack(side=tk.LEFT)

#Destination Block
tk.Label(root, text="2. Select Destination Folder (Clean):", anchor="w").pack(fill="x", padx=20, pady=(15,0))
frame_dest = tk.Frame(root)
frame_dest.pack(pady=5)
entry_dest = tk.Entry(frame_dest, width=35)
entry_dest.pack(side=tk.LEFT, padx=5)
tk.Button(frame_dest, text="Browse", command=select_dest).pack(side=tk.LEFT)

#Progress Bar
progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=350, mode='determinate')
progress_bar.pack(pady=20)

btn_run = tk.Button(root, text="Move & Organize Files", command=start_organizing, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"))
btn_run.pack(pady=5, ipadx=10, ipady=5)

lbl_status = tk.Label(root, text="Ready", font=("Arial", 9, "italic"))
lbl_status.pack(pady=5)

#Loading previously saved settings
settings = load_settings()
entry_source.insert(0, settings.get("source", ""))
entry_dest.insert(0, settings.get("dest", ""))


#Finally done!!!!
root.mainloop()