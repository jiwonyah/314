import enum
from csit314.app import db
from . import User
from csit314.entity.User import User,Role
from sqlalchemy.orm import validates
from datetime import datetime
from flask import g

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

class PropertyImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('propertyListing.id'), nullable=False)
    @classmethod
    def createImage(cls, filename, property_id):
        new_image = cls(filename=filename, property_id=property_id)
        db.session.add(new_image)
        db.session.commit()
        return new_image

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
    is_sold = db.Column(db.Boolean(), default=False)
    images = db.relationship('PropertyImage', backref='propertyListing', lazy='dynamic')

    @validates('client_id')
    def validate_client_id(self, key, client_id):
        # Check if the userid exists in the User table
        user_with_client_id = User.query.filter_by(userid=client_id).first()
        if not user_with_client_id:
            raise ValueError('The provided userid does not exist')
        # Check if the provided client_id corresponds to a seller user
        seller_user = User.query.filter_by(userid=client_id, role=Role.SELLER).first()
        if not seller_user:
            raise ValueError('The client must correspond to a seller user')
        return client_id

    @classmethod
    def displayAllPropertyListing(cls):
        property_listings = PropertyListing.query.order_by(PropertyListing.create_date.desc()).all()
        return property_listings

    @classmethod
    def createPropertyListing(cls, details: dict, image_files: list = None) -> bool:
        agent_id = details.get('agent_id')
        agent = User.query.filter_by(id=agent_id, role=Role.AGENT.value).first()
        if not agent:
            return False
        required_fields = ['subject', 'price', 'address', 'floorSize', 'floorLevel', 'propertyType', 'furnishing',
                           'builtYear', 'client_id']
        if not all(field in details for field in required_fields):
            return False
        new_listing = cls(**details, create_date=datetime.now())
        db.session.add(new_listing)
        db.session.commit()
        if image_files:
            for image_file in image_files:
                new_image = PropertyImage.createImage(filename=image_file, property_id=new_listing.id)
                db.session.add(new_image)
        db.session.commit()
        return True

    @classmethod
    def editPropertyListing(cls, details: dict) -> bool:
        try:
            listing_id = details.get('id')
            listing = PropertyListing.query.get(listing_id)
            if not listing:
                return False
            if 'subject' in details:
                listing.subject = details['subject']
            if 'content' in details:
                listing.content = details['content']
            if 'price' in details:
                listing.price = details['price']
            if 'address' in details:
                listing.address = details['address']
            if 'floorSize' in details:
                listing.floorSize = details['floorSize']
            if 'floorLevel' in details:
                listing.floorLevel = FloorLevel(details['floorLevel'])
            if 'propertyType' in details:
                listing.propertyType = PropertyType(details['propertyType'])
            if 'furnishing' in details:
                listing.furnishing = Furnishing(details['furnishing'])
            if 'builtYear' in details:
                listing.builtYear = details['builtYear']
            if 'modify_date' in details:
                listing.modify_date = datetime.now()
            if 'is_sold' in details:
                listing.is_sold = details['is_sold']
            db.session.commit()
            return True
        except Exception as e:
            print(f"부동산 리스트 수정에 실패했습니다: {e}")
            db.session.rollback()
            return False

    @classmethod
    def getPropertyListing(cls, listing_id: int):
        return cls.query.filter_by(id=listing_id).one_or_none()

    @classmethod
    def removePropertyListing(cls, listing_id: int) -> bool:
        property_listing = cls.getPropertyListing(listing_id)
        if not property_listing:
            return False
        if not g.user:
            return False  # 로그인되지 않은 경우 삭제 권한 없음
        # 로그인된 사용자가 해당 부동산 리스트의 에이전트(등록자)인지 확인
        if property_listing.agent_id != g.user.id:
            return False  # 삭제 권한 없음
        db.session.delete(property_listing)
        db.session.commit()
        return True

    @classmethod
    def displayAllSoldPropertyListing(cls):
        return cls.query.filter_by(is_sold=True).order_by(cls.create_date.desc()).all()

    @classmethod
    def displayAllNotSoldPropertyListing(cls):
        return cls.query.filter_by(is_sold=False).order_by(cls.create_date.desc()).all()






