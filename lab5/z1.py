from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import numpy as np
import scipy


def get_unit_sphere(step=0.05):
    # phi in [0,2*pi] and theta in [0,pi]
    phi, theta = np.mgrid[0.: (2. + 10 ** -2) * np.pi: step, 0.: np.pi: step]
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


def plot_ellipsoid(v: np.array, svd=None, title='Ellipsoid'):
    plt.figure(title, figsize=(10, 10))
    ax = plt.axes(projection='3d')
    ax.plot_surface(v[0], v[1], v[2], alpha=0.6)
    if svd is not None:
        u, s, vh = svd
        col = ['r', 'g', 'b']
        x = ((np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) @ u) * s) @ vh
        for i in range(3):
            ax.quiver(0, 0, 0, x[i][0], x[i][1], x[i][2], color=col[i])
    plt.show()


def random_with_ratio(singularity_ratio=100):
    a = np.random.rand(3, 3)
    svd = np.linalg.svd(a)
    while (np.max(svd[1]) / np.min(svd[1])) < singularity_ratio:
        a = np.random.rand(3, 3)
        svd = np.linalg.svd(a)
    return a


if __name__ == '__main__':
    # Ex. 1
    sphere = get_unit_sphere()
    plot_ellipsoid(sphere, 'Sphere')

    # Ex. 2
    b = np.random.rand(3, 3)
    plot_ellipsoid(transform_sphere(sphere, a), np.linalg.svd(a), "First ellipsoid")

    a = np.random.rand(3, 3)
    plot_ellipsoid(transform_sphere(sphere, a), np.linalg.svd(a), "Second ellipsoid")

    a = np.random.uniform(-1, 1, (3, 3))
    plot_ellipsoid(transform_sphere(sphere, a), np.linalg.svd(a), "Third ellipsoid")

    # Ex. 4
    a = random_with_ratio()
    svd = np.linalg.svd(a)
    ratio = np.max(svd[1]) / np.min(svd[1])
    print("Matrix singularity ratio: ", ratio)
    plot_ellipsoid(transform_sphere(sphere, a), svd, "Singularity ratio "+str(round(ratio,2)))

    # Ex. 5
    u, s, vh = np.linalg.svd(b)
    s = np.diag(s)
    plot_ellipsoid(transform_sphere(sphere, vh))
    plot_ellipsoid(transform_sphere(sphere, s @ vh))
    plot_ellipsoid(transform_sphere(sphere, u @ s @ vh))
