from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter
from backend_api.views.utils import (
    get_query_params,
    get_all_dates_in_month,
    handle_error,
)
from backend_api.models import Receipt
from datetime import date
from rest_framework.permissions import IsAuthenticated


@extend_schema(
    methods=["GET"],
    parameters=[
        OpenApiParameter(name="month", description="Wybrany miesiąc", required=True, type=int),
        OpenApiParameter(name="year", description="Wybrany rok", required=True, type=int),
    ],
    responses={
        200: {
            "type": "array",
            "example": [
                {"day": "2024-01-01", "expense": 5.0, "income": 0.0},
                {"day": "2024-01-02", "expense": 15.0, "income": 10.0},
                {"day": "2024-01-03", "expense": 25.0, "income": 20.0},
            ],
        }
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def fetch_line_sums(request):
    try:
        # Pobierz wymagane parametry miesiąca i roku
        params = get_query_params(request, "month", "year")
        selected_month = params["month"]
        selected_year = params["year"]

        # Pobierz aktualnie zalogowanego użytkownika
        current_user = request.user
    except ValueError as e:
        return handle_error(e, 400, "Niepoprawne parametry zapytania")

    try:
        # Lista wszystkich dni w miesiącu jako stringi
        all_dates = [
            d.isoformat() if isinstance(d, date) else str(d)
            for d in get_all_dates_in_month(selected_year, selected_month)
        ]

        # Inicjalizacja słowników sum dla każdego dnia
        daily_expense = {date: 0 for date in all_dates}
        daily_income = {date: 0 for date in all_dates}

        # Pobierz paragony, które zawierają itemy tego użytkownika
        receipts = Receipt.objects.filter(
            payment_date__month=selected_month,
            payment_date__year=selected_year,
            items__user=current_user,
        ).distinct()

        for receipt in receipts:
            for item in receipt.items.all():
                # Sprawdź, czy item należy do użytkownika
                if item.user == current_user:
                    value_per_owner = float(item.value)  # item ma 1 właściciela

                    payment_date_str = (
                        receipt.payment_date.isoformat()
                        if isinstance(receipt.payment_date, date)
                        else str(receipt.payment_date)
                    )

                    if receipt.transaction_type == "expense":
                        daily_expense[payment_date_str] += value_per_owner
                    elif receipt.transaction_type == "income":
                        daily_income[payment_date_str] += value_per_owner

        # Budujemy wynik z kumulacją
        results = []
        cumulative_expense = 0
        cumulative_income = 0

        for day_str in all_dates:
            cumulative_expense += daily_expense[day_str]
            cumulative_income += daily_income[day_str]
            results.append({
                "day": day_str,
                "expense": round(cumulative_expense, 2),
                "income": round(cumulative_income, 2),
            })

        return JsonResponse(results, safe=False, status=200)
    except Exception as e:
        return handle_error(e, 500, f"Błąd podczas przetwarzania danych: {str(e)}")
