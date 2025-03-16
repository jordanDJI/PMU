import requests
import pandas as pd
import re

# URL de l'API (exemple fictif)
api_url = "https://api.exemple.com/users"

# Récupérer les données de l'API
response = requests.get(api_url)
if response.status_code != 200:
    print("Erreur lors de la récupération des données")
else:
    data = response.json()

# Afficher un échantillon des données récupérées
print(data[:2])  # Affiche les deux premiers utilisateurs (si plusieurs sont renvoyés)

# Fonction de validation des données
def validate_user_data(user):
    # Vérifier que les champs essentiels sont présents
    required_fields = ['name', 'email', 'age', 'country']
    for field in required_fields:
        if field not in user:
            return False, f"Missing {field} field"
    
    # Vérifier que l'email est valide
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, user['email']):
        return False, f"Invalid email: {user['email']}"
    
    # Vérifier que l'âge est un nombre valide (positif)
    if not isinstance(user['age'], int) or user['age'] < 0:
        return False, f"Invalid age: {user['age']}"
    
    # Vérifier que le pays est un code valide (exemple simplifié)
    valid_countries = ['US', 'FR', 'DE', 'IT', 'ES']
    if user['country'] not in valid_countries:
        return False, f"Invalid country: {user['country']}"
    
    return True, "Data is valid"

# Fonction de nettoyage des données
def clean_user_data(user):
    # Convertir l'email en minuscules
    user['email'] = user['email'].lower()
    
    # Transformer le pays en code ISO (si nécessaire)
    country_mapping = {'France': 'FR', 'Germany': 'DE', 'Italy': 'IT'}
    if user['country'] in country_mapping:
        user['country'] = country_mapping[user['country']]
    
    # Retourner les données nettoyées
    return user

# Appliquer la qualification (validation et nettoyage) sur chaque utilisateur
qualified_data = []
for user in data:
    is_valid, message = validate_user_data(user)
    if is_valid:
        cleaned_user = clean_user_data(user)
        qualified_data.append(cleaned_user)
    else:
        print(f"Data issue: {message} - Skipping user {user.get('name', 'Unknown')}")

# Convertir les données qualifiées en DataFrame pour une analyse plus facile
df = pd.DataFrame(qualified_data)

# Afficher les données qualifiées
print(df.head())

# Sauvegarder les données qualifiées (par exemple, dans un fichier CSV)
df.to_csv('qualified_users.csv', index=False)
