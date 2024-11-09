from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Папка для хранения загруженных файлов
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Максимальный размер файла: 16 MB

# Убедитесь, что папка для загрузок существует
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])  # Получаем список файлов
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Файл не найден в запросе"
    
    file = request.files['file']
    if file.filename == '':
        return "Имя файла пустое"
    
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))  # Сохранение файла
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

