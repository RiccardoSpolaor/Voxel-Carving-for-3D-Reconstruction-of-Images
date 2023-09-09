import os
from typing import List
from scipy.io import loadmat
import cv2 as cv
import numpy as np

def get_perspective_projection_matrices(input_directory: str) -> np.ndarray:
    """
    Get the perspective projection matrices of the images of the dinosaur
    from the data directory.

    Parameters
    ----------
    input_directory : str
        The directory containing the perspective projection matrices
        file.

    Returns
    -------
    ndarray
        The perspective projection matrices.
    """
    # Load the camera calibration matrix data.
    data = loadmat(os.path.join(input_directory, 'dino_Ps.mat'))
    return data['P'][0]

def get_images(images_directory: str) -> List[np.ndarray]:
    """Get the images of the dinosaur from the images directory.

    Parameters
    ----------
    images_directory : str
        The directory containing the images of the dinosaur.

    Returns
    -------
    list of ndarray
        A list containing the images of the dinosaur as numpy arrays.
    """
    # Load the images of the dinosaur.
    images = []

    for file_name in os.listdir(images_directory):
        image = cv.imread(os.path.join(images_directory, file_name))
        images.append(image)

    return images
