
from PIL import Image

# Open the image

image = Image.open("C:/Users/WarreGeversNordend/Nordend/Products - Documents/Nordend_Weerstation/Artwork/Dartsboard Images(png)/dartbord_latest.png")

# Get the dimensions of the original image
width, height = image.size
print(width,height)
# Define the area to remove
left = 6
top = 2
right = width-6  # Remove 6 columns from the right
bottom = height-2  # Remove 16 rows from the bottom


cropped_image = image.crop((left, top, right, bottom))

width, height = cropped_image.size
print(width, height)
# Save the cropped image

cropped_image.save("C:/Users/WarreGeversNordend/Nordend/Products - Documents/Nordend_Weerstation/Artwork/Dartsboard Images(png)/dartbord_latest_cropped_test.png")
