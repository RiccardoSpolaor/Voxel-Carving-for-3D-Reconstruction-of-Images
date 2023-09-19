from typing import List
import numpy as np
import cv2 as cv

def _min_max_scale(
    arr: np.ndarray,
    min_value: float,
    max_value: float
    ) -> np.ndarray:
    """
    Scale the values of an array to a given range.

    Parameters
    ----------
    arr : ndarray
        The array to be scaled.
    min_value : float
        The minimum value of the range.
    max_value : float
        The maximum value of the range.

    Returns
    -------
    ndarray
        The scaled vector.
    """
    return min_value + (arr - arr.min()) *\
        (max_value - min_value) / (arr.max() - arr.min())

def get_voxel_grid_points(
    mesh_grid_size: int,
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    z_min: float,
    z_max: float
    ) -> np.ndarray:
    """
    Get an array of points of a voxel grid in homogeneous world coordinates.

    Parameters
    ----------
    mesh_grid_size : int
        The number of points in each dimension of the voxel grid.
    x_min : float
        The minimum value of the x-axis.
    x_max : float
        The maximum value of the x-axis.
    y_min : float
        The minimum value of the y-axis.
    y_max : float
        The maximum value of the y-axis.
    z_min : float
        The minimum value of the z-axis.
    z_max : float
        The maximum value of the z-axis.

    Returns
    -------
    ndarray
        An array of points of the voxel grid in homogeneous world coordinates.
    """
    # Get a coordinate grid of dimension
    # (mesh_grid_size, mesh_grid_size, mesh_grid_size).
    x, y, z = np.meshgrid(
        np.arange(mesh_grid_size),
        np.arange(mesh_grid_size),
        np.arange(mesh_grid_size))
    # Flatten the coordinate arrays.
    x, y, z = x.flatten(), y.flatten(), z.flatten()
    # Scale the coordinate points to the given values of the world space.
    # The values are such that the points of the grid enclose the dinosaur.
    x = _min_max_scale(x, x_min, x_max)
    y = _min_max_scale(y, y_min, y_max)
    z = _min_max_scale(z, z_min, z_max)
    # Stack the coordinate arrays followed by a row of ones to get a matrix of
    # homogeneous world coordinates.
    return np.vstack((x, y, z, np.ones(x.shape))).astype(float)

def get_pixel_points(ppm: np.ndarray, points: np.ndarray) -> np.ndarray:
    """
    Get an array of points of a voxel grid in pixel coordinates.

    Parameters
    ----------
    ppm : ndarray
        The Perspective Projection Matrix.
    points : ndarray
        An array of points of the voxel grid in homogeneous world coordinates.

    Returns
    -------
    ndarray
        An array of points of the voxel grid in pixel coordinates.
    """
    # Get the pixel points in homogeneous coordinates.
    points_2d = ppm @ points
    # Divide the points by the last coordinate to get the pixel coordinates.
    points_2d /= points_2d[-1, :]
    # Round the pixel coordinates to the nearest integer.
    return np.round(points_2d).astype(int)

def get_images_with_voxel_grid(
    images: List[np.ndarray],
    ppms: np.ndarray,
    voxel_points: np.ndarray
    ) -> List[np.ndarray]:
    """
    Get the images with the voxel grid drawn over them.

    Parameters
    ----------
    images : list of ndarray
        The images to draw the voxel grid over.
    ppms : ndarray
        The Perspective Projection Matrices.
    voxel_points : ndarray
        The points of the voxel grid in homogeneous world coordinates.

    Returns
    -------
    list of ndarray
        The images with the voxel grid drawn over them.
    """
    images_with_voxels = []

    for ppm, img in zip(ppms, images):
        img = img.copy()
        points_2d = get_pixel_points(ppm, voxel_points)
        # Convert the image to BGRA to be able to draw transparent circles.
        img = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
        # Iterate over the pixel points by column.
        for point in points_2d.T:
            # Draw a circle at the pixel point on the image.
            img = cv.circle(img, (point[0], point[1]), radius=1,
                            color=(0, 0, 255, 50), thickness=-1)
        images_with_voxels.append(img)

    return images_with_voxels

