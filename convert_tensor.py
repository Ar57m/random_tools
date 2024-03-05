from PIL import Image
import numpy as np
import torch
import os


class TestConvert:
    def __init__(self):
        print("TestConvert On")

    def tohex(self, column):
        return np.vectorize(hex)(column)

    def scale(self, input_tensor, new_min, new_max):
        current_min = np.min(input_tensor)
        current_max = np.max(input_tensor)
        if current_min == current_max: # to avoid infinity
           current_min -= 1
        scaled_tensor = (input_tensor - current_min) * (new_max - new_min) / (current_max - current_min) + new_min
        return scaled_tensor
    
    def image_to_tensor(self, image_path, min, max, dtype= torch.float32):
        img = Image.open(image_path)
    
        array_image = np.array(img)
    
    
        if array_image.ndim != 3:
            array_image = np.array(img.convert("RGBA"))
            
        if array_image.ndim == 3:
              if array_image.shape[2] == 4:
                      array_image = array_image[:, :, :-1].astype(np.int64)
                      
              if array_image.shape[2] == 3:
                      array_image = (array_image[:, :, 0]*(256**2)+array_image[:, :, 1]*(256)+array_image[:, :, 2])
    
        shape = array_image.shape
        array_image = array_image.reshape(shape[0],shape[1])
        tensor_min = np.min(array_image)
        tensor_max = np.max(array_image)
        array_image = self.scale(array_image, min, max)
        array_image = np.clip(array_image , min, max)
        
        return torch.tensor(array_image, dtype=dtype), tensor_min, tensor_max



    def tensor_to_image(self, tensor, imgname, newmin= None, newmax= None):
        shape = tensor.shape
        array_image = np.array(tensor)
        del tensor
        if (newmin == None) or (newmax == None):
            array_image = self.scale(array_image, 0, 16777215)
        else:
            array_image = self.scale(array_image, newmin, newmax)
        array_image = np.round(array_image).astype(np.int64)
        hexa =None

        hexa =  np.apply_along_axis(self.tohex, axis=1, arr=array_image)
        del array_image
    
        hexa_flat = hexa.reshape(-1)
        del hexa
        cor_rgb_flat = np.zeros((hexa_flat.size, 3), dtype=np.int64)
    
        for i, hex_value in enumerate(hexa_flat):
            hex_value = hex_value[2:].zfill(6)
    
            cor_rgb_flat[i, 0] = int(hex_value[0:2],16)
            cor_rgb_flat[i, 1] = int(hex_value[2:4], 16)
            cor_rgb_flat[i, 2] = int(hex_value[4:6], 16)
    
        del hexa_flat
    
        cor_rgb = cor_rgb_flat.reshape(shape[0], shape[1], 3).astype(np.uint8)
        del cor_rgb_flat 
        #oo = np.full((sh[0], sh[1], 1), 255, dtype=np.uint8)
        #cor_rgb = np.concatenate((cor_rgb, oo), axis=2)
    
        imag = Image.fromarray(cor_rgb)
        del cor_rgb
        imag.save(f'{imgname}.png')
        print('Image saved to:' , f'{imgname}.png' )


convert = TestConvert()
k = convert.image_to_tensor("/storage/emulated/0/star.png", 0, 1)

convert.tensor_to_image(k[0],"defaut_min_and_max")

convert.tensor_to_image(k[0],"retrieved_image", k[1],k[2] )













