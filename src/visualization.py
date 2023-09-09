from typing import List
import ipywidgets as wg
import PIL.Image
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def show_image_slider(
    images: List[np.ndarray],
    title: str = 'Image slider',
    color_conversion_code: int = cv.COLOR_BGR2RGBA
    ) -> None:
    """
    Get a widget to slide through a list of images.

    Parameters
    ----------
    images : list of ndarray
        The images to slide through.
    title : str, optional
        The title of the images to show, by default 'Image slider'.
    color_conversion_code : ColorConversionCodes, optional
        The color function to use, by default COLOR_BGR2RGBA.
    """
    def _show_image_by_index(index: int) -> PIL.Image:
        rgb_image = cv.cvtColor(images[index], color_conversion_code)
        return PIL.Image.fromarray(rgb_image)

    print(title)
    wg.interact(
        _show_image_by_index,
        index=wg.IntSlider(min=0, max=len(images)-1, step=1))

def show_image_channels(
    image: np.ndarray,
    channel_names: [str, str, str]) -> None:
    """
    Show the channels of an image.

    Parameters
    ----------
    image : ndarray
        The image to show the channels of.
    channel_names : [str, str, str]
        The names of the channels.
    """
    # Get the image channels.
    channel_1, channel_2, channel_3 = cv.split(image)
    # Get the channel names.
    channel_1_name, channel_2_name, channel_3_name = channel_names

    plt.figure(figsize=(10, 10))
    # Show the original image.
    plt.subplot(2, 2, 1)
    plt.title('Original image')
    plt.imshow(image)
    # Remove the axis ticks.
    plt.axis('off')

    # Show the channels.
    for img, index, name in zip(
        [channel_1, channel_2, channel_3],
        [2, 3, 4],
        [channel_1_name, channel_2_name, channel_3_name]):
        plt.subplot(2, 2, index)
        plt.title(f'Channel {name}')
        plt.imshow(img, cmap='gray')
        # Remove the axis ticks.
        plt.axis('off')

    plt.tight_layout()
    plt.show()
