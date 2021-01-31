from PIL import Image
import numpy as np
import sys, os

class ImageTransform:
    def __init__(self, input_file:str = None):
        self.input_file = input_file

    def open_file(self):
        try:
            self.image = Image.open(self.input_file)
            self.width = self.image.size[0]
            self.height = self.image.size[1]
        except Exception as ex:
            print(ex)
            sys.exit(0)

    def __get_average_color(self, region_pix_arr):
        if type(region_pix_arr[0]) is np.int64:
            avg_color = np.sum(region_pix_arr)/np.power(self.chunk_size,2)
            return int(avg_color)
        elif type(region_pix_arr[0]) is np.ndarray:
            avg_color = np.mean(region_pix_arr, axis=0)
            return tuple(avg_color.astype(int))
        else:
            raise TypeError("Unknown pixel values type!")

    def correct_chunck_size(self, gsd):
        chunck_sizes = []
        for i in range(gsd, 1, -1):
            if self.width % i == 0 and self.height % i == 0:
                chunck_sizes.append(i)
        self.correct_chunck_sizes = chunck_sizes

    def divide_onto_chunks(self, chunk_size:int = 2):
        self.chunk_size = chunk_size
        for x in range(0,self.image.size[0],chunk_size):
            for y in range(0,self.image.size[1], chunk_size):
                try:
                    box = (x, y, x + chunk_size, y + chunk_size, )
                    region = self.image.crop(box)
                    region_pix_arr = np.asarray(region.getdata())
                    avg_color = self.__get_average_color(region_pix_arr)
                    self.image.paste(avg_color, box)

                except TypeError as te:
                    print(te)
                    break

                except Exception as ex:
                    print(ex)
                    continue

    def save_new_file(self, destination = './', output_file_name:str = "out.png"):
        self.image.save(os.path.join(destination, output_file_name))


def gsd(a, b):
    if a == 0:
        return b
    while b != 0:
        if a > b:
            a -= b
        else:
            b -= a
    return a


def main():
    img_transform = ImageTransform('1.gif')
    img_transform.open_file()
    img_transform.correct_chunck_size(gsd(img_transform.width, img_transform.height))
    img_transform.divide_onto_chunks()
    img_transform.save_new_file()

if __name__ == "__main__" : main()