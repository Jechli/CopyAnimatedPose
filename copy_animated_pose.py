from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import pymel.core as pm

"""
COPY ANIMATED RIG POSE TO STATIC RIG
"""

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class CopyPoseTool(QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(CopyPoseTool, self).__init__(parent)
        
        self.setWindowTitle("Copy Pose Tool")
        self.setMinimumWidth(500)
        self.setWindowFlags(QtCore.Qt.Window)
        
        self.copied_rig = []
        
        self.create_widgets()
        self.create_main_layout()
        self.create_connections()
        self.update_lists()
        
        
    def create_widgets(self):
        
        # Section for selecting an animated rig to copy from
        
        self.copy_from_label = QtWidgets.QLabel("Copy Pose From")
        self.copy_from_label.setStyleSheet("padding:5px; font-weight:bold;")
        
        self.copy_pose_list = QtWidgets.QListWidget()
        self.copy_pose_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.copy_button = QtWidgets.QPushButton("Copy")
        
        self.copy_pose_layout = QtWidgets.QVBoxLayout()
        self.copy_pose_layout.addWidget(self.copy_from_label)
        self.copy_pose_layout.addWidget(self.copy_pose_list)
        self.copy_pose_layout.addWidget(self.copy_button)
        
        
        # Section for selecting a static rig to paste to
        
        self.paste_to_label = QtWidgets.QLabel("Paste Pose To")
        self.paste_to_label.setStyleSheet("padding:5px; font-weight:bold;")
        
        self.paste_pose_list = QtWidgets.QListWidget()
        self.paste_pose_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.paste_button = QtWidgets.QPushButton("Paste")
        
        self.paste_pose_layout = QtWidgets.QVBoxLayout()
        self.paste_pose_layout.addWidget(self.paste_to_label)
        self.paste_pose_layout.addWidget(self.paste_pose_list)
        self.paste_pose_layout.addWidget(self.paste_button)
        
        
    def create_main_layout(self):
        
        # Reorganize the copy and paste selection lists on the main layout
        self.pose_section_layout = QtWidgets.QHBoxLayout()
        self.pose_section_layout.addLayout(self.copy_pose_layout)
        self.pose_section_layout.addLayout(self.paste_pose_layout)
        
        # Adding sectional layouts to main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addLayout(self.pose_section_layout)
        
        
    def create_connections(self):
        self.copy_pose_list.itemClicked.connect(self.copy_rig_selected)
        self.paste_pose_list.itemClicked.connect(self.paste_rig_selected)
        self.copy_button.clicked.connect(self.copy_pose)
        self.paste_button.clicked.connect(self.paste_pose)
        
    def update_lists(self):
        pass
        
        
    """
    Functionality
    """

    # Save the rig joint information
    def copy_rig_selected(self):
        self.copied_rig.clear()
        # Grey out any static rigs that don't match joint numbers
    
    # Paste copied rig joint info to selected static rig    
    def paste_rig_selected(self):
        pass
        
    
    def copy_pose(self):
        pass
        
    def paste_pose(self):
        pass


"""
Run Window
"""         
if __name__ == "__main__":
    try:
        ui.deleteLater()
    except:
        pass
    ui = CopyPoseTool()
    
    try:
        ui.show()
    except:
        ui.deleteLater()