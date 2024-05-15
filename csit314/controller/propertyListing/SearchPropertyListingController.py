from flask import request, jsonify, Blueprint
from csit314.entity.PropertyListing import PropertyListing
from sqlalchemy import or_

class SearchPropertyListingController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/search_property_listings/", view_func=self.search_property_listings, methods=['GET'])

    def search_property_listings(self):
        search_query = request.args.get('query')
        if not search_query:
            return jsonify([])
        property_listings = PropertyListing.query.filter(PropertyListing.subject.ilike(f'%{search_query}%')).all()
        result = []
        for listing in property_listings:
            result.append({
                'id': listing.id,
                'subject': listing.subject,
                'create_date': listing.create_date.strftime('%Y-%m-%d')
            })
        return jsonify(result)
