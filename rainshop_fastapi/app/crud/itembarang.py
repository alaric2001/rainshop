from sqlalchemy.orm import Session, selectinload  # atau joinedload
from fastapi import HTTPException
from app import models, schemas
from io import BytesIO
from PIL import Image
import os
import uuid
import json
import base64
import faiss
import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input

# import tensorflow as tf
# from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input

# Load model sekali saja
model = ResNet50(weights="imagenet", include_top=False, pooling="avg")
# Pastikan folder img ada
os.makedirs("img", exist_ok=True)

def image_to_base64(image_path: str) -> str:
    # 1. Buka gambar
    with Image.open(image_path) as img:
        # 2. Konversi ke mode RGB (untuk JPG)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 3. Simpan ke buffer bytes
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=95)
        
        # 4. Encode ke base64
        img_bytes = buffer.getvalue()
        base64_str = base64.b64encode(img_bytes).decode('utf-8')
    
    return f"data:image/jpeg;base64,{base64_str}"

def add_image_attribute(obj, imgBase64, max_images=3):
    for i in range(1, max_images + 1):
        attr_name = f'image{i}'
        if not hasattr(obj, attr_name) or getattr(obj, attr_name) is None:
            setattr(obj, attr_name, imgBase64)
            break  # Hentikan loop setelah berhasil ditambahkan
            



def create_item(db: Session, item: schemas.itembarang.ItemBarangCreate):
 try:    
    # 1. Decode base64 image
    image_data = base64.b64decode(item.image.split(",")[1])
    
    # 2. Buka gambar dengan PIL
    img = Image.open(BytesIO(image_data))

    if not item.item_id:
       item.item_id = str(uuid.uuid4())

    image_id=str(uuid.uuid4())
    filename = f"img_{image_id}.jpg"
    save_path = os.path.join("img", filename)
    
    # 3. Simpan gambar ke folder
    img.save(save_path, "JPEG", quality=95)

    # Resize ke 224x224 untuk ResNet
    img = img.resize((224, 224))
    img_array = np.expand_dims(np.array(img), axis=0)
    img_array = preprocess_input(img_array)

    # Ekstrak fitur dengan ResNet50
    features = model.predict(img_array)
    vector = features[0]  # Sudah bentuk array NumPy

    # Ubah jadi float32 dan 2D (1xN)
    vector = np.array([vector]).astype('float32')  # bentuknya jadi (1, 2048)

    # Buat index Faiss (FlatL2 = jarak Euclidean biasa)

    # index = faiss.IndexFlatL2(vector.shape[1])  # 2048 dimensi

    # # Tambahkan ke index
    # index.add(vector)

    # # Simpan index ke file kalau mau dipakai nanti
    
    # Cek apakah file index Faiss sudah ada
    index_path = "index_barang.bin"

    if os.path.exists(index_path):
        index = faiss.read_index(index_path)
    else:
        index = faiss.IndexFlatL2(vector.shape[1])  # 2048 dimensi

    # Tambah vector baru
    index.add(vector)
    faiss.write_index(index, index_path) # Simpan kembali index ke file

    
    db_item = models.ItemBarang(**item.dict(exclude={"image"}))
    db.add(db_item)

    # Posisi vektor di Faiss
    faiss_position = index.ntotal - 1  # Faiss pakai urutan, jadi ini posisi terbaru
    new_item_image = schemas.ItemImageCreate(
        image_id=image_id,
        item_id=item.item_id,
        image_path=save_path,
        faiss_index=faiss_position
    )
    db_item_image = models.ItemImage(**new_item_image.dict())
    db.add(db_item_image)
    db.commit()
    db.refresh(db_item)

    return { "status": True }
 except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error saat proses gambar: {str(e)}")


def search_items(db: Session, image: str):
    try:
        image_data = base64.b64decode(image.split(",")[1])    
        img = Image.open(BytesIO(image_data))
        img = img.resize((224, 224))
        img_array = np.expand_dims(np.array(img), axis=0)
        img_array = preprocess_input(img_array)

        features = model.predict(img_array)
        vector = features[0]  # Sudah bentuk array NumPy
        vector = np.array([vector]).astype('float32')  # bentuknya jadi (1, 2048)

        # Muat index dari file
        index = faiss.read_index("index_barang.bin")

        # Cari 5 terdekat
        D, I = index.search(vector, k=3)
        similar_items = []
        for idx in I[0]:
            getitem = db.query(models.VwItemBarang).filter(models.VwItemBarang.faiss_index == idx).first()
            if getitem:
                base64_data = image_to_base64(getitem.image_path)
                matching_items = [item for item in similar_items if item.item_id == getitem.item_id]
                # if not any(item.item_id == getitem.item_id for item in similar_items):
                if matching_items:
                    item_to_update = matching_items[0]  # Ambil item pertama yang cocok
                    add_image_attribute(item_to_update,base64_data)
                else: 
                    add_image_attribute(getitem,base64_data)
                    similar_items.append(getitem)

        return similar_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Search Vector Image: {str(e)}")


def get_item(db: Session, item_id: str):
    db_item = db.query(models.ItemBarang).options(
    selectinload(models.ItemBarang.images)  # Eager load relationship
    ).filter(models.ItemBarang.item_id == item_id).first()
    return schemas.itembarang.ItemBarangOut.model_validate(db_item)

def get_all_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.ItemBarang).offset(skip).limit(limit).all()
