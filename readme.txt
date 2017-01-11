#mGui 
###A module for simplifying Maya GUI coding

## Basics
mGui is a python module for simplifying GUI creation using Maya's built-in gui widgets. As such it is not a replacement for something more sophisticated, like PyQT or PySide - it's a way to make simple UI more quickly and reliably (and without the need for distributing any DLLs in older versions of Maya).

The goal is to provide the most consistent and least wordy way of creating simple GUI in Maya. Instead of this:


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

you can write this:
	     
    bound = ImmediateObservableCollection("pCube1", "pPlane1")
    
    with BindingWindow(title = 'example window') as test_window:
        with VerticalForm() as main:
            Text(label = "The following items don't have vertex colors")
            list_view = VerticalList()
            list_view.bind.collection < bind() < bound
            with HorizontalStretchForm('buttons'):
                Button('refresh', l='Refresh')
                Button('close', l='Close')
    test_window.show()             
	            
And make adjustments like this:

   main.buttons.refresh.backgroundColor = (.7, .7, .5)
   
   
   
The module has two main parts.

## Declarative layout

*mGui.core* defines two classes, **Control** and **Layout**. These do the same job: wrapping maya UI objects with a property-oriented syntax.  The *mGui.controls* and *mGui.layouts* provide subclasses of these for all of the control and layout widgets in Maya.


## Bindings

A lot of repetitive GUI coding is simply about shuffling little bits of data around - set the name of a button to match the selected item, or change the color of a field based on what is selected and so on.  In order to simplify this we provide  _bindings_ - classes for getting information from one place and putting it somewhere else. mGui bindings provide a limited form of automatic notifications for data, allowing you to automatically flow updates from the underlying data to the display in your GUI.  In the example above, for example, widgets are created when the collection `bound` is edited, even though there's no need to explicitly revisit the GUI when you manipulate the connection.

This is a very powerful feature and will be familiar if you've used data bindings in WPF or QT. If you find it intimidating... well, mGui works fine without it.
