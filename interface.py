import PIL.ImageShow
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os


# Функция для создания градиента (предыдущий код)
def create_gradient(start_color, end_color, width, height):
    gradient = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(width):
        alpha = i / width
        color = (1 - alpha) * np.array(start_color) + alpha * np.array(end_color)
        gradient[:, i] = color
    return gradient


# Функция для нахождения наиболее ближайшего цвета
def find_closest_color(gradient, target_rgb):
    # Конвертация RGB в BGR
    target_bgr = target_rgb[::-1]

    # Расчет Евклидова расстояния от каждого пикселя до целевого цвета
    distances = np.sqrt(np.sum((gradient - target_bgr) ** 2, axis=2))

    # Находим индекс пикселя с минимальным расстоянием
    min_dist_index = np.unravel_index(np.argmin(distances), distances.shape)

    # Возвращаем цвет пикселя и его позицию
    closest_color = gradient[min_dist_index]
    return closest_color[::-1], min_dist_index  # Возвращаем в формате RGB и позицию


def create_gradient_segment(start_color, end_color, width):
    """Создает горизонтальный градиент между двумя заданными цветами."""
    start_color = np.array(start_color[::-1], dtype=np.uint8)  # Конвертация из RGB в BGR
    end_color = np.array(end_color[::-1], dtype=np.uint8)  # Конвертация из RGB в BGR

    gradient = np.zeros((1, width, 3), dtype=np.uint8)

    for x in range(width):
        alpha = x / (width - 1)
        color = (1 - alpha) * start_color + alpha * end_color
        gradient[0, x] = color

    return gradient


def create_multi_gradient(colors, width, height):
    """Создает градиент через список цветов."""
    segments_count = len(colors) - 1
    segment_width = width // segments_count
    gradient = np.zeros((height, width, 3), dtype=np.uint8)

    for i in range(segments_count):
        segment = create_gradient_segment(colors[i], colors[i + 1], segment_width)
        segment = cv2.resize(segment, (segment_width, height), interpolation=cv2.INTER_LINEAR)
        gradient[:, i * segment_width:(i + 1) * segment_width] = segment

    # Для последнего сегмента, если ширина не делится нацело
    if width % segments_count != 0:
        last_segment_width = width - (segments_count - 1) * segment_width
        last_segment = create_gradient_segment(colors[-2], colors[-1], last_segment_width)
        last_segment = cv2.resize(last_segment, (last_segment_width, height), interpolation=cv2.INTER_LINEAR)
        gradient[:, -last_segment_width:] = last_segment

    return gradient


def process_images_from_folder(folder_path):
    results = []  # Список для хранения результатов

    # Перебор всех файлов в директории
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Проверка формата файла
            file_path = os.path.join(folder_path, filename)
            image = Image.open(file_path)
            width, height = image.size

            # Вычисление координат для квадрата 50x50 пикселей в центре изображения
            left = (width/2) - 50
            top = (height/2) - 50
            right = (width/2) + 50
            bottom = (height/2) + 50

            # Обрезка изображения
            cropped_image = image.crop((int(left), int(top), int(right), int(bottom)))
            # Вычисление средних значений RGB
            average_color = [c for c in cropped_image.resize((1, 1), Image.Resampling.LANCZOS).getpixel((0, 0))]

            # Добавление результатов в список
            results.append([filename.rsplit('.', 1)[0], average_color[0], average_color[1], average_color[2]])

    return results


# Пример использования

# Путь к папке с изображениями
folder_path = 'results'
results = process_images_from_folder(folder_path)

colors = []
# Вывод результатов
for result in results:
    colors.append((result[1], result[2], result[3]))
#print(colors)

# colors = [color5_8, color6_1, color6_4, color6_6, color6_8, color7_0, color7_3, color7_7]
bar_width, bar_height = 800, 100

# Создание градиента
gradient = create_multi_gradient(colors, bar_width, bar_height)
# Целевой цвет RGB
image = Image.open("results/7.6.png")
width, height = image.size

