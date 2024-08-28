import numpy as np
import os
import mrcfile
import cv2
import glob
import pandas as pd


CSV_FILE_LOCATION = "train_val_viruses/annotations/"
MASK_FILE_LOCATION = "train_val_viruses/images/"
MRC_FILE_LOCATION = "train_val_viruses/images/"


    
coordinate_files = glob.glob(f"{MRC_FILE_LOCATION}*.mrc")
for cf in coordinate_files:
    f_name = cf.split("/")[-1][:-4]
    micrograph_filename = f"{MRC_FILE_LOCATION}{f_name}.mrc"
    with mrcfile.open(micrograph_filename, mode='r+', permissive=True) as mrc:
        image = mrc.data

    if image is None:
        continue
    image = image.T
    image = np.rot90(image)

    mask = np.zeros_like(image)
    print(mask.shape)
    try:
        coordf = f"{CSV_FILE_LOCATION}{f_name}.box"
        coordinates = pd.read_csv(coordf, sep='\t',header=None)
        coordinates = coordinates.values
        for i in range(len(coordinates)):
            r = int(coordinates[i,2]/2)

            x = coordinates[i,0]+r
            y = coordinates[i,1]+r
            coords = cv2.circle(mask, (x, y), r, (255, 255, 255), -1)
        print(coords)
        cv2.imwrite(f"{MASK_FILE_LOCATION}{f_name}_mask.png", coords)
        print('Success')
    except:
        print('Error Creating Mask')

