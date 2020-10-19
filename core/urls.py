from django.urls import path
from rooms import views as room_views



app_name = "core"


urlpatterns = [
    path("", room_views.HomeView.as_view(), name="home")
]


# as view(): django에서 view class를 메소드로 만들어주는 함수

