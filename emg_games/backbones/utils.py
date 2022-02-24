import os

__all__ = ['collide_in', 'get_targets', 'get_projectiles', 'get_backgrounds']


# TODO write better collision function
def collide_in(obj1, obj2):
    ((obj1_x1, obj1_y1), (obj1_x2, obj1_y2)) = obj1.corners
    ((obj2_x1, obj2_y1), (obj2_x2, obj2_y2)) = obj2.corners

    if obj1_x1 >= obj2_x1 and obj1_x2 <= obj2_x2:
        return True

    return False


# TODO fix path to use __file__
def get_targets(class_name):
    path = "static/" + class_name + "/target/"
    for root, dirs, files in os.walk(path):
        for name in files:
            path = os.path.join(root, name)
            target_type = name.split('.png')[0]
            yield target_type, path


# TODO fix path to use __file__
def get_projectiles(class_name):
    path = "static/" + class_name + "/projectile/"
    for root, dirs, files in os.walk(path):
        for name in files:
            path = os.path.join(root, name)
            trash_type = root.split('/')[-1]
            yield trash_type, path


# TODO fix path to use __file__
def get_backgrounds(class_name):
    path = "static/" + class_name + "/backgrounds/"
    for root, dirs, files in os.walk(path):
        for name in files:
            path = os.path.join(root, name)
            yield path
