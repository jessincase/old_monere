from datetime import datetime
from channels.auth import channel_session_user_from_http
import jsonpickle
from django.forms.models import model_to_dict
import json
from django.contrib.auth.models import User
import logging
from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user
from .models import Room

log = logging.getLogger(__name__)

@channel_session_user_from_http
def ws_connect(message):
    # Extract the room from the message. This expects message.path to be of the
    # form /chat/{label}/, and finds a Room if the message path is applicable,
    # and if the Room exists. Otherwise, bails (meaning this is a some othersort
    # of websocket). So, this is effectively a version of _get_object_or_404.
    try:
        prefix, label = message['path'].strip('/').split('/')
        if prefix != 'popup_chatroom' and prefix != 'chat':
            log.debug('invalid ws path=%s', message['path'])
            return
        room = Room.objects.get(label=label)
    except ValueError:
        log.debug('invalid ws path=%s', message['path'])
        return
    except Room.DoesNotExist:
        log.debug('ws room does not exist label=%s', label)
        return

    log.debug('chat connect room=%s client=%s:%s',
        room.label, message['client'][0], message['client'][1])

    room.users_in_chat += 1
    room.save()
    Group('chat-'+label, channel_layer=message.channel_layer).add(message.reply_channel)
    message.reply_channel.send({"accept": True}) ##??
    message.channel_session['room'] = [room.label,] # or channel_session['rooms']


@channel_session_user
def ws_receive(message):
    # Look up the room from the channel session, bailing if it doesn't exist
    try:
        #label = message.channel_session['room']
        label = message['path'].strip('/').split('/')[1]

        room = Room.objects.get(label=label)
    except KeyError:
        log.debug('no room in channel_session')
        return
    except Room.DoesNotExist:
        log.debug('recieved message, buy room does not exist label=%s', label)
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.

    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", text)
        return

    if set(data.keys()) != set(('user', 'message')) and set(data.keys()) != set(['message']): #data.keys() returns only message, not user
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        log.debug('chat message room=%s user=%s message=%s',
            room.label, message.user, data['message'])
        data['user'] = message.user
        m = room.messages.create(**data)
        # See above for the note about Group
        Group('chat-'+label, channel_layer=message.channel_layer).send({'text': jsonpickle.encode(m.as_dict())})
        room.last_update = datetime.now()
        room.save()


@channel_session_user
def ws_disconnect(message):
    try:
        label = message.channel_session['room'][0]
        room = Room.objects.get(label=label)
        room.users_in_chat -= 1
        room.save()
        Group('chat-'+label, channel_layer=message.channel_layer).discard(message.reply_channel)

    except (KeyError, Room.DoesNotExist):
        pass


