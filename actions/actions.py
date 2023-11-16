'''
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
import mysql.connector
import requests

class SaveChatToMySQL(Action):
    def name(self):
        return "action_save_chat_to_mysql"

    def run(self, dispatcher, tracker, domain):
        # Initialize variables
        user_id = tracker.sender_id
        message = ""
        bot_response = ""

        # Iterate through tracker events to capture user messages and the last bot response
        for event in reversed(tracker.events):
            if event.get("event") == "user":
                message = event.get("text", "")
                break  # Stop when the last user message is found
            elif event.get("event") == "bot":
                bot_response = event.get("text", "")

        # Insert the data into the MySQL database 
        conn = mysql.connector.connect(
            host="192.168.19.160",
            user="usher",
            password="Um@ir65048420",
            database="rasa"
        )
        cursor = conn.cursor()

        insert_query = "INSERT INTO it_chat_history (user_id, message, bot_response) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (user_id, message, bot_response))
        
        
        # Check if the bot response contains the prompt for name and department
        if "Please wait someone will be with you shortly" in bot_response:
            dispatcher.utter_message("May I know your name and department, please?")
            return [UserUtteranceReverted()]
        
        conn.commit()

        cursor.close()
        conn.close()

        return []
'''

from rasa_sdk import Action
from rasa_sdk.events import SlotSet, UserUtteranceReverted 
import mysql.connector
import requests

class SaveChatToMySQL(Action):
    def name(self):
        return "action_save_chat_to_mysql"

    def run(self, dispatcher, tracker, domain):
        # Initialize variables
        user_id = tracker.sender_id
        timestamp = tracker.latest_message.get('time', None)
        message = ""
        bot_response = ""

        # Iterate through tracker events to capture user messages and bot responses
        # Iterate through tracker events to capture user messages and the last bot response
        for event in reversed(tracker.events):
            if event.get("event") == "user":
                message = event.get("text", "")
                break  # Stop when the last user message is found
            elif event.get("event") == "bot":
                bot_response = event.get("text", "")

        # Insert the data into the MySQL database
        conn = mysql.connector.connect(
            host="192.168.19.160",
            user="usher",
            password="Um@ir65048420",
            database="rasa"
        )
        cursor = conn.cursor()

        insert_query = "INSERT INTO it_chat_history (user_id, message, bot_response) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (user_id, message, bot_response))
        conn.commit()

        cursor.close()
        conn.close()

        return []


        