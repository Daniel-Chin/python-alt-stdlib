from manhattan import *

def rotateAnimate(points, axis_range, n_frames = 100):
    points = [PolarPoint.fromEular(point) for point in points]
    for i in range(n_frames):
        print(i)
        plt.cla()
        scatter(points)
        plt.axis([-axis_range, axis_range, -axis_range, axis_range])
        plt.draw()
        plt.pause(.1)
        for point in points:
            point.theta += 2 * PI / n_frames

# rotateAnimate(circle(1, 50), 2)
# rotateAnimate(square(1, 200), 2)
rotateAnimate(np.array(circle(1, 50)) + Point(2,0), 5)
