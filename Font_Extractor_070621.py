'''
#Created by: Jack Cornwall
#Email: jackcornwall91@gmail.com
#Git hub: https://github.com/JackDCornwall
#Website:https://jackcornwall.co.uk/

#Project: Font extractor
#Date: 07.06.21
#Description: Google fonts can be downloaded all simultaneously from githib, however they are all in directories and
#subd-irectories (source: https://github.com/google/fonts) this script unpacks them all into a single directory for
#easy installation.
'''
#importing required functions
import os
import pandas as pd
import re
import shutil

#working directory
dir = os.getcwd()
crawl_dir = "Google_fonts_test"
dir_list = os.listdir(crawl_dir)

#creating regex checks
re_dir = re.compile("^[^.]+$") #directory names should not contain dots
re_font = re.compile("^[A-z0-9-_]+\.(otf|ttf|ttl|svg|eot|woff(2)?)$")

#the first loop is done outside of the while true statement to populate the initial lists.

#buffer list (current list of files to crawl)
buffer = pd.DataFrame({
    "path": [],
    "class":[],
    "crawled":[]
})

#looping through crawl directory to extract paths
# for ext in dir_list:
#     print(ext)

test_1 = "apache"
test_2 = "README.md"
test_3 = "txt.ttl"

print(re_font.sub("XXX",test_1))
#appending to dataframe
buffer = buffer.append(pd.DataFrame({
    "path": [1],
    "class": [2],
    "crawled": [3]
}))