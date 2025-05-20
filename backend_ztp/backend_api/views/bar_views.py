# myapp/views/bar_views.py
from collections import defaultdict
from decimal import Decimal
from django.http import JsonResponse
from django.db.models import Sum, FloatField
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from backend_api.views.utils import (
    get_query_params,
    handle_error,
    get_top_outlier_receipts,
)
from backend_api.models import Receipt
from backend_api.serializers import PersonExpenseSerializer, ShopExpenseSerializer
from rest_framework.permissions import IsAuthenticated

@extend_schema(
    methods=["GET"],
    parameters=[
        OpenApiParameter(
            name="month", description="Selected month", required=True, type=int
        ),
        OpenApiParameter(
            name="year", description="Selected year", required=True, type=int
        ),
        OpenApiParameter(
            name="category[]",
            description="Selected categories",
            required=False,
            type=str,
            many=True,
            enum=[
                "fuel", "car_expenses", "fastfood", "alcohol", "food_drinks", "chemistry",
                "clothes", "electronics_games", "tickets_entrance", "delivery", "other_shopping",
                "flat_bills", "monthly_subscriptions", "other_cyclical_expenses", "investments_savings",
                "other", "for_study", "work_income", "family_income", "investments_income",
                "money_back", "last_month_balance"
            ],
        ),
    ],
    responses={
        200: ShopExpenseSerializer(many=True),
        400: OpenApiResponse(description="Bad request"),
        500: OpenApiResponse(description="Internal server error"),
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def fetch_bar_shops(request):
    try:
        # Pobierz miesiąc i rok z parametrów GET
        params = get_query_params(request, "month", "year")
        selected_month = params["month"]
        selected_year = params["year"]

        # Ustal aktualnego użytkownika
        current_user = request.user

        # Kategorie – domyślnie kilka najczęstszych
        category_param = request.GET.getlist("category[]")
        category = category_param or [
            "fuel", "car_expenses", "fastfood", "alcohol", "food_drinks", "chemistry",
            "clothes", "electronics_games", "tickets_entrance", "delivery", "other_shopping"
        ]
    except ValueError as e:
        return handle_error(e, 400, "Niepoprawne parametry zapytania")

    try:
        # Filtrowanie paragonów użytkownika
        queryset = (
            Receipt.objects.filter(
                transaction_type="expense",
                payment_date__year=selected_year,
                payment_date__month=selected_month,
                items__category__in=category,
                items__user=current_user,
            )
            .values("shop")
            .annotate(expense_sum=Sum("items__value", output_field=FloatField()))
        )

        sorted_expense_sums = queryset.order_by("-expense_sum")
        serialized_data = [
            {"shop": entry["shop"], "expense_sum": round(entry["expense_sum"], 2)}
            for entry in sorted_expense_sums
        ]

        serializer = ShopExpenseSerializer(data=serialized_data, many=True)
        if serializer.is_valid():
            return JsonResponse(serializer.data, safe=False, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)
    except Exception as e:
        return handle_error(e, 500, "Błąd podczas pobierania danych wydatków")
