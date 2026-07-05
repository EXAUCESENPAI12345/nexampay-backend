from database import create_tables
from config import APP_NAME, VERSION

def start():
    print("=" * 40)
    print(f"{APP_NAME} Backend")
    print(f"Version : {VERSION}")
    print("=" * 40)

    print("Initialisation de la base de données...")
    create_tables()

    print("Base de données prête.")
    print("Backend NexamPay démarré avec succès.")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    start()
