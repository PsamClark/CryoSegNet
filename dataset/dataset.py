# Code for creating dataset

from torch.utils.data import Dataset
import mrcfile
import cv2
import torch
import config

def min_max(image):
    i_min = image.min()
    i_max = image.max()

    image = ((image - i_min)/(i_max - i_min))
    return image

def transform(image):
    i_min = image.min()
    i_max = image.max()
    
    if i_max == 0:
        return image

    image = ((image - i_min)/(i_max - i_min)) * 255
    return image.astype('uint8')



class CryoEMDataset(Dataset):
    def __init__(self, img_dir, transform):
        super().__init__()
        self.img_dir = img_dir
        self.transform = transform

    def __len__(self):
        return len(self.img_dir)

    def __getitem__(self, idx):
        # image = mrcfile.read(self.img_dir[idx])
        # image = image.T
        # image = np.rot90(image)
        
        image_path = self.img_dir[idx]
        mask_path = image_path[:-4] + '_mask.png'
        #mask_path = mask_path.replace('images', 'masks')
        try:
            image = cv2.imread(image_path, 0)
            mask = cv2.imread(mask_path, 0)
          
        
            image = cv2.resize(image, (config.input_image_width, config.input_image_height))
            mask = cv2.resize(mask, (config.input_image_width, config.input_image_height))
        except:
            print(image_path)
        image = torch.from_numpy(image).unsqueeze(0).float()
        mask = torch.from_numpy(mask).unsqueeze(0).float()
        
        image = image/255.0
        mask = mask/255.0

        return (image, mask)
    
class CryoEMFineTuneDataset(Dataset):
    def __init__(self, mask_dir, transform):
        super().__init__()
        self.mask_dir = mask_dir
        self.transform = transform

    def __len__(self):
        return len(self.mask_dir)

    def __getitem__(self, idx):        
        mask_path = self.mask_dir[idx]
        image_path = mask_path[:-9] + '.png'
        image_path = image_path.replace('masks', 'images')
        #image = denoise(image_path)
        image = cv2.imread(image_path, 0)
        mask = cv2.imread(mask_path, 0)
        
        image = cv2.resize(image, (config.input_image_width, config.input_image_height))
        mask = cv2.resize(mask, (config.input_image_width, config.input_image_height))
        
        image = torch.from_numpy(image).unsqueeze(0).float()
        mask = torch.from_numpy(mask).unsqueeze(0).float()
        
        image = image/255.0
        mask = mask/255.0

        return (image, mask)
