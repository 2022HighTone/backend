from django.urls import path

from domains.school.view import DefaultSchoolView, SearchSchoolListView, ResultSchoolView

urlpatterns = [
    path('default-school/', DefaultSchoolView.as_view()),
    path('result-school/', ResultSchoolView.as_view()),
    path('search-school', SearchSchoolListView.as_view())
]
