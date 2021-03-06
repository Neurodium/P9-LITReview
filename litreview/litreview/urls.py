"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView

import reviews.views
import authentication.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.LoginPage.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='authentication/login.html',
                                      redirect_field_name='login'),
         name='logout'),
    path('password-change/', PasswordChangeView.as_view(template_name='authentication/password_change.html'),
         name='password-change'
         ),
    path('password-change-done/', PasswordChangeDoneView.as_view(template_name='authentication/password_change_done.html'),
         name='password-change-done'
         ),
    path('home/', reviews.views.home, name='home'),
    path('register/', authentication.views.register, name='register'),
    path('posts', reviews.views.posts, name='posts'),
    path('ticket', reviews.views.TicketView.as_view(), name='ticket'),
    path('review/', reviews.views.ReviewView.as_view(), name='review'),
    path('review/<int:ticket_id>', reviews.views.ReviewTicketView.as_view(), name='review_ticket'),
    path('abonnements/', reviews.views.SubscribeView.as_view(), name='abonnements'),
    path('edit_ticket/<int:ticket_id>', reviews.views.edit_ticket, name='edit_ticket'),
    path('delete_ticket/<int:ticket_id>', reviews.views.delete_ticket, name='delete_ticket'),
    path('edit_review/<int:ticket_id>', reviews.views.edit_review, name='edit_review'),
    path('delete_review/<int:ticket_id>', reviews.views.delete_review, name='delete_review'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)