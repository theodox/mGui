"""
forms.py

A variety of specialized subclasses of FormLayout which are good shortcuts for common layout problems.
@author: Stephen Theodore


@note

Did some empirical testing, and it appears that lots of attachments is slower
than lots of simple forms. Thus generating a columnLayout containing 1000
buttons, each wrapped in its own formlayout takes .86 seconds on my machine;
where one formlayout with 1000 buttons takes 1.89 seconds if the buttons are
attached to both sides of form and 1.25 if they are not; a differences of
between 50 and 100%

The same 1000 buttons with no individual form layouts  = .53 seconds

For this reason prefer row or column or flowlayouts for repetitive stuff and use
forms for the main architecture

However, for less complex UI groups of 100-odd sets of 3 controls (300 total)
came in under .25s, so it's not a big deal in common cases

"""
import itertools

import maya.cmds as cmds

from mGui.core.layouts import FormLayout
from mGui.styles import Bounds


def physical_controls(widget):
    return (i for i in widget.controls if i.CMD not in (cmds.popupMenu, cmds.menuItem))


class Form(FormLayout):
    """
    A wrapper for FormLayout with convenience methods for attaching controls.
    Use this when you need precise control over form behavior.

    Formbase is entirely manual - it does no automatic layout behavior.

    """

    def __init__(self, key=None, **kwargs):
        super(Form, self).__init__(key, **kwargs)
        self.margin = Bounds(*self._style.get('margin', (0, 0)))
        self.spacing = Bounds(*self._style.get('spacing', (0, 0)))

    def _fill(self, ctrl, *sides, **kwargs):
        """
        convenience wrapper for tedious formLayout editing
        """
        margin = kwargs.get('margin', None)
        ct = [ctrl for _ in sides]
        mr = [margin for _ in sides]
        if margin is None:
            mr = [self.margin[_] for _ in sides]
        self.attachForm = zip(ct, sides, mr)

    def top(self, ctrl, margin=None):
        """
        Docks 'ctrl' against the top of the form, with the supplied margin on top, left and right
        """
        self._fill(ctrl, 'top', 'left', 'right', margin=margin)

    def left(self, ctrl, margin=None):
        """
        dock 'ctrl' along the left side of the form with the supplied margin
        """
        self._fill(ctrl, 'top', 'left', 'bottom', margin=margin)

    def right(self, ctrl, margin=None):
        """
        dock 'ctrl' along the right side of the form with the supplied margin
        """
        self._fill(ctrl, 'top', 'bottom', 'right', margin=margin)

    def bottom(self, ctrl, margin=None):
        """
        dock 'ctrl' along the bottom of the form with the supplied margin
        """
        self._fill(ctrl, 'bottom', 'left', 'right', margin=margin)

    def fill(self, ctrl, margin=None):
        """
        docks 'ctrl' into the form filling it completely with suppled margin on all sides
        """
        sides = ['top', 'bottom', 'left', 'right']
        self._fill(ctrl, *sides, margin=margin)

    def snap(self, ctrl1, ctrl2, edge, space=None):
        """
        docs 'ctrl1' to 'ctrl2' along the supplied edge (top, left, etc) with the supplied margin
        """
        if space is None: space = self.spacing[edge]
        self.attachControl = (ctrl1, edge, space, ctrl2)

    def form_attachments(self, *sides):
        """
        returns a list of (control, side, spacing) values used by attachForm style commands
        """
        attachments = ([side, self.margin[side]] for side in sides)
        ctls = itertools.product(physical_controls(self), attachments)
        return [[a] + b for a, b in ctls]

    def form_series(self, side):
        """
        returns a series of (control, side, space, control) for use in serial placement
        """
        first, second = itertools.tee(physical_controls(self))
        second.next()
        return [(s, side, self.spacing[side], f) for f, s in itertools.izip(first, second)]

    def percentage_series(self, side):

        side2 = {'left': 'right', 'right': 'left', 'top': 'bottom', 'bottom': 'top'}[side]

        widths = [i.width if hasattr(i, 'width') else 0 for i in physical_controls(self)]
        total_width = sum(widths)
        proportions = map(lambda q: q * 100.0 / total_width, widths)
        p_l = len(proportions)
        left_edges = [sum(proportions[:r]) for r in range(0, p_l)]
        right_edges = [sum(proportions[:r]) for r in range(1, p_l + 1)]
        ap = []
        for c, l, r in itertools.izip(physical_controls(self), left_edges, right_edges):
            ap.append((c, side, self.spacing[side], l))
            ap.append((c, side2, self.spacing[side2], r))
        return ap

    def equal_series(self, side):
        side2 = {'left': 'right', 'right': 'left', 'top': 'bottom', 'bottom': 'top'}[side]

        widths = [1 for each_item in physical_controls(self)]
        total_width = sum(widths)
        proportions = map(lambda q: q * 100.0 / total_width, widths)
        p_l = len(proportions)
        left_edges = [sum(proportions[:r]) for r in range(0, p_l)]
        right_edges = [sum(proportions[:r]) for r in range(1, p_l + 1)]
        ap = []
        for c, l, r in itertools.izip(physical_controls(self), left_edges, right_edges):
            ap.append((c, side, self.spacing[side], l))
            ap.append((c, side2, self.spacing[side2], r))
        return ap

    def dock(self, ctrl, top=None, left=None, right=None, bottom=None):
        """
        docks ctrl into the form.

        for each of the optional flags (top, bottom, left, & right), the arguments are interpreted as follows:
        None (default):  Ignore this edge
        Number (eg 10):  dock to form with this margin along this edge
        (ctrl2, number): dock to other control 'ctrl2' along this edge, with supplied margin
        """

        if not hasattr(top, '__iter__'): top = (None, top)
        if not hasattr(bottom, '__iter__'): bottom = (None, bottom)
        if not hasattr(left, '__iter__'): left = (None, left)
        if not hasattr(right, '__iter__'): right = (None, right)

        ac = lambda edge, other, margin: cmds.formLayout(self.widget, e=True, ac=(ctrl, edge, margin, other))
        af = lambda edge, ignore, margin: cmds.formLayout(self.widget, e=True, af=(ctrl, edge, margin))

        if top[0]:
            ac('top', *top)
        elif top[1]:
            af('top', *top)

        if left[0]:
            ac('left', *left)
        elif left[1]:
            af('left', *left)

        if bottom[0]:
            ac('bottom', *bottom)
        elif bottom[1]:
            af('bottom', *bottom)

        if right[0]:
            ac('right', *right)
        elif right[1]:
            af('right', *right)

    def detach(self, *controls):
        """
        call AttachNone on all
        """
        sides = ('top', 'bottom', 'left', 'right')
        # note the order : it's backwards from the others!
        cmds.formLayout(self.widget, an=[(ctl, side) for side, ctl in itertools.product(sides, controls)])


