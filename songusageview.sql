CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `songusageview` AS
    SELECT 
        `song`.`Song_ID` AS `Song_ID`,
        `song`.`Song_Type` AS `Song_Type`,
        `song`.`Title` AS `Title`,
        `song`.`Hymnbook_Num` AS `Hymnbook_Num`,
        `song`.`Arranger` AS `Arranger`,
        MAX(`service`.`Svc_DateTime`) AS `LastUsedDate`
    FROM
        ((`song`
        LEFT JOIN `service_item` ON ((`song`.`Song_ID` = `service_item`.`Song_ID`)))
        LEFT JOIN `service` ON ((`service`.`Service_ID` = `service_item`.`Service_ID`)))
    WHERE
        (`song`.`Song_Type` <> 'C')
    GROUP BY `song`.`Song_ID` , `song`.`Song_Type` , `song`.`Title` , `song`.`Hymnbook_Num` , `song`.`Arranger`
    ORDER BY `LastUsedDate` , `song`.`Title`