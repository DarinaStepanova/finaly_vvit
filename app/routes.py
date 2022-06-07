import os
import pathlib
import uuid

from app import app
from flask import render_template, request
from app.yolov5.detect_original import run
from threading import Thread

last_image=None


@app.route('/', methods=['GET', 'POST'])
def upload():
    global last_image
    if request.method == 'POST':
        f = request.files.get('file') #получает файл
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename)) #получаем полный путь до загруженного файла и сохраняем его по этому пути
        try:
            run(app.config["WEIGHTS_PATH"], f.filename, False, True)#вызов запирающей функции детекции
        except Exception as e:
            print(e)
        else:
            if ".jpg" in f.filename or ".jpeg" in f.filename or ".png" in f.filename:
                last_image = (False, f.filename)
            else:
                last_image = (True, f.filename.replace(".mp4", ".webm")) #Сохраняем имя последнего изображения
        # last_video = f.filename.replace(".mp4", ".webm")
    return render_template('index.html') # если метод GET, то отрисовываем страницу index


@app.route("/redirect/", methods=["GET", "POST"] )
def redirect():
    if not last_image:
        return "Нет результата"
    else:
        is_video, source = last_image
        return render_template('show.html', image=source, show_img=True, video=is_video) #указываем путь к изображению которое хотим показать
