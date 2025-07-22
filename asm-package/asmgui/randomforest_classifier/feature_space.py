##############################################################################
# Author:      Jamie, Germano & Nikhil

# Description: The script extracts a set of features from an image.
#
# References:  The code is heavily influenced by:
#              https://github.com/bnsreenu/python_for_microscopists/blob/
#              master/062-066-ML_06_04_TRAIN_ML_segmentation_All_filters_RForest.py
#              Information regarding gabor filters can be found at
#              https://en.wikipedia.org/wiki/Gabor_filter
##############################################################################
"""Extracction of image features"""
# Import packages
import cv2
import numpy as np
import pandas as pd
from scipy import ndimage as nd
from skimage.filters import sobel, scharr, prewitt

def feature_extraction(img_i, features_i):
    '''
    Extract selected features from an image.

    Args:
        img_i: Original image (2D NumPy array)
        features_i: List of selected feature names

    Returns:
        df: DataFrame containing selected features
    '''
    import pandas as pd

    print('inside feature_extraction')

    # Always include Original image
    data = {'Original image': img_i.reshape(-1)}

    # Add only selected features
    for feature in features_i:
        if feature == 'denoise':
            processed = cv2.fastNlMeansDenoising(np.uint8(img_i), None, 5, 7, 21)
        elif feature == 'Laplacian':
            processed = cv2.Laplacian(img_i, cv2.CV_64F)
        elif feature == 'Canny Edge':
            processed = cv2.Canny(np.uint8(img_i), 100, 200)
        elif feature == 'Sobel':
            processed = sobel(img_i)
        elif feature == 'Scharr':
            processed = scharr(img_i)
        elif feature == 'Prewitt':
            processed = prewitt(img_i)
        elif feature == 'Gaussian σ=3':
            processed = nd.gaussian_filter(img_i, sigma=3)
        elif feature == 'Gaussian σ=7':
            processed = nd.gaussian_filter(img_i, sigma=7)
        elif feature == 'Median size=3':
            processed = nd.median_filter(img_i, size=3)
        else:
            print(f" Unknown feature skipped: {feature}")
            continue

        data[feature] = processed.reshape(-1)

    df = pd.DataFrame(data)
    return df
    