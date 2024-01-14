from flyers import views
from django.urls import path

app_name = 'flyers'

urlpatterns = [
    path('category/<str:category>',
         views.FlyerCategoryView.as_view(), name='category'),
]
