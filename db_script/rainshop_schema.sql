-- ============================================================
--  Rainshop — Schema Lengkap (Fresh Install)
--  Gabungan semua script dari db_script/2025-07-29/ sampai 2025-08-07/
--  Jalankan file ini pada database MySQL yang masih kosong.
-- ============================================================

CREATE DATABASE IF NOT EXISTS `rainshop`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

USE `rainshop`;

-- ------------------------------------------------------------
-- 1. Tabel itembarang
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `itembarang` (
  `item_id`    varchar(36)   NOT NULL,
  `item_name`  varchar(200)  NOT NULL,
  `item_price` float         DEFAULT NULL,
  `item_stock` int(11)       DEFAULT NULL,
  `isactive`   tinyint(1)    DEFAULT NULL,
  `image_id`   varchar(100)  DEFAULT NULL,
  `modified`   datetime      DEFAULT NULL,
  PRIMARY KEY (`item_id`),
  KEY `ix_itembarang_item_id` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 2. Tabel item_images
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `item_images` (
  `image_id`    varchar(36)   NOT NULL,
  `item_id`     varchar(36)   NOT NULL,
  `image_path`  varchar(400)  NOT NULL,
  `faiss_index` int(11)       NOT NULL,
  `modified`    datetime      DEFAULT NULL,
  PRIMARY KEY (`image_id`),
  UNIQUE KEY `faiss_IDX` (`faiss_index`) USING BTREE,
  KEY `item_id` (`item_id`),
  KEY `ix_item_images_image_id` (`image_id`),
  CONSTRAINT `item_images_ibfk_1`
    FOREIGN KEY (`item_id`) REFERENCES `itembarang` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 3. Tabel sales_header
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `sales_header` (
  `sales_id`    varchar(36)   NOT NULL,
  `sales_time`  datetime      NOT NULL,
  `sales_no`    varchar(50)   DEFAULT 'TUNAI',
  `sales_total` float         DEFAULT NULL,
  `sales_paym`  varchar(20)   DEFAULT 'TUNAI',
  `totalitem`   varchar(200)  DEFAULT NULL,
  PRIMARY KEY (`sales_id`),
  UNIQUE KEY `ix_sales_no` (`sales_no`) USING BTREE,
  KEY `ix_tanggal` (`sales_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 4. Tabel sales_line
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `sales_line` (
  `sales_line_id` varchar(36) NOT NULL,
  `sales_id`      varchar(36) NOT NULL,
  `item_id`       varchar(36) NOT NULL,
  `item_price`    float       DEFAULT NULL,
  `qty`           int(11)     NOT NULL,
  `subtotal`      float       DEFAULT NULL,
  PRIMARY KEY (`sales_line_id`),
  KEY `sales_id` (`sales_id`),
  KEY `ix_item_id` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 5. View vw_itembarang  (versi final — 2025-08-07)
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW `vw_itembarang` AS
SELECT
  `ib`.`item_id`    AS `item_id`,
  `ib`.`item_name`  AS `item_name`,
  `ib`.`item_price` AS `item_price`,
  `ib`.`item_stock` AS `item_stock`,
  `ib`.`isactive`   AS `isactive`,
  `ib`.`modified`   AS `modified`,
  `im`.`faiss_index` AS `faiss_index`,
  `im`.`image_path`  AS `image_path`,
  `im`.`image_id`    AS `image_id`
FROM `itembarang` `ib`
JOIN `item_images` `im` ON `ib`.`item_id` = `im`.`item_id`;

-- ------------------------------------------------------------
-- 6. View vw_sales_line
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW `vw_sales_line` AS
SELECT
  `sl`.`sales_line_id` AS `sales_line_id`,
  `sl`.`sales_id`      AS `sales_id`,
  `sl`.`item_id`       AS `item_id`,
  `sl`.`item_price`    AS `item_price`,
  `sl`.`qty`           AS `qty`,
  `sl`.`subtotal`      AS `subtotal`,
  `ib`.`item_name`     AS `item_name`,
  `ib`.`item_price`    AS `item_price_skrg`,
  `ib`.`item_stock`    AS `item_stock`,
  `ib`.`isactive`      AS `isactive`,
  `ib`.`image_id`      AS `image_id`
FROM `sales_line` `sl`
JOIN `itembarang` `ib` ON `sl`.`item_id` = `ib`.`item_id`;

-- ------------------------------------------------------------
-- 7. Stored Procedure usp_sales_nomorbaru
-- ------------------------------------------------------------
DROP PROCEDURE IF EXISTS `usp_sales_nomorbaru`;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `usp_sales_nomorbaru`(
  p_sales_date DATE
)
BEGIN
  DECLARE p_sales_no  VARCHAR(50);
  DECLARE p_nomorMax  VARCHAR(10);
  DECLARE p_nomor     INT;

  SELECT IFNULL(MAX(SUBSTRING(sales_no, 9, 4)), '0000')
    INTO p_nomorMax
    FROM sales_header
   WHERE YEAR(sales_time)  = YEAR(p_sales_date)
     AND MONTH(sales_time) = MONTH(p_sales_date)
     AND sales_no LIKE CONCAT('S', DATE_FORMAT(p_sales_date, '%y%m'), '-%');

  SET p_nomorMax = REPLACE(p_nomorMax, '-', 0);
  SET p_nomor    = CONVERT(p_nomorMax, UNSIGNED INTEGER) + 1;
  SET p_sales_no = CONCAT('S', DATE_FORMAT(p_sales_date, '%y%m'), '-',
                          RIGHT(CONCAT('0000', p_nomor), 4));

  WHILE EXISTS (SELECT sales_no FROM sales_header WHERE sales_no = p_sales_no) DO
    SET p_nomor    = p_nomor + 1;
    SET p_sales_no = CONCAT('S', DATE_FORMAT(p_sales_date, '%y%m'), '-',
                            RIGHT(CONCAT('0000', p_nomor), 4));
  END WHILE;

  SELECT p_sales_no AS sales_no;
END$$
DELIMITER ;
