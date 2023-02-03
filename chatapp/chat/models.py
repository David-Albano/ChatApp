from django.db import models
from datetime import datetime
from string import ascii_letters, digits
import random

def create_id_serial():
    characteres = ''.join(digits + ascii_letters + digits)
    id_serial = ''
    for i in range(60):
        character = random.choice(characteres)
        id_serial += character
    return id_serial

# Create your models here.

class ChatUsers(models.Model):
    objects = None
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    contacts = models.CharField(max_length=9999999, default=None)

class ChatMessages(models.Model):
    objects = None
    id_message = models.CharField(max_length=62, default=create_id_serial, unique=True)
    id_conversation = models.CharField(max_length=61, blank=True)
    value = models.CharField(max_length=1000000)
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    date = models.DateTimeField(default=datetime.now, blank=True)

class Conversations(models.Model):
    objects = None
    id_serial = models.CharField(max_length=61, default=create_id_serial, unique=True)
    user1 = models.CharField(max_length=255)
    user2 = models.CharField(max_length=255)
    last_date = models.DateTimeField(default=datetime.now, blank=True)
