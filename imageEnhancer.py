

from PIL import Image

# Load the image
image = Image.open("C:/Users/WarreGeversNordend/Nordend/Products - Documents/Nordend_Weerstation/Artwork/Dartsboard Images(png)/dartbord_latest_cropped.png")  # Replace 'your_image.jpg' with the path to your image

# Define the new dimensions
new_width = 882*4  # Double the width
new_height = 882*4  # Double the height

# Resize the image
resized_image = image.resize((new_width, new_height), Image.LANCZOS)  # Bilinear interpolation

# Save or display the resized image
resized_image.save("C:/Users/WarreGeversNordend/Nordend/Products - Documents/Nordend_Weerstation/Artwork/Dartsboard Images(png)/dartbord_latest_cropped_test.png")  # Save the resized image to a file
resized_image.show()  # Display the resized image