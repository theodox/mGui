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


## Bindings

A lot of repetitive GUI coding is simply about shuffling little bits of data around - set the name of a button to match the selected item, or change the color of a field based on what is selected and so on.  In order to simplify this we provide  _bindings_ - classes for getting information from one place and putting it somewhere else. The 