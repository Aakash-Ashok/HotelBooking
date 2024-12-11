from django.urls import path
from .views import*

urlpatterns = [
    path("",IndexView.as_view(),name="index"),
    path('register/', CustomerRegisterView.as_view(), name='customer_register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("adminn/",AdminIndexView.as_view(),name="adminindex"),
   
    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/add/', CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    # Seasonal Pricing URLs
    path('seasonalpricing/', SeasonalPricingListView.as_view(), name='seasonalpricing_list'),
    path('seasonalpricing/add/<int:category_id>/',SeasonalPricingCreateView.as_view(), name='seasonalpricing_add'),  
    path('seasonalpricing/<int:pk>/edit/', SeasonalPricingUpdateView.as_view(), name='seasonalpricing_edit'),
    path('seasonalpricing/<int:pk>/delete/', SeasonalPricingDeleteView.as_view(), name='seasonalpricing_delete'),

    # Tourist Location URLs
    path('touristlocations/<int:pk>/edit/', TouristLocationUpdateView.as_view(), name='touristlocation_edit'),
    path('touristlocations/add/', TouristLocationCreateView.as_view(), name='touristlocation_add'),
    path('touristlocations/<int:pk>/edit/', TouristLocationUpdateView.as_view(), name='touristlocation_edit'),
    path('touristlocations/<int:pk>/delete/', TouristLocationDeleteView.as_view(), name='touristlocation_delete'),
]
