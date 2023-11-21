import threading
import pygame


class Jam:
    def __init__(self, name, files):
        self.name = name
        self.files = files
        self.channels = []

    def get_name(self):
        return self.name

    def get_files(self):
        return self.files

    def get_channels(self):
        return self.channels

    def set_channels(self, channels):
        self.channels = channels

    def play(self):
        for audio_file in self.files:
            sound = pygame.mixer.Sound(audio_file)
            channel = pygame.mixer.find_channel(True)
            channel.set_volume(0)
            self.channels.append(channel)
            threading.Thread(target=self.__play_audio, args=(channel, sound)).start()

    def __play_audio(self, channel, sound):
        channel.play(sound, loops=-1)

    def stop(self):
        for channel in self.channels:
            channel.stop()

    def set_level_volume(self, level, volume):
        self.channels[level].set_volume(volume)
