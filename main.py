from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from PIL import Image, ImageEnhance
import requests
from io import BytesIO

app = FastAPI()

@app.get("/merge-images/")
def merge_images(
    house_url: str = Query(..., description="URL of the house image"),
    logo_url: str = Query(..., description="URL of the logo image"),
):
    # Download images
    house_response = requests.get(house_url)
    logo_response = requests.get(logo_url)

    house = Image.open(BytesIO(house_response.content)).convert("RGBA")
    logo = Image.open(BytesIO(logo_response.content)).convert("RGBA")

    # Resize logo
    logo = logo.resize((300, 100))  # Adjust size as needed

    # Enhance brightness (dimming)
    enhancer = ImageEnhance.Brightness(house)
    house = enhancer.enhance(0.6)  # Dimming (0.6 = 60% brightness)

    # Bottom-right position
    house_width, house_height = house.size
    logo_width, logo_height = logo.size
    position = (house_width - logo_width - 10, house_height - logo_height - 10)

    # Paste logo with transparency
    house.paste(logo, position, logo)

    # Output stream
    output = BytesIO()
    house.save(output, format="PNG")
    output.seek(0)

    return StreamingResponse(output, media_type="image/png")
