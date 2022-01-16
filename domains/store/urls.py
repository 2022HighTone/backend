from django.urls import path

from domains.store.view import ReviewCreateView

urlpatterns = [
    path('<int:store_id>/review', ReviewCreateView.as_view()),
]
