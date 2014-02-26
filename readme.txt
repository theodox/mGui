#mGui 
###A module for simplifying Maya GUI coding

## Basics
mGui is a python module for simplifying GUI creation using Maya's built-in gui widgets. As such it is not a replacement for something more sophisticated, like PyQT or PySide - it's a way to make simple UI more quickly and reliably (and without the need for distributing any DLLs in older versions of Maya).

The goal is to provide the most consistent and least wordy way of creating simple GUI in Maya. Instead of this:

<ex>

you can write this:

<ex>

And make adjustments like this:

<ex>


The module has two main parts.

*mGui.core* defines two classes, **Control** and **Layout**. These do the same job: wrapping maya UI objects with a property-oriented syntax.  The *mGui.controls* and *mGui.layouts* provide subclasses of these for all of the control and layout widgets in Maya.


