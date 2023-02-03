"""chatapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from chat.views import index, logging_out, signin, entry_main_interface, chat_room, go_to_chat, delete_chat, send_message, get_messages, show_all_contacts, add_contact, add_contact_from_all, delete_contact, find_user, find_all_users, confirm_delete, delete_account

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('sign-in', signin, name='signin'),
    path('logging_out', logging_out, name='logging_out'),
    path('ChatApp', entry_main_interface, name='entry_main_interface'),
    path('chat_room/<str:username>', chat_room, name='chat_room'),
    path('go_to_chat', go_to_chat, name='go_to_chat'),
    path('delete_chat', delete_chat, name='delete_chat'),
    path('send_message', send_message, name='send_message'),
    path('get_messages/<str:user_conversation>', get_messages, name='get_messages'),
    path('contacts', show_all_contacts, name='show_all_contacts'),
    path('add_contact', add_contact, name='add_contact'),
    path('add_contact_from_all/<str:username>', add_contact_from_all, name='add_contact_from_all'),
    path('delete_contact/<str:username>', delete_contact, name='delete_contact'),
    path('find_user', find_user, name='find_user'),
    path('find_all_users', find_all_users, name='find_all_users'),
    path('delete_account', delete_account, name='delete_account'),
    path('confirm_delete', confirm_delete, name='confirm_delete')
]
