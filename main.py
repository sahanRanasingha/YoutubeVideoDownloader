import tkinter as tk
from tkinter import scrolledtext
from pytube import YouTube
import threading
import time

def download_video():
    video_url = entry_url.get()
    
    # Disable the download button during the download process
    download_button.config(state=tk.DISABLED)
    
    # Enable the title_text widget to show the video title
    title_text.config(state=tk.NORMAL)

    # Show Download Start label
    download_start_label.pack()

    # Create a new thread for the download process
    download_thread = threading.Thread(target=download_video_thread, args=(video_url,))
    download_thread.start()

    # Periodically check the download status
    root.after(100, check_download_status)

def download_video_thread(video_url):
    try:
        yt = YouTube(video_url)
        video = yt.streams.filter(file_extension='mp4', progressive=True).first()
        
        # Get the download file name
        file_name = video.title
        
        # Update the title_text widget with the video title
        root.after(0, lambda: title_text.delete(1.0, tk.END))
        root.after(0, lambda: title_text.insert(tk.END, file_name))
        
        start_time = time.time()
        video.download()
        end_time = time.time()

        # Calculate download time
        download_time = round(end_time - start_time, 2)
        
        # Update the status label in the main thread
        root.after(0, lambda: status_label.config(text=f"Download Successful! Time: {download_time} seconds", fg="green"))
    except Exception as e:
        # Update the status label in the main thread
        root.after(0, lambda: status_label.config(text=f"Error: {str(e)}", fg="red"))
    finally:
        # Enable the download button and disable the title_text widget after the download process is complete
        root.after(0, lambda: download_button.config(state=tk.NORMAL))

        # Hide Download Start label
        download_start_label.pack_forget()


def check_download_status():
    # This function is called periodically to check the download status
    if threading.active_count() > 1:
        # If the download thread is still active, schedule the function to be called again
        root.after(100, check_download_status)
    else:
        # If the download thread is not active, reset the button color
        download_button.config(bg='#008CBA', fg='white')

# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")

# Set the window size and position
window_width = 400
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = int((screen_width - window_width) / 2)
y_position = int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Set window background color
root.configure(bg='#f0f0f0')

# Create and pack widgets with some styling
label_url = tk.Label(root, text="Enter YouTube URL:", bg='#f0f0f0', font=('Arial', 12))
label_url.pack(pady=10)

entry_url = tk.Entry(root, width=40, font=('Arial', 10))
entry_url.pack(pady=10)

download_button = tk.Button(root, text="Download Video", command=download_video, font=('Arial', 12), bg='#008CBA', fg='white')
download_button.pack(pady=10)

title_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=3, font=('Arial', 10), state=tk.DISABLED)
title_text.pack(pady=5)

status_label = tk.Label(root, text="", fg="black", bg='#f0f0f0', font=('Arial', 12))
status_label.pack(pady=10)

# Label for Download Start
download_start_label = tk.Label(root, text="Download Start", fg="blue", bg='#f0f0f0', font=('Arial', 12))
download_start_label.pack_forget()  # Initially hide this label

# Start the GUI main loop
root.mainloop()
