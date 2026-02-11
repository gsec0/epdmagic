from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import Response

from image_ops import process_image
from fetch import fetch_image

import os
from pathlib import Path
import sys
import base64
import re

# Change CWD
APP_PATH = Path(__file__).resolve()
if getattr(sys, 'frozen', False):
    APP_PATH = Path(sys.executable).resolve()
os.chdir(APP_PATH.parent)

APP_NAME = "epdmagic"
APP_VERSION = "0.2.0"

app = FastAPI(title=APP_NAME)

print(f"{APP_NAME} v{APP_VERSION}")
print(f"Current working directory: {Path.cwd()}")

_URL_RE = re.compile(r"^https?://", re.IGNORECASE)

def decode_url(url: str) -> str:
    """
    Try base64-decode the URL.
    If decoding fails or result doesn't look like a URL,
    return the original string.
    """
    try:
        padding = "=" * (-len(url) % 4)
        decoded = base64.urlsafe_b64decode(url + padding).decode("utf-8")

        # Only accept decoded value if it looks like a URL
        if _URL_RE.match(decoded):
            return decoded
    except Exception:
        pass

    return url

@app.post("/convert", response_class=Response)
async def convert(
    file: UploadFile | None = File(None),
    url: str | None = Query(None),
    width: int = Query(800, ge=1), # v0.2.0 allow custom target dimentions
    height: int = Query(480, ge=1),
):
    """
    Convert an image to 800x480 6-colour BMP for ePaper.

    Parameters:
    - file: uploaded image file
    - url: URL to fetch the image from
    """
    if not file and not url:
        raise HTTPException(status_code=400, detail="Provide file or url")

    if file:
        data = await file.read()
    else:
        url = decode_url(url)
        data = await fetch_image(url)

    bmp = process_image(data, target_w=width, target_h=height)

    return Response(
        content=bmp,
        media_type="image/bmp",
        headers={"Content-Disposition": "inline; filename=result.bmp"}
    )
