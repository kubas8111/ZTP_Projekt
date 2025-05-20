from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from backend_api.models import Item, Receipt
from backend_api.serializers import ItemSerializer, ReceiptSerializer
from datetime import date


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username="testuser", password="testpass123")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpass123"))

    def test_create_superuser(self):
        admin = User.objects.create_superuser(username="admin", password="adminpass123")
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)


class ItemModelTest(TestCase):
    def test_create_item(self):
        user = User.objects.create_user(username="user2", password="pass")
        item = Item.objects.create(user=user, category="food_drinks", value=10.50)
        self.assertEqual(item.value, 10.50)
        self.assertEqual(item.user, user)


class ReceiptModelTest(TestCase):
    def test_create_receipt_and_items(self):
        user = User.objects.create_user(username="user3", password="pass")
        receipt = Receipt.objects.create(
            user=user,
            shop="Shell",
            transaction_type="expense",
            payment_date=date.today(),
        )
        item = Item.objects.create(user=user, category="fuel", value=100.00, receipt=receipt)
        self.assertIn(item, receipt.items.all())


def test_valid_item_serializer(self):
    user = User.objects.create_user(username="serializer_user", password="pass")
    data = {
        "category": "food_drinks",
        "value": 15.0,
        "description": "Apples",
        "quantity": 2,
    }
    serializer = ItemSerializer(
        data=data,
        context={"request": type("Request", (), {"user": user})()}
    )
    self.assertTrue(serializer.is_valid(), serializer.errors)



class ReceiptSerializerTest(TestCase):
    def test_valid_receipt_serializer(self):
        user = User.objects.create_user(username="serializer_user", password="pass")
        data = {
            "shop": "TestShop",
            "transaction_type": "expense",
            "payment_date": str(date.today()),
            "items": [
                {
                    "category": "food_drinks",
                    "value": 20.0,
                    "description": "Milk",
                    "quantity": 1
                }
            ]
        }
        serializer = ReceiptSerializer(data=data, context={"request": type("Request", (), {"user": user})()})
        self.assertTrue(serializer.is_valid(), serializer.errors)


class ApiViewsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apitestuser", password="pass")
        self.client.force_authenticate(user=self.user)

        self.receipt = Receipt.objects.create(
            user=self.user,
            shop="Biedronka",
            transaction_type="expense",
            payment_date=date(2025, 1, 10),
        )
        self.item = Item.objects.create(
            user=self.user,
            category="food_drinks",
            value=10.0,
            description="Juice",
            quantity=1,
            receipt=self.receipt,
        )

    def test_create_receipt(self):
        payload = {
            "shop": "Lidl",
            "transaction_type": "expense",
            "payment_date": str(date.today()),
            "items": [
                {
                    "category": "fastfood",
                    "value": 12.0,
                    "description": "Burger",
                    "quantity": 1
                }
            ]
        }
        response = self.client.post("/api/receipts/", payload, format="json")
        self.assertEqual(response.status_code, 201)

    def test_fetch_receipts(self):
        response = self.client.get("/api/receipts/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_fetch_bar_shops(self):
        response = self.client.get("/api/fetch/bar-shops/", {
            "month": 1,
            "year": 2025
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_fetch_line_sums(self):
        response = self.client.get("/api/fetch/line-sums/", {
            "month": 1,
            "year": 2025
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_fetch_pie_categories(self):
        response = self.client.get("/api/fetch/pie-categories/", {
            "month": 1,
            "year": 2025
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
