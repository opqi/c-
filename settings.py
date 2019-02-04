import pytoml as toml

PACKAGE_NAME = 'MD5_light'


def load_config(path):
    with open(path) as f:
        conf = toml.load(f)
    return conf
