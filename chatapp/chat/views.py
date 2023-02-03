from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from chat.forms import UserFormLogin, UserFormSignin, AddContactForm
from chat.models import ChatUsers, ChatMessages, Conversations
from datetime import datetime
# Create your views here.

def get_conversations(request):
    session_username = request.session.get('username')
    session_email = request.session.get('email')
    if session_username or session_email:
        user1 = session_username

        conversations_as_user_1 = Conversations.objects.filter(user1=user1).order_by('-last_date')
        conversations_as_user_2 = Conversations.objects.filter(user2=user1).order_by('-last_date')

        all_conversations = []
        if conversations_as_user_1 or conversations_as_user_2:
            for conversation in conversations_as_user_1:
                conversation_data = {}
                conversation_data['user_conversation'] = conversation.user2
                conversation_data['id_conversation'] = conversation.id_serial
                all_conversations.append(conversation_data)

            for conversation in conversations_as_user_2:
                conversation_data = {}
                conversation_data['user_conversation'] = conversation.user1
                conversation_data['id_conversation'] = conversation.id_serial
                all_conversations.append(conversation_data)

        return all_conversations

    else:
        return redirect('index')

def index(request):
    session_email = request.session.get('email')
    session_username = request.session.get('username')
    if not session_email or not session_username:
        if request.method == 'POST':
            form_data = UserFormLogin(request.POST)
            if form_data.is_valid():
                email = form_data.cleaned_data['email']
                password = form_data.cleaned_data['password']

                try:
                    valid_user = get_object_or_404(ChatUsers, email=email)
                except:
                    msg = 'User does not exist'
                    return render(request, 'index_pages/login.html', {'form_login': UserFormLogin, 'msg': msg})

                if valid_user and valid_user.password == password:

                    request.session['email'] = email
                    request.session['username'] = valid_user.username

                    return redirect('entry_main_interface')
                else:
                    msg = 'Wrong password'
                    return render(request, 'index_pages/login.html', {'form_login': UserFormLogin, 'msg': msg})
        else:
            user_form_login = UserFormLogin
            return render(request, 'index_pages/login.html', {'form_login': user_form_login})
    else:
        return redirect('entry_main_interface')

def logging_out(request):
    session_email = request.session.get('email')
    session_username = request.session.get('username')
    if session_email or session_username:
        if request.method == 'GET':
            request.session.flush()
            return redirect('index')
    else:
        return redirect('index')

def signin(request):
    session_email = request.session.get('email')
    session_username = request.session.get('username')
    if not session_email or not session_username:
        if request.method == 'POST':
            form_signin = UserFormSignin(request.POST)
            if form_signin.is_valid():
                email = form_signin.cleaned_data['email']
                username = form_signin.cleaned_data['username']

                for character in username:
                    if character == ',' or character == ' ' or character == '@':
                        msg = f"Username cannot contain ',' , '@', nor  '  ' (blank space) character"
                        return render(request, 'index_pages/signin.html', {'form_signin': UserFormSignin, 'msg': msg})

                try:
                    unvalid_username = get_object_or_404(ChatUsers, username=username)
                except:
                    unvalid_username = False

                try:
                    unvalid_email = get_object_or_404(ChatUsers, email=email)
                except:
                    unvalid_email = False

                msg = ''
                returning = False
                if len(username) > 12:
                    msg = 'Username length must be 12 characters or less'
                    returning = True
                elif unvalid_email:
                    msg = 'This email already exist'
                    returning = True
                elif unvalid_username:
                    msg = 'Username already used'
                    returning = True
                if not unvalid_email and not unvalid_username:
                    form_signin.save()
                    msg = 'User successfully created. You can login now'
                    returning = True
                if returning:
                    return render(request, 'index_pages/signin.html', {'form_signin': UserFormSignin, 'msg': msg})
        else:
            user_form_signin = UserFormSignin
            return render(request, 'index_pages/signin.html', {'form_signin': user_form_signin})
    else:
        return redirect('entry_main_interface')

