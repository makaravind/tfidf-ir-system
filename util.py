import pickle
import os


def save_obj(obj, name):
    with open('meta/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('meta/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def is_saved(name):
    return os.path.exists('meta/' + name + '.pkl')
