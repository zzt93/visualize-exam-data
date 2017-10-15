import os
import tempfile
import subprocess
import shutil
import scandir


class ExtractController(object):
    def __init__(self, paths):
        if isinstance(paths, str):
            self.paths = [paths]
        elif isinstance(paths, list):
            self.paths = paths
        else:
            raise ValueError('{} parameter error'.format(self.__class__))
        self.temp_dir = None

    def __enter__(self):
        self.temp_dir = tempfile.mkdtemp(dir='/tmp')
        for path in self.paths:
            if path.endswith('zip'):
                ex = ['unzip', path, '-d', tempfile.mkdtemp(dir=self.temp_dir)]
            elif path.endswith('rar'):
                ex = ['unrar', 'x', path, tempfile.mkdtemp(dir=self.temp_dir)]
            else:
                raise ValueError('This is not a archive file')
            subprocess.call(ex)
        return self.temp_dir

    def __exit__(self, exc_type, exc_val, exc_tb):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None
        if exc_type is None:
            pass
        else:
            return False


def scan_dir(dir_path, pattern=None, dir_level=-1):
    def inner_scan_project(in_path, level=0):
        for entry in scandir.scandir(in_path):
            if dir_level == level:
                if pattern is None:
                    yield entry.path
                else:
                    if pattern(entry.name):
                        yield entry.path
                continue
            if entry.is_dir():
                yield from inner_scan_project(entry.path, level=level+1)
            elif entry.is_file():
                if pattern is None:
                    yield entry.path
                else:
                    if pattern(entry.name):
                        yield entry.path
    yield from inner_scan_project(dir_path)
