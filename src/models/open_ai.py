from openai import AsyncOpenAI
from dotenv import load_dotenv
import os


load_dotenv(override=True)

open_ai_key = os.environ["open_ai_key"]


class OpenAIHandler:
    def __init__(self) -> None:
        self.client = open_ai_key

    async def text_extracter_from_html(self, content, model="gpt-4o-mini-2024-07-18"):
        client = AsyncOpenAI(api_key=self.client)
        messages = [
            {
                "role": "system",
                "content": f"""
                Take this html input and extract the relevant texts that is human readable information from it, try and structure it. The information extracted should be ready to be used, dont add any extra comments or information, just extract the relevant information, thats it
                Make sure not to include any irrelevant items such as image height and width, etc and also dont include any styles or anything.
                Description: {content}
                """,
            },
            {"role": "user", "content": content},
        ]
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.0,
        )
        return response.choices[0].message.content

    async def text_organizer_from_html(self, content, model="gpt-4o-mini-2024-07-18"):
        client = AsyncOpenAI(api_key=self.client)
        messages = [
            {
                "role": "system",
                "content": f"""
                Take this information and remove all html tags, leaving only texts that is human readable and relevant for semantic similiarity.
                Remember to try and provide a structure to it, so we can perform good semantic similarity.
                Remember not to add any extra information besides things extracted from the information that is relevant for semantic similarity, dont add any image links or etc
                Dont be repeating sentences and please include every relevant information in the texts in the html, because any missed information would be a disaster for us
                Please dont include any information about what the html is, or what the website uses, its irrelevant for semantic simililarity
                Make sure to structure it very well, each section separated from the other, make it very clear to tell and capture all the details
                Make sure not to call anything like item 1, item 2, provide the actual name as its in the html
                """,
            },
            {"role": "user", "content": content},
        ]
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
                Generate one liner for this company that can be used for a marketing campaign
                Description: {content}
                """,
            },
            {"role": "user", "content": content},
        ]

        response = await client.chat.completions.create(
            model=model, messages=messages, temperature=0.0, max_tokens=150
        )
        return response.choices[0].message.content
