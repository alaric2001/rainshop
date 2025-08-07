-- rainshop.vw_itembarang source

create or replace
algorithm = UNDEFINED view `rainshop`.`vw_itembarang` as
select
    `ib`.`item_id` as `item_id`,
    `ib`.`item_name` as `item_name`,
    `ib`.`item_price` as `item_price`,
    `ib`.`item_stock` as `item_stock`,
    `ib`.`isactive` as `isactive`, `ib`.modified,
    `im`.`faiss_index` as `faiss_index`,
    `im`.`image_path` as `image_path`,
    `im`.`image_id` as `image_id`
from
    (`rainshop`.`itembarang` `ib`
join `rainshop`.`item_images` `im` on
    (`ib`.`item_id` = `im`.`item_id`));
