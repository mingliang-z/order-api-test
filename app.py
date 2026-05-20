from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

app = FastAPI(title="订单管理系统")

class OrderItem(BaseModel):
    product_name: str = Field(..., description="商品名称")
    quantity: int = Field(..., gt=0, description="数量，必须大于0")
    unit_price: float = Field(..., gt=0, description="单价，必须大于0")

class CreateOrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=1, description="客户姓名")
    items: List[OrderItem] = Field(..., min_length=1, description="商品列表，至少一个")
    remark: Optional[str] = Field(None, max_length=200, description="备注，最多200字")

class OrderResponse(BaseModel):
    id: int
    customer_name: str
    items: List[OrderItem]
    total_price: float
    status: str
    remark: Optional[str] = None
    created_at: str

orders_db = {}
order_id_counter = 1

@app.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(request: CreateOrderRequest):
    global order_id_counter
    total_price = sum(item.quantity * item.unit_price for item in request.items)
    order = {
        "id": order_id_counter,
        "customer_name": request.customer_name,
        "items": [item.model_dump() for item in request.items],
        "total_price": round(total_price, 2),
        "status": "待处理",
        "remark": request.remark,
        "created_at": datetime.now().isoformat()
    }
    orders_db[order_id_counter] = order
    order_id_counter += 1
    return order

@app.get("/orders", response_model=List[OrderResponse])
def list_orders(
    status: Optional[str] = Query(None, description="按状态筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量")
):
    result = list(orders_db.values())
    if status:
        result = [o for o in result if o["status"] == status]
    start = (page - 1) * page_size
    end = start + page_size
    return result[start:end]

@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail=f"订单 {order_id} 不存在")
    return orders_db[order_id]

@app.patch("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    new_status: str = Query(..., description="新状态")
):
    valid_statuses = ["待处理", "处理中", "已发货", "已完成", "已取消"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=422,
            detail=f"无效状态。有效值: {', '.join(valid_statuses)}"
        )
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail=f"订单 {order_id} 不存在")
    orders_db[order_id]["status"] = new_status
    return {"order_id": order_id, "new_status": new_status, "message": "状态更新成功"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
