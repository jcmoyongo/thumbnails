import asyncio
import requests
import aiohttp
from PIL import Image
from io import BytesIO
from msal import ConfidentialClientApplication
import msal
import os

# Function to fetch image from URL
async def fetch_image(session, url):
    async with session.get(url) as response:
        return await response.read()

# Function to create a thumbnail in memory
def create_thumbnail(image_data, size):
    image = Image.open(BytesIO(image_data))
    image.thumbnail(size)
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)  # Move to the beginning of the BytesIO buffer
    return img_byte_arr

# Function to upload image to OneDrive
def upload_to_onedrive(file_name, file_data, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/octet-stream'
    }
    response = requests.put(
        f'https://graph.microsoft.com/v1.0/me/drive/root:/{file_name}:/content',
        headers=headers,
        data=file_data
    )
    return response.status_code

async def main(num_images, size):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(num_images):
            url = f"https://picsum.photos/200/200?random={i}"
            tasks.append(fetch_image(session, url))

        # Fetch all images concurrently
        images_data = await asyncio.gather(*tasks)

        # Create thumbnails and upload concurrently
        thumbnail_tasks = []
        for i, image_data in enumerate(images_data):
            thumbnail = create_thumbnail(image_data, size)
            file_name = f'thumbnail_{i}.jpg'
            thumbnail_tasks.append(upload_to_onedrive(file_name, thumbnail.getvalue(), access_token))

        # Execute uploads
        upload_results = await asyncio.gather(*thumbnail_tasks)
        print(upload_results)

# Example usage
if __name__ == "__main__":
    num_images = 5  # Number of images to fetch
    size = (100, 100)  # Thumbnail size

    CLIENT_ID = os.getenv('CLIENT_ID')  # Replace with your Client ID
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')  # Replace with your Client Secret
    TENANT_ID = os.getenv('TENANT_ID')  # Replace with your Tenant ID
    AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
    SCOPE = ['https://graph.microsoft.com/.default']

    
    CLIENT_ID = "2649a458-3588-42c9-baaf-2518f6c83896"
    CLIENT_SECRET = "weg8Q~gb5hJLrs3Mk.FLnlB0nkIi4C23uylX-ceg"
    TENANT_ID = "35ff869d-82b9-4659-a4a4-3050b5afb64e"
    print("Using Client ID:", CLIENT_ID)
    print("Using Tenant ID:", TENANT_ID)
    print("Using Authority:", AUTHORITY)


    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )

    token_response = app.acquire_token_for_client(scopes=SCOPE)
    print("Token Response:", token_response)
    if 'access_token' in token_response:
        access_token = token_response['access_token']
        print("Access Token:", access_token)
    else:
        print("Error obtaining access token:", token_response.get("error"), token_response.get("error_description"))

    asyncio.run(main(num_images, size))
