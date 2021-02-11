from PIL import Image
import numpy as np
import sys, os

class ImageTransform:
    def __init__(self, input_file:str = None):
        self.input_file = input_file

    def open_file(self):
        try:
            self.image = Image.open(self.input_file)
            self.image_pixels = np.array(self.image)
            self.image_pixels.flags.writeable = True
            self.width = self.image.size[0]
            self.height = self.image.size[1]
        except Exception as ex:
            raise Exception(ex)

    def __get_average_color(self, region_pix_arr):
        if type(region_pix_arr[0]) is np.int64:
            avg_color = np.sum(region_pix_arr)/np.power(self.chunk_size,2)
            return int(avg_color)
        elif type(region_pix_arr[0]) is np.ndarray:
            avg_color = np.mean(region_pix_arr, axis=(1))
            return tuple(avg_color.astype(int))
        else:
            raise TypeError("Unknown pixel values type!")

    def divide_onto_chunks(self, chunk_size:int = 4):
        self.chunk_size = chunk_size
        for x in range(0,self.image_pixels.shape[0],chunk_size):
            for y in range(0,self.image_pixels.shape[1], chunk_size):
                try:
                    chunk = self.image_pixels[x:x+self.chunk_size, y:y+self.chunk_size]
                    avg_color = self.__get_average_color(chunk)
                    self.image_pixels[x:x+self.chunk_size, y:y+self.chunk_size] = avg_color[0]
                    
                    
                except TypeError as te:
                    print(te)
                    break

                except Exception as ex:
                    print(ex)
                    continue

    def save_new_file(self, destination = './', output_file_name:str = "out.png"):
        self.image = Image.fromarray(self.image_pixels)
        self.image.save(os.path.join(destination, output_file_name))

def main():
    img_transform = ImageTransform(os.path.join(os.path.dirname(__file__),'1111.png'))
    img_transform.open_file()
    img_transform.divide_onto_chunks()
    img_transform.save_new_file()

if __name__ == "__main__" : main()