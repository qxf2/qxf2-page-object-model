import pathlib

dirs = ["page_objects", "conf", "tests", "utils"]

def create_repo():
    "Create the Test Framework repo locally"
    for dir in dirs:
        path = pathlib.Path(dir)
        path.mkdir(parents=True, exist_ok=True)