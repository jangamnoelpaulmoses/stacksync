import subprocess
import tempfile
import os
import json

NSJAIL      = "/usr/bin/nsjail"
PYTHON_BIN  = "/usr/local/bin/python3"
USE_NSJAIL  = os.getenv("USE_NSJAIL", "true").lower() in ("1","true","yes")

def execute_script(code: str):
    fd, path = tempfile.mkstemp(suffix=".py")
    os.write(fd, code.encode("utf-8"))
    os.close(fd)

    # Build command
    if USE_NSJAIL:
        cmd = [
            NSJAIL,
            "--mode", "o",                    # run once then exit
            "--disable_proc",                 # no /proc
            "-N",                             # disable networking
            "--cwd", "/tmp",                  # workdir
            "--time_limit", "5",              # seconds
            "--max_cpus", "1",                # one CPU
            "--rlimit_as", str(256*1024*1024),   # 256 MB VAS
            "--rlimit_fsize", str(10*1024*1024),  # 10 MB writes
            "--rlimit_nofile", "16",          # max FDs
            "--rlimit_nproc", "16",           # max procs
            "-R", "/:/",                      # mount container root RO
            "-B", "/tmp:/tmp",                # mount /tmp RW
            "-q",                             # quiet logs
            "--", PYTHON_BIN, path
        ]
    else:
        # Cloud Run: skip nsjail
        cmd = [PYTHON_BIN, path]

    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=7,
            text=True,
        )
    finally:
        os.remove(path)

    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip())

    out = proc.stdout.strip()
    # Parse last line as JSON
    try:
        last_line = out.splitlines()[-1]
        result = json.loads(last_line)
    except Exception:
        raise RuntimeError("main() must print its JSON return as the last line")

    if not isinstance(result, dict):
        raise RuntimeError("main() must return a JSON object (dict)")

    return {"result": result, "stdout": out}
