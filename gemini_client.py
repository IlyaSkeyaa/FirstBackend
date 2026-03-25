from google import genai

from config import config_obj

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=config_obj.gemini_api_key)


def get_answer_from_gemini(prompt: str):

    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=prompt
    )
    return response.text

# if __name__ == "__main__":
#     main()