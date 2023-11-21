import time
import pygame
import threading


class AudioManager:
    def __init__(self, key_event_manager):
        self.jam = None
        self.thresholds = None
        self.key_event_manager = key_event_manager
        self.threads = []
        self.running = False

    def __monitor_volume_changes(self):
        while self.running:
            max_levels = len(self.jam.get_channels())

            for i in range(max_levels):
                self.jam.set_level_volume(i, self.__calculate_volume_for_level(i))

            time.sleep(0.1)

    def __calculate_volume_for_level(self, level):
        volume = 0.0
        current_count = self.key_event_manager.get_event_count()

        if current_count == 0:
            return 0.0

        threshold_max = (self.thresholds[1] + self.thresholds[0]) / 2.0
        threshold = self.thresholds[level]

        if current_count >= threshold:
            volume = (current_count - threshold) / threshold_max
            if volume > 1:
                volume = 1
            return volume

        return 0

    def get_thresholds(self):
        return self.thresholds

    def set_thresholds(self, thresholds):
        self.thresholds = thresholds

    def get_jam(self):
        return self.jam

    def set_jam(self, jam):
        self.jam = jam

    def start(self):
        pygame.mixer.pre_init(44100, -16, 2, 64)
        pygame.mixer.init(44100, -16, 2, 64)
        self.running = True
        self.threads.append(threading.Thread(target=self.__monitor_volume_changes))
        for thread in self.threads:
            thread.start()

    def stop(self):
        self.running = False
        for thread in self.threads:
            thread.join()
        self.threads = []
