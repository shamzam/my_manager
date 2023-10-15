import configparser


class Config:
    db_host: str
    db_name: str
    db_user: str
    db_pass: str
    db_port: str

    def read_config(self, filename, section="database"):
        config_parser = configparser.ConfigParser()
        config_parser.read(filename)

        try:
            for name in self.__annotations__:
                setattr(self, name, config_parser[section][name])
        except KeyError as e:
            print(f"{e} didn't exists")
