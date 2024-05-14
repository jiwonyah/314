from csit314.app import db

class UserProfile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    profileName = db.Column(db.String(50), unique=True)
    profileDescription = db.Column(db.String(50))

    @classmethod
    def createUserProfile(cls, profileDetails: dict):
        profileName = cls.query.filter_by(profileName=profileDetails["profileName"]).one_or_none()
        if profileName:
            return False
        new_profile = cls(**profileDetails)
        db.session.add(new_profile)
        db.session.commit()
        return True

    @classmethod
    def profileNameExists(cls, profileDetails):
        return cls.query.filter_by(profileName=profileDetails["profileName"]).one_or_none()
