# Doordash Customer Support Chatbot

This is a customer support chatbot application for handling "Never Delivered" (ND) issues for Doordash customers. The chatbot uses OpenAI's GPT-4 model to process customer inquiries and can make API calls to retrieve relevant information.

## Features

- Interactive GUI for customer support interactions
- Integration with OpenAI's GPT-4 model
- API calls for customer information, delivery status, and resolution
- Session context management
- API call logging

## Setup

1. Clone the repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Application

Run the application using:
```bash
python main.py
```

## Usage

1. The chatbot will greet you with a welcome message
2. Type your message in the input field and press Enter or click Send
3. The chatbot will process your message and respond accordingly
4. API calls made by the chatbot will be displayed in the API Call Info section
5. You can view and modify the session context using the SET CONTEXT button
6. Use the RESET button to start a new conversation

## API Functions

The chatbot can make the following API calls:
- `get_customer_info`: Retrieves customer profile and order history
- `get_delivery_info`: Retrieves the latest shipping and delivery status
- `get_dropoff_photo_and_map`: Retrieves a photo and map of where the package was dropped off
- `check_is_fraud_user`: Checks if the customer account is flagged for suspicious activity
- `provide_resolution`: Applies a resolution such as refund, replacement, or expedited shipping

## Note

This is a mock implementation. In a production environment, you would need to:
1. Implement proper error handling
2. Add authentication and security measures
3. Connect to actual APIs instead of using mock data
4. Add proper logging and monitoring
5. Implement proper session management 