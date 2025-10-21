import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_KEY_FILE = os.path.join(BASE_DIR, 'aminol-475711-79dbe02c04cf.json')

API_SCOPE = 'https://www.googleapis.com/auth/indexing'
ENDPOINT = 'https://indexing.googleapis.com/v3/urlNotifications:publish'

SITE_DOMAIN = "https://aminol.az" 
LANGUAGE_PREFIX = ""

STATIC_PATHS = [
    "/",
    "/about/",
    "/brands/", 
    "/career/", 
    "/contact/",
    "/faq/",
    "/markets/automotive/",
    "/markets/industrial/",
    "/markets/shipping/", 
    "/news/",
    "/product/",
    "/search/",
    "/services/dealer/",
    "/services/laboratory/",
    "/services/logistics/",
]

def get_credentials():
    try:
        creds = service_account.Credentials.from_service_account_file(
            JSON_KEY_FILE, scopes=[API_SCOPE])
        if not creds.valid:
            creds.refresh(Request())
        return creds
    except FileNotFoundError:
        return None
    except Exception as e:
        return None

def submit_url_to_google(url_to_submit, credentials, url_type="URL_UPDATED"):
    session = requests.Session()
    
    if credentials.expired:
        credentials.refresh(Request())
        
    session.auth = (f"Bearer {credentials.token}")
    
    payload = {
        "url": url_to_submit,
        "type": url_type
    }

    try:
        response = session.post(ENDPOINT, json=payload)
        response.raise_for_status() 
        print(f"  BAŞARILI ({url_type}): {url_to_submit}")
        return True

    except requests.exceptions.HTTPError:
        return False
    except Exception as e:
        return False

if __name__ == "__main__":
    creds = get_credentials()
    
    if creds:
        full_urls = [f"{SITE_DOMAIN}{LANGUAGE_PREFIX}{path}" for path in STATIC_PATHS]        
        for i, url in enumerate(full_urls):
            submit_url_to_google(url, creds, "URL_UPDATED")
            time.sleep(0.2)
            
        print("\nStatik URL gönderme işlemi tamamlandı.")
    else:
        print("Kimlik bilgileri alınamadı. İşlem iptal edildi.")