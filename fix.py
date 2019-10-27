from os import listdir
from PIL import Image
import os
   
for filename in listdir('./snapshot'):
  if filename.endswith('.jpg'):
    try:
      Image.MAX_IMAGE_PIXELS = 5336770819
      img = Image.open('./snapshot/'+filename) # open the image file
      img.verify() # verify that it is, in fact an image
    except (IOError, SyntaxError) as e:
        print(filename)
        os.remove('./snapshot/'+filename)
        
  