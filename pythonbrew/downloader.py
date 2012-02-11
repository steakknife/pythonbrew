from pythonbrew.define import PYTHON_VERSION_URL, PYTHONBREW_STABLE_VERSION_URL, \
    PYTHONBREW_UPDATE_URL_PYPI, PYTHONBREW_UPDATE_URL_MASTER,\
    PYTHONBREW_UPDATE_URL_DEVELOP
from pythonbrew.log import logger
from pythonbrew.curl import Curl
from pythonbrew.util import to_str

def get_headerinfo_from_url(url):
    c = Curl()
    return c.readheader(url)

def get_stable_version():
    c = Curl()
    return to_str(c.read(PYTHONBREW_STABLE_VERSION_URL).strip())

class Downloader(object):
    def download(self, msg, url, path, _hash = None):
        logger.info("Downloading %s as %s" % (msg, path))
        c = Curl()
        c.fetch(url, path)
        if _hash:
            check_hash(self, msg, path, _hash)
            
    def check_hash(self, msg, path, _hash):
        import hashlib
        hasher = hashlib.sha()
        with open(path,'rb') as f: 
            for chunk in iter(lambda: f.read(8192), ''): 
                hasher.update(chunk)
        if hasher.hexdigest() != _hash:
            import os
            os.unlink(path)
            raise Exception("Hash on %s failed (was %s, expected %s)" % (msg, hasher.hexdigest, _hash))

def get_pythonbrew_update_url(version):
    if version == "master":
        return PYTHONBREW_UPDATE_URL_MASTER
    elif version == 'develop':
        return PYTHONBREW_UPDATE_URL_DEVELOP
    else:
        return PYTHONBREW_UPDATE_URL_PYPI % (version)

def get_python_version_url(version):
    return PYTHON_VERSION_URL.get(version)
