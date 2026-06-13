import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk

class GifApp(tk.Tk):
    
    def __init__(self):
        super().__init__()

        self.title("Gif Converter App!")
        self.geometry("800x850")

        self.video_path = ''
        self.output_path = ''
        self.frames = []
        self.preview_frame_index = 0

        # select video button:
        self.select_video_button = tk.Button(self, text="Select Video", command=self.select_video)
        self.select_video_button.pack(pady=10)

        # preview label
        self.preview_label = tk.Label(self, text="Video Preview")
        self.preview_label.pack()

        # canvas
        self.canvas = tk.Canvas(self, width=640, height=480)
        self.canvas.pack(pady=10)

        # speed label
        self.speed_label = tk.Label(self, text="Speed (fps): ")
        self.speed_label.pack(pady=10)

        # speed entry
        self.speed_entry = tk.Entry(self)
        self.speed_entry.pack()
        self.speed_entry.insert(0, "10")

        # scale label
        self.scale_label = tk.Label(self, text="Scale (1.0 = 100%): ")
        self.scale_label.pack(pady=10)

        # scale entry
        self.scale_entry = tk.Entry(self)
        self.scale_entry.pack()
        self.scale_entry.insert(0, "10")

        # export button
        self.export_button = tk.Button(self, text="Export GIF", command=self.export_gif)
        self.export_button.pack(pady=20)

        # progress bar
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=100, 
                                        mode="indeterminate")
        self.progress.pack(pady=20)

    def select_video(self):
        """Selects a video to use from files."""
        pass

    def export_gif(self):
        """Converts video into gif."""
        pass


def main():
    test = GifApp()
    test.mainloop()

