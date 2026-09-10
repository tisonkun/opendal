#!/usr/bin/env python3
"""Capture native Cargo diagnostics without changing its exit status."""
import datetime
import json
import os
import resource
import subprocess
import sys
import time

started = time.monotonic()
args = sys.argv[1:]
with open(os.environ["OPENDAL_CARGO_TRACE"], "a", buffering=1) as trace:
    def record(message):
        stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        trace.write(f"[{stamp}] {message}\n")

    record("COMMAND " + json.dumps(args))
    # Quiet output is the only command option changed by this experiment.
    command = [os.environ["OPENDAL_REAL_RUSTUP"], *[arg for arg in args if arg != "--quiet"]]
    child = subprocess.Popen(command, stderr=subprocess.PIPE)
    for line in child.stderr:
        record(line.decode(errors="replace").rstrip())
        sys.stderr.buffer.write(line)
        sys.stderr.buffer.flush()
    code = child.wait()
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    record(f"EXIT {code}; wall={time.monotonic() - started:.3f}s; user={usage.ru_utime:.3f}s; system={usage.ru_stime:.3f}s")
sys.exit(code)
