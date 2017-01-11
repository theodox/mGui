import sys
import maya.cmds as cmds
from mGui import gui, forms


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

    with gui.Window(title="Forms Examples") as window:
        with forms.VerticalExpandForm(width=320) as main:
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
        with forms.FillForm(width=320) as main:
            for label, command in COMMANDS:
                gui.Button(label=label).command += command

    window.show()


def example_FooterForm(*args, **kwargs):
    """
    Warning: If you give this layout less than one child there will be an error.
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_FooterForm()
    """
    with gui.Window(title="FooterForm") as window:
        with forms.FooterForm(width=320) as main:
            for index, (label, command) in enumerate(COMMANDS):
                if index > 1:
                    break
                gui.Button(label=label).command += command

    window.show()


def example_HeaderForm(*args, **kwargs):
    """
    Warning: If you give this layout less than one child there will be an error.
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_HeaderForm()
    """
    with gui.Window(title="HeaderForm") as window:
        with forms.HeaderForm(width=320) as main:
            for index, (label, command) in enumerate(COMMANDS):
                if index > 1:
                    break
                gui.Button(label=label).command += command

    window.show()


def example_HorizontalExpandForm(*args, **kwargs):
    """
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_HorizontalExpandForm()
    """
    with gui.Window(title="HorizontalExpandForm") as window:
        with forms.HorizontalExpandForm(width=320) as main:
            for label, command in COMMANDS:
                gui.Button(label=label).command += command

    window.show()


def example_HorizontalForm(*args, **kwargs):
    """
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_HorizontalForm()
    """
    with gui.Window(title="HorizontalForm") as window:
        with forms.HorizontalForm(width=320) as main:
            for label, command in COMMANDS:
                gui.Button(label=label).command += command

    window.show()


def example_HorizontalStretchForm(*args, **kwargs):
    """
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_HorizontalStretchForm()
    """
    with gui.Window(title="HorizontalStretchForm", height=400) as window:
        with forms.HorizontalStretchForm(width=320) as main:
            for label, command in COMMANDS:
                gui.Button(label=label).command += command

    window.show()


def example_HorizontalThreePane(*args, **kwargs):
    """
    Warning: If you give this layout less than three children there will be an error.
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_HorizontalThreePane()
    """
    with gui.Window(title="HorizontalThreePane") as window:
        with forms.HorizontalThreePane(None, width=320) as main:
            for index, (label, command) in enumerate(COMMANDS):
                if index > 3:
                    break
                gui.Button(label=label).command += command

    window.show()


def example_VerticalExpandForm(*args, **kwargs):
    """
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_VerticalExpandForm()
    """
    with gui.Window(title="VerticalExpandForm") as window:
        with forms.VerticalExpandForm(width=320) as main:
            for label, command in COMMANDS:
                gui.Button(label=label).command += command

    window.show()


def example_VerticalForm(*args, **kwargs):
    """
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_VerticalForm()
    """
    with gui.Window(title="VerticalForm", resizeToFitChildren=True) as window:
        with forms.VerticalForm(width=320) as main:
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
        with forms.VerticalStretchForm(width=320) as main:
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
        with forms.VerticalThreePane(None, width=320) as main:
            for index, (label, command) in enumerate(COMMANDS):
                if index > 3:
                    break
                gui.Button(label=label).command += command

    window.show()


if __name__ == '__main__':
    example = example_Forms()
