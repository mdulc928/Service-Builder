CREATE DEFINER=`root`@`localhost` PROCEDURE `create_service`(IN service_datetime DATETIME, IN theme VARCHAR(0), in person_id int, in tmpltsvc_id int, out error_msg int)
begin
	declare chk_id int;
    declare svc_id int;
    select id, max(Service_ID) + 1 into chk_id, svc_id from service 
    where Svc_DateTime like service_datetime;
    
    if chk_id is not null then
		set error_msg = 1;
	else 
		INSERT INTO `wsoapp`.`service` (`Service_ID`, `Svc_DateTime`,`Theme_Event`)
		VALUES (id, service_datetime, theme);
        
        if person_id is not null then        
			insert into `wsoapp`.`fills_role` values(person_id, svc_id, 'S', 'Y');
        end if;
        
        if tmpltsvc_id is not null then
			insert into service_item
				select max(Service_Item_ID) + 1, Seq_Num, null, null, null, null, null, null, Event_Type_ID, svc_id
                from service_item where Service_ID = tmpltsvc_id;                
		end if;
        
        set error_msg = 0;
    end if;
    

	
end