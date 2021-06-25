'''
#Created by: Jack Cornwall
#Email: jackcornwall91@gmail.com
#Git hub: https://github.com/JackDCornwall
#Website:https://jackcornwall.co.uk/

#Project: Image generator
#Date: 24.06.21
#Description: automatically creates a large library of varied images that can be used for ML
'''
#importing required packages
import cv2
import os
import random
import numpy as np
from PIL import ImageFont,ImageDraw,Image

###########----SETTINGS----###########
blanks = True #should blanks be generated? (Empty sudoku cells)
chars = "0123456789" #All characters to include (Blanks are denoted above)
iterations = 1000 #number of images to create per character
######################################

#extracting characters from string
chars = list(chars)

#generating list of all fonts on pc
fonts = os.listdir("C://Windows/Fonts/")

#################################################----IMPORT FUNCTIONS----#################################################
# defining a function that returns a square with randomized features as needed
# in future versions of the code this will create a more complex square for use
def getSquare_v1():
    img = cv2.imread("White_square_sample_32x32.jpg")  # imports white square
    return img

# def getFont_v1():
#     font = cv2.FONT_HERSHEY_SIMPLEX  # setting font
#
#     return font

#random font selection
def getFont_v2(font_list):

    font_num = random.randrange(0,len(font_list))

    return font_list[font_num]

def getColor_v1():
    color = [0,0,0]
    return color
#################################################----IMPORT FUNCTIONS----#################################################

#appending blank if requested by user in settings
if blanks == True:

    #adding blank as a chars
    chars.append("Blank")

#looping through the user requested number of iterations
for i in range(iterations):

    #loping through each letter
    for char in chars:

        img_in = getSquare_v1() #importing a square to overlay a character on

        #adding letter unless a blank is required
        if char != "Blank":

            image = getSquare_v1()  # importing square

            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  #converting image into RGB for pil

            pil_image = Image.fromarray(image_rgb, "RGB")  #convcerting to pil image object

            draw = ImageDraw.Draw(pil_image)  # preparing window to be drawn on

            font = getFont_v2(fonts)  # randomly selecting a font from the list

            font = ImageFont.truetype(font,12) #preparing to "draw" letter on with selected font

            draw.text((10,8),char,font=font,fill=(0,0,0)) #drawing

            drawn_image = cv2.cvtColor(np.array(pil_image),cv2.COLOR_RGB2BGR) #converting image back to OpenCV format

            image = drawn_image

        else:
            image = img_in

        cv2.imshow("Output",image)

        cv2.waitKey(250)










#code success message
print("The code has run successfully")





