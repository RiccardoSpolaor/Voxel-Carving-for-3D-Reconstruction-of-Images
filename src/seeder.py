import random
import numpy as np
import cv2 as cv

def set_seed(seed: int) -> None:
    """
    Set the random seed for the numpy, cv2 and random modules to
    get reproducible results. 

    Parameters
    ----------
    seed : int
        The random seed to use.
    """
    random.seed(seed)
    np.random.seed(seed)
    cv.setRNGSeed(seed)