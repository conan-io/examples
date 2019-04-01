
from conans import tools

def get_version():
    git = tools.Git()
    try:
        branch = git.get_branch().replace('/', '-')
        rev = git.get_revision()[:8]
        return "%s_%s" % (branch, rev)
    except:
        return None
