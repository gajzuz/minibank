from auth_service.app import db, User, Transaction


def seed_auth_service():
    # Seed Users
    if not User.query.first():  # Check if users exist, if not, seed
        users = [
            User(id="user1", password="password123"),
            User(id="user2", password="pass456"),
        ]
        db.session.add_all(users)
        db.session.commit()
        print("✅ Seeded users in auth-service.")


if __name__ == "__main__":
    seed_auth_service()
