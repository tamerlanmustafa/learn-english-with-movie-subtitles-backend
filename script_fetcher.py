import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed


def fetch_single_script_page(page_url):
    """ Fetch individual page of script content. """
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        print(f"Requesting {page_url}...")  # Log the request for debugging
        response = requests.get(page_url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch {page_url} (Status code: {response.status_code})")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        blockquote = soup.find('blockquote')

        if blockquote:
            text = blockquote.get_text(separator=' ', strip=True)
            if len(text) > 30:  # Ensure there's content in the blockquote
                return text
            else:
                return None
        else:
            print(f"No <blockquote> found on page {page_url}")
            return None
    except Exception as e:
        print(f"Error fetching {page_url}: {e}")
        return None


def get_script_from_link(url, total_pages=50):
    """ Fetch the entire script across multiple pages by looping through each page. """
    script_parts = []

    # Use ThreadPoolExecutor for concurrent fetching
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        for i in range(1, total_pages + 1):
            page_url = f"{url}/{i}"
            futures.append(executor.submit(fetch_single_script_page, page_url))

        for future in as_completed(futures):
            page_text = future.result()
            if page_text:
                script_parts.append(page_text)

    if not script_parts:
        return "Script content not found."

    full_script = ' '.join(script_parts)
    return full_script.strip()


def fetch_script_data(movie_name, api_uid, api_token, base_url):
    """ Fetch script data via API, then get the script from multiple pages. """
    try:
        params = {
            "uid": api_uid,
            "tokenid": api_token,
            "term": movie_name,
            "format": "json"
        }

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(base_url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            result = data.get("result")

            if isinstance(result, dict) and "link" in result:
                script_link = result["link"]
                return get_script_from_link(script_link)
            else:
                return "Script not found for this movie."
        else:
            return f"API request failed with status code: {response.status_code}"

    except Exception as e:
        return f"An error occurred during API request: {str(e)}"
