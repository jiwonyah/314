from csit314.app import db


class UserAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    role = db.Column(db.String(50))
    status = db.Column(db.String(50))

    @classmethod
    def createUserAccount(cls, accountDetails: dict):
        username = cls.query.filter_by(username=accountDetails["username"]).one_or_none()
        email = cls.query.filter_by(email=accountDetails["email"]).one_or_none()
        if username or email:
            return False
        new_account = cls(**accountDetails)
        db.session.add(new_account)
        db.session.commit()
        return True

    @classmethod
    def usernameExists(cls, accountDetails):
        return cls.query.filter_by(username=accountDetails["username"]).one_or_none()

    @classmethod
    def emailExists(cls, accountDetails):
        return cls.query.filter_by(email=accountDetails["email"]).one_or_none()

    @classmethod
    def getUserAccounts(cls):
        return cls.query.all()

    @classmethod
    def getUserDetails(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def updateUserAccount(cls, username, updateDetails):
        user = cls.getUserDetails(username)
        new_email = updateDetails.get('email')
        new_username = updateDetails.get('username')

        if new_email and new_email != user.email:
            if cls.emailExists(updateDetails):
                return False

        if new_username and new_username != user.username:
            if cls.usernameExists(updateDetails):
                return False

        user.full_name = updateDetails.get('full_name', user.full_name)
        user.email = new_email or user.email
        user.username = new_username or user.username
        user.password = updateDetails.get('password', user.password)
        user.role = updateDetails.get('role', user.role)
        user.status = updateDetails.get('status', user.status)

        db.session.commit()
        return True

    @classmethod
    def search_account(cls, searchQuery):
        accounts = cls.query.filter(cls.username.ilike(f'%{searchQuery}%')).all()
        if not accounts:
            return None
        return [account.serialize() for account in accounts]

    def serialize(self):
        return {
            'full_name': self.full_name,
            'email': self.email,
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'status': self.status
        }

    @classmethod
    def suspend_account(cls, username):
        account = cls.getUserDetails(username)
        if account.status == 'Active':
            account.status = 'Suspended'
            db.session.commit()
            return True
        else:
            return False
