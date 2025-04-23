use mad;

DELIMITER //

CREATE TRIGGER trg_update_gps_device
BEFORE UPDATE ON gps_device
FOR EACH ROW
BEGIN
   SET NEW.updated_at = CURRENT_TIMESTAMP;
END;
//

DELIMITER ;