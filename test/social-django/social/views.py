from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.utils import timezone
import time
import datetime
from social.models import Member, Profile, PrivateMessage, PublicMessage
import urllib2
from rest_framework import viewsets
from .serializers import PrivateMessageSerializer
from .serializers import ProfileSerializer
from .serializers import PublicMessageSerializer

class PrivateMessageViewSet(viewsets.ModelViewSet):
        """API endpoint for listing and creating messages."""
        queryset = PrivateMessage.objects.order_by('text')
        serializer_class = PrivateMessageSerializer

class PublicMessageViewSet(viewsets.ModelViewSet):
        """API endpoint for listing and creating messages."""
        queryset = PublicMessage.objects.order_by('text')
        serializer_class = PublicMessageSerializer
        
class ProfileViewSet(viewsets.ModelViewSet):
        """API endpoint for listing and creating profiles."""
        queryset = Profile.objects.order_by('text')
        serializer_class = ProfileSerializer


appname = 'Facemagazine'

def index(request):
    template = loader.get_template('social/index.html')
    context = RequestContext(request, {
            'appname': appname,
        })
    return HttpResponse(template.render(context))

def messages(request):
    if 'username' in request.session:
        username = request.session['username']
        template = loader.get_template('social/messages.html')
        member = Member.objects.get(pk=username)
        context = RequestContext(request, {
                'appname': appname,
                'username': username,
                'Alltext' : member.username,
                'loggedin': True
            })
        # checks for another user has been requested. Calls a different method called mess. 
        if 'view' in request.GET:
            	return mess(request, request.GET['view'])  
		# a message is being posted. On the users own page.        	
        if 'text' in request.POST:
    		text = request.POST['text']
    		useThis = request.POST['pm']
    		check = '0'
    		# posting a public message
    		if check == useThis:
    			# creating a new message and filling in the fields
    			publicMess = PublicMessage(text=text)
    			publicMess.receives = username
    			publicMess.createdby = username
    			publicMess.mytime = "Date: " + time.strftime("%d/%m/%Y") + " Time: " + time.strftime("%H:%M:%S")
    			publicMess.save()
    			member.save()
    			# adds on to the users public message
    			member.publicMessage.add(publicMess)
    		else:
    			# creating a private message, and filling its fields
    			privMess = PrivateMessage(text=text)
    			privMess.receives = username
    			privMess.createdby = username
    			privMess.mytime = "Date: " + time.strftime("%d/%m/%Y") + " Time: " + time.strftime("%H:%M:%S")
    			privMess.save()
    			member.save()
    			# adds on to the users private message
    			member.privateMessage.add(privMess)
    	else:
    		text = ""	
    	# retrieve all private and public messages
    	messages = member.privateMessage.all()
    	publicMess = member.publicMessage.all()
    	# decided to use this. To retrieve all messages that the user received.
    	# Therefore the user can see all its message that has been sent to him. Both public and private
    	messPublic = PublicMessage.objects.filter(receives=username)
    	myMessages = PrivateMessage.objects.filter(receives=username)
    	return render(request, 'social/messages.html', {
            		'appname': appname,
            		'username': username,
            		'messages' : myMessages,
            		'publicMessage' : messPublic,
            		'loggedin': True}
            		)
    else:
    	checkMessage = "User is not logged in, no access to view this mesages page! Please log in."
    	return render(request, 'social/login.html', {
    							'appname':appname,
    							'checkMessage' : checkMessage,
    							'loggedin' : False}
    							)   	
        
