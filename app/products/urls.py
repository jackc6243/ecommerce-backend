from products import views
from django.urls import path
app_name = 'products'


urlpatterns = [
    path('all/', views.AllProductView.as_view(), name='all_products'),
    path('new/', views.NewProductView.as_view(), name='new'),
    path('discounts/', views.DiscountProductView.as_view(), name='discounts'),
    path('categories/<str:category>/',
         views.CategoryProductView.as_view(), name='category'),
    path('<int:pk>', views.RetrieveSingleProduct.as_view(), name='product'),
]
