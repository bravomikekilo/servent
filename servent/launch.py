import os
import io
import sys
from collections import namedtuple

def launch(main, args, log_path):
    try:
        pid = os.fork()
    except OSError as e:
        raise Exception("%s, [%d]" % (e.strerror, e.errno))
    if(pid != 0):
        os._exit(0)
    # child process1
    os.setsid()

    try:
        pid = os.fork()
    except OSError as e:
        raise Exception('%s, [%d]' % (e.strerror, e.errno))

    if(pid != 0):
        os._exit(0)

    with open(log_path, 'w') as f:
    # now we get into second process
        no_stdout = sys.stdout.fileno()
        sys.stdout.flush()
        sys.stdout.close()

        no_stderr = sys.stderr.fileno()
        sys.stderr.flush()
        sys.stderr.close()

        os.dup2(f.fileno(), no_stdout)
        os.dup2(f.fileno(), no_stderr)

        sys.stdout = io.TextIOWrapper(os.fdopen(no_stdout, 'wb'))
        sys.stderr = io.TextIOWrapper(os.fdopen(no_stderr, 'wb'))

        print(pid, flush=True)
        hyper = namedtuple('HyperParameter', args.keys())(*args.values())
        main.run(hyper)
    exit(0)


