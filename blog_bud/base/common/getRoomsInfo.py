from django.db.models import Q
from base.models import Room

def getRoomsInfo(query: str):
    roomsInfo = []
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=query) |
        Q(name__icontains=query) |
        Q(description__icontains=query) 
        )
    
    for room in rooms:
        roomObj = {}
        roomObj['room'] = room
        roomObj['participants_count'] = room.participants.all().count()
        roomsInfo.append(roomObj)
        
    return roomsInfo
    