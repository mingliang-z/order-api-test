import pytest
import allure
from api.order_api import OrderAPI
from data.data_loader import load_test_data


@allure.feature("订单管理")
class TestCreateOrder:
    def setup_class(self):
        self.api = OrderAPI()


    test_data =load_test_data("test_data.json")
    success_cases = test_data["create_order_success"]
    fail_cases = test_data["create_order_missing_fields"]

    @allure.story("正向用例")
    @allure.title("创建订单- {order[customer_name]}")
    @pytest.mark.parametrize("order", success_cases)
    def test_create_order_success(self,order):
        with allure.step("创建订单"):
            response = self.api.create_order(
                customer_name=order["customer_name"],
                items= order["items"]
            )

        with allure.step("验证结果"):
            assert response.status_code == 201, \
                f"期望状态码 201，实际 {response.status_code}"
            data = response.json()
            assert data["customer_name"] == order["customer_name"]
            assert data["total_price"] == order["expected_total_price"]

    @allure.story("反向用例")
    @allure.title("创建异常订- {order[customer_name]}单")
    @pytest.mark.parametrize("order", fail_cases)
    def test_create_order_empty_customer(self,order):
        with allure.step("创建订单"):
            response = self.api.create_order(
                customer_name=order["customer_name"],
                items= order["items"],
                remark = order.get("remark")
            )
        with allure.step("验证结果"):
            assert response.status_code == 422, \
                f"期望状态码 422，实际 {response.status_code}"


    @allure.story("反向用例")
    @allure.title("查询不存在的订单")
    def test_get_order_not_found(self):
        with allure.step("查询不存在的订单"):
            response = self.api.get_order_by_id(999999)
        with allure.step("验证结果"):
            assert response.status_code == 404, \
                f"期望状态码 404，实际 {response.status_code}"

    @allure.story("正向用例")
    @allure.title("更新订单状态为有效值")
    def test_update_order_status_success(self):
        with allure.step("先创建一个订单"):
            create_resp = self.api.create_order("测试", [
                {"product_name": "test", "quantity": 1, "unit_price": 1.00}
            ])
            order_id = create_resp.json()["id"]

        with allure.step("更新状态为'已发货'"):
            response = self.api.update_order_status(order_id, "已发货")
            assert response.status_code == 200, \
                f"期望状态码 200，实际 {response.status_code}"

    @allure.story("反向用例")
    @allure.title("更新订单状态为无效值")
    def test_update_order_invalid_status(self):
        with allure.step("先创建一个订单"):
            create_resp = self.api.create_order("测试", [
                {"product_name": "test", "quantity": 1, "unit_price": 1.00}
            ])
            order_id = create_resp.json()["id"]

        with allure.step("更新状态为无效值"):
            response = self.api.update_order_status(order_id, "不存在的状态")
            assert response.status_code == 422, \
                f"期望状态码 422，实际 {response.status_code}"