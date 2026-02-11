import httpx

async def fetch_image(url: str) -> bytes:
    async with httpx.AsyncClient(timeout=5.0, follow_redirects=True) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.content
