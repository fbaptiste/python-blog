"""This is an example that shows poorly written Python code"""
import csv
import json
import pathlib
import random


def make_TempDirectory(dirName):
    if pathlib.Path("./" + dirName).exists():
        # dir already exists, no need to do anything
        pass
    else:
        pathlib.Path("./" + dirName).mkdir()


def create_csv_file(fileName, cols, rows, types=[]):
    try:
        f = open(temp_dir + "/" + fileName, "w")
    except:
        return
    if not types:
        types = [float, float, str]

    for i in range(rows):
        row = list(
            str(types[j % len(types)](random.random())) for j in range(cols)
        )
        f.write(",".join(row))
        f.write("\n")
    f.close()


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if (
                item.name != "Aged Brie"
                and item.name != "Backstage passes to a TAFKAL80ETC concert"
            ):
                if item.quality > 0:
                    if item.name != "Sulfuras, Hand of Ragnaros":
                        item.quality = item.quality - 1
            else:
                if item.quality < 50:
                    item.quality = item.quality + 1
                    if item.name == "Backstage passes to a TAFKAL80ETC concert":
                        if item.sell_in < 11:
                            if item.quality < 50:
                                item.quality = item.quality + 1
                        if item.sell_in < 6:
                            if item.quality < 50:
                                item.quality = item.quality + 1
            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - 1
            if item.sell_in < 0:
                if item.name != "Aged Brie":
                    if item.name != "Backstage passes to a TAFKAL80ETC concert":
                        if item.quality > 0:
                            if item.name != "Sulfuras, Hand of Ragnaros":
                                item.quality = item.quality - 1
                    else:
                        item.quality = item.quality - item.quality
                else:
                    if item.quality < 50:
                        item.quality = item.quality + 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


# program
if __name__ == "__main__":
    const = (
        "a string"
        "written "
        "over multiple lines "
        "that could fit on one"
    )
    temp_dir = "temp"
    make_TempDirectory(temp_dir)
    create_csv_file("test.csv", 3, 10)
