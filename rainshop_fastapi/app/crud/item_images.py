from sqlalchemy.orm import Session
from app import models, schemas

def create_image(db: Session, image: schemas.item_images.ItemImageCreate):
    db_image = models.ItemImage(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def get_images_by_item_id(db: Session, item_id: str):
    return db.query(models.ItemImage).filter_by(item_id=item_id).all()
