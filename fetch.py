import httpx

async def fetch_image(url: str) -> bytes:
    async with httpx.AsyncClient(timeout=5.0, follow_redirects=True, verify=False) as client: # v0.2.1 remove SSL
        r = await client.get(url)
        r.raise_for_status()
        return r.content
