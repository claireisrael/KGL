from django.db import models
from django.utils import timezone

# This model represents the stock available in the grocery store
class Stock(models.Model):
    branch = [('Matugga', 'Matugga'), ('Mukono', 'Mukono')]
    stock_name = models.CharField(max_length=50, null=False, blank=False)  # Name of the stock item
    total_quantity = models.IntegerField(default=0, null=True, blank=True)  # Total quantity of the stock
    issued_quantity = models.IntegerField(default=0, null=True, blank=True)  # Quantity issued from the stock
    unit_price = models.IntegerField(default=0, null=False, blank=False)  # Price per unit of the stock item
    stock_branch = models.CharField(max_length=50, null=False, blank=False, choices=branch)  # Branch where the stock is located

    def __str__(self):
        return self.stock_name  # Display the stock name when the object is printed

# This model represents a sale transaction in the grocery store
class Sale(models.Model):
    item = models.ForeignKey(Stock, on_delete=models.CASCADE)  # Reference to the Stock item being sold
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Quantity sold
    amount_received = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False, blank=False)  # Amount of money received for the sale
    issued_to = models.CharField(max_length=50, null=True)  # Person the stock is issued to
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)  # Unit price at the time of sale
    recieved_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)  # Quantity received in the sale
    date = models.DateField(default=timezone.now)  # Date of the sale
    created_at = models.DateTimeField(default=timezone.now, editable=False) 
    sale_type = models.CharField(choices=[("cash", "cash"), ("Credit", "Credit")], max_length=50, default="Cash")
    
    
    def get_total(self):
        total = self.quantity * self.item.unit_price
        return int(total)


    def get_change(self):
        change = self.get_total() - self.amount_received
        return abs(int(change))
    
     # Timestamp when the sale was created