def get_voxel_points_projection_is_in_images_mask(
    images_masks: List[np.ndarray],
    ppms: np.ndarray,
    voxel_points: np.ndarray
    ) -> np.ndarray:
    """
    Get a matrix determining for each image mask whether each voxel point
    is inside it or not.

    Parameters
    ----------
    images_masks : list of ndarray
        The images masks.
    ppms : ndarray
        The Perspective Projection Matrices.
    voxel_points : ndarray
        The points of the voxel grid in homogeneous world coordinates.

    Returns
    -------
    ndarray
        A matrix determining for each image mask whether each voxel point
        is inside it or not.
    """
    voxel_points_in_mask = []
    for ppm, img in zip(ppms, images_masks):
        # Get the image width and height.
        image_width, image_height = img.shape[1], img.shape[0]
        points_2d = get_pixel_points(ppm, voxel_points)
        # Get an array tracking whether each voxel point is inside the image
        # or not.
        x_in_image = np.logical_and(
            points_2d[0, :] >= 0, points_2d[0, :] < image_width)
        y_in_image = np.logical_and(
            points_2d[1, :] >= 0, points_2d[1, :] < image_height)
        points_in_image = np.logical_and(x_in_image, y_in_image)
        # Get the indices of the voxel points inside the image.
        indices_in_image = np.where(points_in_image)[0]
        # Get an array tracking whether each voxel point is inside the image
        # mask or not.
        points_in_mask = np.zeros(points_2d.shape[1])
        # Get the pixel coordinates of the voxel points inside the image.
        points_in_image_coords = points_2d[:-1, indices_in_image]
        # Set the voxel points inside the image mask to 1, while the rest
        # are set to 0.
        res = img[points_in_image_coords[1, :], points_in_image_coords[0, :]]
        res = res.astype(bool)
        points_in_mask[indices_in_image] = res 

        voxel_points_in_mask.append(points_in_mask)
    # Stack the result to get an array of shape
    # (number of image masks, number of voxel points).
    return np.vstack(voxel_points_in_mask)

def get_voxel_points_occupancy(
    voxel_points_in_masks: np.ndarray
    ) -> np.ndarray:
    """Get the number of image masks each voxel point is inside.

    Parameters
    ----------
    voxel_points_in_masks : ndarray
        The matrix determining for each image mask whether each voxel point
        is inside it or not.

    Returns
    -------
    ndarray
        The number of image masks each voxel point is inside.
    """
    return np.sum(voxel_points_in_masks, axis=0)

def get_voxel_points_by_minimum_occupancy(
    voxel_points: np.ndarray,
    occupancy: np.ndarray,
    min_occupancy: int
    ) -> np.ndarray:
    """Get the voxel points with a given minimum occupancy.

    Parameters
    ----------
    voxel_points : ndarray
        The points of the voxel grid in homogeneous world coordinates.
    occupancy : ndarray
        The number of image masks each voxel point is inside.
    min_occupancy : int
        The minimum occupancy a voxel point must have to be returned.

    Returns
    -------
    ndarray
        The voxel points with a given minimum occupancy across all images.
    """
    return voxel_points[:, occupancy >= min_occupancy]

def get_images_with_voxel_carving(
    images: List[np.ndarray],
    ppms: np.ndarray,
    voxel_points: np.ndarray
    ) -> List[np.ndarray]:
    """
    Get the images with the voxel carving drawn over them.

    Parameters
    ----------
    images : list of ndarray
        The images to draw the voxel carving over.
    ppms : ndarray
        The Perspective Projection Matrices.
    voxel_points : ndarray
        The voxel points in homogeneous world coordinates.

    Returns
    -------
    list of ndarray
        The images with the voxel carving drawn over them.
    """
    images_with_voxels = []

    for ppm, img in zip(ppms, images):
        img = np.zeros_like(img)
        points_2d = get_pixel_points(ppm, voxel_points)
        # Convert the image to BGRA to be able to draw transparent circles.
        img = cv.cvtColor(img, cv.COLOR_GRAY2BGRA)
        # Iterate over the pixel points by column.
        for point in points_2d.T:
            # Draw a circle at the pixel point on the image.
            img = cv.circle(img, (point[0], point[1]), radius=1,
                            color=(0, 0, 255, 50), thickness=-1)
        images_with_voxels.append(img)

    return images_with_voxels
