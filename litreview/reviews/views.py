from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View
from .models import UserFollows, Ticket
from authentication.models import User

from . import forms


@login_required
def home(request):
    followed_users = UserFollows.objects.filter(user=request.user).values('followed_user')
    followed_tickets = Ticket.objects.filter(user__in=followed_users)
    user_tickets = Ticket.objects.filter(user=request.user)
    tickets = followed_tickets.union(user_tickets).order_by('-time_created')
    message = ''
    return render(request, 'reviews/home.html', context={'tickets': tickets,
                                                         'message': message})


@login_required
def posts(request):
    user_tickets = Ticket.objects.filter(user=request.user).order_by('-time_created')
    message=''
    return render(request, 'reviews/posts.html', context={'tickets': user_tickets,
                                                         'message': message})



class TicketView(LoginRequiredMixin, View):
    ticket_form = forms.TicketForm
    template_name = 'reviews/ticket.html'

    def get(self, request):
        ticket_form = self.ticket_form()
        return render(request, self.template_name, context={'ticket_form': ticket_form})


    def post(self, request):
        ticket_form = self.ticket_form(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            message = "Votre ticket a été créé"
        return render(request, self.template_name, context={'ticket_form': ticket_form,
                                                                'message': message})


class ReviewView(LoginRequiredMixin, View):
    review_form = forms.ReviewForm
    ticket_form = forms.TicketForm
    template_name = 'reviews/review.html'

    def get(self, request):
        ticket_form = self.ticket_form
        review_form = self.review_form
        return render(request, self.template_name, context={'ticket_form': ticket_form,
                                                            'review_form': review_form})

"""    def post(self, request):
        ticket_form = self.ticket_form(request.POST)
        if ticket_form is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user

        review_form = self.review_form(request.POST)
"""


class SubscribeView(LoginRequiredMixin, View):
    subscribe_form = forms.SubscribeForm
    template_name = 'reviews/abonnements.html'


    def get(self, request):
        subscribe_form = self.subscribe_form()
        followed_users = UserFollows.objects.filter(user=request.user)
        followers = UserFollows.objects.filter(followed_user=request.user)
        return render(request, self.template_name, context={'subscribe_form': subscribe_form,
                                                            'followed_users': followed_users,
                                                            'followers': followers})

    def post(self, request):
        followed_users = UserFollows.objects.filter(user=request.user)
        followers = UserFollows.objects.filter(followed_user=request.user)
        subscribe_form = self.subscribe_form()
        message = ''
        users = User.objects.all()
        if 'username' in request.POST:
            subscribe_form = self.subscribe_form(request.POST)
            if subscribe_form.is_valid():
                user_to_follow = subscribe_form.cleaned_data['username']
                if user_to_follow == str(request.user.username):
                    message = "Vous ne pouvez vous abonner à voter propre compte"
                else:
                    try:
                        obj_user_to_follow = User.objects.get(username=user_to_follow)
                        if obj_user_to_follow in users:
                            already_followed = False
                            for f_user in followed_users:
                                if user_to_follow == f_user.followed_user.username:
                                    message = 'User already followed'
                                    already_followed = True
                                    break
                            if already_followed == False:
                                following = UserFollows(user=request.user,
                                                        followed_user=obj_user_to_follow)
                                following.save()
                                message = f"You are following now {user_to_follow}"
                                followed_users = UserFollows.objects.filter(user=request.user)
                    except User.DoesNotExist:
                        followed_users = UserFollows.objects.filter(user=request.user)
                        message = "Utilisateur inconnu"
                return render(request, self.template_name, context={'subscribe_form': subscribe_form,
                                                                    'followed_users': followed_users,
                                                                    'followers': followers,
                                                                    'message': message})
        if 'unsubscribe' in request.POST:
            followed_users = UserFollows.objects.filter(user=request.user)
            user_to_unfollow = request.POST['unsubscribe']
            for followed_user in followed_users:
                if followed_user.followed_user.username == user_to_unfollow:
                    unfollowed_user = UserFollows.objects.get(user=request.user,
                                                               followed_user=followed_user.followed_user)
                    unfollowed_user.delete()
                    message = f"Vous ne suivez plus {followed_user.followed_user.username}"
                    break
            followers = UserFollows.objects.filter(followed_user=request.user)
            followed_users = UserFollows.objects.filter(user=request.user)
            return render(request, self.template_name, context={'subscribe_form': subscribe_form,
                                                                'followed_users': followed_users,
                                                                'followers': followers,
                                                                'message': message})



