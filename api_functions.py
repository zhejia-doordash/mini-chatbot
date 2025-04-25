def get_initial_user_info() -> dict:
    """
    Returns initial user information for the support case.
    This is a mock implementation with dummy data.
    """
    return {
        "customer": {
            "email": "customer@example.com",
            "name": "John Doe",
            "phone": "555-0123",
            "address": "123 Main St, City, State"
        },
        "current_order": {
            "order_id": "12346",
            "order_date": "2024-03-15",
            "items": [
                {
                    "name": "Burger Combo",
                    "quantity": 1,
                    "price": 15.99
                },
                {
                    "name": "Side Salad",
                    "quantity": 1,
                    "price": 5.99
                }
            ],
            "total": 25.99,
            "restaurant": "Burger Palace",
            "status": "never_delivered"
        }
    }

def get_customer_info(email: str = "dummy@example.com") -> dict:
    """
    Retrieves customer profile and order history.
    This is a mock implementation.
    """
    # In a real implementation, this would call an actual API
    return {
        "email": "customer@example.com",
        "name": "John Doe",
        "order_history": [
            {"order_id": "12345", "status": "delivered", "date": "2024-03-01"},
            {"order_id": "12346", "status": "never_delivered", "date": "2024-03-15"}
        ]
    }

def get_delivery_info(order_id: str = "12346") -> dict:
    """
    Retrieves the latest shipping and delivery status.
    This is a mock implementation.
    """
    return {
        "order_id": "12346",
        "status": "never_delivered",
        "delivery_time": "2024-03-15 14:30:00",
        "delivery_address": "123 Main St, City, State",
        "driver_notes": "Could not locate customer"
    }

def get_dropoff_photo_and_map(order_id: str = "12346") -> dict:
    """
    Retrieves a photo and map of where the package was dropped off.
    This is a mock implementation.
    """
    return {
        "order_id": "12346",
        "photo_url": "https://example.com/delivery_photo.jpg",
        "map_url": "https://example.com/delivery_map.jpg",
        "coordinates": {"lat": 37.7749, "lng": -122.4194},
        "attempted_delivery_time": "2024-03-15 14:30:00"
    }

def check_is_fraud_user(email: str = "customer@example.com") -> dict:
    """
    Checks if the customer account is flagged for suspicious activity.
    This is a mock implementation.
    """
    return {
        "email": "customer@example.com",
        "is_fraud": False,
        "risk_score": 0.1,
        "account_age_days": 365,
        "previous_claims": 0
    }

def provide_resolution(order_id: str = "12346", resolution: str = "refund") -> dict:
    """
    Applies a resolution such as refund, replacement, or expedited shipping.
    This is a mock implementation.
    """
    return {
        "order_id": "12346",
        "resolution": "refund",
        "status": "completed",
        "timestamp": "2024-03-15 15:00:00",
        "amount": 25.99,
        "resolution_id": "res_123456"
    } 