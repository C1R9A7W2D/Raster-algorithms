from PIL import Image

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

class FloodFillApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Border select")
        
        self.canvas = tk.Canvas(master, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.image = None

        self.load_button = tk.Button(master, text="Load Image", command=self.load_image)
        self.load_button.pack()
        
        self.canvas.bind("<Button-1>", self.find_and_draw_boundary)
        
    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path).convert("RGBA")
            self.display_image()

    def find_and_draw_boundary(self, event):
        if self.image is not None:
            x, y = event.x, event.y
            target_color = self.image.getpixel((x, y))
            boundary_points = self.find_boundary((x, y), target_color)
            self.draw_boundary(boundary_points)
            self.display_image()

    def find_boundary(self, start_point, target_color):
        width, height = self.image.size
        visited = set()
        boundary_points = []
        stack = [start_point]
        prev_dir = 2

        while stack:
            x, y = stack.pop()
            if (x, y) in visited or x < 0 or x >= width or y < 0 or y >= height:
                continue

            visited.add((x, y))
            current_color = self.image.getpixel((x, y))

            if current_color == target_color:
                boundary_points.append((x, y))
                neighbors = [(x + 1, y), (x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
                for i in range((prev_dir - 2) % 8, (prev_dir - 3) % 8):
                    if neighbors[i] not in visited:
                        stack.append(neighbors[i])

        return boundary_points

    def draw_boundary(self, boundary_points):
        for point in boundary_points:
            self.image.putpixel(point, (255, 0, 0))
        return self.image
            
    def display_image(self):
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = FloodFillApp(root)
    root.mainloop()
