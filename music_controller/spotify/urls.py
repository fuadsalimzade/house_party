from django.urls import path
from . import views

urlpatterns = [
    path("get-auth-url", views.AuthUrl.as_view()),
    path("redirect-url", views.SpotifyCallback.as_view()),
    path("check-user-authentication", views.UserAuthenticated.as_view()),
    path("current-song", views.CurrentSong.as_view()),
    path("pause-song", views.PauseSong.as_view()),
    path("resume-song", views.ResumeSong.as_view()),
    path("skip-song", views.SkipSong.as_view()),
    path("shuffle-song", views.ShuffleSong.as_view()),
]
