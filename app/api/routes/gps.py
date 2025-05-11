from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional
from app.services.GpsService import GpsService
from app.models.GPSDevice import GPSDevice
import json
import asyncio

router = APIRouter(tags=["gps"])

# Lưu trữ kết nối WebSocket tới client
connected_clients: Dict[str, List[WebSocket]] = {}

# API endpoint hiện tại để tạo thiết bị GPS
@router.post("/gps")
async def create_gps_device(gps_device: GPSDevice):
    try:
        is_created = await GpsService.create(gps_device)
        if is_created:
            return {"message": "Created successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to create GPS device")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# API endpoint hiện tại để cập nhật vị trí và pin của thiết bị GPS
@router.put("/gps/update_location_and_battery")
async def update_gps_device_location_and_battery(request: Request):
    print("Received update request")
    data = await request.json()
    print(f"Received data: {data}")
    
    required_fields = ['deviceId', 'latitude', 'longitude']
    for field in required_fields:
        if field not in data:
            raise HTTPException(status_code=400, detail=f"Missing field: {field}")
    
    battery_level = data.get('batteryLevel', -1)
    device_id = data['deviceId']
    latitude = float(data['latitude'])
    longitude = float(data['longitude'])
    
    print(f"Received update for device {device_id}: latitude={latitude}, longitude={longitude}, batteryLevel={battery_level}")
    
    gps_device = GPSDevice(id=device_id, latitude=latitude, longitude=longitude, battery=int(battery_level), status="Connected")
    
    is_gps_device_exists = await GpsService.is_device_id_exists(device_id)
    if not is_gps_device_exists:
        raise HTTPException(status_code=404, detail="GPS device not found")
    
    try:
        is_updated = await GpsService.update_location_and_battery(gps_device)
        if is_updated:
            # Gửi cập nhật thông qua WebSocket cho các client đăng ký
            await broadcast_device_update(device_id, {
                "deviceId": device_id,
                "latitude": latitude,
                "longitude": longitude,
                "batteryLevel": battery_level
            })
            return {"message": "Updated successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to update GPS device")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# API endpoint hiện tại để lấy thông tin vị trí và pin của thiết bị GPS
@router.get("/gps/{device_id}")
async def get_gps_location_and_battery(device_id: str):
    try:
        gps_device = await GpsService.get_gps_location_and_battery(device_id)
        if gps_device:
            return gps_device
        else:
            raise HTTPException(status_code=404, detail="GPS device not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint WebSocket cho kết nối từ thiết bị GPS
@router.websocket("/ws/gps-device/{device_id}")
async def gps_device_websocket(websocket: WebSocket, device_id: str):
    await websocket.accept()
    
    # Kiểm tra xem thiết bị có tồn tại không
    is_device_exists = await GpsService.is_device_id_exists(device_id)
    if not is_device_exists:
        await websocket.close(code=1000, reason="Device not found")
        return
    
    try:
        while True:
            # Nhận dữ liệu từ thiết bị GPS
            data = await websocket.receive_json()
            
            required_fields = ['latitude', 'longitude']
            if not all(field in data for field in required_fields):
                await websocket.send_json({"error": "Missing required fields"})
                continue
            
            battery_level = data.get('batteryLevel', -1)
            latitude = data['latitude']
            longitude = data['longitude']
            
            gps_device = GPSDevice(
                id=device_id, 
                latitude=latitude, 
                longitude=longitude, 
                battery=int(battery_level)
            )
            
            # Cập nhật vị trí và pin trong cơ sở dữ liệu
            is_updated = await GpsService.update_location_and_battery(gps_device)
            
            if is_updated:
                # Gửi cập nhật cho tất cả client đang theo dõi thiết bị này
                await broadcast_device_update(device_id, {
                    "deviceId": device_id,
                    "latitude": latitude,
                    "longitude": longitude,
                    "batteryLevel": battery_level
                })
                await websocket.send_json({"status": "success"})
            else:
                await websocket.send_json({"status": "failed", "error": "Failed to update location"})
                
    except WebSocketDisconnect:
        print(f"GPS device {device_id} disconnected")
    except Exception as e:
        print(f"Error with GPS device {device_id}: {str(e)}")
        await websocket.close(code=1000)

# Endpoint WebSocket cho client muốn theo dõi vị trí của thiết bị GPS
@router.websocket("/ws/client/{client_id}/device/{device_id}")
async def client_websocket(websocket: WebSocket, client_id: str, device_id: str):
    await websocket.accept()
    
    # Kiểm tra xem thiết bị có tồn tại không
    is_device_exists = await GpsService.is_device_id_exists(device_id)
    if not is_device_exists:
        await websocket.close(code=1000, reason="Device not found")
        return
    
    # Lưu kết nối WebSocket của client
    if device_id not in connected_clients:
        connected_clients[device_id] = []
    connected_clients[device_id].append(websocket)
    
    try:
        # Gửi vị trí hiện tại ngay khi kết nối
        gps_device = await GpsService.get_gps_location_and_battery(device_id)
        if gps_device:
            await websocket.send_json({
                "deviceId": device_id,
                "latitude": gps_device.latitude,
                "longitude": gps_device.longitude,
                "batteryLevel": gps_device.battery,
                "timestamp": gps_device.timestamp.isoformat() if hasattr(gps_device, 'timestamp') else None
            })
        
        # Giữ kết nối mở và đợi tin nhắn từ client (nếu cần)
        while True:
            message = await websocket.receive_text()
            # Xử lý tin nhắn từ client (nếu cần)
            
    except WebSocketDisconnect:
        # Xóa kết nối khi client ngắt kết nối
        if device_id in connected_clients and websocket in connected_clients[device_id]:
            connected_clients[device_id].remove(websocket)
            if not connected_clients[device_id]:
                del connected_clients[device_id]
    except Exception as e:
        print(f"Error with client {client_id} for device {device_id}: {str(e)}")
        # Xóa kết nối khi có lỗi
        if device_id in connected_clients and websocket in connected_clients[device_id]:
            connected_clients[device_id].remove(websocket)
            if not connected_clients[device_id]:
                del connected_clients[device_id]

# Hàm để gửi cập nhật đến tất cả client đang theo dõi một thiết bị cụ thể
async def broadcast_device_update(device_id: str, data: dict):
    if device_id in connected_clients:
        disconnected_clients = []
        for client in connected_clients[device_id]:
            try:
                await client.send_json(data)
            except Exception:
                disconnected_clients.append(client)
        
        # Xóa các client đã ngắt kết nối
        for client in disconnected_clients:
            connected_clients[device_id].remove(client)
        
        if not connected_clients[device_id]:
            del connected_clients[device_id]