

import requests



from config.config import config

class BaseAPI:
    def __init__(self):
        self.base_url = config.BASE_URL
        self.session = requests.Session()


    def get(self, path, **kwargs):
        response = self.session.get(self.base_url + path, timeout=config.TIMEOUT, **kwargs)
        return response


    def post(self, path, **kwargs):
        response = self.session.post(self.base_url + path, timeout=config.TIMEOUT, **kwargs)
        return response

    def patch(self, path, **kwargs):
        response = self.session.patch(self.base_url + path, timeout=config.TIMEOUT, **kwargs)
        return response



class OrderAPI(BaseAPI):

    def create_order(self, customer_name, items,remark=None):
        body = {
            "customer_name": customer_name,
            "items": items
        }
        if remark:
            body["remark"] = remark
        return self.post("/orders", json=body)


    def get_orders(self,status=None, page=1, page_size=10):
        params={"page": page, "page_size": page_size}
        #page和page_size是一个常值，意味这个参数必须要有值，可以将其放在初始化params中
        #status是一个空值，他需要传参，所以需要判断
        if status :
            params["status"] = status
        return self.get("/orders", params=params)


    def get_order_by_id(self,order_id):
        return self.get(f"/orders/{order_id}")


    def update_order_status(self,order_id,new_status):
        return self.patch(f"/orders/{order_id}/status", params={"new_status": new_status})
