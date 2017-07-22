class Settings:

    def __init__(self, settings):
        self.settings = settings

    def __getattr__(self, attr_name):
        return self.settings[attr_name]
