from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import re
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_subtitles(imdbId,s=None,e=None, redirects: bool = True):
    async with httpx.AsyncClient(follow_redirects=redirects) as client:
        try:
            url=f"https://vidsrc.vip/subs/{imdbId}{f'-{s}-{e}' if s and e else ''}.txt"
            res = await client.get(url=url,headers={"Referer":"https://vidsrc.vip"})
            res.raise_for_status()  
            return res.json()
           
           
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"HTTP error occurred: {exc}")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"An error occurred while requesting: {exc}")
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {exc}")

async def get_stream(id,s=None,e=None, redirects: bool = True):
    async with httpx.AsyncClient(follow_redirects=redirects) as client:
        try:
            url=f"https://vidsrc.vip/{'hydraxtv' if s and e else 'hydrax'}.php?id={id}" + (f"&season={s}&episode={e}" if s and e else "")
            res = await client.get(url=url,headers={"Referer":"https://vidsrc.vip"})
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
