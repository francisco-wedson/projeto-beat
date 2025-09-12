import pygame
import librosa

y, sr = librosa.load('..', 'assets', 'musicas', 'Its Going Down Now.mp3')

tempo, batidas = librosa.beat.beat_track(y=y, sr=sr)
batidas_tempo = librosa.frames_to_time(batidas, sr=sr)

onsets = librosa.onset.onset_detect(y=y, sr=sr)
onsets_tempo = librosa.frames_to_time(onsets, sr=sr)

