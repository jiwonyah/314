import enum
from csit314.app import db
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

    # Define relationship with Post
    #propertyListing = relationship("PropertyListing", back_populates="author")

    # Define relationship with Favorite
    #oldPropertyListing = relationship("OldPropertyListing", back_populates="user")
