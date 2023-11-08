import requests
from bs4 import BeautifulSoup
import urllib.parse
import codecs
from lxml import etree


def crawl_website(url, visited=set(), max_depth=5, encoding='utf-8', excluded_links=None):
    """
    Crawls a website recursively, keeps track of all visited pages.
    
    Parameters:
    url (str): The URL of the website to crawl.
    visited (set): A set of visited URLs. Defaults to an empty set.
    max_depth (int): The maximum depth to crawl. Defaults to 5 (None = no maximum depth).
    encoding (str): The encoding to use when writing to the text file. Defaults to 'utf-8'.
    excluded_links (list): A list of URLs to exclude from crawling. Defaults to None.
    """
    
    # Parse the URL and get the website domain
    parsed_url = urllib.parse.urlparse(url)
    # print(parsed_url)
    
    domain = parsed_url.netloc
    
    # If this page has already been visited or is outside the website domain, return
    if url in visited:
        return
    
    # Add the URL to the visited set
    visited.add(url)
    with codecs.open(f"visited_links.txt", 'w', encoding) as f:
        f.write(f"{visited}\n")

    # Make a request to the page and get its content
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Error crawling {url}: {e}")
        return
    soup = BeautifulSoup(response.content, 'lxml')
    footer_elements = soup.find_all(class_='footer') + soup.find_all(id='footer')
    for element in footer_elements:
        element.decompose()
            
    # Write the page content to the text file
    # with codecs.open(f"sjsu_people.txt", 'a', encoding='utf-8') as f:
    #         f.write(f"\n{url}\n")
    #         # for tag in soup.find_all('p'):
    #         #     f.write(str(tag))
    #         #     f.write("\n")
    #         p_tags = soup.find_all('p')
    #         for p in p_tags:
    #             for child in p.children:
    #                 if child.name == None:
    #                     f.write(child)
    #         f.write('\n')
    
    # Recursively crawl all links on the page
    if max_depth is None or max_depth > 0:
        for link in soup.find_all('a'):
            href = link.get('href')

            if href:
                # Condition: If href starts with '/', append it to the url that called the function
                if href.startswith('/'):
                    href = urllib.parse.urljoin(url, href)
                # Parse the link and make sure it's within the website domain
                parsed_link = urllib.parse.urlparse(href)
                if not parsed_link.netloc:
                    href = urllib.parse.urljoin(url, href)
                
                if parsed_link.netloc == domain:
                    # Condition 1: If url has no 'sjsu', skip crawling that link
                    if 'sjsu' not in parsed_link.netloc:
                        continue
                    
                    # Condition 3: If url is not starting with 'http', skip crawling that link
                    if not href.startswith('http'):
                        continue
                    
                    # Condition 4: Skip crawling if the url is in excluded_links list
                    if excluded_links and href in excluded_links:
                        continue
                    
                    crawl_website(href, visited, None if max_depth is None else max_depth - 1, encoding, excluded_links)


excluded_links = exclude_links = [
        "http://sjsuparkingstatus.sjsu.edu/",
        "https://info.sjsu.edu/web-dbgen/catalog/degrees/all-degrees.html",
        "https://info.sjsu.edu/home/schedules.html",
        "http://ae.sjsu.edu/",
        "https://www.housing.sjsu.edu/",
        "http://www.engr.sjsu.edu/civil/",
        "http://cadre.sjsu.edu/",
        "http://www.engr.sjsu.edu/",
        "https://engr-extendedstudies.sjsu.edu/",
        "http://www.engr.sjsu.edu/hfe",
        "http://experts.sjsu.edu/",
        "http://publications.sjsu.edu/",
        "http://www.engr.sjsu.edu/ise",
        "http://www.engr.sjsu.edu/students/progs/mep",
        "http://www.transweb.sjsu.edu/",
        "http://photo.sjsu.edu",
        "https://www.sjsu.edu/it.20230314/services/web/forms/website-problem.php",
        "https://www.sjsu.edu/titleix/help/nondiscrimination-notice.php",
        "http://www.sjsu.edu/education/alumni/board/index.html",
        "http://www.sjsu.edu/hammertheatre/",
        "https://www.sjsu.edu/registrar/calendar/fall-2021.php",
        "https://www.sjsu.edu/up/index.html?utm_source=toplevel&utm_medium=301&utm_campaign=newhomepage",
        "https://www.sjsu.edu/discover/academics/index.html",
        "https://www.sjsu.edu/adminfinance/about/budget_central/index.html",
        "https://www.sjsu.edu/contact/index.html",
        "https://www.sjsu.edu/people/amir.armani/index.html",
        "https://www.sjsu.edu/people/sergio.bejar-lopez/index.html",
        "https://www.sjsu.edu/people/akilah.carter-francique/index.html",
        "https://www.sjsu.edu/people/Fatemeh.Davoudi",
        "https://www.sjsu.edu/people/karen.english/",
        "https://www.sjsu.edu/people/shaun.fletcher/index.html",
        "https://www.sjsu.edu/people/Yoonchung.han/index.html",
        "https://www.sjsu.edu/people/vlad.Ionescu/index.html",
        "https://www.sjsu.edu/people/kara.IrelandDAmbrosio/index.html",
        "https://www.sjsu.edu/people/Taehee.Jeong/index.html",
        "https://www.sjsu.edu/people/Rachel.Lazzeriaerts/index.html",
        "https://www.sjsu.edu/people/juneseok.lee/index.html",
        "https://www.sjsu.edu/people/li.zongchao/index.html",
        "https://www.sjsu.edu/people/harry.martinez/index.html",
        "https://www.sjsu.edu/people/jennifer.morrison/index.html"
    ]

# crawl_website('https://www.sjsu.edu/people/', excluded_links=excluded_links)
crawl_website('https://www.sjsu.edu/people', max_depth=10, excluded_links=excluded_links)
