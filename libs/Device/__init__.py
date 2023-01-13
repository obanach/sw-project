
class Device:

    def __init__(self, d_id, d_type, d_name):
        self.d_id = d_id
        self.d_type = d_type
        self.d_name = d_name
        self.actions = None

        if d_type == 'light':
            self.actions = None

    def details(self):
        return [self.d_id, self.d_type, self.d_name]

