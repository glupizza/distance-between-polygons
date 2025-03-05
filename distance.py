import math
import matplotlib.pyplot as plt

def point_to_line_distance(px, py, x1, y1, x2, y2):
    """Вычисляет расстояние от точки (px, py) до отрезка (x1, y1) - (x2, y2)"""
    segment_length_squared = (x2 - x1) ** 2 + (y2 - y1) ** 2
    if segment_length_squared == 0:
        return math.dist((px, py), (x1, y1)), (x1, y1)

    t = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / segment_length_squared
    if t < 0:
        closest_x, closest_y = x1, y1
    elif t > 1:
        closest_x, closest_y = x2, y2
    else:
        closest_x = x1 + t * (x2 - x1)
        closest_y = y1 + t * (y2 - y1)

    return math.dist((px, py), (closest_x, closest_y)), (closest_x, closest_y)


def min_distance_between_polygons(polygon1, polygon2):
    """Находит минимальное расстояние между двумя многоугольниками"""
    min_distance = float("inf")
    closest_points = None

    # Проверяем расстояние от всех вершин poly1 до всех сторон poly2
    for px, py in polygon1[:-1]:
        for (x1, y1), (x2, y2) in zip(polygon2, polygon2[1:]):
            distance, closest_point = point_to_line_distance(px, py, x1, y1, x2, y2)
            if distance < min_distance:
                min_distance = distance
                closest_points = ((px, py), closest_point)

    # Проверяем расстояние от всех вершин poly2 до всех сторон poly1
    for px, py in polygon2[:-1]:
        for (x1, y1), (x2, y2) in zip(polygon1, polygon1[1:]):
            distance, closest_point = point_to_line_distance(px, py, x1, y1, x2, y2)
            if distance < min_distance:
                min_distance = distance
                closest_points = ((px, py), closest_point)

    return min_distance, closest_points


def plot_polygons_and_distance(polygon1, polygon2, closest_points, min_distance):
    """Визуализирует два многоугольника и минимальное расстояние между ними"""
    fig, ax = plt.subplots()

    # Рисуем первый многоугольник
    polygon1_x, polygon1_y = zip(*polygon1)
    ax.plot(polygon1_x + (polygon1_x[0],), polygon1_y + (polygon1_y[0],), label="Polygon 1", color="blue")

    # Рисуем второй многоугольник
    polygon2_x, polygon2_y = zip(*polygon2)
    ax.plot(polygon2_x + (polygon2_x[0],), polygon2_y + (polygon2_y[0],), label="Polygon 2", color="green")

    # Рисуем линию минимального расстояния
    if closest_points:
        (px, py), (closest_x, closest_y) = closest_points
        ax.plot([px, closest_x], [py, closest_y], color="red", linestyle="--", label="Min Distance")

        # Добавляем аннотацию с минимальным расстоянием
        midpoint_x = (px + closest_x) / 2
        midpoint_y = (py + closest_y) / 2
        ax.text(midpoint_x, midpoint_y, f"{min_distance:.2f}", color="red", fontsize=10,
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    ax.legend()
    ax.set_aspect('equal', adjustable='datalim')
    plt.title(f"Минимальное расстояние: {min_distance:.2f}")
    plt.show()


# Пример произвольных многоугольников
polygon1 = [(0, 0), (4, 0), (2, 3), (0, 0)]  # Треугольник
polygon2 = [(5, 1), (7, 1), (7, 4), (5, 4), (5, 1)]  # Прямоугольник

# Вычисляем минимальное расстояние между многоугольниками
min_distance, closest_points = min_distance_between_polygons(polygon1, polygon2)

print(f"Минимальное расстояние между двумя многоугольниками: {min_distance}")

# Визуализируем результат
plot_polygons_and_distance(polygon1, polygon2, closest_points, min_distance)