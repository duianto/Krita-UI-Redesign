"""
    Plugin for Krita UI Redesign, Copyright (C) 2020 Kapyia, Pedro Reis

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from krita import *
from .nuTools.nttoolbox import ntToolBox
from .nuTools.nttooloptions import ntToolOptions
from . import variables
from PyQt5.QtWidgets import QMessageBox
    
class Redesign(Extension):

    usesFlatTheme = False
    usesThinDocumentTabs = False
    usesNuToolbox = False
    usesNuToolOptions = False
    ntTB = None
    ntTO = None
 
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        if Application.readSetting("Redesign", "usesFlatTheme", "true") == "true":
            self.usesFlatTheme = True

        if Application.readSetting("Redesign", "usesThinDocumentTabs", "true") == "true":
            self.usesThinDocumentTabs = True

        if Application.readSetting("Redesign", "usesNuToolbox", "true") == "true":
            self.usesNuToolbox = True
        
        if Application.readSetting("Redesign", "usesNuToolOptions", "true") == "true":
            self.usesNuToolOptions = True

    def createActions(self, window):
        actions = [] 

        actions.append(window.createAction("tabHeight", "Thin Document Tabs", ""))
        actions[0].setCheckable(True)
        actions[0].setChecked(self.usesThinDocumentTabs)

        actions.append(window.createAction("flatTheme", "Use flat theme", ""))
        actions[1].setCheckable(True)
        actions[1].setChecked(self.usesFlatTheme)

        actions.append(window.createAction("nuToolbox", "NuToolbox", ""))
        actions[2].setCheckable(True)
        actions[2].setChecked(self.usesNuToolbox)

        actions.append(window.createAction("nuToolOptions", "NuToolOptions", ""))
        actions[3].setCheckable(True)

        if Application.readSetting("", "ToolOptionsInDocker", "false") == "true":
            actions[3].setChecked(self.usesNuToolOptions)

        menu = window.qwindow().menuBar().addMenu("Redesign")

        for a in actions:
            menu.addAction(a)

        actions[0].toggled.connect(self.tabHeightToggled)
        actions[1].toggled.connect(self.flatThemeToggled)
        actions[2].toggled.connect(self.nuToolboxToggled)
        actions[3].toggled.connect(self.nuToolOptionsToggled)

        variables.buildFlatTheme()

        if (self.usesNuToolOptions and
            Application.readSetting("", "ToolOptionsInDocker", "false") == "true"):
                self.ntTO = ntToolOptions(window)
                self.ntTO.pad.show() 
                self.ntTO.updateStyleSheet()

        if self.usesNuToolbox: 
            self.ntTB = ntToolBox(window)
            self.ntTB.pad.show() 
            self.ntTB.updateStyleSheet()

        self.rebuildStyleSheet(window.qwindow())

    def flatThemeToggled(self, toggled):
        Application.writeSetting("Redesign", "usesFlatTheme", str(toggled).lower())

        self.usesFlatTheme = toggled

        self.rebuildStyleSheet(Application.activeWindow().qwindow())

    
    def tabHeightToggled(self, toggled):
        Application.instance().writeSetting("Redesign", "usesThinDocumentTabs", str(toggled).lower())

        self.usesThinDocumentTabs = toggled

        self.rebuildStyleSheet(Application.activeWindow().qwindow())


    def nuToolboxToggled(self, toggled):
        Application.writeSetting("Redesign", "usesNuToolbox", str(toggled).lower())
        self.usesNuToolbox = toggled

        if toggled:
            self.ntTB = ntToolBox(Application.activeWindow())
            self.ntTB.pad.show() 
            self.ntTB.updateStyleSheet()
        elif not toggled and self.ntTB:
            self.ntTB.close()
            self.ntTB = None

    def nuToolOptionsToggled(self, toggled):
        if Application.readSetting("", "ToolOptionsInDocker", "false") == "true":
            Application.writeSetting("Redesign", "usesNuToolOptions", str(toggled).lower())
            self.usesNuToolOptions = toggled

            if toggled:
                self.ntTO = ntToolOptions(Application.activeWindow())
                self.ntTO.pad.show() 
                self.ntTO.updateStyleSheet()
            elif not toggled and self.ntTO:
                self.ntTO.close()
                self.ntTO = None
        else:
            msg = QMessageBox()
            msg.setText("nuTools requires the Tool Options Location to be set to 'In Docker'. \n\n" +
                        "This setting can be found at Settings -> Configure Krita... -> General -> Tools -> Tool Options Location." +
                        "Once the setting has been changed, please restart Krita.")
            msg.exec_()


    def rebuildStyleSheet(self, window):
        full_style_sheet = ""

        # Dockers
        if self.usesFlatTheme:
            full_style_sheet += f"\n {variables.flat_dock_style} \n"
            full_style_sheet += f"\n {variables.flat_button_style} \n"
            full_style_sheet += f"\n {variables.flat_main_window_style} \n"
            full_style_sheet += f"\n {variables.flat_combo_box_style} \n"
            full_style_sheet += f"\n {variables.flat_status_bar_style} \n"
            full_style_sheet += f"\n {variables.flat_tab_style} \n"
            full_style_sheet += f"\n {variables.flat_tree_view_style} \n"
            full_style_sheet += f"\n {variables.flat_menu_bar_style} \n"

            welcomePage = window.findChild(QWidget, 'KisWelcomePage')
            welcomePage.setStyleSheet(variables.flat_welcome_page)

        window.setStyleSheet(full_style_sheet)

        #print("\n\n")
        #print(full_style_sheet)
        #print("\n\n")

        # Overview
        overview = window.findChild(QWidget, 'OverviewDocker')
        overview_style = ""

        # No border for Recent Documents and News Frame
        recentDocuments = window.findChild(QWidget, 'recentDocsStackedWidget')
        newsFrame = window.findChild(QWidget, 'newsFrame')
        remove_frame_elems = [recentDocuments, newsFrame]

        for elem in remove_frame_elems:
            elem.setFrameStyle(QFrame.NoFrame)
            elem.setFrameShape(QFrame.NoFrame)
            elem.setLineWidth(0)
            elem.setStyleSheet("")
        
        if self.usesFlatTheme:
            overview_style += f"\n {variables.flat_overview_docker_style} \n"

        overview.setStyleSheet(overview_style)

        # For document tab
        canvas_style_sheet = ""

        if self.usesThinDocumentTabs:
            canvas_style_sheet += f"\n {variables.small_tab_style} \n"
        else:
            canvas_style_sheet += f"\n {variables.big_tab_style} \n"

        canvas = window.centralWidget()
        canvas.setStyleSheet(canvas_style_sheet)

        # This is ugly, but it's the least ugly way I can get the canvas to 
        # update it's size (for now)
        canvas.resize(canvas.sizeHint())

        # Update Tool Options stylesheet
        if self.usesNuToolOptions and self.ntTO:
            self.ntTO.updateStyleSheet()

        # Update Toolbox stylesheet
        if self.usesNuToolbox and self.ntTB:
            self.ntTB.updateStyleSheet()  

Krita.instance().addExtension(Redesign(Krita.instance()))
