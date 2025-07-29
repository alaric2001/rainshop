
CREATE TABLE `itembarang` (
  `item_id` varchar(36) NOT NULL,
  `item_name` varchar(200) NOT NULL,
  `item_price` float DEFAULT NULL,
  `item_stock` int(11) DEFAULT NULL,
  `isactive` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`item_id`),
  KEY `ix_itembarang_item_id` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `item_images` (
  `image_id` varchar(36) NOT NULL,
  `item_id` varchar(36) NOT NULL,
  `image_path` varchar(400) NOT NULL,
  `faiss_index` int(11) NOT NULL,
  PRIMARY KEY (`image_id`),
  UNIQUE KEY `faiss_IDX` (`faiss_index`) USING BTREE,
  KEY `item_id` (`item_id`),
  KEY `ix_item_images_image_id` (`image_id`),
  CONSTRAINT `item_images_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `itembarang` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


create or replace
algorithm = UNDEFINED view `rainshop`.`vw_itembarang` as
select
    `ib`.`item_id` as `item_id`,
    `ib`.`item_name` as `item_name`,
    `ib`.`item_price` as `item_price`,
    `ib`.`item_stock` as `item_stock`,
    `ib`.`isactive` as `isactive`,
    `im`.`faiss_index` as `faiss_index`
from
    (`rainshop`.`itembarang` `ib`
join `rainshop`.`item_images` `im` on
    (`ib`.`item_id` = `im`.`item_id`));