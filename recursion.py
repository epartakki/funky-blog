from PIL import Image
import random

def recursive_effect(image, iterations=5, scale_factor=0.5):
    """
    Apply a more visually complex recursive effect to the image.
    """
    for _ in range(iterations):
        width, height = image.size

        # Applying effect to multiple sections
        for __ in range(random.randint(1, 3)):  # Random number of sections
            # Randomly selecting a portion of the image
            x1 = random.randint(0, width // 2)
            y1 = random.randint(0, height // 2)
            x2 = x1 + random.randint(width // 4, width // 2)
            y2 = y1 + random.randint(height // 4, height // 2)

            portion = image.crop((x1, y1, x2, y2))

            # Scale down this portion
            new_width = int((x2 - x1) * scale_factor)
            new_height = int((y2 - y1) * scale_factor)
            portion = portion.resize((new_width, new_height))

            # Place it back onto the original image at a random position
            new_x1 = random.randint(0, width - new_width)
            new_y1 = random.randint(0, height - new_height)
            image.paste(portion, (new_x1, new_y1))

    return image

# Load the input image
input_image_path = 'input.jpg'  # Update this path if needed
input_image = Image.open(input_image_path)

# Apply the recursive effect
recursive_image = recursive_effect(input_image)

# Save the output image
output_image_path = 'output.jpg'  # Update this path if needed
recursive_image.save(output_image_path)
