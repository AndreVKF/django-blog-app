from django.forms import ModelForm, CharField, TextInput, Select, Textarea

from base.models import Room, Topic


class RoomForm(ModelForm):
    name = CharField(widget=TextInput({'placeholder': 'Enter room name...', 'class': 'input_field'}))
    description = CharField(widget=Textarea({'placeholder': 'Enter room description...'}))
    
    topicsTuple = tuple((topic, topic) for index, topic in enumerate(Topic.objects.all().order_by('name')))
    topic = CharField(widget=Select({'placeholder': 'Select topic'}, choices=topicsTuple))
    
    class Meta:
        model = Room 
        fields = '__all__'
        exclude = ['host', 'participants']
        
    field_order = ['host', 'topic', 'name', 'description']
