from django.shortcuts import render, redirect
from django.contrib.auth import login, logout  # Import login and logout functions
from .forms import SaleForm, AddForm  # Import forms used in views
from .forms import *  # Import all forms (generally, this is not recommended; import only what you need)
from django.http import HttpResponse, HttpResponseRedirect  # Import HTTP response classes
from django.urls import reverse  # Import reverse function for URL resolution
from django.contrib.auth.views import LogoutView  # Import LogoutView for custom logout handling
from .filters import StockFilter  # Import StockFilter for filtering stock items

# Accessing our models so that we can get content out of them
from .models import *  # Import all models (consider importing only the required models)

# Borrowing decorators from Django to restrict access to our pages
from django.contrib.auth.decorators import login_required  # Import login_required decorator

# View for the index page
def index(request):
    # Render the index.html template
    return render(request, 'happy_hoe/index.html')

# View for the dashboard page, restricted to logged-in users
@login_required
def dashboard(request):
    # Fetch all products from the Stock model
    products = Stock.objects.all()
    # Apply filters to the queryset using StockFilter
    product_filters = StockFilter(request.GET, queryset=products)
    products = product_filters.qs
    # Render the dashboard.html template with the filtered products and filters
    return render(request, 'happy_hoe/dashboard.html', {'products': products, 'product_filters': product_filters})

# Custom logout view
from django.contrib.auth import logout as auth_logout  # Import logout as auth_logout to avoid naming conflict
from django.shortcuts import redirect  # Import redirect function

def custom_logout(request):
    # Use Django's inbuilt logout function
    auth_logout(request)
    # Redirect to the home page after logout
    return redirect('/')

# View for product detail page, restricted to logged-in users
@login_required
def product_detail(request, product_id):
    # Fetch the product from the Stock model by ID
    product = Stock.objects.get(id=product_id)
    # Render the product_detail.html template with the product details
    return render(request, 'happy_hoe/product_detail.html', {'product': product})

# View for deleting product details, restricted to logged-in users
@login_required
def delete_detail(request, product_id):
    # Fetch the product from the Stock model by ID
    product = Stock.objects.get(id=product_id)
    # Delete the product
    product.delete()
    # Redirect to the dashboard page after deletion
    return HttpResponseRedirect(reverse('dashboard'))

# View for issuing an item, restricted to logged-in users
@login_required
def issue_item(request, pk):
    # Fetch the item from the Stock model by ID
    issued_item = Stock.objects.get(id=pk)
    # Instantiate the SaleForm
    sales_form = SaleForm(request.POST)

    if request.method == 'POST':
        # Check if the form is valid
        if sales_form.is_valid():
            # Create a new sale from the form data
            new_sale = sales_form.save(commit=False)
            new_sale.item = issued_item
            new_sale.unit_price = issued_item.unit_price
            new_sale.save()
            # Update the stock quantity after the sale
            issued_quantity = int(request.POST['quantity'])
            issued_item.total_quantity -= issued_quantity
            issued_item.save()
            # Redirect to the receipt page after saving the sale
            return redirect('receipt')

    # Render the issue_item.html template with the sales form
    return render(request, 'happy_hoe/issue_item.html', {'sales_form': sales_form})

# View for displaying all receipts, restricted to logged-in users
@login_required
def receipt(request):
    # Fetch all sales from the Sale model, ordered by ID in descending order
    sales = Sale.objects.all().order_by('-id')
    # Render the receipt.html template with the sales data
    return render(request, 'happy_hoe/receipt.html', {'sales': sales})

# View for displaying details of a specific receipt, restricted to logged-in users
@login_required
def all_receipts(request, receipt_id):
    # Fetch the receipt from the Sale model by ID
    receipt = Sale.objects.get(id=receipt_id)
    # Render the all_receipts.html template with the receipt details
    return render(request, 'happy_hoe/all_receipts.html', {'receipt': receipt})

# View for adding stock to an item, restricted to logged-in users
@login_required
def add_stock(request, pk):
    # Fetch the item from the Stock model by ID
    issued_item = Stock.objects.get(id=pk)
    # Instantiate the AddForm
    form = AddForm(request.POST)

    if request.method == 'POST':
        # Check if the form is valid
        if form.is_valid():
            # Get the added quantity from the form data
            added_quantity = int(request.POST['total_quantity'])
            # Update the stock quantity
            issued_item.total_quantity += added_quantity
            issued_item.save()
            # Redirect to the dashboard page after updating the stock
            return redirect('dashboard')

    # Render the add_stock.html template with the form
    return render(request, 'happy_hoe/add_stock.html', {'form': form})

# View for displaying all sales, not restricted to logged-in users
def allsales(request):
    # Fetch all sales from the Sale model, ordered by ID in descending order
    sale = Sale.objects.all().order_by('-id')
    # Render the allsales.html template with the sales data
    return render(request, 'happy_hoe/allsales.html', {'sales': sale})
