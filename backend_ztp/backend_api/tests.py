
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from backend_api.models import (
    Person, Item, Receipt, RecentShop, ItemPrediction,
    Wallet, WalletSnapshot, Invest, Instrument
)
from backend_api.serializers import ItemSerializer, ReceiptSerializer
from django.utils import timezone
from datetime import date


class PersonModelTest(TestCase):
    def test_create_person(self):
        user = User.objects.create_user(username="user1", password="pass")
        person = Person.objects.create(user=user, name="Adam", payer=True, owner=False)
        self.assertEqual(str(person), "Adam")
        self.assertTrue(person.payer)
        self.assertFalse(person.owner)


class ItemModelTest(TestCase):
    def test_create_item(self):
        user = User.objects.create_user(username="user2", password="pass")
        person = Person.objects.create(user=user, name="Basia", payer=True)
        item = Item.objects.create(user=user, category="food_drinks", value=10.50)
        item.owners.add(person)
        self.assertEqual(item.value, 10.50)
        self.assertIn(person, item.owners.all())


class ReceiptModelTest(TestCase):
    def test_create_receipt(self):
        user = User.objects.create_user(username="user3", password="pass")
        person = Person.objects.create(user=user, name="Payer", payer=True)
        item = Item.objects.create(user=user, category="fuel", value=100.00)
        receipt = Receipt.objects.create(
            user=user,
            shop="Shell",
            transaction_type="expense",
            payment_date=date.today(),
            payer=person
        )
        receipt.items.add(item)
        self.assertEqual(receipt.shop, "Shell")
        self.assertIn(item, receipt.items.all())


class ItemSerializerTest(TestCase):
    def test_valid_data(self):
        user = User.objects.create_user(username="serializer_user", password="pass")
        person = Person.objects.create(user=user, name="Owner", payer=True)
        data = {
            "category": "food_drinks",
            "value": 15.0,
            "user": user.id,
            "owners": [person.id]
        }
        serializer = ItemSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_data(self):
        serializer = ItemSerializer(data={"category": "", "value": "abc"})
        self.assertFalse(serializer.is_valid())


class ReceiptSerializerTest(TestCase):
    def test_serializer_with_valid_data(self):
        user = User.objects.create_user(username="receipt_user", password="pass")
        person = Person.objects.create(user=user, name="Test Payer", payer=True)
        data = {
            "user": user.id,
            "shop": "TestShop",
            "transaction_type": "expense",
            "payment_date": str(date.today()),
            "payer": person.id,
            "items": []
        }
        serializer = ReceiptSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)


class BarViewsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="baruser", password="123")
        self.client.force_authenticate(user=self.user)

        self.person = Person.objects.create(user=self.user, name="Jan", payer=True)
        self.wallet = Wallet.objects.create(user=self.user, name="Main Wallet")

        # Dodaj paragon
        self.item = Item.objects.create(
            user=self.user,
            category="food_drinks",
            value=100,
        )
        self.item.owners.add(self.person)

        self.receipt = Receipt.objects.create(
            user=self.user,
            shop="ShopX",
            transaction_type="expense",
            payment_date=date(2025, 1, 15),
            payer=self.person
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
            "owners[]": [self.person.id]
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

class ReceiptApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apitestuser", password="pass")
        self.client.force_authenticate(user=self.user)
        self.person = Person.objects.create(user=self.user, name="Payer", payer=True)

    def test_create_receipt(self):
        payload = {
            "shop": "Biedronka",
            "transaction_type": "expense",
            "payment_date": str(date.today()),
            "payer": self.person.id,
            "items": []
        }
        response = self.client.post("/api/receipts/", payload, format="json")
        self.assertEqual(response.status_code, 201)

    def test_get_receipts(self):
        response = self.client.get("/api/receipts/")
        self.assertEqual(response.status_code, 200)
