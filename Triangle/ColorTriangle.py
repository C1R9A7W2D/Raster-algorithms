import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox

class SimpleTriangleApp:
    def __init__(self):
        self.fig, (self.ax, self.ax_input) = plt.subplots(1, 2, figsize=(16, 8))
        plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.25)
    
        self.vertices = np.array([[100, 100], [300, 150], [200, 350]], dtype=float)
        
        self.colors = np.array([[255, 0, 0],  
                               [0, 255, 0],   
                               [0, 0, 255]]) 
        
        self.width, self.height = 500, 500

        self.setup_ui()
        self.update_plot()
    
    def barycentric_coordinates(self, p, v1, v2, v3):
        denom = (v2[1] - v3[1]) * (v1[0] - v3[0]) + (v3[0] - v2[0]) * (v1[1] - v3[1])
        
        if abs(denom) < 1e-10:
            return 0, 0, 0
        
        l1 = ((v2[1] - v3[1]) * (p[0] - v3[0]) + (v3[0] - v2[0]) * (p[1] - v3[1])) / denom
        l2 = ((v3[1] - v1[1]) * (p[0] - v3[0]) + (v1[0] - v3[0]) * (p[1] - v3[1])) / denom
        l3 = 1 - l1 - l2
        
        return l1, l2, l3
    
    def rasterize_triangle(self):
        image = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        v1, v2, v3 = self.vertices
        color1, color2, color3 = self.colors

        min_x = max(0, int(min(v1[0], v2[0], v3[0])))
        max_x = min(self.width - 1, int(max(v1[0], v2[0], v3[0])))
        min_y = max(0, int(min(v1[1], v2[1], v3[1])))
        max_y = min(self.height - 1, int(max(v1[1], v2[1], v3[1])))
        
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                l1, l2, l3 = self.barycentric_coordinates((x, y), v1, v2, v3)
                
                if l1 >= 0 and l2 >= 0 and l3 >= 0:
                    r = l1 * color1[0] + l2 * color2[0] + l3 * color3[0]
                    g = l1 * color1[1] + l2 * color2[1] + l3 * color3[1]
                    b = l1 * color1[2] + l2 * color2[2] + l3 * color3[2]
                    
                    image[y, x] = [int(r), int(g), int(b)]
        
        return image
    
    def setup_ui(self):
        self.text_boxes = []
        coord_labels = ['X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3']
        initial_values = ['100', '100', '300', '150', '200', '350']
        
        for i, (label, initial_val) in enumerate(zip(coord_labels, initial_values)):
            ax_text = plt.axes([0.05 + (i % 3) * 0.15, 0.15 - (i // 3) * 0.04, 0.12, 0.03])
            text_box = TextBox(ax_text, label, initial=initial_val)
            text_box.on_submit(self.update_from_textboxes)
            self.text_boxes.append(text_box)

        ax_r1 = plt.axes([0.65, 0.85, 0.25, 0.02])
        ax_g1 = plt.axes([0.65, 0.80, 0.25, 0.02])
        ax_b1 = plt.axes([0.65, 0.75, 0.25, 0.02])
        
        self.slider_r1 = Slider(ax_r1, 'V1 Красный', 0, 255, valinit=255, color='red')
        self.slider_g1 = Slider(ax_g1, 'V1 Зеленый', 0, 255, valinit=0, color='green')
        self.slider_b1 = Slider(ax_b1, 'V1 Синий', 0, 255, valinit=0, color='blue')
        
        ax_r2 = plt.axes([0.65, 0.65, 0.25, 0.02])
        ax_g2 = plt.axes([0.65, 0.60, 0.25, 0.02])
        ax_b2 = plt.axes([0.65, 0.55, 0.25, 0.02])
        
        self.slider_r2 = Slider(ax_r2, 'V2 Красный', 0, 255, valinit=0, color='red')
        self.slider_g2 = Slider(ax_g2, 'V2 Зеленый', 0, 255, valinit=255, color='green')
        self.slider_b2 = Slider(ax_b2, 'V2 Синий', 0, 255, valinit=0, color='blue')
        
        ax_r3 = plt.axes([0.65, 0.45, 0.25, 0.02])
        ax_g3 = plt.axes([0.65, 0.40, 0.25, 0.02])
        ax_b3 = plt.axes([0.65, 0.35, 0.25, 0.02])
        
        self.slider_r3 = Slider(ax_r3, 'V3 Красный', 0, 255, valinit=0, color='red')
        self.slider_g3 = Slider(ax_g3, 'V3 Зеленый', 0, 255, valinit=0, color='green')
        self.slider_b3 = Slider(ax_b3, 'V3 Синий', 0, 255, valinit=255, color='blue')

        ax_reset = plt.axes([0.72, 0.25, 0.1, 0.04])
        self.button_reset = Button(ax_reset, 'СБРОС', color='lightcoral', hovercolor='red')

        self.slider_r1.on_changed(self.update_from_sliders)
        self.slider_g1.on_changed(self.update_from_sliders)
        self.slider_b1.on_changed(self.update_from_sliders)
        self.slider_r2.on_changed(self.update_from_sliders)
        self.slider_g2.on_changed(self.update_from_sliders)
        self.slider_b2.on_changed(self.update_from_sliders)
        self.slider_r3.on_changed(self.update_from_sliders)
        self.slider_g3.on_changed(self.update_from_sliders)
        self.slider_b3.on_changed(self.update_from_sliders)
        self.button_reset.on_clicked(self.reset)
    
    def update_from_textboxes(self, text):
        try:
            x1 = float(self.text_boxes[0].text)
            y1 = float(self.text_boxes[1].text)
            x2 = float(self.text_boxes[2].text)
            y2 = float(self.text_boxes[3].text)
            x3 = float(self.text_boxes[4].text)
            y3 = float(self.text_boxes[5].text)
            
            x1 = max(0, min(self.width, x1))
            y1 = max(0, min(self.height, y1))
            x2 = max(0, min(self.width, x2))
            y2 = max(0, min(self.height, y2))
            x3 = max(0, min(self.width, x3))
            y3 = max(0, min(self.height, y3))
            
            self.vertices = np.array([[x1, y1], [x2, y2], [x3, y3]], dtype=float)
            self.update_plot()
            
        except ValueError:
            pass
    
    def update_from_sliders(self, val):
        self.colors[0] = [self.slider_r1.val, self.slider_g1.val, self.slider_b1.val]
        self.colors[1] = [self.slider_r2.val, self.slider_g2.val, self.slider_b2.val]
        self.colors[2] = [self.slider_r3.val, self.slider_g3.val, self.slider_b3.val]
        
        self.update_plot()
    
    def update_plot(self):
        self.ax.clear()
        self.ax_input.clear()
        
        image = self.rasterize_triangle()
        
        self.ax.imshow(image, origin='lower', extent=[0, self.width, 0, self.height])
        
        for i, (vertex, color) in enumerate(zip(self.vertices, self.colors)):
            self.ax.plot(vertex[0], vertex[1], 'o', markersize=10, 
                        color=np.array(color)/255, markeredgecolor='black', markeredgewidth=2)
            self.ax.text(vertex[0] + 15, vertex[1] + 15, f'V{i+1}', fontsize=12, 
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        
        self.ax_input.axis('off')
        info_text = (
           "X, Y ∈ [0, 500]\n"
            "RGB ∈ [0, 255]"
        )
        
        self.ax_input.text(0.05, -0.13, info_text, fontsize=11, va='top', 
                          bbox=dict(boxstyle="round,pad=0.8", facecolor="lightblue", alpha=0.7),
                          linespacing=1.5)
        
        self.fig.canvas.draw_idle()
    
    
    def reset(self, event):
        self.vertices = np.array([[100, 100], [300, 150], [200, 350]], dtype=float)
        
        reset_values = ['100', '100', '300', '150', '200', '350']
        for text_box, value in zip(self.text_boxes, reset_values):
            text_box.set_val(value)
        
        self.colors = np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]])
        self.slider_r1.set_val(255)
        self.slider_g1.set_val(0)
        self.slider_b1.set_val(0)
        self.slider_r2.set_val(0)
        self.slider_g2.set_val(255)
        self.slider_b2.set_val(0)
        self.slider_r3.set_val(0)
        self.slider_g3.set_val(0)
        self.slider_b3.set_val(255)
        
        self.update_plot()
    
    def show(self):
        plt.show()

if __name__ == "__main__":

    app = SimpleTriangleApp()
    app.show()