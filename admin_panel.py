from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send
from flask_cors import CORS  # Add this line to import CORS

import mysql.connector

app = Flask(__name__)
socketio = SocketIO(app)
CORS(app)  # Add this line to enable CORS support


@app.route('/')
def index():
    # Fetch user chats from the database
    chats = get_user_chats()
    return render_template('admin.html', chats=chats)

def get_user_chats():
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="192.168.19.160",
        user="usher",
        password="Um@ir65048420",
        database="rasa"
    )
    cursor = conn.cursor(dictionary=True)

    # Fetch user chats
    select_query = "SELECT * FROM it_chat_history"
    cursor.execute(select_query)
    chats = cursor.fetchall()

    cursor.close()
    conn.close()

    return chats

@socketio.on('mark_read')
def handle_mark_read(data):
    marked_as_read = data['read']

    # Update the database to mark selected chats as read
    update_query = "UPDATE it_chat_history SET is_read = 1 WHERE user_id IN ('{}')".format("','".join(marked_as_read))

    conn = mysql.connector.connect(
        host="192.168.19.160",
        user="usher",
        password="Um@ir65048420",
        database="rasa"
    )
    cursor = conn.cursor()
    cursor.execute(update_query)
    conn.commit()  # Commit the changes to the database
    cursor.close()
    conn.close()

    # Update the database with the selected status for each user
    for user_id, status in data.get('status', {}).items():
        status_update_query = f"UPDATE it_chat_history SET status = '{status}' WHERE user_id = '{user_id}'"

        conn = mysql.connector.connect(
            host="192.168.19.160",
            user="usher",
            password="Um@ir65048420",
            database="rasa"
        )
        cursor = conn.cursor()
        cursor.execute(status_update_query)
        conn.commit()
        cursor.close()
        conn.close()

    # Emit the update to all connected clients
    socketio.emit('update_chats', {'message': 'Chats marked as read and status updated'})


if __name__ == '__main__':
    socketio.run(app, debug=True)
