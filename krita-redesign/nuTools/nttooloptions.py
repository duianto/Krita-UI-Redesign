from PyQt5.QtWidgets import QMdiArea, QDockWidget
from .ntadjusttosubwindowfilter import ntAdjustToSubwindowFilter
from .ntwidgetpad import ntWidgetPad

class ntToolOptions():

    def __init__(self, window):
        qWin = window.qwindow()
        mdiArea = qWin.findChild(QMdiArea)
        toolOptions = qWin.findChild(QDockWidget, 'sharedtooldocker')

        # Create "pad"
        self.pad = ntWidgetPad(mdiArea)
        self.pad.setObjectName("toolOptionsPad")
        self.pad.setViewAlignment('right')
        self.pad.borrowDocker(toolOptions)
        # self.pad.setStyleSheet(self.styleSheet()) # Maybe worth tinkering with another time

        # Create and install event filter
        self.adjustFilter = ntAdjustToSubwindowFilter(mdiArea)
        self.adjustFilter.setTargetWidget(self.pad)
        mdiArea.subWindowActivated.connect(self.ensureFilterIsInstalled)
        qWin.installEventFilter(self.adjustFilter)

        # Create visibility toggle action 
        action = window.createAction("showToolOptions", "Show Tool Options", "settings")
        action.toggled.connect(self.pad.toggleWidgetVisible)
        action.setCheckable(True)
        action.setChecked(True)

        # Disable the related QDockWidget
        self.dockerAction = self.findDockerAction(window, "Tool Options")
        self.dockerAction.setEnabled(False)


    def ensureFilterIsInstalled(self, subWin):
        """Ensure that the current SubWindow has the filter installed,
        and immediately move the Toolbox to current View."""
        if subWin:
            subWin.installEventFilter(self.adjustFilter)
            self.pad.adjustToView()
    

    def findDockerAction(self, window, text):
        dockerMenu = None
        
        for m in window.qwindow().actions():
            if m.objectName() == "settings_dockers_menu":
                dockerMenu = m

                for a in dockerMenu.menu().actions():
                    if a.text().replace('&', '') == text:
                        return a
                
        return False


    def styleSheet(self):
        return """
            * { 
                background-color: #00000000;
            }
            
            .QScrollArea { 
                background-color: #00000000;
            }
            
            QScrollArea * { 
                background-color: #00000000;
            }
            
            QScrollArea QToolTip {
                background-color: #ffffff;                           
            }
            
            QToolButton, QPushButton {
                background-color: #80000000;
                border: none;
                border-radius: 4px;
            }
            
            QToolButton:checked, QPushButton:checked {
                background-color: #aa306fa8;
            }
            
            QToolButton:hover, QPushButton:hover {
                background-color: #1c1c1c;
            }
            
            QToolButton:pressed, QPushButton:pressed {
                background-color: #53728e;
            }

            QAbstractSpinBox {
                background-color: #80000000;
                border: none;
                border-radius: 4px;
            }

            QComboBox {
                background-color: #80000000;
                border: none;
                border-radius: 4px;
            }

            KisSliderSpinBox {
                background-color: #80000000;
                border: none;
            }
        """
    
    def close(self):
        self.dockerAction.setEnabled(True)
        return self.pad.close()