class Column():
    def __init__(self, name, data_type):
        self.name = name
        self.data_type = data_type

    def __repr__(self) -> str:
        return f'{self.name} {self.data_type}'
