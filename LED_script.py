import openai
import requests
import numpy
import cv2
from matplotlib import pyplot as plt
import json
import key
import numpy as np
import urllib.request
#from google.colab.patches import cv2_imshow


# print the original image before pixelation
#  cv2_imshow(image)
# this function prints the input image
def printImage(img):
    # we can select different 
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(rgb)

# this image will print a grid of images
def printImageGrid(imglst):
    rbg_img = None
    for i, img in enumerate(imglst):
      plt.subplot(1, 2, i+1)
      # COLOR_RGB2BGR565
      # COLOR_BGR2RGB
      rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      plt.imshow(rgb_img)
    return rgb_img

# this function pixelates the image to a given height and width 
def pixelate(img, w, h):
    height, width = img.shape[:2]

    # Resize input to "pixelated" size
    # INTER_LINEAR is a bilinear interpolation resampling method that uses the distanceweighted 
    # average of the four nearest pixel values to estimate a new pixel value
    temp = cv2.resize(img, (w, h), interpolation=cv2.INTER_LINEAR)

    # Initialize output image
    # determines the “nearest” neighboring pixel and assumes its intensity value
    return cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)


# import the openAI API key
openai.api_key = key.OPENAI_KEY

# implement the DALL E image generation
imagePrompt = input("enter a fire idea for a picture: ") # this is where the image prompt will go

# create the image using DALL E and the image prompt
rawImages = openai.Image.create(
    prompt = imagePrompt,
    n=2,
    size = "1024x1024"
)


# initialize the image lists
img_values = []
# this loops through generated Dall-E URLs and generates a list of pictures
for url_dict in rawImages['data']:
  img_url = url_dict['url']
  with urllib.request.urlopen(img_url) as url_response:
    image_data = url_response.read()
  image = np.asarray(bytearray(image_data), dtype=np.uint8)
  # imglst.append(cv2.imdecode(image, cv2.IMREAD_COLOR))
  image = cv2.imdecode(image, cv2.IMREAD_COLOR)
  # here, we would likely send the picture data to the arduino

  # img_values.append(np.asarray(bytearray(pixelate(image, 32, 32))))
  img_values.append(np.asarray(pixelate(image, 32, 32)))


test_img1 = img_values[0]
test_img2 = img_values[1]

resized_img1 = cv2.resize(test_img1, (32, 32))
resized_img2 = cv2.resize(test_img2, (32,32))

concat_images = np.concatenate((resized_img1, resized_img2), axis = 1)

output_rgbs = concat_images.tolist()

data = []
for i in range(32):
    for j in range(64):
        for k in range(3):
            data.append(output_rgbs[i][j][k])
#print(data)

printImageGrid(img_values)

