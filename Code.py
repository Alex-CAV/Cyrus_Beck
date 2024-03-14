import matplotlib.pyplot as plt
import numpy as np

def cyrus_beck(p1, p2, clip_polygon):
   


    def clip_point(t, p1, p2):
        return [p1[i] + t * (p2[i] - p1[i]) for i in range(2)]

    n = len(clip_polygon)
    t_entry = [0] * 2
    t_exit = [1] * 2

    for i in range(n):
        normal = [-1 * (clip_polygon[(i + 1) % n][1] - clip_polygon[i][1]),
                  clip_polygon[(i + 1) % n][0] - clip_polygon[i][0]]

        D = np.dot(normal, [p2[0] - p1[0], p2[1] - p1[1]])

        if D == 0:  
            if np.dot(normal, [p1[0] - clip_polygon[i][0], p1[1] - clip_polygon[i][1]]) < 0:
                return None  
        else:
            t = -np.dot(normal, [p1[0] - clip_polygon[i][0], p1[1] - clip_polygon[i][1]]) / D

            if D > 0:  
                t_entry = [max(t_entry[j], t) for j in range(2)]
            else:  
                t_exit = [min(t_exit[j], t) for j in range(2)]

    if t_entry[0] > t_exit[0] or t_entry[1] > t_exit[1]:
        return None  

    t_entry = max(t_entry)
    t_exit = min(t_exit)

    if t_entry > t_exit:
        return None  

    entry_point = clip_point(t_entry, p1, p2)
    exit_point = clip_point(t_exit, p1, p2)

    return entry_point, exit_point


def plot_polygon(ax, polygon, color='black'):
    polygon.append(polygon[0])  
    polygon = np.array(polygon)
    ax.plot(polygon[:, 0], polygon[:, 1], color=color)


def plot_clipped_segments(ax, segments, clip_polygon):
    for segment in segments:
        result = cyrus_beck(segment[0], segment[1], clip_polygon)
        if result:
            entry_point, exit_point = result
            ax.plot([segment[0][0], entry_point[0]], [segment[0][1], entry_point[1]], color='blue')
            ax.plot([exit_point[0], segment[1][0]], [exit_point[1], segment[1][1]], color='blue')



clip_polygon = [(2, 3), (5, 3), (5, 5), (5, 6), (1,4)]
segments = [((1, 1), (6, 7)), ((2, 1), (2, 3)), ((3, 4), (5, 5))]

fig, ax = plt.subplots()

plot_polygon(ax, clip_polygon, color='green')


for segment in segments:
    ax.plot([segment[0][0], segment[1][0]], [segment[0][1], segment[1][1]], color='red')

plot_clipped_segments(ax, segments, clip_polygon)

ax.set_xlim(0, 6)
ax.set_ylim(0, 6)
ax.set_aspect('equal', adjustable='box')
plt.show()
