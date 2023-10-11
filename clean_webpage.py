import re
import os
import requests
import urllib.parse
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_unique_filename(filename):
    i = 1
    new_filename = filename
    while os.path.isfile(new_filename):
        # Append underscore and digit to file name
        new_filename = f"{filename}_{i}"
        i += 1
    return new_filename


def clean_text_data(raw_text, filepath):
    #print("Cleaning text data...")
    if raw_text is None:
        return ""
    # Remove newlines and extra whitespace
    # cleaned_text = " ".join(raw_text.split())
    cleaned_text = raw_text.encode("ascii", "ignore").decode()

    # Convert all text to lowercase
    cleaned_text = cleaned_text.lower()
    
    # Remove consecutive whitespace characters
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(cleaned_text)
        f.write(" ")

    # return cleaned_text

def convert_http_links_to_https_and_segregate(urls_file):
    # Create directories to store the data
    data_dir = "data2"
    http_dir = os.path.join(data_dir, "http")
    https_dir = os.path.join(data_dir, "https")
    no_extension_dir = os.path.join(data_dir, "no_extension")
    for dir_path in [data_dir, http_dir, https_dir, no_extension_dir]:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

    # Read the list of URLs from a file
    with open(urls_file, "r") as f:
        urls = f.readlines()

    # Loop over the URLs and convert HTTP links to HTTPS
    for url in tqdm(urls, total=len(urls), desc="Processing lines"):
        # Check if the URL has an extension in the first segment
        parsed_url = urllib.parse.urlparse(url.strip())
        path = parsed_url.path.strip("/")
        path_segments = path.split("/")
        if "." not in path_segments[-1]:
            # Save the URL to a file in the no_extension directory
            filename = os.path.join(no_extension_dir, "no_extension.txt")
            with open(filename, "a") as f:
                f.write(url)
            continue

        category = path_segments[0]

        # Save the entire content of the webpage to a file
        file_dir = os.path.join(https_dir, category) if parsed_url.scheme == "https" else os.path.join(http_dir, category)
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        filename = os.path.join(file_dir, path_segments[-1])
        filename = get_unique_filename(filename)
        # f = open(filename, "w")
    #     with open(filename, "w") as f:
    #         f.write(soup.decode("utf-8"))
    #     print(f"Content of {url} saved to {filename}")
    # else:
    #     print(f"Error downloading {url}: status code {response.status_code}")


        # Convert HTTP links to HTTPS
        if parsed_url.scheme == "http":
            parsed_url = parsed_url._replace(scheme="https")
            url = parsed_url.geturl()

        # Save the content of the URL in a file
        response = requests.get(url)
        if response.status_code == 200:
            content = response.content
            soup = BeautifulSoup(content, "lxml")

            # Remove unnecessary elements from the soup
            for script in soup(["script", "style"]):
                script.decompose()
            # for elem in soup(['header', 'footer']):
            #     elem.extract()
            for header in soup.find_all("header"):
                # print(header)
                header.decompose()
            for footer in soup.find_all("footer"):
                # print(footer)
                footer.decompose()
            covid = soup.find("div", class_="o-emergency u-alert--gray")
            if covid is not None:
                covid.decompose()

            for tag in soup.find_all("a"):
                tag.replaceWithChildren()
            
            p_tags = soup.find_all('p')
            for p in p_tags:
                for child in p.children:
                    if child.name == None:
                        # f.write(child)
                        clean_text_data(child, filename)

    #         f.write('\n')
    # f.close()
convert_http_links_to_https_and_segregate("final_links.txt")
