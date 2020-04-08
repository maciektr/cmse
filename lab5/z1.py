from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import numpy as np
import scipy


def get_unit_sphere(step=0.05):
    # phi in [0,2*pi] and theta in [0,pi]
    phi, theta = np.mgrid[0.: (2. + 10**-2) * np.pi: step, 0.: np.pi: step]
    v = np.array([
        np.cos(phi) * np.sin(theta),
        np.sin(phi) * np.sin(theta),
        np.cos(theta)
    ])
    return v


def transform_sphere(sphere: np.array, matrix: np.array):
    v = sphere.T @ matrix
    x = v[:, :, 0]
    y = v[:, :, 1]
    z = v[:, :, 2]
    return np.stack([x, y, z])


def plot_ellipsoid(v: np.array, title='Ellipsoid'):
    plt.figure(title, figsize=(10, 10))
    plt.axes(projection='3d').plot_surface(v[0], v[1], v[2])
    # plt.draw()
    plt.show()


if __name__ == '__main__':
    sphere = get_unit_sphere()
    # plot_ellipsoid(sphere, 'Sphere')

    a = np.random.uniform(-1, 1, (3, 3))
    plot_ellipsoid(transform_sphere(sphere, a))

    # a = np.random.uniform(-1, 1, (3, 3))
    # plot_ellipsoid(transform_sphere(sphere, a))
    #
    # a = np.random.uniform(-1, 1, (3, 3))
    # plot_ellipsoid(transform_sphere(sphere, a))

    plt.show()
