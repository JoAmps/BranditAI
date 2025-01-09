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
                retry_count = 0
                while retry_count < 5:
                    try:
                        output = await model.text_extracter_from_html(batch)
                        break
                    except Exception as e:
                        error_count += 1
                        retry_count += 1
                        print(f"An error occurred: {str(e)}")
                        print("Retrying...")
                        if error_count > 5:
                            print("An error occured, shutting down")
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

                    retry_count = 0
                    while retry_count < 5:
                        try:
                            output = await model.text_organizer_from_html(batch)
                            break
                        except Exception as e:
                            error_count += 1
                            retry_count += 1
                            print(f"An error occurred: {str(e)}")
                            print("Retrying...")
                            if error_count > 5:
                                print("An error occured, shutting down")
                                break
                            time.sleep(2)

            print(f"Total errors occurred: {error_count}")
            print("Finished")
            return output
