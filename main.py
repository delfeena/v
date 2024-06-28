from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import re
import httpx
from datetime import date

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
headers = {
    "Referer": "https://vidsrc.vip",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Origin": "https://vidsrc.vip"
}


async def get_subtitles(imdbId,s=None,e=None, redirects: bool = True):
    """
    Retrieves subtitles for a video based on the provided IMDb ID and optional season/episode numbers.

    Args:
        imdbId (str): The IMDb ID of the video.
        s (int, optional): The season number of the video. Defaults to None.
        e (int, optional): The episode number of the video. Defaults to None.
        redirects (bool, optional): Whether to follow redirects. Defaults to True.

    Returns:
        dict: A dictionary containing the subtitles for the video.
    """

    async with httpx.AsyncClient(follow_redirects=redirects) as client:
        try:
            url=f"https://vidsrc.vip/subs/{imdbId}{f'-{s}-{e}' if s and e else ''}.txt"
            res = await client.get(url=url,headers=headers)
            res.raise_for_status()  
            return res.json()
           
           
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"HTTP error occurred: {exc}")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"An error occurred while requesting: {exc}")
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {exc}")

async def get_stream(id,s=None,e=None, redirects: bool = True):
    """
    Retrieves a streaming video source from the vidsrc.vip website based on the provided ID and optional season/episode numbers.

    Args:
        id (str): The ID of the video to retrieve.
        s (int, optional): The season number of the video. Defaults to None.
        e (int, optional): The episode number of the video. Defaults to None.
        redirects (bool, optional): Whether to follow redirects. Defaults to True.

    Returns:
        dict: A dictionary containing the streaming video source information, including the source, embed ID, and source URL.
            If subtitles are available for the video, they are also included in the dictionary under the key "captions".

    Raises:
        HTTPException: If an HTTP error occurs while retrieving the video source, or if the vpro link is not found in the response.
        HTTPException: If an error occurs while requesting the video source.
        HTTPException: If an unexpected error occurs while retrieving the video source.

    """

    async with httpx.AsyncClient(follow_redirects=redirects) as client:
        try:
            url=f"https://vidsrc.vip/{'hydraxtv' if s and e else 'hydrax'}.php?id={id}" + (f"&season={s}&episode={e}" if s and e else "")
            res = await client.get(url=url,headers=headers)
            res.raise_for_status()  
            match = re.search(r'const vpro = "(https://.*?)";', res.text)
            imdbid_match = re.search(r'const imdbId = "(tt.*?)";', res.text)
            if imdbid_match:
                imdbid = imdbid_match.group(1)
                subtitles= await get_subtitles(imdbid,s,e)
            if match:
                vpro_link = match.group(1)
                return {"source":"vidsrcVip","embedId":"hydrax","src": vpro_link,"captions":subtitles}
            else:
                raise HTTPException(status_code=404, detail="vpro link not found in the response")
           
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"HTTP error occurred: {exc}")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"An error occurred while requesting: {exc}")
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {exc}")
        

async def get_matches( redirects: bool = True):
       async with httpx.AsyncClient(follow_redirects=redirects) as client:
        try:
            today = date.today()
            url=f"https://api.123goal.to/v1/match/list?date={today.strftime('%Y-%m-%d')}"
            # url=f"https://api.123goal.to/v1/match/list?date=2024-06-28&timezone=Asia/Baghdad"
            print(url)
            res = await client.get(url=url,headers={
    "Referer": "https://vidsrc.vip",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Origin": "https://vidsrc.vip"
})
            res.raise_for_status()  
            return res.json() 
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"HTTP error occurred: {exc}")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"An error occurred while requesting: {exc}")
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {exc}")

async def get_matches( redirects: bool = True):
       async with httpx.AsyncClient(follow_redirects=redirects) as client:
        try:
            today = date.today()
            url=f"https://api.123goal.to/v1/match/list?date={today.strftime('%Y-%m-%d')}"
            res = await client.get(url=url,headers={
    "Referer": "https://123goal.to",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Origin": "https://123goal.to"
})
            res.raise_for_status()  
            return res.json() 
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"HTTP error occurred: {exc}")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"An error occurred while requesting: {exc}")
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {exc}")
        
async def get_match_stream(ts_id, redirects: bool = True):
       async with httpx.AsyncClient(follow_redirects=redirects) as client:
        try:
            url=f"https://api.123goal.to/v1/match/channels?matchId={ts_id}"
            res = await client.get(url=url,headers={
    "Referer": "https://123goal.to",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Origin": "https://123goal.to"
})
            res.raise_for_status()  
            return res.json() 
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"HTTP error occurred: {exc}")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"An error occurred while requesting: {exc}")
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {exc}")

@app.get("/matches")
async def get_todays_matches():
        sources = await get_matches()
        return sources

@app.get("/matches/{ts_id}")
async def get_todays_matches(ts_id: str):
        if ts_id:
            sources = await get_match_stream(ts_id)
            return sources
        else:
            raise HTTPException(status_code=404, detail=f"Invalid id: {ts_id}")
      

@app.get("/vidsrc/{dbid}")
async def vidsrc(dbid: str, s: int = None, e: int = None):
    if dbid:
        sources = await get_stream(dbid,s,e)
        return sources
    else:
        raise HTTPException(status_code=404, detail=f"Invalid id: {dbid}")
    

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
