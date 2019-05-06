
from conans import tools

def get_version():
    git = tools.Git()
    try:
        rev = git.get_revision()[:8]
        return rev
    except:
        return None
