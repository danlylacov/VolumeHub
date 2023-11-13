from flask import Flask, render_template, request
import asyncio
from bot import send_message_to_user
from tg_bot.usersDB import UsersDataBase


# Инициализация Flask приложения
app = Flask(__name__)




@app.route('/')
def admin():
    return render_template('admin.html')





@app.route('/send_message', methods=['GET', 'POST'])
def send_mes():
    if request.method == 'POST':
        chat_id = request.form.get('chat_id')
        message = request.form.get('message')
        send_to_all = request.form.get('send_to_all')
        photo = request.files.get('photo')
        if photo:
            photo.save('uploaded_photo.jpg')
            photo_path = 'uploaded_photo.jpg'
        else:
            photo_path = None

        if send_to_all == '1':
            db = UsersDataBase()
            ids = db.get_userids()
            print(ids)
            for chat_id in ids:
                asyncio.run(send_message_to_user(int(chat_id), message, photo_path=photo_path))

            return "Сообщение отправлено всем пользователям!"
        else:
            asyncio.run(send_message_to_user(chat_id, message, photo_path=photo_path))
            return f"Сообщение отправлено пользователю с id: {chat_id}!"
    return render_template('sendMes.html')



if __name__ == '__main__':
    app.run(debug=True)

