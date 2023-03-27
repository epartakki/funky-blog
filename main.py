from PIL import Image
import numpy as np

# load image
image = Image.open('input_image.jpg')
image = np.array(image)

# funky filter function
def funky_filter(image):
    brightness_factor = np.random.uniform(0.5, 1.5)
    contrast_factor = np.random.uniform(0.5, 1.5)
    
    image = image * brightness_factor
    image = (image - image.mean()) * contrast_factor + image.mean()
    
    return image.astype(np.uint8)
  
funky_image = funky_filter(image)

# output final image
output_image = Image.fromarray(funky_image)
output_image.save('output_image.jpg')