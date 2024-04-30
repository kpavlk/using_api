from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('load_photo.html')


@app.route('/answer')
def answer():
    data = {
        'title': "123",
        'surname': "Mask",
        'name': "Elon",
        'education': "High",
        'profession': "Businessman",
        'sex': "male",
        'motivation': "High",
        'ready': "True"
    }
    return render_template('auto_answer.html', item=data, title=data["title"])


if __name__ == '__main__':
    app.run(debug=True)