def mess(request, view_user):
    if 'username' in request.session:
        username = request.session['username']
        mem = Member.objects.get(pk=view_user)
        if view_user == username:
            greeting = "Your"
        else:
            greeting = view_user + "'s"

        if mem.profile:
            texta = mem.profile.text
        else:
            texta = ""
        if 'text' in request.POST:
    		text = request.POST['text']
    		useThis = request.POST['pm']
    		check = '0'
    		if check == useThis:
    			publicMess = PublicMessage(text=text)
    			publicMess.receives = view_user
    			publicMess.createdby = username
     			publicMess.mytime = "Date: " + time.strftime("%d/%m/%Y") + " Time: " + time.strftime("%H:%M:%S")
    			publicMess.save()
    			mem.save()
    			mem.publicMessage.add(publicMess)
    		else:
    			privMess = PrivateMessage(text=text)
    			privMess.receives = view_user
    			privMess.createdby = username
     			privMess.mytime = "Date: " + time.strftime("%d/%m/%Y") + " Time: " + time.strftime("%H:%M:%S")
    			privMess.save()
    			mem.save()
    			mem.privateMessage.add(privMess)    
    			
        messages = PrivateMessage.objects.filter(receives=view_user, createdby=username)
        publicMess = PublicMessage.objects.filter(receives=view_user)
        return render(request, 'social/message.html', {
            'appname': appname,
            'username': username,
            'view_user' : view_user,
            'messages' : messages,
            'publicMessage': publicMess,
            'greeting': greeting,
            'profile': texta,
            'loggedin': True}
            )
    else:
    	checkMessage = "User is not logged in, no access to view this message page! Please log in."
    	return render(request, 'social/login.html', {
    							'appname':appname,
    							'checkMessage' : checkMessage,
    							'loggedin' : False}
    							)
# 		raise Http404("User is not logged it, no access to members page!")


def signup(request):
    template = loader.get_template('social/signup.html')
    context = RequestContext(request, {
            'appname': appname,
        })
    return HttpResponse(template.render(context))

def register(request):
	if 'user' in request.POST:
		u = request.POST['user']
		p = request.POST['pass']
		try:
			member = Member.objects.get(pk=u)
			message = "User " + u + " already exist"
			template = loader.get_template('social/signup.html')
			context = RequestContext(request, {
        	'appname': appname,
        	'username' : u,
        	'message' : message
        	})
        	except Member.DoesNotExist:
        		template= loader.get_template('social/user-registered.html')
        		user = Member(username=u, password=p)
        		user.save()
        		context = RequestContext(request, {
        		'appname': appname,
        		'username' : u
        		})
		return HttpResponse(template.render(context))
			
def login(request):
    if 'username' not in request.POST:
        template = loader.get_template('social/login.html')
        context = RequestContext(request, {
                'appname': appname,
            })
        return HttpResponse(template.render(context))
    else:
        u = request.POST['username']
        p = request.POST['password']
        try:
            member = Member.objects.get(pk=u)
        except Member.DoesNotExist:
        	message = "User does not exist"
        	return render(request, 'social/login.html', {
        		'appname': appname,
        		'loggedin': False,
        		'message' : message})
        if member.password == p:
            request.session['username'] = u;
            request.session['password'] = p;
            return render(request, 'social/login.html', {
                'appname': appname,
                'username': u,
                'loggedin': True}
                )
        else:
            message = "Incorrect Password"
            return render(request, 'social/login.html', {
        		'appname': appname,
        		'username': u,
        		'pass': p,
        		'loggedin': False,
        		'message' : message})

def logout(request):
    if 'username' in request.session:
        u = request.session['username']
        request.session.flush()        
        template = loader.get_template('social/logout.html')
        context = RequestContext(request, {
                'appname': appname,
                'username': u
            })
        return HttpResponse(template.render(context))
    else:
    	checkMessage = "Can't logout, you are not logged in"
    	return render(request, 'social/login.html', {
    							'appname':appname,
    							'checkMessage' : checkMessage,
    							'loggedin' : False}
    							)
#         raise Http404("Can't logout, you are not logged in")

