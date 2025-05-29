from django.shortcuts import render, redirect
from .models import myuser, Message

def register_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        if myuser.objects.filter(username=username).exists():
            return render(request,'register.html',{"error":'username already exists!'})
        myuser.objects.create(username=username,password=password)
        return render(request,'register.html',{'msg':'User Registration Scusses. You can login.'})
    return render(request,'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = myuser.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            return redirect('messages')
        except myuser.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid Credentials'})
    return render(request, 'login.html')


def message_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    sender = myuser.objects.get(id=user_id)
    users = myuser.objects.exclude(id=sender.id)  # other users for chatting
    messages = []
    selected_user = None

    if request.method == 'POST':
        receiver_username = request.POST.get('receiver')
        content = request.POST.get('content')

        try:
            receiver = myuser.objects.get(username=receiver_username)
            Message.objects.create(sender=sender, receiver=receiver, content=content)
            selected_user = receiver
        except myuser.DoesNotExist:
            return render(request, 'messages.html', {
                'error': 'User not found!',
                'sender': sender.username,
                'users': users,
                'messages': [],
            })

    elif request.method == 'GET' and 'receiver' in request.GET:
        receiver_username = request.GET.get('receiver')
        try:
            selected_user = myuser.objects.get(username=receiver_username)
        except myuser.DoesNotExist:
            selected_user = None

    if selected_user:
        # Get messages between logged-in user and selected user
        messages = Message.objects.filter(
            sender__in=[sender, selected_user],
            receiver__in=[sender, selected_user]
        ).order_by('timestamp')

    return render(request, 'messages.html', {
        'sender': sender.username,
        'users': users,
        'selected_user': selected_user,
        'messages': messages
    })


