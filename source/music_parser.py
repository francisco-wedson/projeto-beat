import pygame
import librosa
import os
import numpy as np

#n_fft - quão detalhado será o espectro de frequência, quanto maior
#mais precisão, mas perde na precisão do tempo

#
def parse_music(filename, n_fft=2048, hop_length=512, allow_chords=False, chord_threshold=0.5):
    music_path = os.path.join('assets', 'musicas', filename)
    y, sr = librosa.load(music_path, sr=None)

    onsets_frames = librosa.onset.onset_detect(y=y, sr=sr, hop_length=hop_length)
    onsets_times = librosa.frames_to_time(onsets_frames, sr=sr, hop_length=hop_length)

    #STFT magnitude
    S = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)

    bands = [(20, 125), (125, 500), (500, 2000), (2000, 8000)]

    notes = [] #lista de tuplas do tempo_em_s e lane_id
    for t in onsets_times:
        col_idx = int(round(t * sr / hop_length))
        if col_idx >= S.shape[1]:
            col_idx = S.shape[1] - 1
        col = S[:, col_idx]

        band_energies = []
        for low, high in bands:
            idx = np.where((freqs >= low) & (freqs < high))[0]
            energy = float(col[idx].sum()) if idx.size else 0.0
            band_energies.append(energy)

        #normalizar para comparar
        max_e = max(band_energies) if band_energies else 1.0
        if max_e == 0:
            band_norm = [0.0]*len(band_energies)

        else:
            band_norm = [b / max_e for b in band_energies]

        if allow_chords:
            lanes = [i for i, v in enumerate(band_norm) if v >= chord_threshold]
            if not lanes:
                lanes = [int(np.argmax(band_norm))]
            notes.append((t, lanes))

        else:
            lane = int(np.argmax(band_norm))
            notes.append((t, lane))

    return notes
