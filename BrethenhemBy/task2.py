import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

def bresenham_line(x0, y0, x1, y1):
    """
    Целочисленный алгоритм Брезенхема для рисования отрезка
    """
    points = []

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    x, y = x0, y0

    x_step = 1 if x1 > x0 else -1
    y_step = 1 if y1 > y0 else -1

    points.append((x, y))

    if dx > dy:
        error = 2 * dy - dx
        for i in range(dx):
            if error >= 0:
                y += y_step
                error -= 2 * dx
            x += x_step
            error += 2 * dy
            points.append((x, y))
    else:
        error = 2 * dx - dy
        for i in range(dy):
            if error >= 0:
                x += x_step
                error -= 2 * dy
            y += y_step
            error += 2 * dx
            points.append((x, y))

    return points

def wu_line(x0, y0, x1, y1):
    """
    Алгоритм Ву для рисования сглаженного отрезка
    """
    points = []

    def plot(x, y, intensity):
        points.append((x, y, intensity))

    steep = abs(y1 - y0) > abs(x1 - x0)

    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0

    if dx == 0:
        gradient = 1.0
    else:
        gradient = dy / dx

    # первая конечная точка
    xend = round(x0)
    yend = y0 + gradient * (xend - x0)
    xgap = 1 - (x0 + 0.5) % 1
    xpxl1 = xend
    ypxl1 = int(yend)

    if steep:
        plot(ypxl1, xpxl1, (1 - (yend % 1)) * xgap)
        plot(ypxl1 + 1, xpxl1, (yend % 1) * xgap)
    else:
        plot(xpxl1, ypxl1, (1 - (yend % 1)) * xgap)
        plot(xpxl1, ypxl1 + 1, (yend % 1) * xgap)

    intery = yend + gradient

    # вторая конечная точка
    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = (x1 + 0.5) % 1
    xpxl2 = xend
    ypxl2 = int(yend)

    if steep:
        plot(ypxl2, xpxl2, (1 - (yend % 1)) * xgap)
        plot(ypxl2 + 1, xpxl2, (yend % 1) * xgap)
    else:
        plot(xpxl2, ypxl2, (1 - (yend % 1)) * xgap)
        plot(xpxl2, ypxl2 + 1, (yend % 1) * xgap)

    # основная часть линии
    for x in range(xpxl1 + 1, xpxl2):
        if steep:
            plot(int(intery), x, 1 - (intery % 1))
            plot(int(intery) + 1, x, intery % 1)
        else:
            plot(x, int(intery), 1 - (intery % 1))
            plot(x, int(intery) + 1, intery % 1)
        intery += gradient

    return points

def create_canvas(width, height):
    """Создает холст для рисования"""
    return np.zeros((height, width))

def draw_points(canvas, points, color=1.0):
    """Рисует точки на холсте"""
    for point in points:
        if len(point) == 2:  # Для Брезенхема
            x, y = point
            if 0 <= x < canvas.shape[1] and 0 <= y < canvas.shape[0]:
                canvas[y, x] = color
        else:  # Для Ву (x, y, intensity)
            x, y, intensity = point
            if 0 <= x < canvas.shape[1] and 0 <= y < canvas.shape[0]:
                canvas[y, x] = max(canvas[y, x], intensity)

