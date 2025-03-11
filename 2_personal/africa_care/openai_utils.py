from openai import OpenAI, AzureOpenAI
import os
import json


def openai_generate_artwork(user_prompt: str, n: int = 1, size: str = "1024x1024") -> str:
    """
    Generate artwork using OpenAI's DALL-E model.

    Args:
        user_prompt (str): The prompt to generate the artwork.
        n (int, optional): The number of images to generate. Defaults to 1.
        size (str, optional): The size of the generated image. Defaults to "1024x1024".

    Returns:
        str: The URL of the generated image.
    """
    client = OpenAI()

    print("\n-_-_ Generating Image with OpenAI DALL-E 3 _-_-\n")
    new_image = client.images.generate(
        model="dall-e-3",
        prompt=user_prompt,
        n=n,
        size=size
    )
    image_url = new_image.data[0].url
    print(f"URL: {image_url}")
    return image_url


def azure_openai_generate_artwork(user_prompt: str, n: int = 1, size: str = "1024x1024") -> str:
    """
    Generate artwork using Azure OpenAI's DALL-E model.

    Args:
        user_prompt (str): The prompt to generate the artwork.
        n (int, optional): The number of images to generate. Defaults to 1.
        size (str, optional): The size of the generated image. Defaults to "1024x1024".

    Returns:
        str: The URL of the generated image.
    """

    client = AzureOpenAI(
        api_version="2024-02-01",  
        api_key=os.environ["AZURE_OPENAI_API_KEY"],  
        azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT']
    )
    
    print("\n-_-_ Generating Image with Azure OpenAI DALL-E 3 _-_-\n")
    new_image = client.images.generate(
        model="dalle3",  # the name of your DALL-E 3 deployment
        prompt=user_prompt,
        n=n,
        size=size
    )

    json_response = json.loads(new_image.model_dump_json())
    image_url = json_response["data"][0]["url"]  # extract image URL from response
    print(f"URL: {image_url}")
    return image_url


if __name__ == "__main__":
    azure_openai_generate_artwork("a close-up of a bear walking throughthe forest")