class LayoutDialogForm(Form):
    """
    Shim that will create a formLayout wrapper from an existing formLayout.
    Used with the maya LayoutDialog command, which creates a form for you,
    so you can still use mGui property access.
    """

    def __init__(self, key):
        self.CMD = self.fake_create
        super(LayoutDialogForm, self).__init__(key)
        self.CMD = cmds.formLayout

    @staticmethod
    def fake_create(*args, **kwargs):
        return cmds.setParent(q=True)


class FillForm(Form):
    """
    Docks the first child so it fills the entire form with the specified margin
    """

    def layout(self):
        for item in physical_controls(self):
            self.fill(item)
        return len(self.controls)


class VerticalForm(Form):
    """
    Lays out children vertically. The first child is attached to the top of
    the form, all children are attached to the left and right
    """

    def layout(self):
        if len(self.controls):
            ctrls = [i for i in physical_controls(self)]

            af = self.form_attachments('left', 'right')
            af.append([ctrls[0], 'top', self.spacing.top])
            ac = self.form_series('top')
            self.attachForm = af
            self.attachControl = ac

        return len(self.controls)


class HorizontalForm(Form):
    """
    Lays out children horizontally. The first child is attacked to the left of
    the form, all children are attached to the top and bottom
    """

    def layout(self):
        if len(self.controls):
            ctrls = [i for i in physical_controls(self)]
            af = self.form_attachments('top', 'bottom')
            af.append((ctrls[0], 'left', self.spacing.top))
            ac = self.form_series('left')
            self.attachForm = af
            self.attachControl = ac
        return len(self.controls)


class VerticalExpandForm(Form):
    """
    Lays out children vertically. The first child is attached to the top of
    the form, and the last to the bottom. The last division will expand with the
    form.
    """

    def layout(self):
        if len(self.controls):
            ctrls = [i for i in physical_controls(self)]
            af = self.form_attachments('left', 'right')
            af.append((ctrls[0], 'top', self.spacing.top))
            af.append((ctrls[-1], 'bottom', self.spacing.bottom))
            ac = self.form_series('top')
            self.attachForm = af
            self.attachControl = ac
        return len(self.controls)


