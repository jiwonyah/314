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
    firstName = db.Column(db.String)
    lastName = db.Column(db.String)
    role = db.Column(db.Enum(Role, values_callable=lambda x: [str(member.value) for member in Role]), nullable=False)
    status = db.Column(db.String(50))

    def serialize_enum(self):
        return self.role.value

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
        This class method is for user sign up.
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
    # ---------------------------------admin function-------------------------------------------
    @classmethod
    def createUserAccount(cls, accountDetails: dict):
        userid = cls.query.filter_by(userid=accountDetails["username"]).one_or_none()
        email = cls.query.filter_by(email=accountDetails["email"]).one_or_none()
        if userid or email:
            return False
        new_account = cls(**accountDetails)
        db.session.add(new_account)
        db.session.commit()
        return True

    @classmethod
    def useridExists(cls, accountDetails):
        return cls.query.filter_by(userid=accountDetails["userid"]).one_or_none()

    @classmethod
    def emailExists(cls, accountDetails):
        return cls.query.filter_by(email=accountDetails["email"]).one_or_none()

    @classmethod
    def getUserAccounts(cls):
        return cls.query.all()

    @classmethod
    def getUserDetails(cls, userid):
        return cls.query.filter_by(userid=userid).first()

    @classmethod
    def updateUserAccount(cls, userid, updateDetails):
        user = cls.getUserDetails(userid)
        new_email = updateDetails.get('email')
        new_userid = updateDetails.get('userid')

        if new_email and new_email != user.email:
            if cls.emailExists(updateDetails):
                return False

        if new_userid and new_userid != user.userid:
            if cls.useridExists(updateDetails):
                return False

        user.firstName = updateDetails.get('firstName', user.firstName)
        user.lastName = updateDetails.get('lastName', user.lastName)
        user.email = new_email or user.email
        user.userid = new_userid or user.userid
        user.password = updateDetails.get('password', user.password)
        user.Role = updateDetails.get('role', user.Role)
        user.status = updateDetails.get('status', user.status)

        db.session.commit()
        return True

    @classmethod
    def search_account(cls, searchQuery):
        accounts = cls.query.filter(cls.userid.ilike(f'%{searchQuery}%')).all()
        if not accounts:
            return None
        return [account.serialize() for account in accounts]

    def serialize(self):
        return {
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'userid': self.userid,
            'password': self.password,
            'role': self.Role,
            'status': self.status
        }

    @classmethod
    def suspend_account(cls, userid):
        account = cls.getUserDetails(userid)
        if account.status == 'Active':
            account.status = 'Suspended'
            db.session.commit()
            return True
        else:
            return False



