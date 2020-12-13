import io
import logging

from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import FileResponse, StreamingResponse
import easyocr

import PIL
from PIL import Image, ImageOps

app = FastAPI()
router = APIRouter()
ocr = easyocr.Reader(["en"])
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ocr")

@app.get("/")
async def root():
    return {"message": "Hello World"}


# @router.post("/ocr")
@app.post("/ocr")
async def do_ocr(request: Request):
    form = await request.form()
    file = form.get("file", None)
    if file is not None:
        res = ocr.readtext(await file.read())
        # return array of strings
        return [item[1] for item in res]
        # probable_text = "\n".join((item[1] for item in res))
        # return StreamingResponse(
        #     io.BytesIO(probable_text.encode()), media_type="text/plain"
        # )

    return { "error": "missing file" }


app.include_router(router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
