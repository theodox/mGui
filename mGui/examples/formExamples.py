import maya.cmds as cmds
import mGui.gui as gui
import mGui.forms as forms


def create_sphere(*arg, **kwarg):
    print "create my sphere"
    cmds.polySphere()


def create_cube(*arg, **kwarg):
    print "create my cube"
    cmds.polyCube()


def create_cone(*arg, **kwarg):
    print "create my cone"
    cmds.polyCone()


def create_plane(*arg, **kwarg):
    print "create my plane"
    cmds.polyPlane()


def create_cylinder(*arg, **kwarg):
    print "create my cylinder"
    cmds.polyCylinder()


commands2 = [{'label': 'Create Sphere',
              'command': create_sphere},
             {'label': 'Create Cube',
              'command': create_cube},
             {'label': 'Create Cone',
              'command': create_cone},
             {'label': 'Create Plane',
              'command': create_plane},
             {'label': 'Create Cylinder',
              'command': create_cylinder}]


def example_FillForm():
    '''
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_HorizontalThreePane()
    '''
    with gui.Window(None, title="Example") as window:
        with forms.FillForm(None, width=320) as main:
            for item in commands2:
                gui.Button(None, label=str(item['label'])).command += item['command']

    cmds.showWindow(window)


def example_FooterForm():
    '''
    Warning: If you give this layout less than one child there will be an error.
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_HorizontalThreePane()
    '''
    with gui.Window(None, title="Example") as window:
        with forms.FooterForm(None, width=320) as main:
            i = 0
            for item in commands2:
                i = i+1
                if i > 1:
                    break
                gui.Button(None, label=str(item['label'])).command += item['command']

    cmds.showWindow(window)


def example_HeaderForm():
    '''
    Warning: If you give this layout less than one child there will be an error.
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_HorizontalThreePane()
    '''
    with gui.Window(None, title="Example") as window:
        with forms.HeaderForm(None, width=320) as main:
            i = 0
            for item in commands2:
                i = i+1
                if i > 2:
                    break
                gui.Button(None, label=str(item['label'])).command += item['command']

    cmds.showWindow(window)


def example_HorizontalExpandForm():
    '''
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_HorizontalExpandForm()
    '''
    with gui.Window(None, title="Example") as window:
        with forms.HorizontalExpandForm(None, width=320) as main:
            for item in commands2:
                gui.Button(None, label=str(item['label'])).command += item['command']

    cmds.showWindow(window)


def example_HorizontalForm():
    '''
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_HorizontalForm()
    '''
    with gui.Window(None, title="Example") as window:
        with forms.HorizontalForm(None, width=320) as main:
            for item in commands2:
                gui.Button(None, label=str(item['label'])).command += item['command']

    cmds.showWindow(window)


def example_HorizontalStretchForm():
    '''
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_HorizontalStretchForm()
    '''
    with gui.Window(None, title="Example", height=400) as window:
        with forms.HorizontalStretchForm(None, width=320) as main:
            for item in commands2:
                gui.Button(None, label=str(item['label'])).command += item['command']

    cmds.showWindow(window)


def example_HorizontalThreePane():
    '''
    Warning: If you give this layout less than three children there will be an error.
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_HorizontalThreePane()
    '''
    with gui.Window(None, title="Example") as window:
        with forms.HorizontalThreePane(None, width=320) as main:
            i = 0
            for item in commands2:
                i = i+1
                if i > 3:
                    break
                gui.Button(None, label=str(item['label'])).command += item['command']

    cmds.showWindow(window)


def example_VerticalExpandForm():
    '''
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_VerticalExpandForm()
    '''
    with gui.Window(None, title="Example") as window:
        with forms.VerticalExpandForm(None, width=320) as main:
            for item in commands2:
                gui.Button(None, label=str(item['label'])).command += item['command']

    cmds.showWindow(window)


def example_VerticalForm():
    '''
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_VerticalForm()
    '''
    with gui.Window(None, title="Example", resizeToFitChildren=True) as window:
        with forms.VerticalForm(None, width=320) as main:
            for item in commands2:
                gui.Button(None, label=str(item['label'])).command += item['command']
    cmds.showWindow(window)


def example_VerticalStretchForm():
    '''
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_VerticalStretchForm()
    '''
    with gui.Window(None, title="Example", height=400) as window:
        with forms.VerticalStretchForm(None, width=320) as main:
            for item in commands2:
                gui.Button(None, label=str(item['label'])).command += item['command']

    cmds.showWindow(window)


def example_VerticalThreePane():
    '''
    Warning: If you give this layout less than three children there will be an error.
    Example:
    import mGui.examples.formExamples as formExamples
    formExamples.example_HorizontalThreePane()
    '''
    with gui.Window(None, title="Example") as window:
        with forms.VerticalThreePane(None, width=320) as main:
            i = 0
            for item in commands2:
                i = i+1
                if i > 3:
                    break
                gui.Button(None, label=str(item['label'])).command += item['command']

    cmds.showWindow(window)
