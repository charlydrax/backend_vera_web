import httpx
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"

async def send_message(chat_id, text):
    async with httpx.AsyncClient() as client:
        await client.post(f"{API}/sendMessage", json={
            "chat_id": chat_id,
            "text": text
        })

async def download_telegram_file(file_id):
    async with httpx.AsyncClient() as client:
        # Récupérer infos du fichier
        r = await client.get(f"{API}/getFile?file_id={file_id}")
        file_path = r.json()["result"]["file_path"]

        # Télécharger le fichier
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
        data = (await client.get(file_url)).content

        # Sauver localement
        output = "/tmp/input.bin"
        with open(output, "wb") as f:
            f.write(data)

        return output
