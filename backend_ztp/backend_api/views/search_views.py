# myapp/views/search_views.py
from collections import defaultdict
from django.http import JsonResponse
from django.utils.timezone import now
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework.views import APIView
from backend_api.models import RecentShop, Receipt, ItemPrediction
from rest_framework.permissions import IsAuthenticated

class RecentShopSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "").strip()
        if not query:
            shops = RecentShop.objects.filter(user=request.user).order_by("name")
            results = [
                {"id": shop.id, "name": shop.name.capitalize()} for shop in shops
            ]
            return JsonResponse({"results": results})

        if len(query) < 3:
            return JsonResponse({"results": []})

        shops = RecentShop.objects.filter(user=request.user, name__icontains=query).order_by("-last_used")[:10]
        results = [{"id": shop.id, "name": shop.name.capitalize()} for shop in shops]

        return JsonResponse({"results": results})

    @staticmethod
    def scan_and_update_shops(user, new_shops=None):
        receipt_shops = Receipt.objects.filter(user=user).values_list("shop", flat=True)
        all_shops = set(shop.strip().lower() for shop in receipt_shops if shop)
        if new_shops:
            all_shops.update(shop.strip().lower() for shop in new_shops)
        for shop in all_shops:
            RecentShop.objects.update_or_create(
                user=user, name=shop, defaults={"last_used": now()}
            )
        return all_shops

    def post(self, request, *args, **kwargs):
        new_shops = request.data.get("new_shops", [])
        if not isinstance(new_shops, list):
            return JsonResponse(
                {"error": "Invalid data format. Provide a list."}, status=400
            )
        updated_shops = self.scan_and_update_shops(request.user, new_shops)
        return JsonResponse(
            {
                "message": "Shops updated successfully.",
                "updated_shops": list(updated_shops),
            }
        )

    def delete(self, request, *args, **kwargs):
        RecentShop.objects.filter(user=request.user).delete()
        return JsonResponse({"message": "All recent shops have been deleted."})


class ItemPredictionSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "").strip().lower()
        predictions = ItemPrediction.objects.filter(user=request.user)
        if query:
            if len(query) < 3:
                return JsonResponse({"results": []})
            predictions = predictions.filter(item_description__icontains=query)
        predictions = predictions.values("item_description", "frequency").order_by(
            "-frequency" if query else "item_description"
        )
        results = [
            {
                "name": prediction["item_description"].capitalize(),
                "frequency": prediction["frequency"],
            }
            for prediction in predictions
        ]
        return JsonResponse({"results": results})

    @staticmethod
    def scan_and_update_predictions(user):
        receipts = Receipt.objects.filter(user=user).prefetch_related("items").all()
        frequency_map = defaultdict(int)
        for receipt in receipts:
            for item in receipt.items.all():
                item_description = item.description.strip().lower()
                if not item_description:
                    continue
                frequency_map[item_description] += 1
        for item_description, frequency in frequency_map.items():
            prediction, created = ItemPrediction.objects.get_or_create(
                user=user, item_description=item_description
            )
            prediction.frequency = frequency
            prediction.save()
        return "ItemPrediction table updated."

    def post(self, request, *args, **kwargs):
        result = self.scan_and_update_predictions(request.user)
        return JsonResponse({"message": result})

    def delete(self, request, *args, **kwargs):
        ItemPrediction.objects.filter(user=request.user).delete()
        return JsonResponse({"message": "All predictions have been deleted."})
