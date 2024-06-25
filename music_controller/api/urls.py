from django.urls import path
from . import views

urlpatterns = [
    path("list", views.RoomView.as_view(), name = "list-room"),
    path("create", views.RoomCreate.as_view(), name = "create-room"),
    path("room/", views.GetRoom.as_view(), name = "get-room"),
    path("check-user-room", views.CheckUserRoom.as_view(), name= "check-user-room"),
    path("leave-room", views.LeaveRoom.as_view(), name= "leave-room"),
    path("update-room", views.UpdateRoomSettings.as_view(), name= "update-room"),


]