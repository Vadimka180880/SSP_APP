import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from datetime import datetime

# 🟡 Імпорти для Google Sheets API
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ✅ Функція запису в Google Таблицю
def write_to_google_sheet(data: dict):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    import json
    creds_info = json.loads(os.environ.get("GOOGLE_CREDS_JSON"))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
    client = gspread.authorize(creds)

    # 📌 Вкажи назву своєї Google Таблиці
    sheet = client.open("ssp-submissions").sheet1

    row = [
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        data.get('name'),
        data.get('email'),
        data.get('department'),
        data.get('comment'),
        data.get('photo_url')
    ]
    sheet.append_row(row)


app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# 🛠 Створюємо директорію, якщо її немає (щоб уникнути FileNotFoundError)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
print("✅ Папка для фото:", app.config['UPLOAD_FOLDER'])

# 1. Головна — вибір департаменту
@app.route('/')
def home():
    return render_template('home.html')

# 2. Логін для конкретного департаменту
@app.route('/department/<name>', methods=['GET', 'POST'])
def login(name):
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email and password:
            session['user'] = email
            return redirect(url_for('form', name=name))
        else:
            return 'Невірний логін або пароль'

    return render_template('login.html', department=name)

# 3. Форма після логіну
@app.route('/department/<name>/form', methods=['GET', 'POST'])
def form(name):
    if 'user' not in session:
        return redirect(url_for('login', name=name))

    if request.method == 'POST':
        name_input = request.form['name']
        comment = request.form['comment']
        photo = request.files['photo']

        if photo:
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(photo_path)

            # ✨ Відправляємо дані у Google Таблицю
            write_to_google_sheet({
                'name': name_input,
                'email': session.get('user'),
                'department': name,
                'comment': comment,
                'photo_url': url_for('static', filename='uploads/' + filename, _external=True)
            })

            return render_template('success.html', name=name_input, filename=filename)

    return render_template('form.html', department=name)

# 4. Вихід
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

# 🔁 Запуск сервера
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
