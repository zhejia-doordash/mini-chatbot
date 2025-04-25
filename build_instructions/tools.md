get_customer_info(email: str): Retrieves customer profile and order history.

get_delivery_info(order_id: str): Retrieves the latest shipping and delivery status.

get_dropoff_photo_and_map(order_id: str): Retrieves a photo and map of where the package was dropped off.

check_is_fraud_user(email: str): Checks if the customer account is flagged for suspicious or fraudulent activity (use this internally; do not disclose fraud status to the customer).

provide_resolution(order_id: str, resolution: str): Applies a resolution such as refund, replacement, or expedited shipping.