def visualize_comparison(x0, y0, x1, y1, canvas_size=(100, 100)):
    """Визуализирует сравнение двух алгоритмов"""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    # Алгоритм Брезенхема
    canvas_bresenham = create_canvas(canvas_size[0], canvas_size[1])
    bresenham_points = bresenham_line(x0, y0, x1, y1)
    draw_points(canvas_bresenham, bresenham_points)

    ax1.imshow(canvas_bresenham, cmap='gray', interpolation='nearest')
    ax1.set_title(f'Алгоритм Брезенхема\nОтрезок ({x0},{y0})→({x1},{y1})')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')

    # Алгоритм Ву
    canvas_wu = create_canvas(canvas_size[0], canvas_size[1])
    wu_points = wu_line(x0, y0, x1, y1)
    draw_points(canvas_wu, wu_points)

    ax2.imshow(canvas_wu, cmap='gray', interpolation='nearest')
    ax2.set_title(f'Алгоритм Ву\nОтрезок ({x0},{y0})→({x1},{y1})')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')

    # Сравнение (увеличенный фрагмент)
    zoom_center_x = (x0 + x1) // 2
    zoom_center_y = (y0 + y1) // 2
    zoom_size = 20

    start_x = max(0, zoom_center_x - zoom_size // 2)
    end_x = min(canvas_size[0], zoom_center_x + zoom_size // 2)
    start_y = max(0, zoom_center_y - zoom_size // 2)
    end_y = min(canvas_size[1], zoom_center_y + zoom_size // 2)

    ax3.imshow(canvas_wu[start_y:end_y, start_x:end_x],
               cmap='gray', interpolation='nearest')
    ax3.set_title(f'Алгоритм Ву (увеличение)\nОбласть {zoom_size}x{zoom_size}')
    ax3.grid(True, alpha=0.3)
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')

    plt.tight_layout()
    plt.show()

    # Вывод информации
    print(f"Алгоритм Брезенхема: {len(bresenham_points)} точек")
    print(f"Алгоритм Ву: {len(wu_points)} точек")
    print(f"Координаты отрезка: ({x0},{y0}) → ({x1},{y1})")

# Демонстрация работы алгоритмов
if __name__ == "__main__":
    print("Демонстрация алгоритмов рисования отрезков")
    print("=" * 50)

    # Тестовые случаи
    test_cases = [
        (10, 10, 80, 40),    # Небольшой наклон
        (20, 70, 70, 20),    # Отрицательный наклон
        (10, 50, 90, 50),    # Горизонтальная линия
        (50, 10, 50, 90),    # Вертикальная линия
        (10, 10, 90, 80),    # Сильный наклон
        (10, 80, 80, 10),    # Сильный отрицательный наклон
    ]

    for i, (x0, y0, x1, y1) in enumerate(test_cases, 1):
        print(f"\nТест {i}:")
        visualize_comparison(x0, y0, x1, y1)

    # Дополнительная демонстрация с разными углами
    print("\n" + "=" * 50)
    print("Демонстрация линий под разными углами:")

    center_x, center_y = 50, 50
    radius = 35

    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.flatten()

    for i, angle in enumerate(range(0, 360, 45)):
        rad = np.radians(angle)
        end_x = int(center_x + radius * np.cos(rad))
        end_y = int(center_y + radius * np.sin(rad))

        canvas = create_canvas(100, 100)
        points = wu_line(center_x, center_y, end_x, end_y)
        draw_points(canvas, points)

        axes[i].imshow(canvas, cmap='gray', interpolation='nearest')
        axes[i].set_title(f'Угол: {angle}°')
        axes[i].grid(True, alpha=0.3)
        axes[i].set_xlabel('X')
        axes[i].set_ylabel('Y')

    plt.tight_layout()
    plt.show()

    # Сравнение качества сглаживания
    print("\n" + "=" * 50)
    print("Сравнение качества сглаживания на наклонной линии:")

    # Линия с небольшим наклоном для демонстрации сглаживания
    x0, y0, x1, y1 = 10, 45, 90, 55

    canvas_bresenham = create_canvas(100, 100)
    canvas_wu = create_canvas(100, 100)

    bresenham_points = bresenham_line(x0, y0, x1, y1)
    wu_points = wu_line(x0, y0, x1, y1)

    draw_points(canvas_bresenham, bresenham_points)
    draw_points(canvas_wu, wu_points)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    im1 = ax1.imshow(canvas_bresenham[40:60, :], cmap='gray',
                     interpolation='nearest', vmin=0, vmax=1)
    ax1.set_title('Алгоритм Брезенхема (лестничный эффект)')
    ax1.grid(True, alpha=0.3)

    im2 = ax2.imshow(canvas_wu[40:60, :], cmap='gray',
                     interpolation='nearest', vmin=0, vmax=1)
    ax2.set_title('Алгоритм Ву (сглаживание)')
    ax2.grid(True, alpha=0.3)

    plt.colorbar(im1, ax=ax1, fraction=0.046)
    plt.colorbar(im2, ax=ax2, fraction=0.046)
    plt.tight_layout()
    plt.show()