def entry_main_interface(request):
    session_email = request.session.get('email')
    session_username = request.session.get('username')
    if session_email or session_username:
        all_conversations = get_conversations(request)
        return render(request, 'general_interface/main_interface.html', {'all_conversations': all_conversations, 'num_chats': len(all_conversations)})
    else:
        return redirect('index')

def chat_room(request, username):
    session_username = request.session.get('username')
    session_email = request.session.get('email')
    if session_username or session_email:
        user1 = session_username
        try:
            valid_username = get_object_or_404(ChatUsers, username=username)
            user2 = valid_username.username
        except:
            return redirect('show_all_contacts')

        conversation_query1 = Conversations.objects.filter(user1=user1, user2=user2).exists()
        conversation_query2 = Conversations.objects.filter(user1=user2, user2=user1).exists()

        if conversation_query1:
            conversation = get_object_or_404(Conversations, user1=user1, user2=user2)
            id_conversation = conversation.id_serial
        elif conversation_query2:
            conversation = get_object_or_404(Conversations, user1=user2, user2=user1)
            id_conversation = conversation.id_serial
        else:
            new_room = Conversations.objects.create(user1=user1, user2=user2)
            new_room.save()
            id_conversation_query = get_object_or_404(Conversations, user1=user1, user2=user2)
            id_conversation = id_conversation_query.id_serial

        conversation = get_object_or_404(Conversations, id_serial=id_conversation)
        conversation.last_date = datetime.now()
        conversation.save()

        user_session = get_object_or_404(ChatUsers, email=session_email)

        is_contact = False
        if username in user_session.contacts:
            is_contact = True

        all_conversations = get_conversations(request)
        return render(request, 'general_interface/chat_room.html', {'user_conversation': username, 'id_conversation': id_conversation, 'is_contact': is_contact, 'all_conversations': all_conversations, 'num_chats': len(all_conversations)})
    else:
        return redirect('index')

def go_to_chat(request):
    session_email = request.session.get('email')
    session_username = request.session.get('username')
    if session_email or session_username:

        username = request.POST.get('user_conversation')
        id_conversation = request.POST.get('id_chat')

        return redirect('chat_room', username=username)
    else:
        return redirect('index')

def delete_chat(request):
    session_email = request.session.get('email')
    session_username = request.session.get('username')
    if session_email or session_username:

        id_conversation = request.POST.get('id_conversation')
        print('Este es el id', id_conversation)
        conversation = get_object_or_404(Conversations, id_serial=id_conversation)
        conversation.delete()

        messages_by_id = ChatMessages.objects.filter(id_conversation=id_conversation)
        messages_by_id.delete()

        return redirect('show_all_contacts')
    else:
        return redirect('index')

def send_message(request):
    session_username = request.session.get('username')
    if session_username:
        user_sender = session_username

        message = request.POST['message']

        if message == '' or message.isspace():
            return

        message = message.strip()

        user_receiver = request.POST['user_conversation']
        id_conversation = request.POST['id_conversation']

        new_message = ChatMessages.objects.create(
            id_conversation=id_conversation,
            value=message,
            sender=user_sender,
            receiver=user_receiver
        )
        new_message.save()

        conversation = get_object_or_404(Conversations, id_serial=id_conversation)
        conversation.last_date = datetime.now()
        conversation.save()

        return HttpResponse('Message sent successfully')
    else:
        return redirect('index')

def get_messages(request, user_conversation):
    session_username = request.session.get('username')
    if session_username:
        user_sender = session_username

        conversation_query1 = Conversations.objects.filter(user1=user_sender, user2=user_conversation).exists()
        conversation_query2 = Conversations.objects.filter(user1=user_conversation, user2=user_sender).exists()

        if conversation_query1:
            conversation = get_object_or_404(Conversations, user1=user_sender, user2=user_conversation)
            id_conversation = conversation.id_serial
        elif conversation_query2:
            conversation = get_object_or_404(Conversations, user1=user_conversation, user2=user_sender)
            id_conversation = conversation.id_serial
        else:
            id_conversation = False

        try:
            messages = ChatMessages.objects.filter(id_conversation=id_conversation).order_by('date')
        except:
            return redirect('show_all_contacts')

        return JsonResponse({"messages": list(messages.values())})
    else:
        return redirect('index')

