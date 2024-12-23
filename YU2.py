import tkinter
import tkinter as tk
from PIL import Image ,ImageTk
from tkinter import filedialog, messagebox
from tkinter import ttk

try:
    import yt_dlp
except ModuleNotFoundError:
    import sys
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp
# Ensure moviepy is installed with pip: pip install moviepy
import moviepy.audio.io.AudioFileClip as mp
import os
import time

def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a YouTube URL")
        return

    download_path = filedialog.askdirectory()
    if not download_path:
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', None)
            video_ext = info_dict.get('ext', None)
            downloaded_file = os.path.join(download_path, f"{video_title}.{video_ext}")
            convert_to_mp3(downloaded_file, download_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video: {str(e)}")


def convert_to_mp3(file_path, download_path):
    mp3_path = file_path.rsplit(".", 1)[0] + ".mp3"

    try:
        clip = mp.AudioFileClip(file_path)
        clip.write_audiofile(mp3_path)
        os.remove(file_path)
        messagebox.showinfo("Conversion Complete", "Video converted to MP3 successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert video: {str(e)}")


app = tk.Tk()
app.title("YouTube Downloader and MP3 Converter")

tk.Label(app, text="YouTube URL:").grid(row=1, column=1, padx=10, pady=10)
url_entry = tk.Entry(app, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=5)

download_button = tk.Button(app, text="Download & Convert", command=download_video)
download_button.grid(row=1, column=0, columnspan=2, pady=20)

# configuracion de vista de ventana
app.geometry("500x300")
app.configure(bg="#f0f0f0")

# Add a title label at the top

title_label = tk.Label(app, text="   YouTube Downloader BY v3noms   ", font=('Helvetica', 18, 'bold'), bg="#990099", fg="#333")
title_label.grid(row=0, column=0, columnspan=2, pady=5)

# Establecer el tamaño de la ventana
app.geometry("500x300")
# Ajusta el tamaño según tus necesidades
# Evitar redimensionamiento de la ventana
app.resizable(False, False) #
#Establecer el fondo de pantalla
bg_image = Image.open("space.jpg")
# Reemplaza con tu archivo de imagen
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(app, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)
# Asegurar que otros widgets se coloquen encima de la imagen de fondo
bg_label.lower()
# Add YouTube URL label and entry field
tk.Label(app, text="YouTube URL:", bg="#ff0000", font=('Helvetica', 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
url_entry = tkinter.Entry(app, width=50)
url_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")



button_style = {
'font': ('Helvetica', 12, 'bold'),# tipo de fuente
    'bg': 'red', #color de fondo rojo
    'fg':'white' ,#color de texto blanco
    'activebackground': 'purple', # color de fondo al hacer click
    'activeforeground': 'white', #color de texto al hacer click
    'relief': tk.RAISED,
    'bd':5 #ancho del borde
}
# Create the styled Download & Convert button
download_button = tk.Button(app, text="Download & Convert", command=download_video, **button_style)
download_button.grid(row=2, column=1, pady=20, sticky="e")


app.resizable(False, False)

# Crear el menú contextual
context_menu = tk.Menu(app, tearoff=0)
def paste_text():
    try:
        url_entry.insert(tk.END, app.clipboard_get())
    except tk.TclError:
        pass
##menu contextual pegar or paste
context_menu.add_command(label="Pegar", command=paste_text)
# Asignar el menú contextual al evento de clic derecho
url_entry.bind("<Button-3>", lambda event: context_menu.post(event.x_root, event.y_root))

download_button = tk.Button(app, text="Download & Convert", command=download_video, **button_style)
download_button.grid(row=2, column=1, pady=20, sticky="e")


app.mainloop()
