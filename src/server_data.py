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
                           'noise_sensitivity', 'acoustic_technician']
        create_csv_file(self.users_filepath, self.users_keys)

        self.metadata_from_users_filepath = f'{basedir_statistics_records}/metadata_from_users.csv'
        self.metadata_from_users_keys = ['timer', 'sound_index', 'class_name', 'start_perc', 'end_perc',
                                         'silent_environment', 'device']
        self.metadata_from_users_keys_reverse = {v: k for k, v in enumerate(['user', *self.metadata_from_users_keys])}
        create_csv_file(self.metadata_from_users_filepath, self.metadata_from_users_keys)

    def exists_user(self, user):
        for line in open(self.users_filepath).readlines():
            if line.startswith(user):
                return True
        return False

    def __user_to_index__(self, user):
        for line in reversed(open(self.metadata_from_users_filepath).readlines()):
            if line.startswith(user):
                return int(line.split(',')[self.metadata_from_users_keys_reverse['sound_index']]) + 1
        return 0

    def audio_track_metadata(self, user):
        index = self.__user_to_index__(user)
        if index is None:
            return None
        try:
            audio_path = self.audio_paths[index]
            result = json.load(open(audio_path))
            return dict(
                sound_index=index,
                sound_name=audio_path.split('/')[-1].split('.')[0],
                sound=result['sound_base64'],
                spl=result['spl'],
                duration=result['duration'],
            )
        except:
            return None

    def send_user_info(self, user_info):
        user = user_info['user']
        if not self.exists_user(user):
            timestamp = datetime.now()
            register_csv_row([user_info], self.users_filepath, user, self.users_keys, timestamp)

    def send_class_labeling(self, user, labeling):
        if self.exists_user(user):
            timestamp = datetime.now()
            register_csv_row(labeling, self.metadata_from_users_filepath, user, self.metadata_from_users_keys,
                             timestamp)

    def get_categories(self, language):
        return [cat[1 if 'it' in language.lower() else 0] for cat in self.categories]
