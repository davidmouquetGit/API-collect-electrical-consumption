import psycopg2
from psycopg2 import sql

# Configuration de la connexion à la base de données RDS
db_config = {
    "host": "conso.cr2m0qmgsjvc.eu-north-1.rds.amazonaws.com",
    "database": "conso",
    "user": "postgres",
    "password": "Labrax_007",
}

# Chemin vers ton fichier CSV sur EC2
csv_file_path = "courbecharge.csv"

# Nom de la table dans PostgreSQL
table_name = "consohoraire"

def import_csv_to_postgresql(conn, csv_file_path):
    with conn.cursor() as cursor:
        with open(csv_file_path, "r") as f:
            # Ignore la première ligne (en-tête)
            next(f)
            # Utilise une table temporaire pour éviter les conflits
            cursor.execute(
                sql.SQL("""
                    CREATE TEMP TABLE temp_import AS
                    SELECT * FROM {} LIMIT 0
                """).format(sql.Identifier(table_name))
            )
            # Import dans la table temporaire
            cursor.copy_expert(
                sql.SQL("""
                    COPY temp_import (timestamp, value)
                    FROM STDIN
                    WITH (FORMAT csv, DELIMITER ',')
                """),
                f,
            )
            # Insère les données en ignorant les doublons
            cursor.execute(
                sql.SQL("""
                    INSERT INTO {}
                    SELECT * FROM temp_import
                    ON CONFLICT (timestamp) DO NOTHING
                """).format(sql.Identifier(table_name))
            )
        conn.commit()

# Connexion à la base de données et exécution
try:
    conn = psycopg2.connect(**db_config)
    print("Connexion à la base de données réussie.")
    import_csv_to_postgresql(conn, csv_file_path)
    print("Données importées avec succès !")
except Exception as e:
    print(f"Erreur : {e}")
finally:
    if conn is not None:
        conn.close()
        print("Connexion fermée.")
