from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .models import UserFollows, Ticket, Review
from authentication.models import User
from itertools import chain

from . import forms


# get the user's feed according to his subscriptions
@login_required
def home(request):
    # find users that are followed by current user
    followed_users = UserFollows.objects.filter(user=request.user).values('followed_user')
    # find tickets created by followed users found previously
    followed_tickets = Ticket.objects.filter(user__in=followed_users)
    # find user tickets
    user_tickets = Ticket.objects.filter(user=request.user)
    # merge ticket queries
    tickets = followed_tickets.union(user_tickets)
    # find reviews created by followed users found previously
    followed_reviews = Review.objects.filter(user__in=followed_users)
    # find user reviews
    user_reviews = Review.objects.filter(user=request.user)
    # find reviews made on user tickets
    user_ticket_reviews = Review.objects.filter(ticket__in=user_tickets)
    # merge of reviews queries
    reviews = followed_reviews.union(user_reviews).union(user_ticket_reviews)
    # sort reviews and tickets by date
    all_tickets = sorted(chain(tickets, reviews),
                         key=lambda instance: instance.time_created,
                         reverse=True)
    tickets_dict = {}
    # find for each ticket if a review has been written
    for ticket in all_tickets:
        if ticket.__class__.__name__ == 'Ticket':
            reviewed = Review.objects.filter(ticket=ticket)
            if not reviewed:
                tickets_dict[ticket] = 'No'
            else:
                tickets_dict[ticket] = 'Yes'
        else:
            tickets_dict[ticket] = 'Review'
    return render(request, 'reviews/home.html', context={'tickets': tickets_dict})


@login_required
def posts(request):
    # find user tickets
    user_tickets = Ticket.objects.filter(user=request.user)
    # find user reviews
    user_reviews = Review.objects.filter(user=request.user)
    # sort reviews and tickets by date
    all_tickets = sorted(chain(user_tickets, user_reviews),
                         key=lambda instance: instance.time_created,
                         reverse=True)
    return render(request, 'reviews/posts.html', context={'tickets': all_tickets})


@login_required
def edit_ticket(request, ticket_id):
    # get ticket of the url
    ticket = get_object_or_404(Ticket, id=ticket_id)
    # check if the user is the owner of the ticket
    if request.user == ticket.user:
        edit_form = forms.TicketForm(instance=ticket)
        if request.method == 'POST':
            if 'edit_ticket' in request.POST:
                edit_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
                if edit_form.is_valid():
                    # fill the ticket information with the user and save the new data
                    modified_ticket = edit_form.save(commit=False)
                    modified_ticket.user = request.user
                    modified_ticket.save()
                    return redirect('posts')
        return render(request, 'reviews/edit_ticket.html', context={'edit_form': edit_form,
                                                                    'ticket': ticket})
    else:
        return redirect('home')


@login_required
def delete_ticket(request, ticket_id):
    # get ticket of the url
    ticket = get_object_or_404(Ticket, id=ticket_id)
    # check if the user is the owner of the ticket
    if request.user == ticket.user:
        # delete the ticket
        ticket.delete()
        return redirect('posts')
    else:
        return redirect('home')


@login_required
def edit_review(request, ticket_id):
    # get ticket of the url
    ticket = get_object_or_404(Ticket, id=ticket_id)
    # get review of the ticket
    review = get_object_or_404(Review, ticket=ticket)
    # check if the user is the owner of the review
    if request.user == review.user:
        edit_form = forms.ReviewForm(instance=review)
        if request.method == 'POST':
            if 'edit_review' in request.POST:
                edit_form = forms.ReviewForm(request.POST, instance=review)
                if edit_form.is_valid():
                    # fill the review information with the user and save the new data
                    modified_review = edit_form.save(commit=False)
                    modified_review.user = request.user
                    modified_review.ticket = ticket
                    modified_review.save()
                    return redirect('posts')
        return render(request, 'reviews/edit_review.html', context={'edit_form': edit_form,
                                                                    'ticket': ticket,
                                                                    'review': review})
    else:
        return redirect('home')


@login_required
def delete_review(request, ticket_id):
    # get ticket of the url
    ticket = get_object_or_404(Ticket, id=ticket_id)
    # get review of the ticket
    review = get_object_or_404(Review, ticket=ticket)
    # check if the user is the owner of the ticket
    if request.user == review.user:
        # delete review
        review.delete()
        return redirect('posts')
    else:
        return redirect('home')


class TicketView(LoginRequiredMixin, View):
    ticket_form = forms.TicketForm
    template_name = 'reviews/ticket.html'

    def get(self, request):
        ticket_form = self.ticket_form()
        return render(request, self.template_name, context={'ticket_form': ticket_form})

    def post(self, request):
        ticket_form = self.ticket_form(request.POST, request.FILES)
        if ticket_form.is_valid():
            # take the ticket data from form and save it in Ticket
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('posts')


