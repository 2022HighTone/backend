from domains.auth.view import SignUpView, LoginView, DefaultSchoolSettingView, UserProfileView
from django.urls import path

urlpatterns = [
    path('sign-up/', SignUpView.as_view()),
    path('sign-in/', LoginView.as_view()),
    path('default-school-setting/', DefaultSchoolSettingView.as_view()),
    path('profile/', UserProfileView.as_view()),
]
