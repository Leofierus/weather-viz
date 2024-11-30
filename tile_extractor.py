import numpy as np
import os

from PIL import Image
from scipy.ndimage import label

# Load the image
image_path = 'misc/trees/leaves.png'
output_folder = 'misc/trees/extracted_tiles'
os.makedirs(output_folder, exist_ok=True)

image = Image.open(image_path).convert("RGBA")
data = np.array(image)

# Create a binary mask (treat non-transparent pixels as part of components)
alpha_channel = data[:, :, 3]
binary_mask = alpha_channel > 0

# Label connected components
labeled_array, num_features = label(binary_mask)

# Extract each component and save as a separate PNG
for component_id in range(1, num_features + 1):
    # Find pixels belonging to the current component
    component_mask = labeled_array == component_id
    if not np.any(component_mask):
        continue

    # Find the bounding box of the component
    coords = np.argwhere(component_mask)
    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)

    # Crop the component from the original image
    cropped_data = data[y_min:y_max + 1, x_min:x_max + 1]
    cropped_mask = component_mask[y_min:y_max + 1, x_min:x_max + 1]

    # Apply the alpha channel to retain transparency
    cropped_data[:, :, 3] = (cropped_mask * 255).astype(np.uint8)

    # Convert back to an image
    component_image = Image.fromarray(cropped_data, 'RGBA')

    # Save the component as a separate PNG
    component_image.save(os.path.join(output_folder, f"tile_{component_id}.png"))

print(f"Extracted {num_features} components and saved them in {output_folder}")
