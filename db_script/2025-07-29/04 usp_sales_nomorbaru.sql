
DROP PROCEDURE IF EXISTS `usp_sales_nomorbaru`;

DELIMITER $$
$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `usp_sales_nomorbaru`(
	p_sales_date date
)
BEGIN
  declare p_sales_no varchar(50);
  declare p_nomorMAx varchar(10)  ;
  declare p_nomor int  ;

		SELECT ifnull(max(substring(sales_no,9,4)),'0000') into p_nomorMAx FROM sales_header 
			where year(sales_time)=year(p_sales_date) and month(sales_time)=month(p_sales_date) 
		    and sales_no like concat('S',DATE_FORMAT(p_sales_date, '%y%m'),'-%');
		   
			set p_nomorMAx = replace (p_nomorMAx,'-',0);
			 set p_nomor = convert(p_nomorMAx,UNSIGNED INTEGER) + 1 ;           
		
		 set p_sales_no = concat('S',DATE_FORMAT(p_sales_date, '%y%m'),'-',right(concat('0000' ,p_nomor), 4))  ;
		
	    WHILE exists(select sales_no from sales_header where sales_no =p_sales_no ) DO
		 set p_Nomor = p_Nomor + 1 ;     
		 set p_sales_no = concat('S',DATE_FORMAT(p_sales_date, '%y%m'),'-',right(concat('0000' ,p_nomor), 4))  ;
    	END WHILE;
		
		 select p_sales_no as sales_no;
END$$
DELIMITER ;
call usp_sales_nomorbaru('2025-07-31')