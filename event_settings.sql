use mad;
SET GLOBAL event_scheduler = ON;

DELIMITER $$

CREATE EVENT IF NOT EXISTS update_gps_status_disconnected
ON SCHEDULE EVERY 1 MINUTE
DO
BEGIN
  UPDATE gps_device
  SET status = 'Disconnected'
  WHERE updated_at < NOW() - INTERVAL 5 MINUTE
    AND status != 'Disconnected';
END$$

DELIMITER ;
