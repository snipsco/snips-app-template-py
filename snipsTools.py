import ConfigParser
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section: {option_name : option for option_name, option in self.items(section)} for section in self.sections()}

    @staticmethod
    def read_configuration_file(configuration_file):
        try:
            with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
                conf_parser = SnipsConfigParser()
                conf_parser.readfp(f)
                return conf_parser.to_dict()
        except (IOError, ConfigParser.Error) as e:
            print(e)
            return dict()

    @staticmethod
    def write_configuration_file(configuration_file, data):
        conf_parser = SnipsConfigParser()
        for key in data.keys():
            conf_parser.add_section(key)
            for inner_key in data[key].keys():
                conf_parser.set(key, inner_key, data[key][inner_key])
        try:
            with open(configuration_file, 'w') as f:
                conf_parser.write(f)
        except (IOError, ConfigParser.Error) as e:
            print(e)
            return False

