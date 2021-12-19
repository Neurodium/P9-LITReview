# P9-LITReview
 WebSite for reviewing books

# Setup virtual environment
python3.5 -m venv venv/

# Activate virtual environment
source venv/bin/activate

# Clone project
git clone https://github.com/Neurodium/P9-LITReview.git

# Install dependencies
pip install -r src/requirements.txt

# Initialize database
manage.py migrate

# Features
[Register] http://127.0.0.1:8000/register/<br>
  Create your account
  
[Login] http://127.0.0.1:8000/
  Log into your account with your credentials 
  
[Flux] http://127.0.0.1:8000/home/
  Your tickets and reviews and also the ones of the users you follow 
  Create a review or create a ticket to ask for a review
  
[Posts] http://127.0.0.1:8000/posts
  The tickets or reviews you have created 
  
[Abonnements] http://127.0.0.1:8000/abonnements/
  Manage the users you want to follow

[YourUsername] http://127.0.0.1:8000/password-change/
  Change your password
  
[Se déconnecter] http://127.0.0.1:8000/logout/
  Disconnect from website
