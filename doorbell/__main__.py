import sys
import os
from doorbell import Doorbell
import signal
import logging

def shutdown(doorbell):
    logging.warning('You pressed Ctrl+C!')
    doorbell.shutdown()
    sys.exit(0)


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    doorbell = Doorbell()
    try:
        signal.signal(signal.SIGINT, lambda sig, frame: shutdown(doorbell))
        doorbell.run()
    except KeyboardInterrupt:
        doorbell.shutdown()
    else:
        doorbell.shutdown()


def pid_is_running(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return
    else:
        return pid


def write_pidfile_or_die(pidfile):
    if os.path.exists(pidfile):
        pid = int(open(pidfile).read())
        if pid_is_running(pid):
            logging.warning("Sorry, found a pidfile! Process {0} is still running.".format(pid))
            sys.exit(-1)
    else:
        pid = str(os.getpid())
        open(pidfile, 'w').write(pid)


if __name__ == "__main__":
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    pidfile = "/tmp/doorbell-pi.pid"
    write_pidfile_or_die(pidfile)
    try:
        main()
    finally:
        os.unlink(pidfile)
