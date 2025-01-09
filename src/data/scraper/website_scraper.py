import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time


class WebsiteScraper:
    def __init__(self):
        pass

    def access_html_of_url(self, url):
        """Generates the html of the webpage and retrieves its length
        Args:
        url(webpage url): The url of the webpage

        Returns:
            html(html): The generated html of the webpage
            content_length(int): The length of the html page
        """
        response = requests.get(url)
        html = response.content
        return html

    def remove_irrelevant_elements(self, html):
        """Removes the irrelevant elements from an html
        Args:
        html(html): The generated html of the webpage

        Returns:
            modified_html(html): The html with the irrelevant elements removed
        """

        # Create a BeautifulSoup object from the HTML
        soup = BeautifulSoup(html, "html.parser")

        # Define a list of elements to remove
        elements_to_remove = [
            "img",
            "video",
            "audio",
            "head",
            "meta",
            "link",
            "input",
            "button",
            "style",
            "script",
        ]

        # Remove the specified elements from the HTML
        for element in elements_to_remove:
            for tag in soup.find_all(element):
                tag.decompose()

        # Get the modified HTML without the removed elements
        modified_html = str(soup)

        return modified_html

    async def scraper(self, html, model):
        batch_size = 20_000
        combined_content = []
        count = 0
        error_count = 0

        html = self.remove_irrelevant_elements(html)

        with tqdm(total=len(html), desc="Processing") as pbar:
            for i in tqdm(range(0, len(html), batch_size), desc="Batches"):
                batch = html[
                    i : i + batch_size
                ]  # Convert the batch back to a string if needed
                count += 1
                pbar.set_description(f"Generating batch {count}")
                if isinstance(batch, bytes):
                    batch = batch.decode("utf-8")
                prompt = f"""
                    Take this html input and extract the relevant texts that is human readable information from it, try and structure it. The information extracted should be ready to be used, dont add any extra comments or information, just extract the relevant information, thats it
                    Make sure not to include any irrelevant items such as image height and width, etc and also dont include any styles or anything        "<{batch}>"
                    """
                retry_count = 0
                while retry_count < 5:
                    try:
                        output = await model.model(prompt)
                        break
                    except Exception as e:
                        error_count += 1
                        retry_count += 1
                        print(f"An error occurred: {str(e)}")
                        print("Retrying...")
                        if error_count > 5:
                            print("Moving to next url, too many errors")
                            break
                        time.sleep(2)
                combined_content.append(output)
                pbar.update(batch_size)
                time.sleep(2)

            all_combined_content = ",".join(combined_content)
            with tqdm(
                total=len(all_combined_content),
                desc="Combining",
            ) as pbar:
                for i in tqdm(
                    range(0, len(all_combined_content), batch_size),
                    desc="Batches",
                ):
                    batch = all_combined_content[i : i + batch_size]

                    prompt = f"""
                        Take this information and remove all html tags, leaving only texts that is human readable and relevant for semantic similiarity.
                        Remember to try and provide a structure to it, so we can perform good semantic similarity.
                        Remember not to add any extra information besides things extracted from the information that is relevant for semantic similarity, dont add any image links or etc
                        DOnt be repeating sentences and please include every relevant information in the texts in the html, because any missed information would be a disaster for us
                        Please dont include any information about what the html is, or what the website uses, its irrelevant for semantic simililarity
                        Make sure to structure it very well, each section separated from the other, make it very clear to tell and capture all the details
                        Make sure not to call anything like item 1, item 2, provide the actual name as its in the html
                        "<{batch}>"
                        """
                    retry_count = 0
                    while retry_count < 5:
                        try:
                            output = await model.model(prompt)
                            break
                        except Exception as e:
                            error_count += 1
                            retry_count += 1
                            print(f"An error occurred: {str(e)}")
                            print("Retrying...")
                            if error_count > 5:
                                print("Moving to next url, too many errors")
                                break
                            time.sleep(2)

            print(f"Total errors occurred: {error_count}")
            print("Finished")
            return output
