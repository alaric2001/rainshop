from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from gtts import gTTS
import io

router = APIRouter(prefix="/voiceover", tags=["Voiceover"])

@router.get("/")
def generate_voiceover():
    text = """Inilah aplikasi Penjualan masa kini,
    Alhamdulillah sudah terimplementasi di toko pernak-pernik Rain-shop milik kami. 
    kami tidak perlu melakukan pengkodean dan labeling barcode pada setiap item barang,
    berkat ei ai Similarity Search, teknologi yang dipakai Facebook untuk mengenali wajah.
    Sehingga penjaga toko tidak perlu kode barang atau harus tahu namanya untuk entry item jualan,
    cukup tunjukkan barang tersebut ke kamera. 
    ... hubungi whatsApp 081290482972
    """



    # Generate TTS
    tts = gTTS(text=text, lang="id")
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    # Return sebagai file download
    return StreamingResponse(mp3_fp, media_type="audio/mpeg", headers={
        "Content-Disposition": "attachment; filename=voiceover.mp3"
    })
