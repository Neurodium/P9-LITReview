# P9-LITReview
 WebSite for reviewing books

# Setup vitrual environment
python3.5 -m venv env/


# Activation de cet environnement
source env/bin/activate

# Clonage du projet - récupération des sources
# Actuellement, la branche par défaut du projet est develop
# Ce sera celle qui sera active par défaut immédiatement après le clonage
git clone https://github.com/neogeo-technologies/geocontrib.git src/

# Installer les dépendances
pip install -r src/requirements.txt

# Création d'un projet Django
django-admin startproject config .

# Création de liens symboliques pour que les sources soient visibles par Django
ln -s src/geocontrib/ .
ln -s src/api/ .