def member(request, view_user):
    if 'username' in request.session:
        username = request.session['username']
        member = Member.objects.get(pk=view_user)
        if view_user == username:
            greeting = "Your"
        else:
            greeting = view_user + "'s"
            
        if member.profile:
            text = member.profile.text
        else:
            text = ""
        return render(request, 'social/member.html', {
            	'appname': appname,
            	'username': username,
            	'member': member,
            	'greeting': greeting,
            	'profile': text,
            	'loggedin': True}
            	)
    else:
    	checkMessage = "User is not logged in, no access to view this member page! Please log in."
    	return render(request, 'social/login.html', {
    							'appname':appname,
    							'checkMessage' : checkMessage,
    							'loggedin' : False}
    							)
#         raise Http404("User is not logged it, no access to members page!")

def friends(request):
    if 'username' in request.session:
        username = request.session['username']
        member_obj = Member.objects.get(pk=username)
        # list of people I'm following
        following = member_obj.following.all()
        # list of people that are following me
        followers = Member.objects.filter(following__username=username)
        # render reponse
        return render(request, 'social/friends.html', {
            'appname': appname,
            'username': username,
            'members': members,
            'following': following,
            'followers': followers,
            'loggedin': True}
            )
    else:
    	checkMessage = "User is not logged in, no access to friends page! Please log in."
    	return render(request, 'social/login.html', {
    							'appname':appname,
    							'checkMessage' : checkMessage,
    							'loggedin' : False}
    							)
#         raise Http404("User is not logged it, no access to members page!")

def members(request):
    if 'username' in request.session:
        username = request.session['username']
        member_obj = Member.objects.get(pk=username)
        # follow new friend
        if 'add' in request.GET:
            friend = request.GET['add']
            friend_obj = Member.objects.get(pk=friend)
            member_obj.following.add(friend_obj)
            member_obj.save()
        # unfollow a friend
        if 'remove' in request.GET:
            friend = request.GET['remove']
            friend_obj = Member.objects.get(pk=friend)
            member_obj.following.remove(friend_obj)
            member_obj.save()
        # view user profile
        if 'view' in request.GET:
            return member(request, request.GET['view'])
        else:
            # list of all other members
            members = Member.objects.exclude(pk=username)
            # list of people I'm following
            following = member_obj.following.all()
            # list of people that are following me
            followers = Member.objects.filter(following__username=username)
            # render reponse
            return render(request, 'social/members.html', {
                'appname': appname,
                'username': username,
                'members': members,
                'following': following,
                'followers': followers,
                'loggedin': True}
                )
    else:
    	checkMessage = "User is not logged in, no access to members page! Please log in."
    	return render(request, 'social/login.html', {
    							'appname':appname,
    							'checkMessage' : checkMessage,
    							'loggedin' : False}
    							)
#         raise Http404("User is not logged it, no access to members page!")

def profile(request):
    if 'username' in request.session:
        u = request.session['username']
        member = Member.objects.get(pk=u)
        if 'text' in request.POST:
            text = request.POST['text']
            if member.profile:
                member.profile.text = text
                member.profile.save()
            else:
                profile = Profile(text=text)
                profile.save()
                member.profile = profile
            member.save()
        else:
            if member.profile:
                text = member.profile.text
            else:
                text = ""
        return render(request, 'social/profile.html', {
            'appname': appname,
            'username': u,
            'text' : text,
            'loggedin': True}
            )
    else:
    	checkMessage = "User is not logged in, no access to profiles! Please log in."
    	return render(request, 'social/login.html', {
    							'appname':appname,
    							'checkMessage' : checkMessage,
    							'loggedin' : False}
    							)
        # raise Http404("User is not logged it, no access to profiles!")

def checkuser(request):
    if 'user' in request.POST:
        u = request.POST['user']
        try:
            member = Member.objects.get(pk=u)
        except Member.DoesNotExist:
            member = None
        if member is not None:
        	message = "This username is taken"
        	return HttpResponse("<span class='taken'>&nbsp;&#x2718; This username is taken</span>")
        else:
            return HttpResponse("<span class='available'>&nbsp;&#x2714; This username is available</span>")
