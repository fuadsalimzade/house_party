from rest_framework import generics, status
from .serializer import RoomSerializer, CreateRoomSerializer, GetRoomSerializer, UpdateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class GetRoom(APIView):
    serializer_class = GetRoomSerializer
    
    def get(self, request, format=None, *args, **kwargs):
        if not request.session.exists(request.session.session_key):
            request.session.create()
        code = request.GET.get('roomCode')
        if code != None:
            queryset = Room.objects.filter(code = code)
            if queryset.exists():
                data = RoomSerializer(queryset[0]).data
                data["ishost"] = queryset[0].host == self.request.session.session_key
                serializer = self.serializer_class(data={
                    "guest_can_pause": data["guest_can_pause"],
                    "votes_to_skip": data["votes_to_skip"],
                    "host": data["ishost"],
                })
                self.request.session["room_code"] = code
                return Response(serializer.initial_data, status=status.HTTP_200_OK)
            else:
                return Response({"Error": "Room does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error": "Room code not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
class CheckUserRoom(APIView):
    
    def get(self, request, format=None, *args, **kwargs):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        room_code = self.request.session.get("room_code")
        if room_code != None and len(room_code) > 0:
            return Response({"room_code": room_code}, status=status.HTTP_200_OK)
        else:
            return Response({"Error": "User does not belong to a room"}, status=status.HTTP_400_BAD_REQUEST)
                
class RoomCreate(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format= None, *args, **kwargs):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields = ['guest_can_pause', 'votes_to_skip'])
                self.request.session["room_code"] = room.code
            else:
                room = Room(guest_can_pause = guest_can_pause, votes_to_skip=votes_to_skip, host = host)
                room.save()
                self.request.session["room_code"] = room.code

            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
        else:
            return Response({'Bad Request': 'Invalid data..'}, status=status.HTTP_400_BAD_REQUEST)
        

class LeaveRoom(APIView):

    def post(self, request, format=None, *args, **kwargs):
        request.session.pop("room_code")

        host_id = request.session.session_key
        queryset = Room.objects.filter(host = host_id)
        if queryset.exists():
            room = queryset[0]
            room.delete()

        return Response({"Sucess": "User left room"}, status=status.HTTP_200_OK)
    
class UpdateRoomSettings(APIView):
    serializer_class = UpdateRoomSerializer

    def patch(self, request, format=None, *args, **kwargs):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data.get("code")
            queryset = Room.objects.filter(code = code)
            host_id = request.session.session_key

            if queryset.exists() and (queryset[0].host == host_id):
                room = queryset[0]
                room.guest_can_pause = serializer.data.get("guest_can_pause")
                room.votes_to_skip = serializer.data.get("votes_to_skip")
                room.save(update_fields= ['guest_can_pause', 'votes_to_skip'])

                return Response({"success" : "Room settings have been updated"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"error" : "Room does not exist or User does not have permission to change settings"}, 
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'Bad Request': 'Invalid data..'}, status=status.HTTP_400_BAD_REQUEST)







