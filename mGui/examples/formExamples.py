import maya.cmds as cmds

from mGui import gui, forms

"""
This example creates a window which shows many of the different types of form layouts in mGui.
"""


def create_sphere(*args, **kwargs):
    print "create my sphere"
    cmds.polySphere()


def create_cube(*args, **kwargs):
    print "create my cube"
    cmds.polyCube()


def create_cone(*args, **kwargs):
    print "create my cone"
    cmds.polyCone()


def create_plane(*args, **kwargs):
    print "create my plane"
    cmds.polyPlane()


def create_cylinder(*args, **kwargs):
    print "create my cylinder"
    cmds.polyCylinder()


COMMANDS = [('Create Sphere', create_sphere),
            ('Create Cube', create_cube),
            ('Create Cone', create_cone),
            ('Create Plane', create_plane),
            ('Create Cylinder', create_cylinder)]


def example_Forms(*args, **kwargs):
    """
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_Forms()
    """
    # Defining these in here, because well, the functions don't exist yet.
    examples = [("FillForm", example_FillForm),
                ("FooterForm", example_FooterForm),
                ("HeaderForm", example_HeaderForm),
                ("HorizontalExpandForm", example_HorizontalExpandForm),
                ("HorizontalForm", example_HorizontalForm),
                ("HorizontalStretchForm", example_HorizontalStretchForm),
                ("HorizontalThreePane", example_HorizontalThreePane),
                ("VerticalExpandForm", example_VerticalExpandForm),
                ("VerticalForm", example_VerticalForm),
                ("VerticalStretchForm", example_VerticalStretchForm),
                ("VerticalThreePane", example_VerticalThreePane)]

    with gui.Window(title="Forms Examples", height=128) as window:
        with forms.FillForm(margin=(12, 12)):
            with forms.HeaderForm(width=320) as main:
                gui.ScrollField(height=80,
                                text="""This example shows many of the different kinds of formlayout presets in mGui.forms. Click buttons to show examples, and resize the windows to see the behavior""",
                                ww=True, ed=0)
                with forms.VerticalForm(spacing=(0, 4)):
                    for example_name, example_command in examples:
                        gui.Button(label=example_name).command += example_command

    window.show()


def example_FillForm(*args, **kwargs):
    """
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_FillForm()
    """
    with gui.Window(title="FillForm") as window:
        with forms.FillForm(width=320, margin=(12, 12)) as main:
            for label, command in COMMANDS:
                gui.Button(label="Expands to fill form").command += command

    window.show()


def example_FooterForm(*args, **kwargs):
    """
    Warning: If you give this layout less than one child there will be an error.
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_FooterForm()
    """
    with gui.Window(title="FooterForm") as window:
        with forms.FooterForm(width=320, margin=(12, 12)) as main:
            gui.ScrollField(text="expandable top section")
            gui.Button(label='footer')
    window.show()


def example_HeaderForm(*args, **kwargs):
    """
    Warning: If you give this layout less than one child there will be an error.
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_HeaderForm()
    """
    with gui.Window(title="HeaderForm") as window:
        with forms.HeaderForm(width=320, margin=(12, 12)) as main:
            gui.Button(label='header')
            gui.ScrollField(text="expandable bottom section")

    window.show()


def example_HorizontalExpandForm(*args, **kwargs):
    """
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_HorizontalExpandForm()
    """
    with gui.Window(title="HorizontalExpandForm") as window:
        with forms.HorizontalExpandForm(margin=(12, 12)) as main:
            gui.Button(label="Items Stack Horizontally")

            for label, command in COMMANDS:
                gui.Button(label=label).command += command
            gui.ScrollField(text="Last item expands", ed=0, ww=1)

    window.show()


def example_HorizontalForm(*args, **kwargs):
    """
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_HorizontalForm()
    """
    with gui.Window(title="HorizontalForm", height=64, width=512) as window:
        with forms.HorizontalForm(width=320, margin=(12, 12)) as main:
            gui.ScrollField(text="Components stack horizontally", ed=0, width=128, ww=True)
            for label, command in COMMANDS:
                gui.Button(label=label, width=80).command += command

    window.show()


def example_HorizontalStretchForm(*args, **kwargs):
    """
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_HorizontalStretchForm()
    """
    with gui.Window(title="HorizontalStretchForm", height=64, width=512) as window:
        with forms.HorizontalStretchForm(width=320, margin=(12, 12)) as main:
            gui.ScrollField(text="Components stretch horizontally", ed=0, ww=True, width=64, height=40)

            for label, command in COMMANDS:
                gui.Button(label=label, height=40).command += command

    window.show()


def example_HorizontalThreePane(*args, **kwargs):
    """
    Warning: If you give this layout less than three children there will be an error.
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_HorizontalThreePane()
    """
    with gui.Window(title="HorizontalThreePane", height=64, width=512) as window:
        with forms.HorizontalThreePane(width=320, margin=(12, 12)) as main:
            gui.ScrollField(text="Fixed left pane", ed=0, width=128)

            for index, (label, command) in enumerate(COMMANDS):
                if index > 2:
                    break
                gui.Button(label=label, width=32).command += command
            gui.ScrollField(text="Fixed right pane", ed=0, width=128)

    window.show()


def example_VerticalExpandForm(*args, **kwargs):
    """
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_VerticalExpandForm()
    """
    with gui.Window(title="VerticalExpandForm", height=128) as window:
        with forms.VerticalExpandForm(width=320, margin=(12, 12)) as main:
            gui.ScrollField(text="Components stack vertically", ed=0, height=24)
            for label, command in COMMANDS:
                gui.Button(label=label).command += command
            gui.ScrollField(text="last item stretches", ed=0, height=48)

    window.show()


def example_VerticalForm(*args, **kwargs):
    """
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_VerticalForm()
    """
    with gui.Window(title="VerticalForm", resizeToFitChildren=True) as window:
        with forms.VerticalForm(width=320, margin=(12, 12)) as main:
            gui.ScrollField(text="Components stack vertically", ed=0, height=24)

            for label, command in COMMANDS:
                gui.Button(label=label).command += command

    window.show()


def example_VerticalStretchForm(*args, **kwargs):
    """
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_VerticalStretchForm()
    """
    with gui.Window(title="VerticalStretchForm", height=400) as window:
        with forms.VerticalStretchForm(width=320, margin=(12, 12)) as main:
            gui.ScrollField(text="Components Stretch vertically", ed=0, height=24)
            for label, command in COMMANDS:
                gui.Button(label=label).command += command
    window.show()


def example_VerticalThreePane(*args, **kwargs):
    """
    Warning: If you give this layout less than three children there will be an error.
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_VerticalThreePane()
    """
    with gui.Window(title="VerticalThreePane") as window:
        with forms.VerticalThreePane(None, width=320, height=320, margin=(12, 12)) as main:
            gui.ScrollField(text="Fixed Header, stretchy center", height=24, ed=False)
            for index, (label, command) in enumerate(COMMANDS):
                if index > 3:
                    break
                gui.Button(label=label, height=24).command += command

            gui.ScrollField(text="Fixed footer", height=24, ed=0)
    window.show()


if __name__ == '__main__':
    example = example_Forms()
