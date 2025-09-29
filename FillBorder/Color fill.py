from PIL import Image

def find_boundaries(image, x, y, target_color):
    left = x
    right = x

    while left > 0 and image.getpixel((left - 1, y)) == target_color:
        left -= 1

    while right < image.width - 1 and image.getpixel((right + 1, y)) == target_color:
        right += 1

    return left, right

def flood_fill(image, x, y, target_color, replacement_color):
    if y < 0 or y >= image.height or x < 0 or x >= image.width:
        return
    if image.getpixel((x, y)) != target_color:
        return
    if image.getpixel((x, y)) == replacement_color:
        return

    left, right = find_boundaries(image, x, y, target_color)

    for j in range(left, right + 1):
        image.putpixel((j, y), replacement_color)

    if y > 0:
        for j in range(left, right + 1):
            flood_fill(image, j, y - 1, target_color, replacement_color)

    if y < image.height - 1:
        for j in range(left, right + 1):
            flood_fill(image, j, y + 1, target_color, replacement_color)

if __name__ == "__main__":
    image = Image.new("RGB", (5, 5), "white")
    pixels = image.load()

    pixels[1, 1] = (0, 0, 0)
    pixels[1, 2] = (0, 0, 0)
    pixels[2, 1] = (0, 0, 255)
    pixels[2, 3] = (0, 255, 0)
    pixels[3, 1] = (0, 0, 0)
    pixels[3, 2] = (0, 0, 0)
    pixels[3, 3] = (0, 0, 0)

    print("Исходное изображение:")
    image = Image.open('channels4_profile.jpg')
    image.show()

    target_color = (0, 0, 0)

    pixels = image.load()
    target_color = pixels[1, 1];    #Выбираем цвет конкретного пикселя
    
    replacement_color = (255, 0, 0)  # Красный цвет
    flood_fill(image, 1, 1, target_color, replacement_color)

    print("\nИзображение после заливки:")
    image.show()
