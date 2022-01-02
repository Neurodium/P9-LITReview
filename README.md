# P9-LITReview
 WebSite for reviewing books

# Setup virtual environment
python3.5 -m venv venv/

# Activate virtual environment
source venv/bin/activate

# Clone project
git clone https://github.com/Neurodium/P9-LITReview.git

# Install dependencies
run pip install -r src/requirements.txt

# Initialize database
 run manage.py migrate

# Launch Server
run manage.py runserver

# Django application access
Go to: http://127.0.0.1:8000/

# Features
[Register] http://127.0.0.1:8000/register/<br>
&nbsp;&nbsp;Create your account
  
[Login] http://127.0.0.1:8000/<br>
&nbsp;&nbsp;Log into your account with your credentials 
  
[Flux] http://127.0.0.1:8000/home/<br>
&nbsp;&nbsp;Your tickets and reviews and also the ones of the users you follow <br>
&nbsp;&nbsp;Create a review or create a ticket to ask for a review
  
[Posts] http://127.0.0.1:8000/posts<br>
&nbsp;&nbsp;The tickets or reviews you have created 
  
[Abonnements] http://127.0.0.1:8000/abonnements/<br>
&nbsp;&nbsp;Manage the users you want to follow

[YourUsername] http://127.0.0.1:8000/password-change/<br>
&nbsp;&nbsp;Change your password
  
[Se déconnecter] http://127.0.0.1:8000/logout/<br>
&nbsp;&nbsp;Disconnect from website
