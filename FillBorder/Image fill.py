from PIL import Image

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

class FloodFillApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Flood Fill with Pattern")
        
        self.canvas = tk.Canvas(master, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.pattern = None
        self.start_x = None
        self.start_y = None
        self.image = Image.new("RGBA", (500, 500), (255, 255, 255, 255))  # Создаем пустое изображение
        self.draw = ImageDraw.Draw(self.image)
        self.drawing = False

        self.load_button = tk.Button(master, text="Load Image", command=self.load_image)
        self.load_button.pack()
        
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw_area)
        self.canvas.bind("<ButtonRelease-1>", self.end_drawing)
        self.canvas.bind("<Button-3>", self.flood_fill)
        
    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.pattern = Image.open(file_path).convert("RGBA")

    def start_drawing(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.drawing = True

    def draw_area(self, event):
        if self.drawing:
            # Рисуем линию на холсте
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill="black", width=2)
            # Рисуем на изображении
            self.draw.line([self.start_x, self.start_y, event.x, event.y], fill="black", width=2)
            self.start_x = event.x
            self.start_y = event.y

    def end_drawing(self, event):
        self.drawing = False

    def flood_fill(self, event):
        if self.pattern is not None:
            x, y = event.x, event.y  # Получаем координаты щелчка
            target_color = self.image.getpixel((x, y))
            self.flood_fill_algorithm_up(x, y, target_color)        #Алгоритм разделён на две части, потому что двусторонний постоянно пересекается сам с собой
            self.flood_fill_algorithm_down(x, y + 1, target_color)
            self.display_image()

    def find_boundaries(self, x, y, target_color):
        left = x
        right = x

        while left > 0 and self.image.getpixel((left - 1, y)) == target_color:
            left -= 1

        while right < self.image.width - 1 and self.image.getpixel((right + 1, y)) == target_color:
            right += 1

        return left, right

    def flood_fill_algorithm_up(self, x, y, target_color):
        if y < 0 or y >= self.image.height or x < 0 or x >= self.image.width:
            return
        if self.image.getpixel((x, y)) != target_color:
            return

        left, right = self.find_boundaries(x, y, target_color)

        for j in range(left, right + 1):
            self.image.paste(self.pattern, (j, y), self.pattern)

        if y > 0:
            for j in range(left, right + 1):
                self.flood_fill_algorithm_up(j, y - 1, target_color)

    def flood_fill_algorithm_down(self, x, y, target_color):
        if y < 0 or y >= self.image.height or x < 0 or x >= self.image.width:
            return
        if self.image.getpixel((x, y)) != target_color:
            return

        left, right = self.find_boundaries(x, y, target_color)

        for j in range(left, right + 1):
            self.image.paste(self.pattern, (j, y), self.pattern)

        if y < self.image.height - 1:
            for j in range(left, right + 1):
                self.flood_fill_algorithm_down(j, y + 1, target_color)
            
    def display_image(self):
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = FloodFillApp(root)
    root.mainloop()
