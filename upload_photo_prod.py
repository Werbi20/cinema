import os
import base64
import requests

BASE_URL = os.environ.get("PROD_BASE_URL", "https://palaoro-production.firebaseapp.com")
LOCATION_ID = int(os.environ.get("LOCATION_ID", "1"))
CAPTION = os.environ.get("PHOTO_CAPTION", "Foto teste")
IS_PRIMARY = os.environ.get("IS_PRIMARY", "true").lower() in {"1", "true", "yes"}
API_KEY = os.environ.get("API_KEY")  # opcional

PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAA4AAAAPCAIAAAB8x0bcAAAACXBIWXMAAAsTAAALEwEAmpwYAAAB" \
    "HUlEQVQoz4WSv0tCURTHP7fNm9tNm2mTSaZpEISgCBYKiUgrFkIWoVhY2BhKCmI/gIygo2FgIliI" \
    "aFQkLCwsrCwsLBR8w1KZpOuefPnPOnDn3nHNf8/1+P6NG0zQHf+J5PqfPsFrHcRznkF2bYB6bYwzj" \
    "GEYAt7lcrlcqlQqPR6PRAJ/Ph9/vR0VRlEqlgs/n4/V6nUKh0wqlUqlUpmkwmEYhjEYjUaDTqcDj" \
    "8fD4bDbDZrPJZLJYLNZpPJZBLpdBrVajQYDAYqlUrdbvdUKvV6/X4fD4VCqVarXazWYRi8XgcDqfz" \
    "eDz+QyKRCI/HA5PJBL/fB5PJhNfrhVgsxg8fhyAIgiAI6/V6mUwmq9UKwWBQKBQKhUK/Xw+Px4PNZ" \
    "pNFoNBrP5xGIx+Px+Fw+F2+2m02m80mEwmA7fbDbfbjQajUa/X4fP53O53O4wzAMsywLquq6L6/X6" \
    "/R6v1+s1m82iKIoCgKqqoij6fz+fz+fz+fzWYz+cxzHMdx3EcwzAMwzAM4/0DrGNVopgK1G8AAAAA" \
    "SUVORK5CYII="
)

def ensure_image(path: str):
    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(base64.b64decode(PNG_B64))

def upload_photo():
    image_path = "test_upload.png"
    ensure_image(image_path)

    url = f"{BASE_URL}/api/v1/locations/{LOCATION_ID}/photos"
    params = {"caption": CAPTION, "is_primary": str(IS_PRIMARY).lower()}

    headers = {}
    if API_KEY:
        headers["X-API-Key"] = API_KEY

    with open(image_path, "rb") as f:
        files = {"photo": (os.path.basename(image_path), f, "image/png")}
        resp = requests.post(url, params=params, files=files, headers=headers, timeout=30)

    print("POST", resp.status_code)
    try:
        print(resp.json())
    except Exception:
        print(resp.text)

    # Listar fotos
    list_url = f"{BASE_URL}/api/v1/locations/{LOCATION_ID}/photos"
    r2 = requests.get(list_url, headers=headers, timeout=15)
    print("GET /photos", r2.status_code)
    try:
        print(r2.json())
    except Exception:
        print(r2.text)

if __name__ == "__main__":
    upload_photo()
