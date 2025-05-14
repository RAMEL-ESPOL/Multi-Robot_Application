class World():
    def __init__(self, name: str, world_path: str, map_path: str) -> None:
        self.name = name
        self.world_path = world_path
        self.map_path = map_path

    def to_yaml(self) -> dict:
        return {
            'name': self.name,
            'world_path': self.world_path,
            'map_path': self.map_path
        }