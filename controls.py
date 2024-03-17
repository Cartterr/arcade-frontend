class SelectionController:
    def __init__(self):
        self.selected = 0  # Start with left option selected

    def move_left(self):
        self.selected = 0

    def move_right(self):
        self.selected = 1

    def get_selected(self):
        return self.selected
