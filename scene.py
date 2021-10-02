class Scene (object):
    def __init__(self, director):
        self.done = False
        self.director = director
        self.next = None
        self.prev = None

    def on_event (self, event):
        pass

    def on_update (self):
        pass

    def on_display (self, screen):
        pass
