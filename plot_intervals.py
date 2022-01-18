import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def plot_line_intervals(intervals):
    fig, ax = plt.subplots()
    for i in range(len(intervals)):
        ax.add_patch(Rectangle((intervals[i].inf, 0), intervals[i].sup - intervals[i].inf, 10, color="blue"))
    plt.xlabel('b')
    plt.xlim(7, 14)
    plt.ylim(0, 11)
    plt.show()

def plot_rectangles(rectangles):
    print(rectangles)
    fig, ax = plt.subplots()
    for i in range(len(rectangles)):
        ax.add_patch(Rectangle((rectangles[i][0].inf, rectangles[i][1].inf), rectangles[i][0].sup - rectangles[i][0].inf
                               , rectangles[i][1].sup - rectangles[i][1].inf, color="yellow"))
    plt.ylabel('b2')
    plt.ylim(4, 16)
    plt.xlabel('b1')
    plt.xlim(2, 7)
    plt.show()
