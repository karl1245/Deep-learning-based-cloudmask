from s2cloudless import S2PixelCloudDetector, CloudMaskRequest
from xml.dom import minidom
import sys
import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt

#TODO: get data from image
bands = ['B01','B02','B03', 'B04','B05','B06', 'B07','B08','B8A','B09','B10','B11','B12']

cloud_detector = S2PixelCloudDetector(threshold=0.4, average_over=4, dilation_size=2, all_bands=True)

print(sys.argv)

if len(sys.argv) != 2:
    print("missing argument")
    exit(0)
else:
    xml_path = sys.argv[1]

print(f'Reading data from {xml_path}')

files_path = os.path.dirname(xml_path)

print(files_path)

pure_data = []

RESULT_SIZE = 1830

def plot_cloud_mask(mask, figsize=(15, 15), fig=None):
    """
    Utility function for plotting a binary cloud mask.
    """
    if fig == None:
        plt.figure(figsize=figsize)
    plt.imshow(mask, cmap=plt.cm.gray)
    plt.show()
    # plt.savefig('myfilename.png', dpi=100)

root = xmldoc = minidom.parse(xml_path)
for node in root.getElementsByTagName('IMAGE_FILE'):
    file_name = node.firstChild.nodeValue
    file_path = os.path.join(files_path, file_name) + ".jp2"

    if file_name[-3:] in bands:
        print(f"Reading {file_name[-3:]}")
        with rasterio.open(file_path) as f:
            file_data = f.read(1)
            print(f'Read {file_name[-3:]} with size {f.width} x {f.height}')
            # for r in range(len(file_data)):
            #     for f in range(len(file_data[r])):
            #         file_data[r][f] /= 10000
            every_x = int(f.width/RESULT_SIZE)
            every_y = int(f.height/RESULT_SIZE)
            resized = np.array(file_data)[::every_x, ::every_y]
            print(resized.shape)
            pure_data.append(resized)

input_array = np.array([pure_data]) / 10000

input_array.shape = (1, 1830, 1830, 13)

plot_cloud_mask(input_array[0])

print(input_array.shape)

print("Mapping clouds")

#cloud_probs = cloud_detector.get_cloud_probability_maps(input_array)

cloud_masks = cloud_detector.get_cloud_masks(input_array)

print("Mapping finished")
print(cloud_masks.shape)

plot_cloud_mask(cloud_masks[0])
