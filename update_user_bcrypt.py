import bcrypt
import mysql.connector

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

conn = mysql.connector.connect(
    host='mariadb',
    user='Marais_R_Site_User',
    password='Marais_R_Site_User/123',
    database='Marais_R_Site'
)
cursor = conn.cursor()

hashed = hash_password("ADMIN")

cursor.execute(
    "UPDATE utilisateur SET mot_de_passe_utilisateur = %s WHERE nom_utilisateur = 'USER_TEST'",
    (hashed,)
)
conn.commit()
cursor.close()
conn.close()

print("✅ Utilisateur mis à jour avec bcrypt")
print("Hash :", hashed)