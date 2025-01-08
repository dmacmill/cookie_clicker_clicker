class BuildingElement:
    """
    Represents an element in the store.

    element (WebElement): The element in the store.
    owned (int): The number of buildings owned.
    price (int): The price of the building.
    is_enabled (bool): Can the building be purchased or not.
    """
    element = None
    owned = None
    price = None
    is_enabled = False