def show_all_contacts(request):
    if request.method == 'GET':
        session_email = request.session.get('email')
        if session_email:
            user_session = get_object_or_404(ChatUsers, email=session_email)
            contacts = user_session.contacts
            if contacts is None:
                msg = "You don't have any contact added"
                return render(request, 'contacts_section/show_all_contacts.html', {'msg': msg})

            contacts = contacts.split(',')
            all_contacts = []
            for contact in contacts:
                if contact:
                    contact_data = {}
                    contact_data['username'] = contact
                    try:
                        existen_user = get_object_or_404(ChatUsers, username=contact)
                        if existen_user:
                            contact_data['exist'] = True
                    except:
                        contact_data['exist'] = False

                    all_contacts.append(contact_data)

            msg = f'All  contacts: {len(all_contacts)}'
            all_conversations = get_conversations(request)
            return render(request, 'contacts_section/show_all_contacts.html', {'contacts': all_contacts, 'msg': msg, 'all_conversations': all_conversations, 'num_chats': len(all_conversations)})
        else:
            return redirect('index')
    elif request.method == 'POST':
        user_delete = request.POST.get('username')
        return redirect('delete_contact', username=user_delete)

def verify_username(user_session, user_added):
    if user_session.username == user_added:
        return 'same'

    user_session = get_object_or_404(ChatUsers, username=user_session.username)

    if user_session.contacts is None:
        user_session.contacts = ''
        user_session.contacts += user_added + ','
    else:
        all_contacts = user_session.contacts.split(',')
        for contact in all_contacts:
            if contact == user_added:
                return 'contact'

        user_session.contacts += user_added + ','
    return user_session.contacts

def add_contact(request):
    session_email = request.session.get('email')
    if session_email:
        all_conversations = get_conversations(request)
        if request.method == 'POST':
            form_contact = AddContactForm(initial={'contact1': session_email})
            form_contact_fill = AddContactForm(request.POST)
            if form_contact_fill.is_valid():
                username_added = form_contact_fill.cleaned_data['contact2']
                try:
                    for i in username_added:
                        if i == '@':
                            raise Exception
                except:
                    msg = 'Invalid username. Enter a username without "@" character'
                    return render(request, 'contacts_section/all_contacts_form.html', {'form_contact': form_contact, 'msg': msg, 'all_conversations': all_conversations, 'num_chats': len(all_conversations)})

                try:
                    valid_user = get_object_or_404(ChatUsers, username=username_added)
                except:
                    msg = 'This user does not exist in the database'
                    return render(request, 'contacts_section/all_contacts_form.html', {'form_contact': form_contact, 'msg': msg, 'all_conversations': all_conversations, 'num_chats': len(all_conversations)})

                user_session = get_object_or_404(ChatUsers, email=session_email)

                own_username = verify_username(user_session, valid_user.username)

                if own_username == 'same':
                    msg = 'Invalid username. This is you own username'
                    return render(request, 'contacts_section/all_contacts_form.html',
                                  {'form_contact': form_contact, 'msg': msg, 'all_conversations': all_conversations, 'num_chats': len(all_conversations)})
                elif own_username == 'contact':
                    msg = 'This user is already your contact'
                    return render(request, 'contacts_section/all_contacts_form.html',
                                  {'form_contact': form_contact, 'msg': msg, 'all_conversations': all_conversations, 'num_chats': len(all_conversations)})
                else:
                    user_session.contacts = own_username

                user_session.save()
                msg = 'Contact successfully added'
                return render(request, 'contacts_section/all_contacts_form.html', {'form_contact': form_contact, 'msg': msg, 'all_conversations': all_conversations, 'num_chats': len(all_conversations)})
        else:
            form_contact = AddContactForm(initial={'contact1': session_email})
            return render(request, 'contacts_section/all_contacts_form.html', {'form_contact': form_contact, 'all_conversations': all_conversations, 'num_chats': len(all_conversations)})
    else:
        return redirect('index')

