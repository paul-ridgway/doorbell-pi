import sys
from doorbell import Doorbell

PI = False

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    doorbell = Doorbell()
    doorbell.run()

if __name__ == "__main__":
    main()