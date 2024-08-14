from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/video', methods=['GET'])
def get_video():
    return jsonify({
        'ad_video_url': 'https://www.youtube.com/embed/rXzfcLIzGQU',
        'main_video_url': 'https://www.youtube.com/embed/51QV0v8GGbM'
    })

if __name__ == '__main__':
    app.run(debug=True)
