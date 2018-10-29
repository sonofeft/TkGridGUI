.. 2018-10-27 sonofeft e964e0c3c1a8cd9b2b519778d7fcea1b1d494239
   Maintain spacing of "History" and "GitHub Log" titles

History
=======

GitHub Log
----------

* Oct 27, 2018
    - (by: sonofeft) 
        - Added fg+bg color selector
* Oct 25, 2018
    - (by: sonofeft) 
        - history update

* Oct 25, 2018
    - (by: sonofeft) 
        - Fixed some coordination betweenPreviewWin and GridNotebook
* Oct 24, 2018
    - (by: sonofeft) 
        - removed warning for pre-alpha
        - passed basic Linux and Windows for py 2.7 and 3.x
        - working out multi-platform bugs
        - First Commit to GitHub
    - (by: Charlie Taylor) 
        - Initial commit

Mercurial Log
-------------


* Oct 23, 2018
    - (by: sonofeft)
        - added Help and started Docs
        - Some source cleanup
        - Added delete containers
        
* Oct 22, 2018
    - (by: sonofeft)
        - added console_script launch, fixed self.MainWin, changed row/col insert
        - added changed file warnings for New, Open and Exit
        - fixed drag and drop, tab switching, error-on-open

* Oct 19, 2018
    - (by: sonofeft)
        - made newForm more comprehensive.
        - Made menu ctrl keys optional
        - Added helpful line3 to Labels on grid_notebook

* Oct 18, 2018
    - (by: sonofeft)
        - added accelerator keys to menu and some dialog fixes
        - added get_docstring

* Oct 17, 2018
    - (by: sonofeft)
        - added button bind to Treeview
        - makes source with all widgets
        - made tab selections in grid_notebook affect Preview and visa-versa
        - fixed read of tabs with widgets
        - added x and xy scrolling
        - fixed moving Tabs on Notebook

* Oct 16, 2018
    - (by: sonofeft)
        - First semi-working notebook

* Oct 13, 2018
    - (by: sonofeft)
        - made highlight corrections for edited widget
        - wrapped all preview widgets with PW_Widget to enable scroll bars and future expansions

* Oct 10, 2018
    - (by: sonofeft)
        - enabled y scrolling for Text, Canvas, Listbox and Treeview
        - changed duplicate widget label to show current selection as well

* Oct 09, 2018
    - (by: sonofeft)
        - hooked up dialog StrinVar to results
        - added OK and Cancel buttons to dialog PreviewWin
        - got weights working for Main and container widgets
        - Fixed some basic weights functionality

* Oct 08, 2018
    - (by: sonofeft)
        - added repaint_all_labels with rowspan columnspan logic
        - added rowspan colspan and duplicate widget

* Oct 07, 2018
    - (by: sonofeft)
        - fixed load error with larger than default grid size
        - removed widget weight attribute
        - added friendly controls to edit widget attr

* Oct 06, 2018
    - (by: sonofeft)
        - Added label to Canvas PreviewWin
        - made common StringVar for RadioGroups
        - first working rewrite of component source gen
        - started new component source gen logic

* Oct 05, 2018
    - (by: sonofeft)
        - Menu and statusbar show on launch
        - put menu and statusbar on PreviewWin
        - fixed menu format in \*.def file

* Oct 04, 2018
    - (by: sonofeft)
        - set up Menubutton source generation
        - fixed Spinbox from\_ and StringVar
        - corrected all print to py3.x

* Oct 03, 2018
    - (by: sonofeft)
        - First semi-working source code generation
        - added basic source generation from tk_happy
        - added file read/save
        - lots of active interface updates

* Oct 02, 2018
    - (by: sonofeft)
        - made editing a double click
        - Added edit dialog

* Oct 01, 2018
    - (by: sonofeft)
        - got all widgets displaying
        - go PreviewWin working and drop onto container objects

* Sep 30, 2018
    - (by: sonofeft)
        - made initial stand-alone grid_notebook
        - moved GridWidget out of project

* Sep 29, 2018
    - (by: sonofeft)
        - added drag and drop
        - Added debug Add All Widgets Button

* Sep 28, 2018
    - (by: sonofeft)
        - Added Notebook

* Sep 26, 2018
    - (by: sonofeft)
        - started adding config_file
        - moved widget creation to widget_defs
        - commit just before removing None option

* Sep 25, 2018
    - (by: sonofeft)
        - added cursor changes to grid controls
        - First commit of rough layout

* Sep 24, 2018
    - (by: sonofeft)
        - First Created TkGridGUI with PyHatch