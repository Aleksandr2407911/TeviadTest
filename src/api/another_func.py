import aiohttp
import base64


async def get_token_tevian(email: str, password: str) -> str:
    url = "https://backend.facecloud.tevian.ru/api/v1/login"
    data = {"email": email, "password": password}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                json_response = await response.json()
                return json_response["data"]["access_token"]
            else:
                raise Exception(f"Error: {response.status} - {await response.text()}")


async def detect(token: str, file_path: str) -> dict:
    url = "https://backend.facecloud.tevian.ru/api/v1/detect?demographics=true"
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
        "Content-Type": "image/jpeg",
    }
    with open(file_path, "rb") as image_file:
        image_data = image_file.read()

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=image_data) as response:
            if response.status == 200:
                result = await response.json()
                return result
            else:
                raise Exception(f"Error: {response.status} - {await response.text()}")
