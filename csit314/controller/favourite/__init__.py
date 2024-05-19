from .BuyerSavePropertyListingController import BuyerSavePropertyListingController
from .SellerViewSaveCountController import SellerViewSaveCountController
from .ViewSavedPropertyListingController import ViewSavedPropertyListingController

buyer_save_property_listing_controller = BuyerSavePropertyListingController(name="BuyerSavePropertyListingController",
                                                                            import_name=__name__)
seller_view_save_count_controller = SellerViewSaveCountController(name="SellerViewSaveCountController",
                                                                  import_name=__name__)
view_saved_property_listing_controller = ViewSavedPropertyListingController(name="ViewSavedPropertyListingController",
                                                                            import_name=__name__)

