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
        self.assertFalse(user.is_staff)  # Domyślnie False

    def test_create_superuser(self):
        admin = User.objects.create_superuser(username="admin", password="adminpass123")
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)


class ItemModelTest(TestCase):
    def test_create_item_with_owner(self):
        user = User.objects.create_user(username="user2", password="pass")
        item = Item.objects.create(user=user, category="food_drinks", value=10.50)
        item.owners.add(user)
        self.assertEqual(item.value, 10.50)
        self.assertIn(user, item.owners.all())


class ReceiptModelTest(TestCase):
    def test_create_receipt(self):
        user = User.objects.create_user(username="user3", password="pass")
        item = Item.objects.create(user=user, category="fuel", value=100.00)
        receipt = Receipt.objects.create(
            user=user,
            shop="Shell",
            transaction_type="expense",
            payment_date=date.today(),
            payer=user
        )
        receipt.items.add(item)
        self.assertEqual(receipt.shop, "Shell")
        self.assertIn(item, receipt.items.all())


class ItemSerializerTest(TestCase):
    def test_valid_data(self):
        user = User.objects.create_user(username="serializer_user", password="pass")
        data = {
            "category": "food_drinks",
            "value": 15.0,
            "description": "Apples",
            "quantity": 2,
            "owners": [user.id],
        }
        serializer = ItemSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_data(self):
        serializer = ItemSerializer(data={"category": "", "value": "abc"})
        self.assertFalse(serializer.is_valid())


class ReceiptSerializerTest(TestCase):
    def test_serializer_with_valid_data(self):
        user = User.objects.create_user(username="receipt_user", password="pass")
        data = {
            "shop": "TestShop",
            "transaction_type": "expense",
            "payment_date": str(date.today()),
            "payer": user.id,
            "items": [],
        }
        serializer = ReceiptSerializer(
            data=data, context={"request": type("Request", (), {"user": user})()}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)


class BarViewsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="baruser", password="123")
        self.client.force_authenticate(user=self.user)

        # Dodaj przedmiot i przypisz właściciela
        self.item = Item.objects.create(
            user=self.user,
            category="food_drinks",
            value=100,
            description="Groceries",
            quantity=1,
        )
        self.item.owners.add(self.user)

        # Dodaj paragon z self.user jako payer
        self.receipt = Receipt.objects.create(
            user=self.user,
            shop="ShopX",
            transaction_type="expense",
            payment_date=date(2025, 1, 15),
            payer=self.user
        )
        self.receipt.items.add(self.item)

    def test_bar_expenses_endpoint(self):
        response = self.client.get("/api/fetch/bar-persons/", {
            "month": 1,
            "year": 2025
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("shared_expenses", response.json())

    def test_bar_shops_endpoint(self):
        response = self.client.get("/api/fetch/bar-shops/", {
            "month": 1,
            "year": 2025,
            "owners[]": [self.user.id]
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)


class ReceiptApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apitestuser", password="pass")
        self.client.force_authenticate(user=self.user)

    def test_create_receipt(self):
        payload = {
            "shop": "Biedronka",
            "transaction_type": "expense",
            "payment_date": str(date.today()),
            "payer": self.user.id,
            "items": []
        }
        response = self.client.post("/api/receipts/", payload, format="json")
        self.assertEqual(response.status_code, 201)

    def test_get_receipts(self):
        response = self.client.get("/api/receipts/")
        self.assertEqual(response.status_code, 200)
