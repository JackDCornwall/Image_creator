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

###########----SETTINGS----###########
blanks = True #should blanks be generated? (Empty sudoku cells)
chars = "0123456789" #All characters to include (Blanks are denoted above)
iterations = 10 #number of images to create per character
######################################

#extracting characters from string
chars = list(chars)

#defining a function that returns a square with randomized features as needed
#in future versions of the code this will create a more complex square for use
def getSquare_v1():

    img = cv2.imread("White_square_sample_32x32.jpg") #imports white square
    return img

#appending blank if requested by user in settings
if blanks == True:

    #adding blank as a chars
    chars.append("Blank")

#looping through the user requested number of iterations
for i in range(iterations):

    #loping through each letter
    for char in chars:

        img_in = getSquare_v1() #importing a square to overlay a character on

        #adding text to square

        print(i, char)

#code success message
print("The code has run successfully")
