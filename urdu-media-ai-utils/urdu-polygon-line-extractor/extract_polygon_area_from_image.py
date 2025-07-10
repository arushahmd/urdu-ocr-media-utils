import os
import json
from PIL import Image, ImageDraw, ImageStat

def extract_polygon_regions_vott(annotation_file, images_folder, output_folder):
    """
         Extracts the images annotated using polygon shape in vott.
    :param annotation_file: .json annotation file by vott
    :param images_folder: folder containing book page images
    :param output_folder: folder to output extracted line images
    :return: extracts and save extracted line images to output folder
    """

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the annotation file
    with open(annotation_file, 'r') as f:
        annotations = json.load(f)

    # Get the image name from the 'asset' section
    image_name = annotations['asset']['name']

    # Open the corresponding image
    image_path = os.path.join(images_folder, image_name)
    with Image.open(image_path) as img:

        # Create a white background image
        background = Image.new('RGB', img.size, (255, 255, 255))

        # # Convert to grayscale to calculate the background color
        # grayscale_img = img.convert("L")
        # mean_intensity = ImageStat.Stat(grayscale_img).mean[0]
        #
        # # Create a background image with the same size and mean intensity
        # background = Image.new('L', img.size, int(mean_intensity))
        # background = background.convert("RGB")  # Convert back to RGB

        for i, region in enumerate(annotations['regions']):
            # Get the polygon points
            polygon = [(point['x'], point['y']) for point in region['points']]

            # Create a mask for the polygon
            mask = Image.new('L', img.size, 0)
            ImageDraw.Draw(mask).polygon(polygon, outline=1, fill=255)

            # Apply the mask to the image with the matching background
            masked_img = Image.composite(img, background, mask)

            # Get the bounding box of the polygon to crop the image to the polygon's extent
            bbox = mask.getbbox()
            if bbox:
                cropped_img = masked_img.crop(bbox)

                # Save the cropped polygon region
                output_path = os.path.join(output_folder, f"{os.path.splitext(image_name)[0]}_region_{i + 1}.png")
                cropped_img.save(output_path)

                print(f"Saved: {output_path}")

if __name__ == "__main__":

    # Example usage
    annotation_file = 'data-books/B150/Annotated/2ed2691d0be7f664d0482fc5763d75dd-asset.json' # vott annotation json file
    images_folder = 'data-books/B150/Image' # folder contianing book page images
    output_folder = 'output' # folder to output images to

    extract_polygon_regions_vott(annotation_file, images_folder, output_folder)