def delete_contact(request, username):
    session_email = request.session.get('email')
    if session_email:
        user_session = get_object_or_404(ChatUsers, email=session_email)
        all_contacts = user_session.contacts.split(',')

        final_all_contacts = []
        for contact in all_contacts:
            if contact != username:
                final_all_contacts.append(contact)

        if len(final_all_contacts) > 0:
            user_session.contacts = ','.join(final_all_contacts)
        else:
            user_session.contacts = ''
        user_session.save()
        return redirect('show_all_contacts')
    else:
        return redirect('index')

def find_user(request):
    session_email = request.session.get('email')
    if session_email:
        all_conversations = get_conversations(request)
        user_query = request.POST.get('find_users').lower()
        user_query = user_query.strip()

        all_users_query = ChatUsers.objects.filter(username__icontains=user_query)

        msg = f'Search: "{user_query}"'
        if user_query == '' or user_query.isspace() or len(all_users_query) == 0:
            msg = f'Search: "{user_query}" 0 results'
            all_users = False
        else:
            user_session = get_object_or_404(ChatUsers, email=session_email)
            all_users = []
            for contact in all_users_query:
                user = {'username': contact.username, 'email': contact.email}
                try:
                    if contact.username in user_session.contacts:
                        user['contact'] = True
                    else:
                        user['contact'] = False
                except:
                    user['contact'] = False

                if contact.username == user_session.username:
                    user['own_username'] = True
                else:
                    user['own_username'] = False

                all_users.append(user)
        return render(request, 'general_interface/all_users.html', {'all_users': all_users, 'msg': msg, 'all_conversations': all_conversations, 'num_chats': len(all_conversations)})
    else:
        return redirect('index')

def find_all_users(request):
    session_email = request.session.get('email')
    if session_email:
        all_conversations = get_conversations(request)

        all_users_query = ChatUsers.objects.all()

        msg = ''

        user_session = get_object_or_404(ChatUsers, email=session_email)
        all_users = []
        for contact in all_users_query:
            user = {'username': contact.username, 'email': contact.email}
            try:
                if contact.username in user_session.contacts:
                    user['contact'] = True
                else:
                    user['contact'] = False
            except:
                user['contact'] = False

            if contact.username == user_session.username:
                user['own_username'] = True
            else:
                user['own_username'] = False

            all_users.append(user)

        return render(request, 'general_interface/all_users.html', {'all_users': all_users, 'msg': msg, 'all_conversations': all_conversations, 'num_chats': len(all_conversations)})
    else:
        return redirect('index')

def add_contact_from_all(request, username):
    session_email = request.session.get('email')
    if session_email:
        if request.method == 'POST':
            user_added = username
            user_session = get_object_or_404(ChatUsers, email=session_email)

            own_username = verify_username(user_session, user_added)

            user_session.contacts = own_username

            user_session.save()
            return redirect('show_all_contacts')
        else:
            return
    else:
        return redirect('index')

def delete_account(request):
    session_email = request.session.get('email')
    if session_email:
        if request.method == 'GET':
            return redirect('confirm_delete')
    else:
        return redirect('index')

def confirm_delete(request):
    session_email = request.session.get('email')
    if session_email:
        if request.method == 'POST':
            user = get_object_or_404(ChatUsers, email=session_email)
            try:
                user.delete()
                return redirect('logout')
            except:
                return
        else:
            all_conversations = get_conversations(request)
            return render(request, 'general_interface/confirm_delete.html', {'all_conversations': all_conversations, 'num_chats': len(all_conversations)})
    else:
        return redirect('index')
