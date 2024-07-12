from flask import Flask, request, jsonify
from src.server_data import ServerData

app = Flask(__name__, static_url_path='')
sd = ServerData(
    categories=[
        ('speaking', 'parlato'),
        ('car', 'macchina'),
        ('truck', 'camion'),
        ('plane', 'aereo'),
        ('train', 'treno'),
        ('motorbike', 'moto'),
        ('dog', 'cane'),
        ('birds', 'uccelli'),
        ('clap', 'applauso'),
        ('pneumatic gun', 'pistola pneumatica'),
        ('saw', 'sega'),
        ('whisk', 'frullino'),
    ],
    server_cache_dir='assets/server_cache',
    basedir_statistics_records='assets',
)

@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route("/api/audio_track_metadata", methods=["POST"])
def audio_track_metadata():
    user = request.json['user']
    metadata = sd.audio_track_metadata(user)
    if metadata is None:
        return jsonify(dict(terminated=True))
    return jsonify(metadata)


@app.route("/api/audio_tracks_info", methods=["GET"])
def audio_tracks_info():
    return jsonify(dict(length=len(sd.audio_paths)))


@app.route("/api/is_registered_user", methods=["POST"])
def is_registered_user():
    user_info = request.json['user']
    registered = sd.exists_user(user_info)
    return jsonify(dict(registered=registered))


@app.route("/api/send_user_info", methods=["POST"])
def send_user_info():
    user_info = request.json['user_info']
    sd.send_user_info(user_info)
    return jsonify(dict())


@app.route("/api/send_class_labeling", methods=["POST"])
def send_class_labeling():
    user = request.json['user']
    labeling = request.json['labeling']
    sd.send_class_labeling(user, labeling)
    return jsonify(dict())


@app.route("/api/get_categories", methods=["GET"])
def get_categories():
    language = ''
    if 'language' in request.headers:
        language = request.headers['language']
    categories = sd.get_categories(language)
    return jsonify(dict(categories=categories))


def main():
    app.run(host="localhost", port=8000, debug=False)


if __name__ == '__main__':
    main()
