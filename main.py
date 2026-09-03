from fastapi import FastAPI
from pydantic import BaseModel
import uuid

app = FastAPI(title="Hubway Shipping API")

class RateRequest(BaseModel):
    city_from: str
    city_to: str
    weight: float

class ShipmentRequest(BaseModel):
    order_id: str
    customer_name: str
    customer_phone: str
    delivery_address: str
    city: str
    weight: float

class TrackRequest(BaseModel):
    tracking_number: str

class CancelRequest(BaseModel):
    tracking_number: str

@app.post("/calculate-rates")
def calculate_rates(data: RateRequest):
    base_rate = 25.0
    if data.weight > 15:
        base_rate += (data.weight - 15) * 2.0
    return {
        "success": True,
        "company_name": "Hubway Shipping",
        "cost": base_rate,
        "currency": "SAR",
        "estimated_days": "1-2 Business Days"
    }

@app.post("/create-shipment")
def create_shipment(data: ShipmentRequest):
    tracking_num = f"HUB-{uuid.uuid4().hex[:8].upper()}"
    return {
        "success": True,
        "tracking_number": tracking_num,
        "waybill_url": f"https://hubway-shipping-api.onrender.com/waybill/{tracking_num}",
        "status": "created"
    }

@app.post("/track-shipment")
def track_shipment(data: TrackRequest):
    return {
        "success": True,
        "tracking_number": data.tracking_number,
        "status": "out_for_delivery",
        "status_arabic": "جاري التوصيل مع مندوب Hubway"
    }

@app.post("/cancel-shipment")
def cancel_shipment(data: CancelRequest):
    return {
        "success": True,
        "tracking_number": data.tracking_number,
        "status": "cancelled"
    }
