from flask import Flask, render_template, request, redirect, url_for
import asyncio
from bot import send_message_to_user
from tg_bot.adminDB import UsersDataBase


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

@app.route('/change_z', methods=['GET', 'POST'])
def change_z():
    db = UsersDataBase()
    z = db.get_Z()

    if request.method == 'POST':
        new_z = request.form.get('input_z')
        db.update_Z(new_z)
        return redirect(url_for('change_z'))
    return render_template('change_z.html', z=z)

@app.route('/change_texts')
def change_texts():
    return render_template('change_texts.html')

@app.route('/change_texts/change_about', methods=['GET', 'POST'])
def change_about():
    db = UsersDataBase()
    about = db.get_about_bot_text()

    if request.method == 'POST':
        new_about = request.form.get('input_about')
        db.update_about_bot_text(new_about)
        return redirect(url_for('change_about'))

    return render_template('change_about.html', about=about)

@app.route('/change_texts/change_prices', methods=['GET', 'POST'])
def change_prices():
    db = UsersDataBase()
    prices = db.get_prices()
    if request.method == 'POST':
        new_30 = request.form.get('input_30')
        new_90 = request.form.get('input_90')
        new_365 = request.form.get('input_365')
        db.update_prices(new_30, new_90, new_365)
        return redirect(url_for('change_prices'))
    return render_template('change_prices.html', days30=prices[0], days90=prices[1], days365=prices[2])


@app.route('/change_texts/change_subscription', methods=['GET', 'POST'])
def change_subscription():
    db = UsersDataBase()
    subscription = db.get_subscription_text()

    if request.method == 'POST':
        new_subscription= request.form.get('input_subscription')
        db.update_subscription_text(new_subscription)
        return redirect(url_for('change_subscription'))

    return render_template('change_subscription_text.html', subscription=subscription)





if __name__ == '__main__':
    app.run(debug=True)

