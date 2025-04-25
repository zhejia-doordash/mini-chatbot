import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                            QLabel, QScrollArea, QProgressBar, QRadioButton,
                            QButtonGroup, QGroupBox)
from PyQt6.QtCore import Qt, QTimer
import openai
from dotenv import load_dotenv
import json
from api_functions import get_initial_user_info, get_customer_info, get_delivery_info, get_dropoff_photo_and_map, check_is_fraud_user, provide_resolution

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url="https://api.openai.com/v1"
)

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Customer Service Chatbot")
        self.setGeometry(100, 100, 1200, 1000)
        
        # Initialize conversation history and context
        self.conversation_history = []
        self.session_context = get_initial_user_info()
        self.force_fraud_status = None  # Will be True or False based on selection
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Chat window
        self.chat_window = QTextEdit()
        self.chat_window.setReadOnly(True)
        layout.addWidget(self.chat_window)
        
        # Input area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(send_button)
        layout.addLayout(input_layout)
        
        # API Call Info
        api_layout = QVBoxLayout()
        api_label = QLabel("API Call Info")
        self.api_info = QTextEdit()
        self.api_info.setReadOnly(True)
        self.api_info.setMaximumHeight(300)
        api_layout.addWidget(api_label)
        api_layout.addWidget(self.api_info)
        layout.addLayout(api_layout)
        
        # Session Context
        context_layout = QVBoxLayout()
        context_label = QLabel("Session Context")
        self.context_display = QTextEdit()
        self.context_display.setMaximumHeight(300)
        context_layout.addWidget(context_label)
        context_layout.addWidget(self.context_display)
        
        # Display initial context
        self.context_display.setText(json.dumps(self.session_context, indent=2))
        
        # Context buttons
        context_buttons = QHBoxLayout()
        set_context_button = QPushButton("SET CONTEXT")
        set_context_button.clicked.connect(self.set_context)
        context_buttons.addWidget(set_context_button)
        context_layout.addLayout(context_buttons)
        
        # Add context layout to main layout
        layout.addLayout(context_layout)
        
        # Bottom section with fraud status and reset
        bottom_layout = QHBoxLayout()
        
        # Fraud Status Selection
        fraud_group = QGroupBox("Fraud Status")
        fraud_layout = QHBoxLayout()  # Changed to horizontal layout
        self.fraud_button_group = QButtonGroup()
        
        self.fraud_buttons = {
            "false": QRadioButton("False"),
            "true": QRadioButton("True")
        }
        
        for i, (status, button) in enumerate(self.fraud_buttons.items()):
            self.fraud_button_group.addButton(button, i)
            fraud_layout.addWidget(button)
            if status == "false":  # Set default
                button.setChecked(True)
                self.force_fraud_status = False
        
        # Connect button group to handler
        self.fraud_button_group.buttonClicked.connect(self.handle_fraud_status_change)
        
        fraud_group.setLayout(fraud_layout)
        bottom_layout.addWidget(fraud_group)
        
        # Add stretch to push reset button to the right
        bottom_layout.addStretch()
        
        # Reset button
        reset_button = QPushButton("RESET")
        reset_button.clicked.connect(self.reset_conversation)
        bottom_layout.addWidget(reset_button)
        
        # Add bottom layout to main layout
        layout.addLayout(bottom_layout)
        
        # Send welcome message with user info
        self.add_message("System", f"Customer Information Loaded:\nName: {self.session_context['customer']['name']}\nEmail: {self.session_context['customer']['email']}\nOrder ID: {self.session_context['current_order']['order_id']}")
        self.add_message("Chatbot", "Welcome to Doordash Customer Support! I understand you're having an issue with your order. How can I help you today?")
    
    def add_message(self, sender, message):
        self.chat_window.append(f"{sender}: {message}\n")
        # Scroll to bottom
        self.chat_window.verticalScrollBar().setValue(
            self.chat_window.verticalScrollBar().maximum()
        )
        if sender != "System":  # Don't add system messages to conversation history
            self.conversation_history.append({"role": "user" if sender == "Customer" else "assistant", "content": message})
    
    def update_api_info(self, message):
        self.api_info.append(message)
        # Scroll to bottom
        self.api_info.verticalScrollBar().setValue(
            self.api_info.verticalScrollBar().maximum()
        )
        # Force update
        QApplication.processEvents()
    
    def handle_fraud_status_change(self, button):
        self.force_fraud_status = button.text().lower() == "true"
    
    def update_context_display(self):
        """Update the context display with current session context"""
        self.context_display.setText(json.dumps(self.session_context, indent=2))
    
    def handle_function_call(self, function_name, arguments):
        try:
            args = json.loads(arguments)
            response = None
            
            if function_name == "get_customer_info":
                response = get_customer_info(args.get("email"))
                self.session_context["customer_info"] = response
            elif function_name == "get_delivery_info":
                response = get_delivery_info(args.get("order_id"))
                self.session_context["delivery_info"] = response
            elif function_name == "get_dropoff_photo_and_map":
                response = get_dropoff_photo_and_map(args.get("order_id"))
                self.session_context["dropoff_info"] = response
            elif function_name == "check_is_fraud_user":
                if self.force_fraud_status is not None:
                    response = {"is_fraud": self.force_fraud_status}
                else:
                    response = check_is_fraud_user(args.get("email"))
                self.session_context["fraud_status"] = response
            elif function_name == "provide_resolution":
                response = provide_resolution(args.get("order_id"), args.get("resolution"))
                self.session_context["resolution"] = response
            
            # Update context display
            self.update_context_display()
            return response
            
        except Exception as e:
            error_response = {"error": str(e)}
            self.session_context["last_error"] = error_response
            self.update_context_display()
            return error_response
    
    def send_message(self):
        message = self.input_field.text().strip()
        if not message:
            return
        
        # Clear input field immediately
        self.input_field.clear()
        
        # Clear previous API info
        self.api_info.clear()
        
        self.add_message("Customer", message)
        
        # Process message with OpenAI
        try:
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_customer_info",
                        "description": "Retrieves customer profile and order history",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "email": {"type": "string"}
                            },
                            "required": ["email"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_delivery_info",
                        "description": "Retrieves the latest shipping and delivery status",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "order_id": {"type": "string"}
                            },
                            "required": ["order_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_dropoff_photo_and_map",
                        "description": "Retrieves a photo and map of where the package was dropped off",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "order_id": {"type": "string"}
                            },
                            "required": ["order_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "check_is_fraud_user",
                        "description": "Checks if the customer account is flagged for suspicious activity",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "email": {"type": "string"}
                            },
                            "required": ["email"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "provide_resolution",
                        "description": "Applies a resolution such as refund, replacement, or expedited shipping",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "order_id": {"type": "string"},
                                "resolution": {"type": "string"}
                            },
                            "required": ["order_id", "resolution"]
                        }
                    }
                }
            ]
            
            # First API call
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"""You are a Doordash customer support agent. Current customer information: {json.dumps(self.session_context)}
                    
                    Important rules:
                    1. Always check fraud status before offering any compensation
                    2. If the user is flagged as fraudulent, do not offer any compensation
                    3. For fraudulent users, explain that you cannot provide compensation due to account security measures
                    4. For legitimate users, proceed with normal support process
                    5. Always check delivery status and photos before making any decisions
                    """},
                    *self.conversation_history
                ],
                tools=tools
            )
            
            # Handle function calls if present
            if response.choices[0].message.tool_calls:
                for tool_call in response.choices[0].message.tool_calls:
                    self.update_api_info(f"API Call: {tool_call.function.name}\n")
                    self.update_api_info(f"Parameters: {tool_call.function.arguments}\n")
                    
                    # Execute the function call
                    function_response = self.handle_function_call(
                        tool_call.function.name,
                        tool_call.function.arguments
                    )
                    
                    # Display function response
                    self.update_api_info(f"Response: {json.dumps(function_response, indent=2)}\n\n")
                    
                    # Add function response to conversation
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [tool_call]
                    })
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(function_response)
                    })
            
            # Second API call to get final response
            final_response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"""You are a Doordash customer support agent. Current customer information: {json.dumps(self.session_context)}
                    
                    Important rules:
                    1. Always check fraud status before offering any compensation
                    2. If the user is flagged as fraudulent, do not offer any compensation
                    3. For fraudulent users, explain that you cannot provide compensation due to account security measures
                    4. For legitimate users, proceed with normal support process
                    5. Always check delivery status and photos before making any decisions
                    """},
                    *self.conversation_history
                ]
            )
            
            # Add the final response to the conversation
            if final_response.choices[0].message.content:
                self.add_message("Chatbot", final_response.choices[0].message.content)
            else:
                self.add_message("Chatbot", "I apologize, but I'm having trouble processing your request. Please try again.")
            
        except Exception as e:
            self.add_message("Chatbot", f"Error: {str(e)}")
        finally:
            # Re-enable input
            self.input_field.setEnabled(True)
    
    def set_context(self):
        try:
            context = json.loads(self.context_display.toPlainText())
            self.session_context = context
            self.update_context_display()
            self.add_message("System", "Context updated successfully")
        except json.JSONDecodeError:
            self.add_message("System", "Error: Invalid JSON format")
    
    def reset_conversation(self):
        self.conversation_history = []
        self.chat_window.clear()
        self.api_info.clear()
        self.context_display.clear()
        self.session_context = get_initial_user_info()
        self.update_context_display()
        self.add_message("System", f"Customer Information Loaded:\nName: {self.session_context['customer']['name']}\nEmail: {self.session_context['customer']['email']}\nOrder ID: {self.session_context['current_order']['order_id']}")
        self.add_message("Chatbot", "Welcome to Doordash Customer Support! I understand you're having an issue with your order. How can I help you today?")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec()) 