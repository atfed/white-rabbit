VITAL_DATA = ['gname', 'xres', 'yres']

class Config:
    def __init__(self, conftype):
        self.conftype = conftype
        self.data = dict()

    def add(self, name, value):
        self.data[name] = value

    def __repr__(self):
        response = f'{self.conftype} - Configuration:\n'
        for i in self.data:
            response += f'{i} = {self.data[i]},'
        return response
