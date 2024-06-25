import base64
import os

import secrets
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv
from rest_framework.renderers import JSONRenderer
from requests import Request, post

from api.models import Room
from .models import Spotify, Vote
from .utils import *

load_dotenv("music_controller/.env")
redirect_uri = os.environ.get("REDIRECT_URL", "")
client_id = os.environ.get("CLIENT_ID", "")
client_secret = os.environ.get("CLIENT_SECRET", "")
state = secrets.token_hex(8)

# Create your views here.
class AuthUrl(APIView):

    def get(self, request, format = None, *args, **kwargs):
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'

        url = Request('GET', "https://accounts.spotify.com/authorize", params={
            'response_type': 'code',
            'client_id': client_id,
            'scope': scopes,
            'redirect_uri': redirect_uri,
            'state': state,
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)
    

class SpotifyCallback(APIView):

    def get(self, request, format = None, *args, **kwargs):
        code = self.request.GET.get('code')
        state_returned = self.request.GET.get('state')
        error = self.request.GET.get('error') or ""

        auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        response = post('https://accounts.spotify.com/api/token', data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            },
            headers={
                'Authorization': f'Basic {auth_header}',
                'content-type': 'application/x-www-form-urlencoded',
            }).json()

        access_token = response.get('access_token')
        refresh_token = response.get('refresh_token')
        token_type = response.get('token_type')
        expires_in = response.get('expires_in')
        error = response.get('error')

        if not request.session.exists(request.session.session_key):
            request.session.create()

        spotify_session = update_or_create_spotify_session(session_key = request.session.session_key,
                                access_token = access_token,
                                refresh_token = refresh_token,
                                token_type = token_type,
                                expires_in = expires_in)
        if spotify_session == True:
            return redirect("frontend:")
        else:
            return Response({"error": str(spotify_session)}, status=status.HTTP_400_BAD_REQUEST)
    

class UserAuthenticated(APIView):

    def get(self, request, format=None):
        if not request.session.exists(request.session.session_key):
            request.session.create()
        session_key = self.request.session.session_key

        autheticated = user_authentication(session_key)
        return Response({"status": autheticated}, status=status.HTTP_200_OK)
        

class CurrentSong(APIView):
    def post(self, request, format = None, *args, **kwargs):
        if not request.session.exists(request.session.session_key):
            request.session.create()
        endpoint = 'player/currently-playing'    
        code = self.request.session.get('room_code')

        queryset = Room.objects.filter(code = code)
        if queryset.exists():
            host = queryset[0].host
            current_song = execute_spotify_api_call(host, endpoint)

            if 'error' in current_song or 'item' not in current_song:
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            
            votes = len(Vote.objects.filter(room = queryset[0], song = current_song['item']['id']))
            
            song = {}
            song['currently_playing'] = current_song['is_playing']
            song['progress_ms'] = current_song['progress_ms']
            song['image_cover'] = current_song['item']['album']['images'][0]['url']
            song['name'] = current_song['item']['name']
            song['duration_ms'] = current_song['item']['duration_ms']
            song['song_id'] = current_song['item']['id']
            song['votes'] = votes
            song['votes_to_skip'] = queryset[0].votes_to_skip

            artists = ""
            for i, artist in enumerate(current_song['item']['artists']):
                if i > 0:
                    artists += ", "
                    artists += artist['name']
                else:
                    artists += artist['name']

            song['artists'] = artists

            self.update_room_song(queryset[0], song['song_id'])
            return Response(song, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
    def update_room_song(self, room, song_id):
        if room.current_song != song_id:
            room.current_song = song_id
            room.save(update_fields = ['current_song'])
            vote = Vote.objects.filter(room = room)
            if vote.exists():
                vote.delete()
        
class PauseSong(APIView):
    def get(self, request, format = None, *args, **kwargs):
        if not request.session.exists(request.session.session_key):
            request.session.create()
        endpoint = 'player/pause'
        code = self.request.session.get('room_code')
        queryset = Room.objects.filter(code = code)
        if queryset.exists():
            host = queryset[0].host
            if self.request.session.session_key == host or queryset[0].guest_can_pause:
                song = execute_spotify_api_call(host, endpoint, put_=True, device_id=get_device_id(host))
                if 'error' in song:
                    return Response(song, status=status.HTTP_400_BAD_REQUEST)
                return Response(song, status=status.HTTP_200_OK)
            return Response(song, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

class ResumeSong(APIView):
    def get(self, request, format = None, *args, **kwargs):
        if not request.session.exists(request.session.session_key):
            request.session.create()
        endpoint = 'player/play'
        code = self.request.session.get('room_code')
        queryset = Room.objects.filter(code = code)
        if queryset.exists():
            host = queryset[0].host
            if self.request.session.session_key == host or queryset[0].guest_can_pause:
                song = execute_spotify_api_call(host, endpoint, put_=True, device_id=get_device_id(host))
                if 'error' in song:
                    return Response(song, status=status.HTTP_400_BAD_REQUEST)
                return Response(song, status=status.HTTP_200_OK)
            return Response(song, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
class SkipSong(APIView):
    def get(self, request, format = None, *args, **kwargs):
        if not request.session.exists(request.session.session_key):
            request.session.create()
        endpoint = 'player/next'
        code = self.request.session.get('room_code')
        queryset = Room.objects.filter(code = code)
        if queryset.exists():
            host = queryset[0].host
            votes = Vote.objects.filter(room = queryset[0], song = queryset[0].current_song)
            if self.request.session.session_key == host or len(votes) >= queryset[0].votes_to_skip:
                song = execute_spotify_api_call(host, endpoint, post_=True, device_id=get_device_id(host))
                if 'error' in song:
                    return Response(song, status=status.HTTP_400_BAD_REQUEST)
                votes.delete()
                return Response(song, status=status.HTTP_200_OK)
            else:
                vote = Vote(user = self.request.session.session_key, room = queryset[0], song = queryset[0].current_song)
                vote.save()

            return Response(song, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
class ShuffleSong(APIView):
    def get(self, request, format = None, *args, **kwargs):
        if not request.session.exists(request.session.session_key):
            request.session.create()
        endpoint = 'player/shuffle'
        code = self.request.session.get('room_code')
        queryset = Room.objects.filter(code = code)
        if queryset.exists():
            host = queryset[0].host
            if self.request.session.session_key == host:
                song = execute_spotify_api_call(host, endpoint, put_=True, device_id=get_device_id(host))
                if 'error' in song:
                    return Response(song, status=status.HTTP_400_BAD_REQUEST)
                return Response(song, status=status.HTTP_200_OK)
            return Response(song, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)