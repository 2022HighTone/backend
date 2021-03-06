from django.urls import path, include

urlpatterns = [
    path('category/', include('domains.category.urls')),
    path('auth/', include('domains.auth.urls')),
    path('school/', include('domains.school.urls')),
    path('store/', include('domains.store.urls'))
]
