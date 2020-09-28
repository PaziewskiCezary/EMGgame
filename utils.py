import os

__all__ = ['collide_in', 'get_bins', 'get_trashes', 'get_backgrounds']

def collide_in(obj1, obj2):
    ((obj1_x1, obj1_y1), (obj1_x2, obj1_y2)) = obj1.corrners
    ((obj2_x1, obj2_y1), (obj2_x2, obj2_y2)) = obj2.corrners

    if obj1_x1 >= obj2_x1 and obj1_x2 <= obj2_x2:
        return True

    return False



def get_bins(path="static/bins/"):
    for root, dirs, files in os.walk(path):
        for name in files:
            path = os.path.join(root, name)
            bin_type = name.split('.png')[0]
            yield bin_type, path

def get_trashes(path="static/trash/"):
    for root, dirs, files in os.walk(path):
        for name in files:
            path = os.path.join(root, name)
            trash_type = root.split('/')[-1]
            yield trash_type, path


def get_backgrounds(path="static/backgrounds"):
    for root, dirs, files in os.walk(path):
        for name in files:
            path = os.path.join(root, name)
            yield path
