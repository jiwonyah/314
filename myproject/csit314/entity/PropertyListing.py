import enum

from sqlalchemy import true

from csit314.app import db
from csit314.entity.User import User,Role
from sqlalchemy.orm import validates
from datetime import datetime
from flask import current_app, g, session

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
    modify_date = db.Column(db.DateTime(), nullable=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    agent = db.relationship('User', foreign_keys=[agent_id], backref=db.backref('property_listing_set'))
    client_id = db.Column(db.String, db.ForeignKey('user.userid', ondelete='CASCADE'), nullable=False)
    client = db.relationship('User', foreign_keys=[client_id], backref=db.backref('client_property_listings'))
    view_counts = db.Column(db.Integer, default=0, nullable=False)
    favourites = db.relationship('Favourite', back_populates='propertyListing', lazy='dynamic')
    shortlist_count = db.Column(db.Integer, default=0)
    is_sold = db.Column(db.Boolean(), default=False)

    @classmethod
    def sortByMostView(cls, client_id: int):
        return cls.query.filter_by(client_id=client_id).order_by(
            PropertyListing.view_counts.desc()).all()

    @classmethod
    def sortByMostFavourite(cls, client_id: int):
        return cls.query.filter_by(client_id=client_id).order_by(
            PropertyListing.shortlist_count.desc()).all()

    @classmethod
    def sortByRecent(cls, client_id: int):
        return cls.query.filter_by(client_id=client_id).order_by(
            PropertyListing.create_date.desc()).all()
