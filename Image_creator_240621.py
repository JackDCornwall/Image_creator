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
import pandas as pd
from PIL import ImageFont,ImageDraw,Image
from fontTools.ttLib import TTFont

###########----SETTINGS----###########
blanks = True #should blanks be generated? (Empty sudoku cells)
chars = "0ABC89" #All characters to include (Blanks are denoted above)
iterations = 100 #number of images to create per character
######################################

#extracting characters from string
chars = list(chars)

#setting font path
fonts_path = "C://Windows/Fonts/"

#generating list of all fonts on pc
fonts = os.listdir(fonts_path)

#converting fonts list to np array to subset
fonts = pd.DataFrame(fonts)

#########################Font clean up########################
#removing all .fon fonts as these break PIL
fonts = fonts.loc[fonts[0].str.contains("^.*\.fon$|^.*\.FON$")==False]

#removing all .ttc fonts as these break the glyph check function
fonts = fonts.loc[fonts[0].str.contains("^.*\.ttc$|^.*\.TTC$")==False]

#removing all .CompositeFont fonts as these break the glyph check function
fonts = fonts.loc[fonts[0].str.contains("^.*\.CompositeFont$")==False]

#removing all .xml fonts as these break the glyph check function
fonts = fonts.loc[fonts[0].str.contains("^.*\.xml$|^.*\.XML$")==False]

#resetting the index as all .fon fonts have been removed
fonts = fonts.reset_index(drop=True)
###############################################################


#################################################----IMPORT FUNCTIONS----#################################################
# defining a function that returns a square with randomized features as needed
# in future versions of the code this will create a more complex square for use
def getSquare_v1():
    img = cv2.imread("White_square_sample_32x32.jpg")  # imports white square
    return img

def getFont_v1():
    font = fonts[0][0]  # setting font

    return font

#random font selection
def getFont_v2(font_list):

    #selecting a random font from inputted list
    font_num = random.randrange(0,len(font_list))

    #returning a random font
    return font_list[0][font_num]

#creating function to check for the existence of a glyph in a font library
def glyphCheck(font,char):

    #path to font for glyph search
    font_path = str(fonts_path + font)

    #extracting font to check for char glyph
    gFont = TTFont(font_path)

    #running through tables in fonts cmap
    for table in gFont["cmap"].tables:

        #checking if character has a font
        if ord(char) in table.cmap.keys():
            return True #returns true if a glyph is found

    return False #returns false if a glyph cannot be found

#selecting font size to use based on random size requirements
def getFontSize(font,char):

    # path to font for glyph search
    font_path = str(fonts_path + font)

    #randomly selecting target size between 10 and 30 (this will be the target size of the maximum dimension)
    target = np.random.randint(10,31)

    #a for loop that will attempt 20 times to generate a font of the desired size (if not return the largest)
    for attempt in range(20):

        #preparing font to test size
        try_font = ImageFont.truetype(font_path,9+attempt)

        #extracting font dimensions
        font_dim = try_font.getsize(char)

        #extracting maximum dimension
        max_dim = max(font_dim)

        #checking if the dimension has been reached
        if max_dim > target:

            return 8+attempt,font_dim #returning last number that didn't exceed dimensions

    return 8+attempt,font_dim #if no tested size is larger than the target, return the largest to use

#getting starting location based on letter size and a bit of random flair
def getLoc(dim):

    if max(dim)>31:
        return (0,0) #if a ridiculously large font is detected shove it in as best as possible

    ####Starting X coordinate ####
    #extracting width from dimensions
    width = dim[1]

    #calculating maximum x offset
    x_offset_max = ((32 - width)//2)

    #calculating x_offset randomly
    x_offset = np.random.randint((-1*x_offset_max),x_offset_max,1)

    #calculating starting x coord
    x_loc = ((32 - width)//2) + x_offset[0]

    ####Starting Y coordinate ####
    #extracting width from dimensions
    height = dim[0]

    #calculating maximum x offset
    y_offset_max = ((32 - height)//2)

    #calculating x_offset randomly
    y_offset = np.random.randint((-1*y_offset_max),y_offset_max,1)

    #calculating starting x coord
    y_loc = ((32 - height)//2) + y_offset[0]

    return (y_loc,x_loc)

########################################################################################################################
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

            image_rgb = cv2.cvtColor(img_in, cv2.COLOR_BGR2RGB)  #converting image into RGB for pil

            pil_image = Image.fromarray(image_rgb, "RGB")  #convcerting to pil image object

            draw = ImageDraw.Draw(pil_image)  # preparing window to be drawn on

            font = getFont_v2(fonts)  # randomly selecting a font from the list

            #extracting font size and dimensions used to calculate font origin
            font_size,dimensions = getFontSize(font,char)

            #checking required glyph exists
            glyph = glyphCheck(font,char)

            #if required glyph exists
            if glyph == 1:

                # getting starting location to input into draw function
                start_loc = getLoc(dimensions)

                font = ImageFont.truetype(font,font_size) #preparing to "draw" letter on with selected font

                draw.text(start_loc,char,font=font,fill=(0,0,0)) #drawing if possible

                drawn_image = cv2.cvtColor(np.array(pil_image),cv2.COLOR_RGB2BGR) #converting image back to OpenCV format

                image = drawn_image #selecting output if font has been added

                #displaying for test purposes
                cv2.imshow("Output", image)
                cv2.waitKey(250)

            else:

                print("Glyph doesnt exists  for font :",font)

        #skipping if blank is required
        else:
            image = img_in #selecting image without font to take forward

            # #displaying for test purposes
            # cv2.imshow("Output",image)
            # cv2.waitKey(250)


#code success message
print("The code has run successfully")