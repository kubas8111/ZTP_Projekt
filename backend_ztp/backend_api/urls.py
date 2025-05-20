from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from backend_api.views import (
    ItemViewSet,
    ReceiptListCreateView,
    ReceiptUpdateDestroyView,
    RecentShopSearchView,
    ItemPredictionSearchView,
    fetch_line_sums,
    fetch_bar_shops,
    fetch_pie_categories,
    DuplicateReceiptDebugView
)

router = DefaultRouter()

router.register(r"items", ItemViewSet)
# router.register(r"receipts", ReceiptViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("receipts/", ReceiptListCreateView.as_view(), name="receipt-create"),
    path(
        "receipts/<int:pk>/", ReceiptUpdateDestroyView.as_view(), name="receipt-update"
    ),
    path("recent-shops/", RecentShopSearchView.as_view(), name="recent-shop-search"),
    path(
        "item-predictions/",
        ItemPredictionSearchView.as_view(),
        name="item-predictions",
    ),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("fetch/line-sums/", fetch_line_sums, name="fetch-line-sums"),
    path("fetch/bar-shops/", fetch_bar_shops, name="fetch-bar-shops"),
    path("fetch/pie-categories/", fetch_pie_categories, name="fetch-pie-categories"),
    path('debug/receipts/duplicates/', DuplicateReceiptDebugView.as_view(), name='receipt-duplicates-debug'),
]
