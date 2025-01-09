from openai import AsyncOpenAI
from dotenv import load_dotenv
import os


load_dotenv(override=True)

open_ai_key = os.environ["open_ai_key"]


class OpenAIHandler:
    def __init__(self) -> None:
        self.client = open_ai_key

    async def model(self, prompt, model="gpt-4o-mini-2024-07-18"):
        client = AsyncOpenAI(api_key=self.client)
        messages = [{"role": "user", "content": prompt}]
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.0,
        )
        return response.choices[0].message.content

    async def summarize_brand_website(self, content, model="gpt-4o"):
        """Generates a summary of the outfit descriptions to further reduce the number of words but keeping the content intact
        Args:
        content(str): The description of the outfit
        model(str): The LLM model to be used, it defaults to gpt-3.5-turbo-0125

        Returns:
            A summarized version of the description of the outfit
        """
        client = AsyncOpenAI(api_key=self.client)
        messages = [
            {
                "role": "system",
                "content": f"""
                Summarize this description, reduce it very much, but make sure all vital information is in there
                Description: {content}
                """,
            },
            {"role": "user", "content": content},
        ]

        response = await client.chat.completions.create(
            model=model, messages=messages, temperature=0.0, max_tokens=150
        )
        return response.choices[0].message.content

    async def generate_one_liner(self, content, model="gpt-4o"):
        """Generates a summary of the outfit descriptions to further reduce the number of words but keeping the content intact
        Args:
        content(str): The description of the outfit
        model(str): The LLM model to be used, it defaults to gpt-3.5-turbo-0125

        Returns:
            A summarized version of the description of the outfit
        """
        client = AsyncOpenAI(api_key=self.client)
        messages = [
            {
                "role": "system",
                "content": f"""
                Generate one liner for this company
                Description: {content}
                """,
            },
            {"role": "user", "content": content},
        ]

        response = await client.chat.completions.create(
            model=model, messages=messages, temperature=0.0, max_tokens=150
        )
        return response.choices[0].message.content
