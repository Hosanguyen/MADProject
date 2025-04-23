from app.core.database import Database
from app.models.GPSDevice import GPSDevice

"""
class GPSDevice(BaseModel):
    id: str
    name: str
    latitude: float = -1.0
    longitude: float = -1.0
    status: str = "Connected"
    battery: str
    image_url: Optional[str] = None
    petid: str
"""

class GpsService:
    db = Database()
    table_name = "gps_device"
    
    @staticmethod
    async def create(gps_device: GPSDevice) -> bool:
        conn = await GpsService.db.acquire()
        query = f"INSERT INTO {GpsService.table_name} (id, name, latitude, longitude, status, battery, image_url, petid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (gps_device.id, gps_device.name, gps_device.latitude, gps_device.longitude, gps_device.status, gps_device.battery, gps_device.image_url, gps_device.petid)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                await conn.commit()
        except Exception as e:
            print(f"Error creating GPS device: {e}")
            return False
        finally:
            await GpsService.db.release(conn)
        return True
    
    @staticmethod
    async def update_location_and_battery(gps_device: GPSDevice) -> bool:
        conn = await GpsService.db.acquire()
        query = f"UPDATE {GpsService.table_name} SET latitude = %s, longitude = %s, battery = %s WHERE id = %s"
        values = (gps_device.latitude, gps_device.longitude, gps_device.battery, gps_device.id)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                await conn.commit()
        except Exception as e:
            print(f"Error updating GPS device location and battery: {e}")
            return False
        finally:
            await GpsService.db.release(conn)
        return True
    
    @staticmethod
    async def is_device_id_exists(device_id: str) -> bool:
        conn = await GpsService.db.acquire()
        query = f"SELECT id FROM {GpsService.table_name} WHERE id = %s"
        values = (device_id,)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                result = await cursor.fetchone()
                return result is not None
        except Exception as e:
            print(f"Error checking if device ID exists: {e}")
            return False
        finally:
            await GpsService.db.release(conn)
    
    @staticmethod
    async def get_gps_location_and_battery(device_id: str):
        conn = await GpsService.db.acquire()
        query = f"SELECT latitude, longitude, status, battery FROM {GpsService.table_name} WHERE id = %s"
        values = (device_id,)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                result = await cursor.fetchone()
                if result:
                    return {
                        "latitude": result[0],
                        "longitude": result[1],
                        "status": result[2],
                        "battery": result[3]
                    }
                return None
        except Exception as e:
            print(f"Error getting GPS device location and battery: {e}")
            return None
        finally:
            await GpsService.db.release(conn)

            