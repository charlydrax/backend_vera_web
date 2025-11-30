from fastapi import Request, APIRouter
from ...utils.telegram import send_message, download_telegram_file
from ...utils.video import video_to_text
from ...utils.image import image_to_text
from ...utils.vera import ask_vera

# app = FastAPI()
router = APIRouter(prefix="/webhook", tags=["webhook"])

@router.post("/")
async def telegram_webhook(request: Request):
    update = await request.json()

    if "message" not in update:
        return {"ok": True}

    message = update["message"]
    chat_id = message["chat"]["id"]

    # --- TEXTE ---
    if "text" in message:
        user_text = message["text"]
        vera_output = await ask_vera(user_text)
        await send_message(chat_id, vera_output)
        return {"ok": True}

    # --- PHOTO ---
    if "photo" in message:
        file_id = message["photo"][-1]["file_id"]
        image_path = await download_telegram_file(file_id)

        extracted_text = image_to_text(image_path)
        vera_output = await ask_vera(extracted_text)

        await send_message(chat_id, vera_output)
        return {"ok": True}

    # --- VIDÉO ---
    if "video" in message:
        file_id = message["video"]["file_id"]
        video_path = await download_telegram_file(file_id)

        extracted_text = video_to_text(video_path)
        vera_output = await ask_vera(extracted_text)

        await send_message(chat_id, vera_output)
        return {"ok": True}

    return {"ok": True}
