import traceback
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models, schemas
from app.utils.image_helper import preprocess_image, image_to_base64, add_image_attribute, faiss_write, faiss_search 
from io import BytesIO
from PIL import Image
import os
import uuid
import base64

os.makedirs("img", exist_ok=True)

def get_max_faiss_index(db: Session) -> int:
    result = db.query(func.max(models.ItemImage.faiss_index)).scalar()
    return result if result is not None else 0


def create_image(db: Session, frm: schemas.item_images.ItemImageForm):
 try:
    # 1. Decode base64 image
    image_data = base64.b64decode(frm.image.split(",")[1])
    
    # 2. Buka gambar dengan PIL
    img = Image.open(BytesIO(image_data))

    image_id=str(uuid.uuid4())
    filename = f"img_{image_id}.jpg"
    save_path = os.path.join("img", filename)
    
    # 3. Simpan gambar ke folder
    img.save(save_path, "JPEG", quality=95)

    vector = preprocess_image(img)
    faiss_index = get_max_faiss_index(db) + 1
    faiss_write (vector,faiss_index)   

    new_item_image = schemas.ItemImageCreate(
        image_id=image_id,
        item_id=item.item_id,
        image_path=save_path,
        faiss_index=faiss_index
    )
    db_item_image = models.ItemImage(**new_item_image.dict())
    db.add(db_item_image)
    db.commit()
    db.refresh(db_item)

    return { "status": True }
 except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=500, detail=f"Error saat proses gambar: {str(e)}")

def update_image(db: Session, image_id: str, image: str):
 try:
    # 1. Decode base64 image

    rekord = db.query(models.ItemImage).filter_by(image_id=image_id).first()
    if not rekord:
        raise HTTPException(status_code=404, detail="Image not found")

    image_data = base64.b64decode(image.split(",")[1])
    
    # 2. Buka gambar dengan PIL
    img = Image.open(BytesIO(image_data))
    filename = f"img_{image_id}.jpg"
    save_path = os.path.join("img", filename)
    
    # 3. Simpan gambar ke folder
    img.save(save_path, "JPEG", quality=95)

    vector = preprocess_image(img)
    faiss_write (vector,rekord.faiss_index)   

    # db.commit()
    # db.refresh(rekord)

    return { "status": True }
 except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=500, detail=f"Error saat update gambar: {str(e)}")

def get_image(db: Session, image_id: str):
    getitem = db.query(models.VwItemBarang).filter(models.VwItemBarang.image_id == image_id).first()
    if getitem:
        return image_to_base64(getitem.image_path)
    else:
       print (f' image not found dg id:{image_id}')


def get_images_by_item_id(db: Session, item_id: str):
    return db.query(models.ItemImage).filter_by(item_id=item_id).all()
