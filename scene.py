class Scene (object):
    # When False, the Escape key is passed to the scene instead of quitting the game.
    esc_quits = True

    def __init__(self, director):
        self.director = director
        self.next = None

    def on_event(self, event):
        pass

    def on_update(self):
        pass

    def on_display(self, screen):
        pass
