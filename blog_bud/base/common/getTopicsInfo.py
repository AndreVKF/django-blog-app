from django.db.models import Q
from base.models import Room, Topic, Message
# TODO: improve query
def getTopicsInfo():
    topics = Topic.objects.all().order_by('name')
    topics_info = [
        {'name': 'All', 'room_count': Room.objects.all().count()}
    ]
    for topic in topics:
        topic_obj = {}
        topic_obj['name'] = topic
        topic_obj['room_count'] = Room.objects.all().filter(Q(topic__name__icontains=topic)).count()
        topics_info.append(topic_obj)
        
    return topics_info