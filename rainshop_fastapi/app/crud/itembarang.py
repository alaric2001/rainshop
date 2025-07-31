import traceback
from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload  # atau joinedload
from fastapi import HTTPException
from app import models, schemas
from app.utils.image_helper import preprocess_image, image_to_base64, add_image_attribute, faiss_write, faiss_search 
from io import BytesIO
from PIL import Image
import os
import uuid
import base64

# Pastikan folder img ada
os.makedirs("img", exist_ok=True)
            
def get_max_faiss_index(db: Session) -> int:
    result = db.query(func.max(models.ItemImage.faiss_index)).scalar()
    return result if result is not None else 0


def create_item(db: Session, item: schemas.itembarang.ItemBarangCreate):
 try:    
    # 1. Decode base64 image
    image_data = base64.b64decode(item.image.split(",")[1])
    
    # 2. Buka gambar dengan PIL
    img = Image.open(BytesIO(image_data))

    item.item_id = str(uuid.uuid4())

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
    item.image_id=image_id
    db_item = models.ItemBarang(**item.dict(exclude={"image","image2","image3"}))
    db.add(db_item)
    db_item_image = models.ItemImage(**new_item_image.dict())
    db.add(db_item_image)

    if item.image2 is not None:
        image_data = base64.b64decode(item.image2.split(",")[1])
        img2 = Image.open(BytesIO(image_data))
        image_id=str(uuid.uuid4())
        filename = f"img_{image_id}.jpg"
        save_path = os.path.join("img", filename)
        img2.save(save_path, "JPEG", quality=95)

        vector = preprocess_image(img2)
        faiss_index = faiss_index + 1
        faiss_write (vector,faiss_index)   

        new_item_image = schemas.ItemImageCreate(
            image_id=image_id,
            item_id=item.item_id,
            image_path=save_path,
            faiss_index=faiss_index
        )
        db.add(models.ItemImage(**new_item_image.dict()))
    else:
        print ("image2 kosong")


    if item.image3 is not None:
        image_data = base64.b64decode(item.image3.split(",")[1])
        img3 = Image.open(BytesIO(image_data))
        image_id=str(uuid.uuid4())
        filename = f"img_{image_id}.jpg"
        save_path = os.path.join("img", filename)
        img3.save(save_path, "JPEG", quality=95)

        vector = preprocess_image(img3)
        faiss_index = faiss_index + 1
        faiss_write (vector,faiss_index)   

        new_item_image = schemas.ItemImageCreate(
            image_id=image_id,
            item_id=item.item_id,
            image_path=save_path,
            faiss_index=faiss_index
        )
        db.add(models.ItemImage(**new_item_image.dict()))
    else:
        print ("image3 kosong")

    db.commit()
    db.refresh(db_item)

    return { "status": True }
 except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=500, detail=f"Error saat proses gambar: {str(e)}")


def search_items(db: Session, image: str):
    try:
        image_data = base64.b64decode(image.split(",")[1])    
        img = Image.open(BytesIO(image_data))
        vector = preprocess_image(img)
        D, I = faiss_search(vector)   
         
        similar_items = []
        for idx in I[0]:
            getitem = db.query(models.VwItemBarang).filter(models.VwItemBarang.faiss_index == idx).first()
            if getitem:
                matching_items = [item for item in similar_items if item.item_id == getitem.item_id]
                # if not any(item.item_id == getitem.item_id for item in similar_items):
                if matching_items:
                    item_to_update = matching_items[0]  # Ambil item pertama yang cocok
                    add_image_attribute(item_to_update,image_to_base64(getitem.image_path))
                else: 
                    add_image_attribute(getitem,image_to_base64(getitem.image_path))
                    similar_items.append(getitem)

        return similar_items
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error Search Vector Image: {str(e)}")



def update_item(db: Session, item_id: str, frm: schemas.itembarang.ItemBarangUpdate):
 try:    
    item = db.query(models.ItemBarang).filter_by(item_id=item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Itembarang tidak ditemukan")

    item.item_name = frm.item_name
    item.item_price = frm.item_price
    item.item_stock = frm.item_stock
    if not frm.isactive:
        item.isactive = frm.isactive

    db.commit()
    db.refresh(item)

    return { "status": True }
 except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=500, detail=f"Error saat Update Itembarang: {str(e)}")


def get_item(db: Session, item_id: str):
    db_item = db.query(models.ItemBarang).options(
    selectinload(models.ItemBarang.images)  # Eager load relationship
    ).filter(models.ItemBarang.item_id == item_id).first()
    return schemas.itembarang.ItemBarangOut.model_validate(db_item)
    

def get_all_items(db: Session, item_name: str="", skip: int = 0, limit: int = 10):
    filters = []
    if item_name:
        print ("cari item: ", item_name);
        if '%' in item_name:
            filters.append(models.ItemBarang.item_name.ilike(item_name))
        else:
            filters.append(models.ItemBarang.item_name.ilike(f"%{item_name}%"))

    query = db.query(models.ItemBarang)

    if filters:
        query = query.filter(*filters).offset(skip).limit(limit)
    else:
        query = query.offset(skip).limit(limit)

    return query.all()

