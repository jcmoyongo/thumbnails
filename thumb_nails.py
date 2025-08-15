import os
from PIL import Image
import requests
from io import BytesIO
import aiohttp
import asyncio
import uuid
import traceback

# def create_thumbnails(input_folder, output_folder, size=(128, 128)):
#     """
#     Creates thumbnails for JPG and JPEG images in a folder.

#     Args:
#         input_folder (str): The path to the folder containing images.
#         output_folder (str): The path to the folder where thumbnails will be saved.
#         size (tuple): The size of the thumbnail (width, height).
#     """

#     # Create the output folder if it doesn't exist
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     for filename in os.listdir(input_folder):
#         if filename.lower().endswith((".jpg", ".jpeg")):
#             try:
#                 # Open the image
#                 img_path = os.path.join(input_folder, filename)
#                 img = Image.open(img_path)

#                 # Create a thumbnail
#                 img.thumbnail(size)

#                 # Save the thumbnail
#                 thumbnail_path = os.path.join(output_folder, f"thumbnail_{filename}")
#                 img.save(thumbnail_path)

#                 print(f"Created thumbnail for {filename}")

#             except Exception as e:
#                 print(f"Error processing {filename}: {e}")


# def create_thumbnails_from_api(output_folder, num_images=5, size=(128, 128)):
#     """
#     Creates thumbnails for N random images from a public image API.

#     Args:
#         output_folder (str): The path to the folder where thumbnails will be saved.
#         num_images (int): The number of random images to fetch.
#         size (tuple): The size of the thumbnail (width, height).
#     """
    
#     # Create the output folder if it doesn't exist
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     for i in range(num_images):
#         try:
#             # Fetch a random image from Lorem Picsum
#             response = requests.get(f"https://picsum.photos/200/200?random={i}")
#             response.raise_for_status()  # Raise an error for bad responses

#             # Open the image from the response content
#             img = Image.open(BytesIO(response.content))

#             # Create a thumbnail
#             img.thumbnail(size)

#             # Save the thumbnail
#             thumbnail_path = os.path.join(output_folder, f"thumbnail_{i}.jpg")
#             img.save(thumbnail_path)

#             print(f"Created thumbnail for image {i + 1}")

#         except Exception as e:
#             print(f"Error processing image {i + 1}: {e}")


def diagnose_thumbnail_save(thumbnail, output_folder, filename):
    # Ensure directory exists
    if not os.path.exists(output_folder):
        print("⚠️ Output folder does not exist, creating it...")
        os.makedirs(output_folder)

    # Confirm access
    print(f"🧠 Platform: {os.name}")
    print(f"📁 Saving to: {output_folder}")
    print(f"🧪 Writable: {os.access(output_folder, os.W_OK)}")
    print(f"👤 User ID (if on Unix): {getattr(os, 'getuid', lambda: 'N/A')()}")

    # Convert to RGB (if needed)
    if thumbnail.mode != "RGB":
        print(f"🎨 Converting image from {thumbnail.mode} to RGB...")
        thumbnail = thumbnail.convert("RGB")

    # Try to save thumbnail
    try:
        save_path = os.path.join(output_folder, filename)
        thumbnail.save(save_path, format="JPEG")  # Explicitly set format
        print(f"✅ Saved thumbnail to {save_path}")

        filename+= ".txt"  # Ensure the fi
        with open(os.path.join(output_folder, filename), "w") as f:
            f.write("Testing write from container!")
            print(f"✅ {filename} created in", output_folder)
    except Exception as e:
        print(f"❌ Error saving thumbnail:")
        print(f"🗨️ Exception: {e}")
        traceback.print_exc()


async def fetch_image(session, url):
    async with session.get(url) as response:
        response.raise_for_status()  # Raise an error for bad responses
        return await response.read()

async def create_thumbnail(image_data, size):
    img = Image.open(BytesIO(image_data))
    img.thumbnail(size)
    return img

async def create_thumbnails_from_api_async(output_folder, num_images=5, size=(128, 128)):
    """
    Creates thumbnails for N random images from a public image API asynchronously.

    Args:
        output_folder (str): The path to the folder where thumbnails will be saved.
        num_images (int): The number of random images to fetch.
        size (tuple): The size of the thumbnail (width, height).
    """
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(num_images):
            url = f"https://picsum.photos/200/200?random={i}"
            tasks.append(fetch_image(session, url))

        # Fetch all images concurrently
        images_data = await asyncio.gather(*tasks)

        # Create thumbnails concurrently
        thumbnail_tasks = []
        for i, image_data in enumerate(images_data):
            thumbnail_tasks.append(create_thumbnail(image_data, size))

        thumbnails = await asyncio.gather(*thumbnail_tasks)

        # Save thumbnails
        for i, thumbnail in enumerate(thumbnails):
            name_part = str(uuid.uuid4()).split('-')[0]  # Generate a unique name part  
            thumbnail_path = os.path.join(output_folder, f"thumbnail_{i+1}_{name_part}.jpg")  
            #thumbnail_path = os.path.join(output_folder, f"thumbnail_{i+1}_{name_part}.jpg")
            #Because of the volume mount, anything written to app/thumb_nails inside the container is actually written to the local directory
            # docker run -v C:/Users/jeanc/OneDrive/Projects/Study/thumb-nails/output_thumb_nails:/app/thumb_nails -it --rm thumb_nails /bin/bash
            try:
                # with open(os.path.join(output_folder,f"test_write_{i}.txt"), "w") as f:
                #     f.write("Testing write from container!")
                #     print("✅ test_write.txt created in", output_folder)

                thumbnail.save(thumbnail_path, "JPEG")  # Save the thumbnail as JPEG
                print(f"Created thumbnail for image {i + 1} in {thumbnail_path}")

                # diagnose_thumbnail_save(thumbnails[i], output_folder, f"thumbnail_{i+1}_{name_part}.jpg")
            except Exception as e:
                print(f"Error saving thumbnail: {e}")
                traceback.print_exc()
    

# Detect if running in container
inside_container = os.path.exists("/mnt/thumb_nails")

if inside_container:
    output_folder = "/mnt/thumb_nails"
else:
    output_folder = r"C:\Users\jeanc\thumb_nails"

print(f"🔍 Running {'inside' if inside_container else 'outside'} container. Output folder: {output_folder}")

if not os.path.exists(output_folder):
    try:
        os.makedirs(output_folder)
        print(f"📂 Created output folder at: {output_folder}")
    except Exception as e:
        print(f"❌ Failed to create folder: {e}")

test_file_path = os.path.join(output_folder, "python_test_write.txt")
try:
    with open(test_file_path, "w") as f:
        f.write("Hello from Python inside container!\n")
    print(f"✅ Successfully wrote test file to {test_file_path}")
except Exception as e:
    print(f"❌ Failed to write test file: {e}")

asyncio.run(create_thumbnails_from_api_async(output_folder, num_images=5))


# Example usage (replace with your actual output folder path)
# output_folder = r'C:\Users\jeanc\OneDrive\Projects\Study\thumb-nails\output_thumb_nails'  # Replace with your output folder path
# Replace with your output folder path
#create_thumbnails_from_api(output_folder, num_images=5)

# Example usage (replace with your actual paths)
#input_folder = r'C:\Users\jeanc\OneDrive\Projects\Study\thumb-nails\input_images'  # Replace with your input folder path
# output_folder = r'C:\Users\jeanc\OneDrive\Projects\Study\thumb-nails\output_thumb_nails'  # Replace with your output folder path
#(input_folder, output_folder)
