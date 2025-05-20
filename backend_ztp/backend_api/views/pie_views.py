from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from django.db.models import Sum
from django.core.exceptions import ValidationError
from backend_api.views.utils import get_query_params, handle_error
from backend_api.models import Receipt
from backend_api.serializers import CategoryPieExpenseSerializer
from rest_framework.permissions import IsAuthenticated

@extend_schema(
    methods=["GET"],
    parameters=[
        OpenApiParameter(
            name="month", description="Wybrany miesiąc", required=True, type=int
        ),
        OpenApiParameter(
            name="year", description="Wybrany rok", required=True, type=int
        ),
    ],
    responses={
        200: CategoryPieExpenseSerializer(many=True),
        400: OpenApiResponse(description="Bad request"),
        500: OpenApiResponse(description="Internal server error"),
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def fetch_pie_categories(request):
    try:
        # Parametry miesiąca i roku
        params = get_query_params(request, "month", "year")
        selected_month = params["month"]
        selected_year = params["year"]

        # Filtrowanie paragonów użytkownika (uwzględnia tylko itemy usera)
        receipts = Receipt.objects.filter(
            transaction_type="expense",
            payment_date__month=selected_month,
            payment_date__year=selected_year,
            items__user=request.user,
        ).distinct()

        # Pobieranie elementów powiązanych z paragonami
        from backend_api.models import Item  # Dostosuj import do struktury projektu

        item_qs = Item.objects.filter(receipt__in=receipts).distinct()

        # Agregacja według kategorii
        category_totals = {}
        for item in item_qs:
            if item.user == request.user:
                category_totals[item.category] = category_totals.get(item.category, 0) + float(item.value)

        # Lista wyników
        aggregated_data = [
            {
                "category": category,
                "expense_sum": round(total, 2),
                "fill": f"var(--color-{category})",
            }
            for category, total in category_totals.items()
        ]
        aggregated_data.sort(key=lambda x: x["category"])

        serializer = CategoryPieExpenseSerializer(data=aggregated_data, many=True)
        if serializer.is_valid():
            return JsonResponse(serializer.data, safe=False, status=200)
        else:
            return JsonResponse(serializer.errors, safe=False, status=400)

    except ValidationError as e:
        return handle_error(e, 400, "Invalid category")
    except Exception as e:
        return handle_error(e, 500, "Error while fetching pie categories")
