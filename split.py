import cv2
import numpy as np
import os
import re
from enhancement import median_blur, gaussian_blur
from binary import mean_threshold, simple_binary, segment, thinned



def split_and_process_stack(images, thresh, median):
    # Dividir o stack em partes
    n = len(images)
    stack = []
    for f in range(5):
        images_part = images[n*f//5:n*(f+1)//5, :, :]
        # Processar cada parte individualmente
        threshold1 = mean_threshold(images_part, thresh)
        binary1 = simple_binary(images_part, threshold1)
        seg_part = segment(images_part, binary1)
        denoising_part = median_blur(seg_part, median)
        threshold2 = mean_threshold(denoising_part, thresh)
        binary2 = simple_binary(denoising_part, threshold2)
        print(threshold1,threshold2)
        stack.append(binary2)

    return np.concatenate(stack, axis=0)