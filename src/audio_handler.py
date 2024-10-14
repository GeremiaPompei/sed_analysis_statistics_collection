import base64
import json
import math
import os

import librosa
import numpy as np
from pydub import AudioSegment
from tqdm import tqdm


class AudioHandler:

    def __init__(
            self,
            audio_tracks_dir,
            server_cache,
    ):
        for fp in tqdm(os.listdir(audio_tracks_dir), desc="Audio track loading..."):
            if fp.lower().endswith('.wav'):
                self.get_cached_spl_spec(os.path.join(audio_tracks_dir, fp), server_cache=server_cache)

    def read_audio(self, audio_data) -> np.array:
        if type(audio_data) == str:
            audio_time_series, sample_rate = librosa.load(audio_data)
        else:
            audio_time_series, sample_rate = audio_data
        if audio_time_series.ndim == 1:
            audio_time_series = audio_time_series.reshape(1, -1)
        return audio_time_series, sample_rate

    def amplitude_to_spl_and_spectrogram3o(self, signal, sampling_rate):
        if len(signal.shape) == 2:
            signal = signal.mean(axis=0)
        window = sampling_rate // 10
        pad_right = (math.ceil(signal.shape[-1] / window) * window) - signal.shape[-1]
        signal = np.pad(signal, (0, pad_right), "constant", constant_values=(0, 0))
        n_windows = math.ceil(len(signal) / window)
        signals = np.zeros((n_windows, window))
        for i in range(n_windows):
            s = signal[i * window:(i + 1) * window]
            s[s == 0] = 1e-17
            signals[i, :] = s[:]

        rms = np.sqrt(np.mean(np.square(signals), axis=1))
        spl = 20 * np.log10(rms / 2e-5)
        return spl

    def audio_to_spl(self, data):
        sample, sampling_rate = self.read_audio(data)
        spl = self.amplitude_to_spl_and_spectrogram3o(sample, sampling_rate)
        return spl

    def get_cached_spl_spec(self, audio_path, server_cache):
        hashed_ap = audio_path.split('/')[-1].split('.')[0]
        fp = f'{server_cache}/{hashed_ap}.json'
        if not os.path.exists(fp):
            data, sr = librosa.load(audio_path)
            duration = librosa.get_duration(y=data, sr=sr)
            spl = list(self.audio_to_spl((data, sr)))
            audio_path_mp3 = audio_path.replace('wav', 'mp3')
            AudioSegment.from_wav(audio_path).export(audio_path_mp3, format="mp3")
            with open(audio_path_mp3, "rb") as file:
                sound_base64 = base64.b64encode(file.read()).decode('ascii')
            os.remove(audio_path_mp3)
            json.dump(dict(spl=spl, duration=duration * 1000, sound_base64=sound_base64), open(fp, 'w'))
        return fp
