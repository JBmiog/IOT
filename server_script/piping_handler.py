# stack overflow -> embed-bash-in-python
def run_script(script, stdin=None):
    print(script)
    """Returns (stdout, stderr), raises error on non-zero return code"""
    import subprocess
    # Note: by using a list here (['bash', ...]) you avoid quoting issues, as the
    # arguments are passed in exactly this order (spaces, quotes, and newlines won't
    # cause problems):
    proc = subprocess.Popen(['bash', '-c', script],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        stdin=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode:
        exception = "probably illigal character in filename such as ( %^  or a space)!"
        print(exception)
        # raise ScriptException(proc.returncode, stdout, stderr, script)
    return stdout, stderr



class ScriptException(Exception):
    def __init__(self, returncode, stdout, stderr, script):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        print("returncode", returncode)
        print("stdout", stdout)
        print("stderr", stderr)
        print("script", script)


