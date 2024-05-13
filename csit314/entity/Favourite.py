from csit314.app import db

class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_userid = db.Column(db.String(32), db.ForeignKey('user.userid', ondelete='CASCADE'), nullable=False)
    propertyListing_id = db.Column(db.Integer, db.ForeignKey('propertyListing.id', ondelete='CASCADE'), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    # Add relationship with PropertyListing model
    propertyListing = db.relationship('PropertyListing', back_populates='favourites') # backref=db.backref('favourites')
