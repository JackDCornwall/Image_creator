'''
#Created by: Jack Cornwall
#Email: hello@jackcornwall.co.uk
#Git hub: https://github.com/JackDCornwall
#Website:https://jackcornwall.co.uk/

#Project: Image color converter
#Date: 10.07.21
#Description: Converts BGR to RGB images using the cv2 package. (created to convert Mnist dataset downloaded from kaggle)
'''
# importing required packages
import os
import pandas as pd
import cv2

###########################SETTINGS###########################
folder = "C://Users/conta/Documents/python/opencv_ocr/Training Data/trainingSet/trainingSet/9" # folder of images to convert
##############################################################

#### creating/deleting directories

# checking if converted folder exists
if os.path.exists(folder+"/Converted/"):

    # if it exists we delete it
    os.rmdir(folder+"/Converted/")

# creating os directory
os.mkdir(folder+"/Converted/")

#### manipulating data

# extracting all images to list
images = os.listdir(folder)

# converting to pandas array
images = pd.DataFrame(images, columns=["image"])

#subsetting to only images with required file extension
images = images.loc[images["image"].str.contains("\.png$|\.jpg$|\.jpeg$|\.bmp$",regex=True)]
images = images.reset_index(drop=True) #resetting index in case any images have been removed

#### Looping through all images
for image in images["image"]:

    image_in = cv2.imread(folder + "/" + image) # importing bgr image

    image_out = 255 - image_in #inverting image colours

    cv2.imwrite(folder+"/Converted/"+image,image_out) #storing newly converted image

    # # displaying output image for testing purposes
    # cv2.imshow("Output", image_out)
    # cv2.waitKey(250)

# code success message
print("The code has run successfully")
