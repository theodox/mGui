# mGui 
### A module for simplifying Maya GUI coding

## Basics
mGui is a python module for simplifying GUI creation using Maya's built-in gui widgets. As such it is not a replacement for something more sophisticated, like PyQT or PySide - it's a way to make simple UI more quickly and reliably (and without the need for distributing any DLLs in older versions of Maya).

The goal is to provide the most consistent and least wordy way of creating simple GUI in Maya. Instead of this:

```python
items = ("pCube1", "pPlane2")
window  = cmds.window()
w, margin = 400, 10
mainform = cmds.formLayout( width=w ) 
maincol = cmds.columnLayout( adj=True ) 
main_attach = [( maincol, 'top', margin ), ( maincol, 'left', margin ), ( maincol, 'right', margin )]
col_w = int( ( w - ( margin * 2 ) ) / 3 ) - 1
cmds.setParent( mainform ) 
dis_row = cmds.rowLayout( nc=3, ct3=( 'both', 'both', 'both' ), cw3=( col_w, col_w, col_w ) ) 
dis_attach = [( dis_row, 'bottom', margin ), ( dis_row, 'left', margin ), ( dis_row, 'right', margin )]
cmds.formLayout( mainform, e=True, attachForm=main_attach + dis_attach ) 
cmds.formLayout( mainform, e=True, ac=( maincol, 'bottom', margin, dis_row ) ) 
cmds.setParent( dis_row ) 
cmds.button( "Refresh", width=col_w)
cmds.text( ' ' ) 
cmds.button( "Close", width=col_w)
cmds.setParent( maincol ) 
cmds.text( " " ) 
cmds.text( "The following items don't have vertex colors:", align='left' ) 
cmds.text( " " ) 
Itemlist = cmds.textScrollList( numberOfRows=8, allowMultiSelection=True, append=items ) 
dis_row = cmds.rowLayout( nc=5, ct5=( 'both', 'both', 'both', 'both', 'both' ) ) 
cmds.showWindow(window)
```
you can write this:
```python

bound = ObservableCollection("pCube1", "pPlane1")

with BindingWindow(title = 'example window') as test_window:
    with VerticalForm() as main:
        Text(label = "The following items don't have vertex colors")
        list_view = VerticalList()
        list_view.bind.collection < bind() < bound
        with HorizontalStretchForm() as buttons:
            Button('refresh', l='Refresh')
            Button('close', l='Close')
test_window.show()             
```
And make adjustments like this:
```python
main.buttons.refresh.backgroundColor = (.7, .7, .5)
```


# Key parts

## mGui.gui: object oriented gui classes

The main tool in the library is a complete wrapper set for for all of the widgets in the 
Maya GUI library in the module **mGui.gui**.  These wrapper classes are assembled using a 
special metaclass which allows you to get and set their properties with traditional dot 
notation, rather than Maya's cumbersome command-based syntax.  Layouts, windows and menus are 
treated as context managers,  allowing you to write neatly nested layouts and keep your 
logical structure separate from the visual details.  The layouts also 'know' the names of their
children, so that you can access controls directly through the hierarchy of your layout: 
in the example above, you can acces the 'close' button as
```python
example_window.main.buttons.refresh
```
without doing any manual management of variables.


## Styles

To make it easier to manage the visual look of your layouts -- and more importantly, to keep the
visuals separated cleanly from the logical structure of the code -- **mgui.Styles** creates
style dictionaries which work very much like CSS styles in web design.  Styles can be targeted at 
individual controls or entire classes of controls; they can be inherited and overridden for maximal
flexibility.


## Bindings

A lot of repetitive GUI coding is simply about shuffling little bits of data around - setting the name
of a button to match that of the selected item, changing the color of a field based on the state of 
a checkbox, and so on.  

In order to simplify this process, **mGui.bindings** defines  _Bindings_ - classes which can get information
 from one place and putting it somewhere else in a structured way. Bindings can be created declaratively,
 rather than requiring you to manually manage the relationships. Thus
```python
Text('example').bind.label < bind() < 'pCube1.tx'
```
 will set the label of a text widget to the X-transform of pCube1, while
 
     CheckBox('vis').bind.value > bind() > 'pCube1.visibility' 
     
 will tie the visibility of the cube to the state of the checkbox.
 
 The module `mGui.lists` provides a set of pre-built collection widgets designed for use with binding. The `VerticalList`, `HorizontalList`, `WrapList` and `ColumnList` will draw items in a scrolling list view for every item in their bound collections. The `itemTemplate` class allows you to create a custom widget display for any incoming data type, so you can create rich UIs with inline controls, multiple lines of data, and customizable styles.
 
## Forms 

The traditional Maya formLayout command is the most powerful and flexible type of layout. Unfortunately, it's also the most awkward to use. Attaching childrent to a form requires creating long chains of argument which are tough to read and to parse.

**mGui.forms** provides a number of pre-built forms, which automatically attach their own children in predictable ways.  The key types are:

*  **HorizontalForm** and **VerticalForm**.  As the names imply, these lay out their children horizontally or vertically, each child snapped to the previous one. The form expands but the children don't move. 
*  **HorizontalExpandForm** and **VerticalExpandForm** are similar to regular forms, except that the last child will expand with the form.  They are commonly used to divide an area between a header and content, or between a navigation column and content.
*  **HorizontalStretchForm** and **VerticalStretchForm** will expand all their children as the overall form grows or shrink. Handy for things like maintaining evenly sized divisions in a window.
*  **HorizontalThreePane** and **VerticalThreePane**  These form expect exactly three children. The first and last children are glues to the beginning and end of the form, respectively, while the middle child expands with the form. Handy for layouts with headers and footers or with tools surrounding a content pane.

## Events

Maya GUI widgets can fire callbacks, but they have several important limitations. In particular, vanilla 
Maya callbacks don't retain any knowledge of the widget which sent them, which obliges you to write complex 
code to track callbacks to their sources and understand their context.

**mGui.Events** introduces event delegates - classes which catch maya gui callbacks when they fire and add
useful information about the widget which raised the callback. These events can be forwarded to multiple handlers,
so that a single button press can move an object in your scene, highlight a button, and print a message in the help
line using 3 simple functions rather than one big monster with lots of unrelated moving parts.  


# Installation

The directory **mGui** is a Python package. Simply drop a copy of it into a location that's visible to your python path. You can then import modules in the usual way.

# Usage

The module **mGui.gui** contains most of the key components: the windows, buttons, layouts and so on (they are defined in other modules, particulary **mGui.core.controls** and **mGui.core.layouts**, but collected into the *gui** module for easier access in your code.  **mGui.gui** is safe for star imports -- as safe as it can be, anyway --  so a common idiom is
```python
from mGui.gui import *

with Window('example') as w:
    with ColumnLayout('cl'):
        Text('msg', 'Hello World!')
```
The main components are named identically to their Maya.cmds counterparts except for the fact that, being classes rather than commands, they are capitalized. Thus  **cmds.button** becomes **mGui.gui.Button**. **cmds.window** becomes **mGui.gui.Window** and so on.

# Learm more

Check out our [wiki pages](https://github.com/theodox/mGui/wiki).  We're always looking for volunteers to help us improve our documentation!

----------------

This project is provided under the MIT License: it's free for any kind of use as long as you retain the copyright notice in *`mGui.__init__`*.  
     
