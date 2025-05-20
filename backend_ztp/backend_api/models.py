from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


# Model User (używamy wbudowanego modelu User z Django, ale możesz go dostosować)

# Model Item
class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    CATEGORY_CHOICES = [
        ("fuel", "Paliwo"),
        ("car_expenses", "Wydatki na samochód"),
        ("fastfood", "Fast Food"),
        ("alcohol", "Alkohol"),
        ("food_drinks", "Picie & jedzenie"),
        ("chemistry", "Chemia"),
        ("clothes", "Ubrania"),
        ("electronics_games", "Elektornika & gry"),
        ("tickets_entrance", "Bilety & wejściówki"),
        ("delivery", "Dostawa"),
        ("other_shopping", "Inne zakupy"),
        ("flat_bills", "Rachunki za mieszkanie"),
        ("monthly_subscriptions", "Miesięczne subskrypcje"),
        ("other_cyclical_expenses", "Inne cykliczne wydatki"),
        ("investments_savings", "Inwestycje & oszczędności"),
        ("other", "Inne"),
        ("for_study", "Na studia"),
        ("work_income", "Przychód z pracy"),
        ("family_income", "Przychód od rodziny"),
        ("investments_income", "Przychód z inwestycji"),
        ("money_back", "Zwrot pieniędzy"),
        ("last_month_balance", "Saldo z poprzedniego miesiąca"),
    ]

    save_date = models.DateField(auto_now_add=True, null=True)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True, default="")
    quantity = models.DecimalField(max_digits=10, decimal_places=0, default=1)
    # owners = models.JSONField(blank=False, default=list)
    owners = models.ManyToManyField(User, related_name="items")

    def __str__(self):
        return self.description


# Model Receipt
class Receipt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    TRANSACTION_CHOICES = [
        ("expense", "Expense"),
        ("income", "Income"),
    ]
    save_date = models.DateField(auto_now_add=True, null=True)
    payment_date = models.DateField()
    payer = models.ForeignKey(
        User,
        related_name="payer_receipts",
        on_delete=models.CASCADE,
    )

    shop = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=255, choices=TRANSACTION_CHOICES)
    items = models.ManyToManyField(Item, related_name="receipts")
    payment_date = models.DateField()

    def __str__(self):
        return f"Receipt {self.id}"


class RecentShop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    last_used = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name = self.name.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ItemPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_description = models.CharField(
        max_length=255, unique=True
    )  # Unique item descriptions
    frequency = models.PositiveIntegerField(
        default=0
    )  # Frequency of item occurrence in receipts

    def increment_frequency(self):
        """Increase the frequency of the item."""
        self.frequency += 1
        self.save()

    def __str__(self):
        return f"{self.item_description}: {self.frequency} times"
