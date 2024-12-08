from WebAPI.User.UserController import UserController

class BlueprintManager:
    def __init__(self, app):
        self.app = app
        self.blueprints = []

    def add_blueprint(self, blueprint):
        self.blueprints.append(blueprint)

    def register_blueprints(self):
        for blueprint in self.blueprints:
            self.app.register_blueprint(blueprint)
