
import south
from south.db import db
from django.db import models

class Migration(object):
    def forwards(self, orm):
        print 'core', '0003_bbb', 'up'
        plugins = getattr(south, 'plugins', {})
        for p in plugins.get(("core", "0003_bbb"), set()):
            p.forwards(orm)

    def backwards(self, orm):
        print 'core', '0003_bbb', 'down'
        plugins = getattr(south, 'plugins', {})
        for p in plugins.get(("core", "0003_bbb"), set()):
            p.backwards(orm)

    models = {
    }

