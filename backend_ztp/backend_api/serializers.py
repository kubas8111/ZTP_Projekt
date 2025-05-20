from django.utils.timezone import now
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    Item,
    Receipt,
    RecentShop,
    ItemPrediction,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class PersonExpenseSerializer(serializers.Serializer):
    payer = serializers.IntegerField()
    expense_sum = serializers.FloatField()
    receipt_ids = serializers.ListField(child=serializers.IntegerField())
    top_outlier_receipts = serializers.ListField()

class ShopExpenseSerializer(serializers.Serializer):
    shop = serializers.CharField()
    expense_sum = serializers.FloatField()

class ItemSerializer(serializers.ModelSerializer):
    owners = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all()
    )

    class Meta:
        model = Item
        fields = [
            "id",
            "save_date",
            "category",
            "value",
            "description",
            "quantity",
            "owners",
        ]

    def create(self, validated_data):
        owners_data = validated_data.pop("owners", [])
        item = Item.objects.create(**validated_data)
        item.owners.set(owners_data)
        return item

    def update(self, instance, validated_data):
        owners_data = validated_data.pop("owners", [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.owners.set(owners_data)
        return instance


class ReceiptSerializer(serializers.ModelSerializer):
    payer = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    items = ItemSerializer(many=True)

    class Meta:
        model = Receipt
        fields = [
            "id",
            "save_date",
            "payment_date",
            "payer",
            "shop",
            "transaction_type",
            "items",
        ]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        user = self.context["request"].user
        receipt = Receipt.objects.create(user=user, **validated_data)   

        shop_name = validated_data.get("shop", "").strip().lower()
        if shop_name:
            recent_shop, created = RecentShop.objects.get_or_create(
                user=self.context["request"].user,
                name=shop_name
            )
            if not created:
                recent_shop.last_used = now()
                recent_shop.save()

        for item_data in items_data:
            item_data["owners"] = [
                owner.id if isinstance(owner, User) else owner
                for owner in item_data.get("owners", [])
            ]
            item_serializer = ItemSerializer(data=item_data)
            item_serializer.is_valid(raise_exception=True)
            item = item_serializer.save()
            receipt.items.add(item)

        return receipt

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.items.clear()

        for item_data in items_data:
            item_data["owners"] = [
                owner.id if hasattr(owner, "id") else owner
                for owner in item_data.get("owners", [])
            ]
            item_serializer = ItemSerializer(data=item_data)
            item_serializer.is_valid(raise_exception=True)
            item = item_serializer.save()
            instance.items.add(item)

        return instance

    def update_item_prediction(self, item, shop_name):
        """
        Aktualizuje model ItemPrediction z danymi przedmiotu z paragonu.
        """
        item_description = item.description.strip().lower()
        if not item_description:
            return

        # Pobierz lub utwórz predykcję na podstawie opisu przedmiotu
        prediction, created = ItemPrediction.objects.get_or_create(
            item_description=item_description
        )

        # Zwiększ częstotliwość, jeśli predykcja już istnieje
        if not created:
            prediction.frequency += 1
        else:
            prediction.frequency = 1  # Ustaw początkową wartość częstotliwości

        prediction.save()


class ItemPredictionSerializer(serializers.ModelSerializer):
    item_description = serializers.CharField(source="item.description", read_only=True)
    shop_name = serializers.CharField(source="shop.name", read_only=True)

    class Meta:
        model = ItemPrediction
        fields = [
            "id",
            "item",
            "item_description",
            "shop",
            "shop_name",
            "frequency",
        ]


class UserExpenseSerializer(serializers.Serializer):
    payer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    expense_sum = serializers.FloatField()

    class Meta:
        fields = ["payer", "expense_sum"]


class ShopExpenseSerializer(serializers.Serializer):
    shop = serializers.CharField()
    expense_sum = serializers.FloatField()

    class Meta:
        fields = ["shop", "expense_sum"]


class CategoryPieExpenseSerializer(serializers.Serializer):
    category = serializers.CharField(source="transactions__category")
    expense_sum = serializers.FloatField()
    fill = serializers.CharField()

    class Meta:
        fields = ["category", "expense_sum", "fill"]
