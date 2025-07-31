
drop table if exists `sales_header`;
CREATE TABLE `sales_header` (
  `sales_id` varchar(36) NOT NULL,
  `sales_time` datetime NOT NULL,
  `sales_no` varchar(50) DEFAULT 'TUNAI',
  `sales_total` float DEFAULT NULL,
  `sales_paym` varchar(20) DEFAULT 'TUNAI',
  `totalitem` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`sales_id`),
  UNIQUE KEY `ix_sales_no` (`sales_no`) USING BTREE,
  KEY `ix_tanggal` (`sales_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

drop table if exists `sales_line`;
CREATE TABLE `sales_line` (
  `sales_line_id` varchar(36) NOT NULL,
  `sales_id` varchar(36) NOT NULL,
  `item_id` varchar(36) NOT NULL,
  `item_price` float DEFAULT NULL,
  `qty` int(11) NOT NULL,
  `subtotal` float DEFAULT NULL,
  PRIMARY KEY (`sales_line_id`),
  KEY `sales_id` (`sales_id`),
  KEY `ix_item_id` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- rainshop.vw_sales_line source

create or replace
algorithm = UNDEFINED view `rainshop`.`vw_sales_line` as
select
    `sl`.`sales_line_id` as `sales_line_id`,
    `sl`.`sales_id` as `sales_id`,
    `sl`.`item_id` as `item_id`,
    `sl`.`item_price` as `item_price`,
    `sl`.`qty` as `qty`,
    `sl`.`subtotal` as `subtotal`,
    `ib`.`item_name` as `item_name`,
    `ib`.`item_price` as `item_price_skrg`,
    `ib`.`item_stock` as `item_stock`,
    `ib`.`isactive` as `isactive`, `ib`.`image_id`
from
    (`rainshop`.`sales_line` `sl`
join `rainshop`.`itembarang` `ib` on
    (`sl`.`item_id` = `ib`.`item_id`));