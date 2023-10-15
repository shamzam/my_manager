import configparser


def read_config(config, filename, section="database"):
    config_parser = configparser.ConfigParser()
    config_parser.read(filename)

    try:
        for name in config.__annotations__:
            setattr(config, name, config_parser[section][name])
    except KeyError as e:
        print(f"{e} didn't exists")
