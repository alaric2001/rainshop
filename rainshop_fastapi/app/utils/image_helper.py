# utils/image_helper.py

from io import BytesIO
from PIL import Image
import os
import base64
import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
import faiss

# Load model sekali saja
model = ResNet50(weights="imagenet", include_top=False, pooling="avg")

def faiss_write(vector: np.ndarray, faiss_index: int):
    vector = np.array([vector]).astype('float32')  # bentuknya jadi (1, 2048)

    # Cek apakah file index Faiss sudah ada
    index_path = "index_barang.bin"
    if os.path.exists(index_path):
        # Muat index dari file
        index = faiss.read_index(index_path)
    else:
        # Buat IndexIDMap index Faiss (FlatL2 = jarak Euclidean biasa)
        index = faiss.IndexIDMap(faiss.IndexFlatL2(2048))

    # index.add_with_ids(np.array([vector]), np.array([faiss_index], dtype=np.int64))
    index.add_with_ids(vector, np.array([faiss_index], dtype=np.int64))
    # # Simpan index ke file kalau mau dipakai nanti
    faiss.write_index(index, index_path) # Simpan kembali index ke file

def faiss_search(vector: np.ndarray):
    vector = np.array([vector]).astype('float32')  # bentuknya jadi (1, 2048)

    # Cek apakah file index Faiss sudah ada
    index_path = "index_barang.bin"
    if os.path.exists(index_path):
        # Muat index dari file
        index = faiss.read_index(index_path)
    else:
        # Buat IndexIDMap index Faiss (FlatL2 = jarak Euclidean biasa)
        index = faiss.IndexIDMap(faiss.IndexFlatL2(2048))

    return index.search(vector, k=5)

def faiss_remove(faiss_index: int):
    # Cek apakah file index Faiss sudah ada
    index_path = "index_barang.bin"
    if os.path.exists(index_path):
        # Muat index dari file
        index = faiss.read_index(index_path)
    else:
        # Buat IndexIDMap index Faiss (FlatL2 = jarak Euclidean biasa)
        index = faiss.IndexIDMap(faiss.IndexFlatL2(2048))

    index.remove_ids(np.array([faiss_index], dtype=np.int64))    
    return {"status" : True}


def preprocess_image(img):    
    # Resize ke 224x224 untuk ResNet
    img = img.resize((224, 224))
    img_array = np.expand_dims(np.array(img), axis=0)
    img_array = preprocess_input(img_array)

    # # Ekstrak fitur dengan ResNet50
    features = model.predict(img_array)
    vector = features[0]  # Sudah bentuk array NumPy
    return vector


def image_to_base64(image_path: str) -> str:
    # 1. Buka gambar
    with Image.open(image_path) as img:
        # 2. Konversi ke mode RGB (untuk JPG)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 3. Simpan ke buffer bytes
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=95)
        
        # 4. Encode ke base64
        img_bytes = buffer.getvalue()
        base64_str = base64.b64encode(img_bytes).decode('utf-8')
    
    return f"data:image/jpeg;base64,{base64_str}"

def add_image_attribute(obj, imgBase64):
    max_images=3
    for g in range(1, max_images + 1):
        attr_name = f'image{g}'
        if not hasattr(obj, attr_name) or getattr(obj, attr_name) is None:
            # print (f'image_id={image_id}  setattr {attr_name}')
            setattr(obj, attr_name, imgBase64)
            # setattr(obj, f'image{g}_id', image_id)
            break  # Hentikan loop setelah berhasil ditambahkan
