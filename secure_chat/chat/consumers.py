import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .encryption import dual_encrypt, dual_decrypt  # Import your encryption functions

# Temporary hardcoded keys (replace with secure storage later)
NTEA_KEY = b"1234567890123456"
AES_KEY = b"1234567890123456"

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Retrieve room name from the URL route
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Retrieve the username from the authenticated user (Django user model)
        self.username = self.scope.get("user", None)
        if self.username and self.username.is_authenticated:
            self.username = self.username.username  # Use the authenticated username
        else:
            self.username = "Anonymous"  # Default to Anonymous if user is not authenticated

        # Join the room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Accept the WebSocket connection
        await self.accept()
        print(f"WebSocket connected to room: {self.room_name} (User: {self.username})")

    async def receive(self, text_data):
        print(f"Raw message received: {text_data}")
        try:
            # Parse the received message
            data = json.loads(text_data)
            print(f"Parsed JSON: {data}")
        except json.JSONDecodeError:
            print("Error: Received invalid JSON")
            return

        # Ensure the message has the 'message' field
        if "message" not in data:
            print("Error: 'message' key missing in message")
            return

        # Use the username from the connection if no 'username' is in the message
        username = data.get("username", self.username)  # Use the default or provided username
        message = data["message"]

        # Encrypt the message before sending
        encrypted_message, padding_length = dual_encrypt(message.encode('utf-8'), NTEA_KEY, AES_KEY)

        # Send the encrypted message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "username": username,  # Send the username along with the message
                "message": encrypted_message.hex(),  # Send as hex for easier transmission
                "padding_length": padding_length  # Send padding length for decryption
            },
        )

    async def chat_message(self, event):
        # Decrypt the message before sending it to the WebSocket
        encrypted_message = bytes.fromhex(event["message"])  # Convert from hex back to bytes
        decrypted_message = dual_decrypt(encrypted_message, NTEA_KEY, AES_KEY, event["padding_length"])  # Use the padding length passed from the sender

        # Send the decrypted message to the WebSocket
        await self.send(text_data=json.dumps({
            "username": event["username"],  # Pass the username with the decrypted message
            "message": decrypted_message.decode('utf-8'),
        }))











































# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .encryption import dual_encrypt, dual_decrypt  # Import your encryption functions

# # Temporary hardcoded keys (replace with secure storage later)
# NTEA_KEY = b"1234567890123456"
# AES_KEY = b"1234567890123456"

# # consumers.py
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Retrieve room name from the URL route
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = f"chat_{self.room_name}"

#         # Log the user from the scope to check the authentication status
#         print(f"User from scope: {self.scope.get('user')}")

#         # Retrieve the username from the authenticated user (Django user model)
#         self.username = self.scope.get("user", None)
#         if self.username and self.username.is_authenticated:
#             self.username = self.username.username  # Use the authenticated username
#         else:
#             self.username = "Anonymous"  # Default to Anonymous if user is not authenticated

#         # Join the room group
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)

#         # Accept the WebSocket connection
#         await self.accept()
#         print(f"WebSocket connected to room: {self.room_name} (User: {self.username})")


#     async def receive(self, text_data):
#         print(f"Raw message received: {text_data}")
#         try:
#             # Parse the received message
#             data = json.loads(text_data)
#             print(f"Parsed JSON: {data}")
#         except json.JSONDecodeError:
#             print("Error: Received invalid JSON")
#             return

#         # Ensure the message has the 'message' field
#         if "message" not in data:
#             print("Error: 'message' key missing in message")
#             return

#         # Use the username from the connection if no 'username' is in the message
#         username = data.get("username", self.username)  # Use the default or provided username
#         message = data["message"]

#         # Encrypt the message before sending
#         encrypted_message, padding_length = dual_encrypt(message.encode('utf-8'), NTEA_KEY, AES_KEY)

#         # Send the encrypted message to the room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 "type": "chat_message",
#                 "username": username,  # Send the username along with the message
#                 "message": encrypted_message.hex(),  # Send as hex for easier transmission
#             },
#         )

#     async def chat_message(self, event):
#         # Decrypt the message before sending it to the WebSocket
#         encrypted_message = bytes.fromhex(event["message"])  # Convert from hex back to bytes
#         decrypted_message = dual_decrypt(encrypted_message, NTEA_KEY, AES_KEY, 0)  # 0 padding_length as placeholder

#         # Send the decrypted message to the WebSocket
#         await self.send(text_data=json.dumps({
#             "username": event["username"],  # Pass the username with the decrypted message
#             "message": decrypted_message.decode('utf-8'),
#         }))
