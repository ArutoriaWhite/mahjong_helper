import os
import shutil
import numpy as np
import cv2 as cv

def resize(dir):
    shutil.rmtree(os.path.join('resized_imgs/',dir))
    os.makedirs(os.path.join('resized_imgs/',dir),exist_ok=True)
    imgs_name = os.listdir(dir)
    for n in imgs_name:
        img = cv.imread(os.path.join(dir,n))
        try:
            h,w = img.shape[:2]
            h //= 2
            w //= 2

            to_save: list[np.ndarray] = []
            to_save.append(img)
            to_save.append(img[:h,:w])
            to_save.append(img[h:2*h,:w])
            to_save.append(img[:h,w:2*w])
            to_save.append(img[h:2*h,w:2*w])

            for i in to_save:
                i = cv.resize(i,(416,416))
                print(cv.imwrite(os.path.join('resized_imgs/',dir,n),img))
        except:
            pass

resize('imgs/four_corner')
#resize('imgs/line')