class ReviewView(LoginRequiredMixin, View):
    review_form = forms.ReviewForm
    ticket_form = forms.TicketForm
    template_name = 'reviews/review.html'

    def get(self, request):
        ticket_form = self.ticket_form
        review_form = self.review_form
        return render(request, self.template_name, context={'ticket_form': ticket_form,
                                                            'review_form': review_form})

    def post(self, request):
        ticket_form = self.ticket_form(request.POST)
        if ticket_form.is_valid():
            # saved ticket is pending
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            review_form = self.review_form(request.POST)
            if review_form.is_valid():
                # saved review is pending
                review = review_form.save(commit=False)
                review.ticket = ticket
                review.user = request.user
                # save ticket and review
                ticket.save()
                review.save()
                return redirect('posts')


class ReviewTicketView(LoginRequiredMixin, View):
    review_form = forms.ReviewForm
    template_name = 'reviews/review.html'

    def get(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        message = ticket
        review_form = self.review_form
        return render(request, self.template_name, context={'ticket': ticket,
                                                            'review_form': review_form,
                                                            'message': message})

    def post(self, request, ticket_id):
        review_form = self.review_form(request.POST)
        ticket = Ticket.objects.get(id=ticket_id)
        reviewed = Review.objects.filter(ticket=ticket)
        if not reviewed:
            if review_form.is_valid():
                # review save is pending
                review = review_form.save(commit=False)
                review.ticket = ticket
                review.user = request.user
                # save review
                review.save()
                return redirect('posts')


class SubscribeView(LoginRequiredMixin, View):
    subscribe_form = forms.SubscribeForm
    template_name = 'reviews/abonnements.html'

    def get(self, request):
        subscribe_form = self.subscribe_form()
        # find users that are being followed by logged user
        followed_users = UserFollows.objects.filter(user=request.user)
        # find users that are following logged user
        followers = UserFollows.objects.filter(followed_user=request.user)
        return render(request, self.template_name, context={'subscribe_form': subscribe_form,
                                                            'followed_users': followed_users,
                                                            'followers': followers})

    def post(self, request):
        # find users that are being followed by logged use
        followed_users = UserFollows.objects.filter(user=request.user)
        # find users that are following logged user
        followers = UserFollows.objects.filter(followed_user=request.user)
        subscribe_form = self.subscribe_form()
        message = ''
        users = User.objects.all()
        # check that in POST data username is in it
        if 'username' in request.POST:
            subscribe_form = self.subscribe_form(request.POST)
            if subscribe_form.is_valid():
                user_to_follow = subscribe_form.cleaned_data['username']
                # checks that username entered is not current user
                if user_to_follow == str(request.user.username):
                    message = "Vous ne pouvez vous abonner à voter propre compte"
                else:
                    try:
                        # find user object corresponding to the one entered in subscribe form
                        obj_user_to_follow = User.objects.get(username=user_to_follow)
                        # checks that user exists in the database
                        if obj_user_to_follow in users:
                            already_followed = False
                            # find if user is already followed
                            for f_user in followed_users:
                                if user_to_follow == f_user.followed_user.username:
                                    message = 'User already followed'
                                    already_followed = True
                                    break
                            # if user is not followed then current with user will follow it
                            if not already_followed:
                                following = UserFollows(user=request.user,
                                                        followed_user=obj_user_to_follow)
                                following.save()
                                message = f"You are following now {user_to_follow}"
                                followed_users = UserFollows.objects.filter(user=request.user)
                    # manage exception when user does not exist in the db
                    except User.DoesNotExist:
                        followed_users = UserFollows.objects.filter(user=request.user)
                        message = "Utilisateur inconnu"
                return render(request, self.template_name, context={'subscribe_form': subscribe_form,
                                                                    'followed_users': followed_users,
                                                                    'followers': followers,
                                                                    'message': message})
        # checks that in POST request unsubscribe exists
        if 'unsubscribe' in request.POST:
            # find users that are being followed by logged use
            followed_users = UserFollows.objects.filter(user=request.user)
            # get username to be unfollowed
            user_to_unfollow = request.POST['unsubscribe']
            # find the user that is to be unfollowed and delete the relation to it
            for followed_user in followed_users:
                if followed_user.followed_user.username == user_to_unfollow:
                    unfollowed_user = UserFollows.objects.get(user=request.user,
                                                              followed_user=followed_user.followed_user)
                    unfollowed_user.delete()
                    message = f"Vous ne suivez plus {followed_user.followed_user.username}"
                    break
            # refresh the followers and followed users        
            followers = UserFollows.objects.filter(followed_user=request.user)
            followed_users = UserFollows.objects.filter(user=request.user)
            return render(request, self.template_name, context={'subscribe_form': subscribe_form,
                                                                'followed_users': followed_users,
                                                                'followers': followers,
                                                                'message': message})
