from pathlib import Path

class Helper:
    @staticmethod
    def get_project_root() -> Path:
        return Path(__file__).parent.parent.parent
