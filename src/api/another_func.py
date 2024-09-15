# from pydantic_settings import BaseSettings, SettingsConfigDict

# class Settings(BaseSettings):
#     USERNAME: str = "Misha"
#     PASSWORD: str = "misha_coder_911"
#     model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# settings = Settings()
import aiohttp
import base64
import logging

async def get_token_tevian(email, password):
    url = "https://backend.facecloud.tevian.ru/api/v1/login"
    data = {
        "email": email,
        "password": password
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                json_response = await response.json()
                return json_response["data"]["access_token"]
            else:
                raise Exception(f"Error: {response.status} - {await response.text()}")


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def detect(token, image_file):
    url = "https://backend.facecloud.tevian.ru/api/v1/detect"
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
        "Content-Type": "image/jpeg"
    }
    form_data = aiohttp.FormData()
    form_data.add_field('file', image_file, content_type='image/jpeg')

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=form_data) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Error: {response.status} - {await response.text()}")