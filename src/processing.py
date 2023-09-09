from typing import List, Tuple
import cv2 as cv
import numpy as np

def get_cropped_images(
    images: List[np.ndarray],
    top: int = 5,
    bottom: int = 0,
    left: int = 0,
    right: int = 30
    ) -> List[np.ndarray]:
    """
    Crop the images to remove the black borders.

    Parameters
    ----------
    images : list of ndarray
        The images to crop.
    top : int, optional
        The number of pixels to remove from the top, by default 5.
    bottom : int, optional
        The number of pixels to remove from the bottom, by default 0.
    left : int, optional
        The number of pixels to remove from the left, by default 0.
    right : int, optional
        The number of pixels to remove from the right, by default 30.

    Returns
    -------
    list of ndarray
        The cropped images.
    """
    if not len(images):
        return images
    # Get the image dimensions.
    image_height, image_width, _ = images[0].shape
    # Crop images black borders.
    return [
        img[top:image_height-bottom, left:image_width-right]
        for img in images]

def get_images_to_original_dimensions(
    images: List[np.ndarray],
    top: int = 5,
    bottom: int = 0,
    left: int = 0,
    right: int = 30
    ) -> List[np.ndarray]:
    """
    Add back the cropped borders to the images to restore the original image
    dimensions.
    
    Parameters
    ----------
    images : list of ndarray
        The images to add back the cropped borders to.
    top : int, optional
        The number of pixels to add back to the top, by default 5.
    bottom : int, optional
        The number of pixels to add back to the bottom, by default 0.
    left : int, optional
        The number of pixels to add back to the left, by default 0.
    right : int, optional
        The number of pixels to add back to the right, by default 30.
    
    Returns
    -------
    list of ndarray
        The images with the cropped borders added back.
    """
    # Add back the cropped borders to the images.
    return [
        cv.copyMakeBorder(
            img,
            top=top,
            bottom=bottom,
            left=left,
            right=right,
            borderType=cv.BORDER_CONSTANT,
            value=[0, 0, 0])
        for img in images]
    
def get_gaussian_blurred_images(
    images: List[np.ndarray],
    kernel_size: Tuple[int, int] = (21, 21)) -> List[np.ndarray]:
    """
    Apply a Gaussian blur to the images.

    Parameters
    ----------
    images : list of ndarray
        The images to blur.
    kernel_size : (int, int), optional
        The kernel size of the Gaussian blur, by default (21, 21).

    Returns
    -------
    list of ndarray
        The blurred images.
    """
    # Apply a Gaussian blur to the images.
    return [cv.GaussianBlur(img, kernel_size, 0) for img in images]

def get_color_space_converted_images(
    images: List[np.ndarray],
    color_conversion_code: int = cv.COLOR_BGR2LAB) -> List[np.ndarray]:
    """
    Convert the images to a different color space.

    Parameters
    ----------
    images : list of ndarray
        The images to convert.
    color_conversion_code : int, optional
        The color space to convert the images to, by default cv.COLOR_BGR2GRAY.

    Returns
    -------
    list of ndarray
        The converted images.
    """
    # Convert the images to a different color space.
    return [cv.cvtColor(img, color_conversion_code) for img in images]

def get_images_channel(
    images: List[np.ndarray],
    channel: int
    ) -> List[np.ndarray]:
    """Get the specified channel of the images.

    Parameters
    ----------
    images : list of ndarray
        The images to get the channel of.
    channel : int
        The number of the channel to get.

    Returns
    -------
    list of ndarray
        The specified channel of the images.
    """
    # Get the B channel of the LAB color space.
    return [img[..., channel] for img in images]

def get_otsu_threshold_masks(images: List[np.ndarray]) -> List[np.ndarray]:
    """
    Apply a Otsu threshold to the images.

    Parameters
    ----------
    images : list of ndarray
        The images to apply an Otsu threshold to.

    Returns
    -------
    list of ndarray
        The threshold masks.
    """
    # Apply a Otsu threshold to the images.
    return [cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]
            for img in images]
    
def get_segmented_images(
    images: List[np.ndarray],
    masks: List[np.ndarray]
    ) -> List[np.ndarray]:
    """
    Segment the images.

    Parameters
    ----------
    images : list of ndarray
        The images to segment.
    masks : list of ndarray
        The masks to segment the images with.

    Returns
    -------
    list of ndarray
        The segmented images.
    """
    # Segment the images.
    return [cv.bitwise_and(img, img, mask=mask) for img, mask in zip(images, masks)]