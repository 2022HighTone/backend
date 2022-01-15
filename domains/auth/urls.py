from domains.auth.view import SignUpView, LoginView
from django.urls import path

urlpatterns = [
    path('sign-up/', SignUpView.as_view()),
    path('sign-in/', LoginView.as_view()),
]
