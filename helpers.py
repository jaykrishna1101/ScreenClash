import requests

from flask import redirect, render_template, session
from functools import wraps
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

TMDB_API_KEY = "84f4c28d169ca3aa73ee7756f0ac24df"
BASE_URL = "https://api.themoviedb.org/3"
TMDB_BEARER_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4NGY0YzI4ZDE2OWNhM2FhNzNlZTc3NTZmMGFjMjRkZiIsIm5iZiI6MTc0MzA3NjYxOS4zMjMsInN1YiI6IjY3ZTUzZDBiNDIxZWI4YzMzMWJhNGFkNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.g05h5ksepY7xqyK1bNlWUwDIEkyR0F7gKEelElKzEqc"

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def omDetails(ttid):
    url = f"https://www.omdbapi.com/?i={ttid}&apikey=b7fa41c7"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0',
        }
        response = requests.get(url,headers=headers)
        response.raise_for_status()
        link = response.json()
        return link
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print("Data parsing error: {e}")
    return None

def get_tv_show_details(show_id):
    url = f"https://api.themoviedb.org/3/tv/{show_id}?language=en-US&append_to_response=external_ids"

    headers = {
        "Authorization": f"Bearer {TMDB_BEARER_TOKEN}",
        "accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=1,
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)

    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch show details for ID {show_id}:", e)
        return {}
    

def search_tv_show(query):
    url = "https://api.themoviedb.org/3/search/tv"
    params = {
        "query": query,
        "language": "en-US",
        "page": 1,
        "include_adult": "false"
    }

    headers = {
        "Authorization": f"Bearer {TMDB_BEARER_TOKEN}",
        "accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=1,
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)

    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        response = session.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return []