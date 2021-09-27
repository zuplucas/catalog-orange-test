import subprocess


# Todo use https://github.com/gitpython-developers/GitPython
def commit_all_files(target, msg):
    subprocess.check_call(["git", "add", "."], cwd=str(target))
    subprocess.check_call(["git", "commit", "-m", msg], cwd=str(target))
    output = subprocess.check_output(
        ['git', 'log', '--format="%H"', '-n', '1'], cwd=str(target)).decode("utf-8")
    output = output.replace('"', "")
    output = output.replace('\n', "")
    return output


# Todo use https://github.com/gitpython-developers/GitPython
def revert_commit(target, commit_id):
    subprocess.check_call(
        ["git", "revert", commit_id, "--no-edit"], cwd=str(target))


def init_git(target):
    subprocess.check_call(["git", "init"], cwd=str(target))
