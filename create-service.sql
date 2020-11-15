CREATE DEFINER=`root`@`localhost` PROCEDURE `create_service`(IN service_datetime DATETIME, IN theme VARCHAR(40), in person_id int, in tmpltsvc_id int, out error_msg int, out newsvc_id int)
begin
	declare chk_id int;    
    declare svc_id int;
    declare newitem_id int;
    
SELECT 
    Service_ID
INTO chk_id FROM
    service
WHERE
    Svc_DateTime = service_datetime;
    
    if chk_id is not null then
		set error_msg = 1;
	else 
		select max(Service_ID) + 1 into svc_id from service;
        
		INSERT INTO `wsoapp2`.`service` (`Service_ID`, `Svc_DateTime`,`Theme_Event`)
		VALUES (svc_id, service_datetime, theme);
        
        if person_id is not null then        
			insert into `wsoapp2`.`fills_role`(`Person_ID`,`Service_ID`,`Role_Type`,`Confirmed`)
            values(person_id, svc_id, 'S', 'Y');
        end if;
        
        if tmpltsvc_id is not null then
			select max(Service_Item_ID) into newitem_id from service_item;
			
			insert into service_item
				select @newitem_id + 1, svc_id, Seq_Num, Event_Type_ID, null, null, Confirmed, null, null, null
                from service_item where Service_ID = tmpltsvc_id;                
		end if;
        
        set newsvc_id = svc_id;
        set error_msg = 0;
    end if;
end