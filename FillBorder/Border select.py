from PIL import Image
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

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
        direction = 0
        current_point = start_point
        x, y = current_point
        
        while self.image.getpixel((x, y)) == target_color:
            x += 1
            
        current_point = (x, y)

        while True:
            x, y = current_point
            if (x, y) in visited or x < 0 or x >= width or y < 0 or y >= height:
                break

            visited.add((x, y))
            current_color = self.image.getpixel((x, y))

            boundary_points.append((x, y))

            for i in range(8):
                next_direction = (direction + i) % 8
                neighbor = self.get_neighbor(current_point, next_direction)

                neighbor_color = self.image.getpixel(neighbor)
                if neighbor_color != target_color:
                    current_point = neighbor
                    direction = (direction + i - 2) % 8
                    break

        boundary_points.sort(key=lambda point: (point[1], point[0]))
        return boundary_points

    def get_neighbor(self, point, direction):
        x, y = point
        if direction == 0:
            return (x, y + 1)
        elif direction == 1:
            return (x + 1, y + 1)
        elif direction == 2:
            return (x + 1, y)
        elif direction == 3:
            return (x + 1, y - 1)
        elif direction == 4:
            return (x, y - 1)
        elif direction == 5:
            return (x - 1, y - 1)
        elif direction == 6:
            return (x - 1, y)
        elif direction == 7:
            return (x - 1, y + 1)

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
