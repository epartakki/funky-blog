from PIL import Image
import numpy as np

# Recursive Ripple Effect
def ripple_effect_recursive(image, depth=3):
    if depth == 0:
        return image

    ripple_scale = np.random.uniform(10, 30) / depth  # Reduce effect in each recursion
    ripple_frequency = np.random.uniform(0.05, 0.1)

    x, y = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]), indexing='ij')
    dx = np.sin(2 * np.pi * y * ripple_frequency) * ripple_scale
    dy = np.sin(2 * np.pi * x * ripple_frequency) * ripple_scale

    x_new = np.clip(x + dx, 0, image.shape[1] - 1).astype(np.int32)
    y_new = np.clip(y + dy, 0, image.shape[0] - 1).astype(np.int32)

    return ripple_effect_recursive(image[y_new, x_new], depth - 1)

# Recursive Vortex Effect
def vortex_effect_recursive(image, intensity=5, depth=3):
    if depth == 0:
        return image

    height, width = image.shape[:2]
    y, x = np.meshgrid(np.arange(height), np.arange(width), indexing='ij')

    center_y, center_x = height / 2, width / 2
    rel_x, rel_y = x - center_x, y - center_y

    distance = np.sqrt(rel_x**2 + rel_y**2)
    angle = np.arctan2(rel_y, rel_x) + intensity * np.pi * distance / max(width, height)

    x_new = np.clip(center_x + distance * np.cos(angle), 0, width - 1).astype(np.int32)
    y_new = np.clip(center_y + distance * np.sin(angle), 0, height - 1).astype(np.int32)

    new_intensity = max(intensity - 1, 1)  # Reduce intensity for each recursive step
    return vortex_effect_recursive(image[y_new, x_new], new_intensity, depth - 1)

# Recursive Original Effect
def original_effect_recursive(image, depth=3):
    if depth == 0:
        return image

    brightness_factor = np.random.uniform(0.5, 1.5)
    contrast_factor = np.random.uniform(0.5, 1.5)
    adjusted_image = image * brightness_factor
    adjusted_image = (adjusted_image - adjusted_image.mean()) * contrast_factor + adjusted_image.mean()

    return original_effect_recursive(adjusted_image.astype(np.uint8), depth - 1)

# Create Collage Function
def create_collage(image):
    height, width = image.shape[:2]

    # Calculate the splitting points
    height_mid = height // 2
    width_mid = width // 2

    # Divide the image into four parts
    top_left = image[:height_mid, :width_mid]
    top_right = image[:height_mid, width_mid:]
    bottom_left = image[height_mid:, :width_mid]
    bottom_right = image[height_mid:, width_mid:]

    # Apply different recursive effects
    top_left = ripple_effect_recursive(top_left)
    top_right = vortex_effect_recursive(top_right)
    bottom_left = original_effect_recursive(bottom_left)
    bottom_right = original_effect_recursive(bottom_right)  # or another effect

    # Pad the sections if needed to match dimensions for concatenation
    def pad_to_match(img1, img2, axis):
        if img1.shape[axis] > img2.shape[axis]:
            diff = img1.shape[axis] - img2.shape[axis]
            padding = [(0, 0)] * len(img1.shape)
            padding[axis] = (0, diff)
            img2 = np.pad(img2, padding, mode='constant', constant_values=0)
        elif img1.shape[axis] < img2.shape[axis]:
            diff = img2.shape[axis] - img1.shape[axis]
            padding = [(0, 0)] * len(img1.shape)
            padding[axis] = (0, diff)
            img1 = np.pad(img1, padding, mode='constant', constant_values=0)
        return img1, img2

    top_left, top_right = pad_to_match(top_left, top_right, 0)
    bottom_left, bottom_right = pad_to_match(bottom_left, bottom_right, 0)

    top_half = np.concatenate((top_left, top_right), axis=1)
    bottom_half = np.concatenate((bottom_left, bottom_right), axis=1)

    top_half, bottom_half = pad_to_match(top_half, bottom_half, 1)
    collage = np.concatenate((top_half, bottom_half), axis=0)

    return collage

# Load the image
image = Image.open('input.jpg')
image = np.array(image)

# Create the collage
collage_image = create_collage(image)

# Convert the collage image to an 8-bit unsigned integer type
collage_image = collage_image.astype(np.uint8)

# Output final image
output_image = Image.fromarray(collage_image)
output_image.save('output_collage.jpg')
