import bcrypt

from database.db import SessionLocal
from database.models import User


# ===========================================
# HASH PASSWORD
# ===========================================

def hash_password(password: str) -> str:
    """
    Convert plain password into hashed password.
    """
    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")


# ===========================================
# VERIFY PASSWORD
# ===========================================

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify user password.
    """
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


# ===========================================
# REGISTER USER
# ===========================================

def register_user(full_name, email, password):

    db = SessionLocal()

    try:

        existing_user = db.query(User).filter(
            User.email == email
        ).first()

        if existing_user:

            return False, "Email already registered."

        new_user = User(

            full_name=full_name,

            email=email,

            password=hash_password(password)

        )

        db.add(new_user)

        db.commit()

        return True, "Registration Successful."

    except Exception as e:

        db.rollback()

        return False, str(e)

    finally:

        db.close()


# ===========================================
# LOGIN USER
# ===========================================

def login_user(email, password):

    db = SessionLocal()

    try:

        user = db.query(User).filter(
            User.email == email
        ).first()

        if not user:

            return False, "User not found."

        if verify_password(password, user.password):

            return True, user

        return False, "Invalid Password."

    finally:

        db.close()