# noinspection PyNoneFunctionAssignment
class GameObject:
    def __init__(self, app, pos):

        self.app = app

        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()

    def get_pix_pos(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def move(self):
        pass

    def time_to_move(self):
        pass
