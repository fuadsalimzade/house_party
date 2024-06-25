import base64
import os
from requests import get, post, put
from .models import Spotify
from django.utils import timezone
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

client_id = os.environ.get("CLIENT_ID", "")
client_secret = os.environ.get("CLIENT_SECRET", "")
BASE_API = "https://api.spotify.com/v1/me/"

def user_authentication(session_key):
    queryset = Spotify.objects.filter(user = session_key)

    if queryset.exists():
        spotify_user = queryset[0]
        expiry = spotify_user.expires_in
        if expiry <= timezone.now():
            refresh_new_access_tokens(session_key)
        return True
        
    return False

def update_or_create_spotify_session(session_key, access_token, refresh_token, token_type, expires_in):
    queryset = Spotify.objects.filter(user = session_key)

    try:
        if queryset.exists():
            spotify_user = queryset[0]
            expires_in = timezone.now() + timedelta(seconds=expires_in)
            spotify_user.access_token = access_token
            spotify_user.refresh_token = refresh_token
            spotify_user.token_type = token_type
            spotify_user.expires_in = expires_in
            spotify_user.save(update_fields = ['access_token', 'refresh_token', 'token_type', 'expires_in'])

        else:
            expires_in = timezone.now() + timedelta(seconds=expires_in)
            spotify_user = Spotify(user = session_key, 
                                   access_token = access_token,
                                   refresh_token = refresh_token,
                                   token_type = token_type,
                                   expires_in = expires_in)
            spotify_user.save()

        return True
        
    except Exception as e:
        return e


def refresh_new_access_tokens(spotify_user):
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    response = post('https://accounts.spotify.com/api/token', data={
    'grant_type': 'refresh_token',
    'refresh_token': spotify_user.refresh_token,
    }, headers={
        'Authorization': f'Basic {auth_header}',
        'content-type': 'application/x-www-form-urlencoded',
    }).json()

    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')

    update_or_create_spotify_session(spotify_user.user, access_token, refresh_token, token_type, expires_in)


def execute_spotify_api_call(session_key, endpoint, post_=False, put_=False, device_id = None):
    api_url = BASE_API + endpoint

    queryset = Spotify.objects.filter(user = session_key)
    spotify_user = queryset[0]
    access_token = spotify_user.access_token
    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    if device_id:
        headers['device_id'] = device_id

    if post_:
        response = post(api_url, headers=headers)
    elif put_:
        response = put(api_url, headers=headers)
    else:
        response = get(api_url, headers=headers)

    try:
        if response.status_code == 204 or not response.content:
            return {"status": "success"}
        return response.json()
    except Exception as e :
        return {"error": f"{e}"}
    

def get_device_id(host):
    endpoint = 'player'
    playback_state = execute_spotify_api_call(host, endpoint)
    device_id = playback_state["device"]["id"]

    return device_id

