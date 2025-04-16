import requests
from bs4 import BeautifulSoup
import re


def get_script_from_link(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            script_content = soup.get_text(separator=' ', strip=True)

            # Clean up excessive whitespace and line breaks
            cleaned_script = re.sub(r'\s+', ' ', script_content)

            return cleaned_script if cleaned_script else "Script content not found."
        else:
            return f"Failed to retrieve webpage, status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred while fetching the script: {str(e)}"


def fetch_script_data(movie_name, api_uid, api_token, base_url):
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
