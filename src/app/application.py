import sys
from mazegenerator import MazeGenerator


class Application:
    @staticmethod
    def run() -> None:
        try:
            generator = MazeGenerator()
            generator.generate()
            print(generator.maze)
        except NotImplementedError as e:
            print(f"Error: not implemented yet: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print("Interrupted,", file=sys.stderr)
            sys.exit(130)
        except Exception as e:
            print(f"Unexpected error: {type(e).__name__}: {e}", file=sys.stderr)
            sys.exit(1)
            