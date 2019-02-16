class Configs():
    configs = {}

    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.load_configs()

    def get_config_by_name(self, name):
        return self.configs[name]

    def get_all_configs(self):
        return self.configs

    def load_configs(self):
        self.configs = {}
        config_file = open(self.config_file_path, 'r')
        for line in config_file:
            split_line = line.split('=')
            self.configs[split_line[0]] = split_line[1].strip('\n')
