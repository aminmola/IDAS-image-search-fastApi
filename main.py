from compair import similar_postid
import uvicorn
from fastapi import FastAPI, File, UploadFile
from starlette.responses import FileResponse
import requests
import numpy as np
from utils.logger import Logger

app = FastAPI()

log = Logger("ImageSearch")


# sp = Compair()


@app.post("/")
async def upload_file(postid_count: int = 5, file: UploadFile = File(...), source: str = "kukala"):
    # params = {"postid_count": n }
    try:
        a = requests.request("POST", "http://192.168.110.45:4050/", headers={}, data={},
                             files=[('file', (file.filename, file.file, 'image/jpeg'))])
        vec = np.array(a.json(), dtype=np.float32)
        my_dict = {"similar_posts": similar_postid(vec, postid_count)}
        log.info(f"Request sent By {source}", status="succeed", origin=source)
    except:
        log.info(f"Request sent By {source}", status="failed", origin=source)
    return my_dict


@app.get("/")
async def read_index():
    return FileResponse('api/index.html')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4040)
