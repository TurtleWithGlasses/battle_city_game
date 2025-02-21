import pygame
import os
import csv


class LevelData:
    def __init__(self):
        self.level_data = self.load_level_data()

    def load_level_data(self):
        game_stages = []
        for stage in os.listdir("levels"):
            level_data = [[] for i in range(27)]
            with open(os.path.join("levels", stage), newline="") as csvFile:
                reader = csv.reader(csvFile, delimiter=",")
                for i, row in enumerate(reader):
                    for j, tile in enumerate(row):
                        level_data[i].append(int(tile))
            game_stages.append(level_data)
        return game_stages

    def save_level_data(self, level_data):
        for i, level in enumerate(level_data):
            num = f"{i+1:02d}"  # Always generates 01, 02, ..., 10, etc.
            file_path = os.path.join("levels", f"BattleCityLevel{num}.csv")
            with open(file_path, "w", newline="") as csvFile:
                writer = csv.writer(csvFile, delimiter=",")
                writer.writerows(level)
        return
            