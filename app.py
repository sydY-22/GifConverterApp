import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk

BLACK_COLOR = "#2C2C2C"

class GifApp(tk.Tk):
    
    def __init__(self):
        super().__init__()

        self.title("Gif Converter App!")
        self.geometry("800x875")
        self.config(bg=BLACK_COLOR)

        self.video_path = ''
        self.output_path = ''
        self.frames = []
        self.preview_frame_index = 0

        # title label:
        self.label_title = tk.Label(self, text="GIF Converter App!", font=("bold", 20))
        self.label_title.pack(pady=0.5)

        # select video button:
        self.select_video_button = tk.Button(self, text="Select Video", command=self.select_video)
        self.select_video_button.pack(pady=5)

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
        self.scale_entry.insert(0, "0.5")

        # export button
        self.export_button = tk.Button(self, text="Export GIF", command=self.export_gif)
        self.export_button.pack(pady=5)

        # progress bar
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=100, 
                                        mode="indeterminate")
        self.progress.pack(pady=5)

    def select_video(self):
        """Selects a video to use from files."""
        self.video_path = filedialog.askopenfilename(title="Select Video", 
                                                     filetypes=(("MP4 Files", "*mp4"), ("All Files", "*.*")))
        if self.video_path:
            self.process_video()


    def process_video(self):
        """Processes the video using capture, frames and color."""
        if not self.video_path:
            return
        
        cap = cv2.VideoCapture(self.video_path)
        self.frames = []

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.frames.append(frame)
        
        cap.release()

        self.preview_frame_index = 0
        self.animate_preview()

    def animate_preview(self):
        """Show the animation in canvas to show preview."""

        # check if you have frames:
        if not self.frames:
            return
        
        frame = self.frames[self.preview_frame_index] # get each frame
        frame_image = Image.fromarray(frame)
        frame_image = frame_image.resize((640, 480), Image.Resampling.LANCZOS)
        frame_photo = ImageTk.PhotoImage(frame_image)

        # take the current image and resize it then put on canvas:
        self.canvas.create_image(0, 0, anchor=tk.NW, image=frame_photo)
        self.canvas.image = frame_photo

        # get current value then increase by 1 then loop frame
        self.preview_frame_index = (self.preview_frame_index + 1) % len(self.frames)
        self.after(100, self.animate_preview)

    def export_gif(self):
        """Converts video into gif."""
        fps = int(self.speed_entry.get())
        scale = float(self.scale_entry.get())

        if not self.frames or fps <= 0 or scale <= 0:
            messagebox.showerror("Error", "Invalid options")
            return
        
        self.output_path = filedialog.asksaveasfilename(defaultextension='.gif', 
                                                        filetypes=(("GIF Files", "*.gif"), ("All Files", "*.*")))
        
        if not self.output_path:
            return
        
        self.progress.start(10)
        threading.Thread(target=self.create_gif, args=(fps, scale), daemon=True).start()

    def create_gif(self, fps, scale):
        """Creates the gif."""
        output_frames = []

        for frame in self.frames:
            img = Image.fromarray(frame)
            img = img.resize((int(img.width * scale), int(img.height * scale)), Image.Resampling.LANCZOS) # resize frame
            output_frames.append(img) # put resize frame in output frame

        output_frames[0].save(self.output_path, save_all=True, 
                                append_images=output_frames[1:], optimize=False, duration=1000//fps, loop=0) # export to gif
            
        self.after(0, self.progress.stop)
        messagebox.showinfo("Success", "GIF Successfully Exported!")


def main():
    test = GifApp()
    test.mainloop()

