import enum
from csit314.app import db
from . import User
from . import Favourite

#enum type data
class FloorLevel(enum.Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class PropertyType(enum.Enum):
    HDB = 'hdb'
    CONDO = 'condo'
    APARTMENT = 'apartment'
    STUDIO = 'studio'

class Furnishing(enum.Enum):
    PartiallyFurnished = 'partially_furnished'
    FullyFurnished = 'fully_furnished'
    NotFurnished = 'not_furnished'

class PropertyListing(db.Model):
    __tablename__ = 'propertyListing'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    floorSize = db.Column(db.Integer, nullable=False)
    floorLevel = db.Column(db.Enum(FloorLevel, values_callable=lambda x: [str(member.value) for member in FloorLevel]), nullable=False)
    propertyType = db.Column(db.Enum(PropertyType, values_callable=lambda x: [str(member.value) for member in PropertyType]), nullable=False)
    furnishing = db.Column(db.Enum(Furnishing, values_callable=lambda x: [str(member.value) for member in Furnishing]), nullable=False)
    builtYear = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('propertyListing_set'))
    favourites = db.relationship('Favourite', back_populates='propertyListing', lazy='dynamic')
    shortlist_count = db.Column(db.Integer, default=0)
