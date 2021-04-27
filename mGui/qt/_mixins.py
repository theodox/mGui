from maya import cmds
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin


class QWidgetBaseMixin(MayaQWidgetBaseMixin):
    def __init__(self, parent=None, *args, **kwargs):
        super(QWidgetBaseMixin, self).__init__(parent, *args, **kwargs)
        try:
            cmds.setParent(self)
        except RuntimeError:
            pass

    def __unicode__(self):
        return self.objectName()

    def __repr__(self):
        return self.objectName()
