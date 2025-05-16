from flask import Flask, request, jsonify

from src.mail_handler import MailHandler
from src.server_data import ServerData

basedir = ''
app = Flask(__name__, static_url_path='')

mail_handler = MailHandler(
    credentials_path=f'{basedir}credentials.json',
    thanks_and_inform_message_path=f'{basedir}assets/mail_texts/thanks_and_inform.json'
)
sd = ServerData(
    categories=[
    ('Jet aircrafts', 'Aerei a reazione'),
    ('Bells', 'Campane'),
    ('Birds', 'Uccelli'),
    ('Cat fights and moans', 'Liti e miagolii di gatti'),
    ('Chicken coop', 'Pollaio'),
    ('Cicadas and crickets', 'Cicale e grilli'),
    ('Horn', 'Clacson'),
    ('Crows seagulls and magpies', 'Corvi gabbiani e gazze'),
    ('Dog barkings and howlings', 'Abbaiare e ululare di cani'),
    ('Glass breaking', 'Rottura di vetri'),
    ('Propeller aircrafts', 'Aerei a elica'),
    ('Lawn mower brush cutter and olive shaker', 'Tosaerba decespugliatore e scuotitore per olive'),
    ('Music', 'Musica'),
    ('Sirens and alarms', 'Sirene e allarmi'),
    ('Thunder fireworks and gunshot', 'Tuoni fuochi artificio e spari'),
    ('Train', 'Treno'),
    ('Vacuum cleaner fan and hairdryer', 'Aspirapolvere ventilatore e asciugacapelli'),
    ('Vehicle idling', 'Stazionamento di veicolo'),
    ('Vehicle pass-by', 'Passaggio di veicolo'),
    ('Voices', 'Voci'),
    ('Wind turbine', 'Turbina eolica'),
    ('Workshop', 'Officina')
],
    server_cache_dir=f'{basedir}assets/server_cache',
    basedir_statistics_records=f'{basedir}assets',
    mail_handler=mail_handler,
)


def get_language_id_from_header():
    language = ''
    if 'language' in request.headers:
        language = request.headers['language']
    return 1 if 'it' in language.lower() else 0


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
    sd.send_class_labeling(user, labeling, language_id=get_language_id_from_header())
    return jsonify(dict())


@app.route("/api/get_categories", methods=["GET"])
def get_categories():
    categories = sd.get_categories(language_id=get_language_id_from_header())
    return jsonify(dict(categories=categories))


def main():
    app.run(host="localhost", port=8000, debug=False)


if __name__ == '__main__':
    main()
