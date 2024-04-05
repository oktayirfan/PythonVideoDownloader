from pytube import YouTube
import tkinter as tk
from tkinter import filedialog, ttk
import threading  # Import threading module
import os  # Import os module for opening the download folder
import subprocess  # Import subprocess for opening the folder across platforms

def on_download_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = int((bytes_downloaded / total_size) * 100)
    progress_bar['value'] = percentage
    app.update_idletasks()  # Update the GUI to reflect the progress change

def open_download_folder(path):
    """Open the download folder in the file explorer."""
    try:
        if os.name == 'nt':  # Windows
            os.startfile(path)
        elif os.name == 'posix':  # macOS, Linux
            subprocess.Popen(['open' if sys.platform == 'darwin' else 'xdg-open', path])
    except Exception as e:
        print(f"Error opening folder: {e}")

def show_open_folder_button(path):
    """Show the 'Open Folder' button."""
    open_folder_button = tk.Button(app, text="Open Downloaded Folder", command=lambda: open_download_folder(path))
    open_folder_button.pack(pady=5)

def download_video_thread(url, save_path):
    try:
        yt = YouTube(url, on_progress_callback=on_download_progress)
        streams = yt.streams.filter(progressive=True, file_extension='mp4')
        highest_res_stream = streams.get_highest_resolution()
        highest_res_stream.download(output_path=save_path)
        print("Video downloaded successfully!")
        app.after(0, show_open_folder_button, save_path)  # Show the 'Open Folder' button on the GUI thread
    except Exception as e:
        print(f"Error: {e}")

def start_download():
    url = url_entry.get()
    save_path = save_path_label.cget("text")
    if not save_path:
        print("Please select a save path first.")
        return
    # Start the download in a separate thread
    threading.Thread(target=download_video_thread, args=(url, save_path), daemon=True).start()

def select_save_path():
    folder_selected = filedialog.askdirectory()  # Open dialog to choose directory
    if folder_selected:
        save_path_label.config(text=folder_selected)

# Set up the GUI
app = tk.Tk()
app.title("Video Downloader")

# URL entry
tk.Label(app, text="YouTube URL:").pack()
url_entry = tk.Entry(app)
url_entry.pack(pady=5)

# Path selection
tk.Button(app, text="Select Download Folder", command=select_save_path).pack()
save_path_label = tk.Label(app, text="")
save_path_label.pack()

# Progress bar
progress_bar = ttk.Progressbar(app, orient=tk.HORIZONTAL, length=400, mode='determinate')
progress_bar.pack(pady=20)

# Download button - this is always visible from the start
download_button = tk.Button(app, text="Download Video", command=start_download)
download_button.pack(pady=20)

app.geometry('500x200')
app.mainloop()