# Вычисление координат для квадрата 50x50 пикселей в центре изображения
left = (width / 2) - 50
top = (height / 2) - 50
right = (width / 2) + 50
bottom = (height / 2) + 50

# Обрезка изображения
cropped_image = image.crop((int(left), int(top), int(right), int(bottom)))
# Вычисление средних значений RGB
average_color = [c for c in cropped_image.resize((1, 1), Image.Resampling.LANCZOS).getpixel((0, 0))]
print(average_color)
target_rgb = (average_color[0], average_color[1], average_color[2])
# Поиск наиболее ближайшего цвета
closest_color, position = find_closest_color(gradient, target_rgb)

print(f"Ближайший цвет: {closest_color} на позиции: {position}")
delta_ph = 8 - 5.8
res = 5.8 + delta_ph*(position[1]/bar_width)
print(res)
# Отображение изображения с маркером ближайшего цвета
cv2.line(gradient, (position[1], 0), (position[1], gradient.shape[0]), (0, 0, 255), thickness=1)
cv2.imshow('Gradient with Closest Color Marked', gradient)
cv2.waitKey(0)
cv2.destroyAllWindows()



def main():
    def choose_bromothymol_blue():
        global colors, delta_ph, low_num, name, name_en
        colors = [(205, 188, 109),
                  (202, 188, 126),
                  (187, 177, 130),
                  (182, 174, 130),
                  (191, 188, 150),
                  (180, 180, 154),
                  (188, 193, 168),
                  (175, 186, 174),
                  (167, 182, 176),
                  (158, 178, 179),
                  (148, 172, 178),
                  (143, 170, 184),
                  (125, 162, 180)]
        delta_ph = 8 - 5.8
        low_num = 5.8
        name = 'Бромтимоловый синий'
        name_en = 'Bromothymol Blue'
        root.title("pH_detector")
        root.iconbitmap('photos/icon.ico')

    def choose_bromocresol_purple():
        global colors, delta_ph, low_num, name, name_en
        colors = [(201, 193, 159),
                  (201, 195, 159),
                  (206, 201, 172),
                  (209, 204, 172),
                  (201, 198, 173),
                  (203, 199, 171),
                  (201, 197, 171),
                  (210, 204, 174),
                  (198, 196, 176),
                  (206, 200, 176),
                  (201, 197, 176),
                  (197, 191, 172),
                  (190, 184, 168),
                  (187, 184, 174),
                  (184, 181, 174),
                  (181, 181, 181),
                  (177, 176, 178),
                  (177, 177, 181),
                  (179, 178, 185),
                  (180, 178, 185),
                  (175, 176, 191),
                  (165, 166, 182),
                  (166, 167, 186),
                  (161, 161, 184),
                  (155, 156, 177)]
        delta_ph = 7.2 - 4.8
        low_num = 4.8
        name = 'Бромкрезоловый пурпурный'
        name_en = 'Bromocresol purple'
        root.title("pH_detector")
        root.iconbitmap('photos/icon.ico')

    root = tk.Tk()
    root.title("Выбор шкалы")
    root.iconbitmap('photos/icon.ico')

    scale_label = tk.Label(root, text="Выберите шкалу градиента:")
    scale_label.pack()

    frame = tk.Frame(root)
    frame.pack()

    bromothymol_button = tk.Button(frame, text="Бромтимоловый синий", command=lambda: (choose_bromothymol_blue, process_image(root)))
    bromothymol_button.pack(side=tk.LEFT)

    bromocresol_button = tk.Button(frame, text="Бромкрезоловый пурпурный", command=lambda: (choose_bromocresol_purple, process_image(root)))
    bromocresol_button.pack(side=tk.RIGHT)

    start_button = tk.Button(root, text="Выбрать фотографию", command=lambda: process_image(root))

    center_window(root, 400, 90)

    root.mainloop()