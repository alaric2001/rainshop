ALTER TABLE rainshop.itembarang ADD image_id varchar(100) NULL;
update itembarang inner join item_images on itembarang.item_id=item_images.item_id
  set itembarang.image_id=item_images.image_id
  where itembarang.image_id is null;