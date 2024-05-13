import enum
from csit314.app import db
from flask import flash
class Role(enum.Enum):
    SELLER = 'seller'
    BUYER = 'buyer'
    AGENT = 'agent'
    ADMIN = 'admin'

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    #phone = db.Column(db.String(250), nullable=False, unique=True)
    firstName = db.Column(db.String)
    lastName = db.Column(db.String)
    role = db.Column(db.Enum(Role, values_callable=lambda x: [str(member.value) for member in Role]), nullable=False)

    @classmethod
    def findAUserByUserID(cls, userid: str) -> "User | None":
        """
        Find a user by user ID.
        :param userid: The user ID to search for.
        :return: The user object if found, otherwise None.
        """
        return cls.query.filter_by(userid=userid).one_or_none()

    @classmethod
    def searchAllUsers(cls) -> list["User"]:
        """
        Retrieve all users from the database.
        :return: A list of User objects.
        """
        return cls.query.all()

    @classmethod
    def createNewUser(cls, user_details: dict) -> bool:
        """
        Create a new user with the provided details.
        :param user_details: A dictionary containing user details.
        :return: True if the user was successfully created, False otherwise.
        """
        userid = cls.query.filter_by(userid=user_details["userid"]).one_or_none()
        email = cls.query.filter_by(email=user_details["email"]).one_or_none()
        if userid or email:
            # Reject creation of a user with already registered userid or email
            return False
        if user_details.get('role') == Role.ADMIN.value:
            # Reject creation of a user with the role as Admin
            return False
        # Create a new user
        new_user = cls(**user_details)
        db.session.add(new_user)
        db.session.commit()
        return True