class HorizontalExpandForm(Form):
    """
    Lays out children horizontally. The first child is attacked to the left of
    the form, and the last to the right. The last division will expand with the
    form.
    """

    def layout(self):
        if len(self.controls):
            af = self.form_attachments('top', 'bottom')
            af.append((self.controls[0], 'left', self.spacing.top))
            ac = self.form_series('left')
            self.attachForm = af
            self.attachControl = ac
        return len(self.controls)


class HorizontalStretchForm(Form):
    """
    Lays out children horizontally. All children will scale proportionally as the form changes size
    """

    def layout(self):
        if len(self.controls):
            af = self.form_attachments('top', 'bottom')
            ap = self.percentage_series('left')
            self.attachForm = af
            self.attachPosition = ap
        return len(self.controls)


class VerticalStretchForm(Form):
    """
    Lays out children vertically, with sizes proportional to their original heights
    """

    def layout(self):
        if len(self.controls):
            af = self.form_attachments('left', 'right')
            ap = self.percentage_series('top')
            self.attachForm = af
            self.attachPosition = ap
        return len(self.controls)


class VerticalThreePane(Form):
    """
    First child is glued to the top, last child is glued to the bottom, intermediate childredn are stretched
    """

    def layout(self):
        if len(self.controls) < 3:
            raise ValueError("VerticalThreePane requires at least 3 children")
        af = self.form_attachments('left', 'right')
        ap = self.percentage_series('top')
        self.attachForm = af
        self.attachForm = (self.controls[-1], 'bottom', self.spacing.bottom)
        self.attachPosition = ap[2:-2]
        self.attachControl = (self.controls[1], 'top', self.spacing.top, self.controls[0])
        self.attachControl = (self.controls[-2], 'bottom', self.spacing.bottom, self.controls[-1])
        return len(self.controls)


class HorizontalThreePane(Form):
    """
    First child is glued to the left, last child is glued to the right, intermediate childredn are stretched
    """

    def layout(self):
        if len(self.controls) < 3:
            raise ValueError("HorizontalThreePane requires at least 3 children")
        af = self.form_attachments('top', 'bottom')
        ap = self.percentage_series('left')
        self.attachForm = af
        self.attachForm = (self.controls[-1], 'right', self.spacing.right)
        self.attachPosition = ap[2:-2]
        self.attachControl = (self.controls[1], 'left', self.spacing.left, self.controls[0])
        self.attachControl = (self.controls[-2], 'right', self.spacing.right, self.controls[-1])
        return len(self.controls)


class FooterForm(VerticalForm):
    """
    A vertical layout with two children. The first expands with the container, the second is glued to the bottom
    """

    def layout(self):
        if len(self.controls) != 2:
            raise ValueError("FooterForm requires at exactly 2 children")
        af = self.form_attachments('left', 'right')
        self.attachForm = af
        self.attachForm = (self.controls[0], 'top', self.spacing.top)
        self.attachForm = (self.controls[-1], 'bottom', self.spacing.bottom)
        self.attachControl = (self.controls[0], 'bottom', self.spacing.bottom, self.controls[1])
        return len(self.controls)


class HeaderForm(VerticalForm):
    """
    A vertical layout with two children. The second expands with the container, the first is glued to the top
    """

    def layout(self):
        if len(self.controls) != 2:
            raise ValueError("FooterForm requires at exactly 2 children")
        af = self.form_attachments('left', 'right')
        self.attachForm = af
        self.attachForm = (self.controls[0], 'top', self.spacing.top)
        self.attachForm = (self.controls[-1], 'bottom', self.spacing.bottom)
        self.attachControl = (self.controls[1], 'top', self.spacing.bottom, self.controls[0])
        return len(self.controls)


class NavForm(HorizontalForm):
    """
    A two-pane horizontal form. THe first is fixed to the left size, the second expands with the container
    """

    def layout(self):
        af = self.form_attachments('top', 'bottom')
        self.attachForm = af
        self.attachForm = (self.controls[0], 'left', self.margin.left)
        self.attachForm = (self.controls[-1], 'right', self.margin.right)
        self.attachControl = (self.controls[1], 'left', self.spacing.left, self.controls[0])
        return len(self.controls)


__all__ = ['FillForm', 'VerticalForm', 'HorizontalForm', 'VerticalExpandForm', 'HorizontalExpandForm',
           'VerticalStretchForm', 'HorizontalStretchForm', 'HorizontalThreePane', 'VerticalThreePane',
           'HeaderForm', 'FooterForm', 'NavForm']
