import json
import os
from datetime import datetime

from src.csv_utils import create_csv_file, register_csv_row


class ServerData:

    def __init__(self, categories, server_cache_dir, basedir_statistics_records):
        self.categories = categories
        self.server_cache_dir = server_cache_dir
        self.audio_paths = sorted([f'{self.server_cache_dir}/{fn}' for fn in os.listdir(self.server_cache_dir) if
                                   not fn.startswith('.') and fn.endswith('.json')])

        open(f'{basedir_statistics_records}/sound_tracks.csv', 'w').write(
            "\n".join(['sound_index,sound_name', *[f'{i},{ap}' for i, ap in enumerate(self.audio_paths)]]))
        self.users_filepath = f'{basedir_statistics_records}/users.csv'
        self.users_keys = ['biological_sex', 'years', 'qualification', 'hearing_difficulty', 'hearing_aids',
                           'noise_sensitivity', 'acoustic_technician', 'silent_environment']
        create_csv_file(self.users_filepath, self.users_keys)

        self.metadata_from_users_filepath = f'{basedir_statistics_records}/metadata_from_users.csv'
        self.metadata_from_users_keys = ['timer', 'sound_index', 'class_name', 'start_perc', 'end_perc']
        create_csv_file(self.metadata_from_users_filepath, self.metadata_from_users_keys)

    def audio_track_metadata(self, index):
        audio_path = self.audio_paths[index]
        result = json.load(open(audio_path))
        return dict(
            sound_index=index,
            sound_name=audio_path.split('/')[-1].split('.')[0],
            sound=result['sound_base64'],
            spectrogram_3o=result['spectrogram_3o'],
            freq3o=result['freq3o'],
            spl=result['spl'],
            duration=result['duration'],
        )

    def send_class_labeling(self, user_info, labeling):
        user = user_info['user']
        timestamp = datetime.now()
        register_csv_row([user_info], self.users_filepath, user, self.users_keys, timestamp)
        register_csv_row(labeling, self.metadata_from_users_filepath, user, self.metadata_from_users_keys, timestamp)

    def get_categories(self, language):
        return [cat[1 if 'it' in language.lower() else 0] for cat in self.categories]
