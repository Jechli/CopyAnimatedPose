"""
A TOOL TO COPY AN ANIMATED RIG POSE TO STATIC RIG (OR ANY RIG FOR THAT MATTER)
"""


from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui


""" Getting a reference to the main maya window """
def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


"""
Copy Pose Tool class

Encapsulates all the UI and functionality of the tool.

"""

class CopyPoseTool(QtWidgets.QDialog):
    
    """ Initialize Class """
    def __init__(self, parent=maya_main_window()):
        super(CopyPoseTool, self).__init__(parent)
        
        # Set up window
        self.setWindowTitle("Copy Pose Tool")
        self.setMinimumWidth(500)
        self.setWindowFlags(QtCore.Qt.Window)
        
        # Lists for storing pose information after pressing Copy Pose button
        self.copied_rig_joint_names = []
        self.copied_rig_translate = []
        self.copied_rig_rotate = []
        
        # UI layout
        self.create_widgets()
        self.create_main_layout()
        self.create_connections()
        self.update_lists()
        
        
    """ Creates all the widgets that will be used in building the UI """    
    def create_widgets(self):
        
        # Button to refresh lists
        self.refresh_button = QtWidgets.QPushButton("Refresh Lists")
        
        # Section for selecting an animated rig to copy from
        self.copy_from_label = QtWidgets.QLabel("Copy Pose From")
        self.copy_from_label.setStyleSheet("padding:5px; font-weight:bold;")
        
        self.copy_pose_list = QtWidgets.QListWidget()
        self.copy_pose_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.copy_button = QtWidgets.QPushButton("Copy Pose")
        
        self.copy_pose_layout = QtWidgets.QVBoxLayout()
        self.copy_pose_layout.addWidget(self.copy_from_label)
        self.copy_pose_layout.addWidget(self.copy_pose_list)
        self.copy_pose_layout.addWidget(self.copy_button)
        
        # Section for selecting a static rig to paste to
        self.paste_to_label = QtWidgets.QLabel("Paste Pose To")
        self.paste_to_label.setStyleSheet("padding:5px; font-weight:bold;")
        
        self.paste_pose_list = QtWidgets.QListWidget()
        self.paste_pose_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.paste_button = QtWidgets.QPushButton("Paste Pose")
        
        self.paste_pose_layout = QtWidgets.QVBoxLayout()
        self.paste_pose_layout.addWidget(self.paste_to_label)
        self.paste_pose_layout.addWidget(self.paste_pose_list)
        self.paste_pose_layout.addWidget(self.paste_button)
        
        
    """ Puts together all the widgets for the overall UI layout """ 
    def create_main_layout(self):
        
        # Set up the layout of the overall UI window
        self.pose_section_layout = QtWidgets.QHBoxLayout()
        self.pose_section_layout.addLayout(self.copy_pose_layout)
        self.pose_section_layout.addLayout(self.paste_pose_layout)
        
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.refresh_button)
        self.main_layout.addLayout(self.pose_section_layout)
        

    """ Creates connections to functionality for user actions """
    def create_connections(self):
        
        # Any functionality that needs to be linked to selecting items on the lists and clicking the buttons
        self.refresh_button.clicked.connect(self.update_lists)
        self.copy_pose_list.itemClicked.connect(self.copy_rig_item_selected)
        self.paste_pose_list.itemClicked.connect(self.paste_rig_item_selected)
        self.copy_button.clicked.connect(self.copy_pose)
        self.paste_button.clicked.connect(self.paste_pose)
        

    """ Updates the rig lists if any rigs have been added/deleted in the scene """
    def update_lists(self):
        
        # Get all root joints in the scene
        list_of_rigs = [jnt for jnt in cmds.ls(type='joint') if not cmds.listRelatives(jnt, parent=True,type='joint')]
        
        # Clear the list to have a clean start
        self.copy_pose_list.clear()
        self.paste_pose_list.clear()
        
        # Add the rigs to the list
        for rig in list_of_rigs:
            self.copy_pose_list.addItem(rig)
            self.paste_pose_list.addItem(rig)
     
    
    """ Select the copy-from rig in the scene when it is selected in the list """
    def copy_rig_item_selected(self):   
    
        selected_rig = self.copy_pose_list.currentItem().text()
        cmds.select(selected_rig)
        
        
    """ Add to the selection the copy-to rig in the scene when it is selected in the list """
    def paste_rig_item_selected(self):
        
        # Reselect the copy-from rig to refresh the selection
        if len(cmds.ls(selection=True)) > 1:
            self.copy_rig_item_selected()
            
        # Add the copy-to rig to the selection
        selected_rig = self.paste_pose_list.currentItem().text()
        cmds.select(selected_rig, add=True)
        
    
    """ Save the copy-from rig pose information into the 3 lists that were initialized in this class
    
    This is done recursively with the add_joints_to_copy_list() function. It will recursrively go through all the joints connected from the root to the tips.
    """
    def copy_pose(self):
        
        # Clear lists
        self.copied_rig_joint_names.clear()
        self.copied_rig_translate.clear()
        self.copied_rig_rotate.clear()
        
        # Save copy-from pose information
        root = self.copy_pose_list.currentItem().text()
        self.add_joints_to_copy_list(root)
        

    """ Paste the copied rig pose information onto the rig that was chosen to be copied to
    
    This is done recursively with the copy_pose_to_rig() function. It will recursrively go through all the joints connected from the root to the tips.
    """
    def paste_pose(self):
        
        # Only paste pose if there is rig pose information that has been copied
        if (len(self.copied_rig_joint_names) and len(self.copied_rig_translate) and len(self.copied_rig_rotate)):
            root_index = 0
            root = self.paste_pose_list.currentItem().text()
            self.copy_pose_to_rig(root_index, root)
            
        
    """ Recursively goes through all the joints from root to tips and saves the joint information into the 3 lists created at class initialization """    
    def add_joints_to_copy_list(self, root):
        
        # Get translation and rotation information from given root joint
        root_translate = cmds.getAttr(root+'.translate')
        root_rotate = cmds.getAttr(root+'.rotate')
        
        # The 3 lists containing the names of the joints, and their translation and rotation information
        self.copied_rig_joint_names.append(root)
        self.copied_rig_translate.append(root_translate)
        self.copied_rig_rotate.append(root_rotate)
        
        # Get all child joints
        children = cmds.listConnections(root, type="joint", source=False)
        
        # Recursively copy the information from the child joints
        if (children):
            for child in children:
                self.add_joints_to_copy_list(child)


    """ Recursively goes through all the joints from root to tips and copies the joint information to the chosen static rig """  
    def copy_pose_to_rig(self, root_index, root):
        
        # Filtering for transation information from list of tuples
        translate_tuple = self.copied_rig_translate[root_index][0]
        translate_X = translate_tuple[0]
        translate_Y = translate_tuple[1]
        translate_Z = translate_tuple[2]
        
        # Filtering for rotation information from list of tuples
        rotate_tuple = self.copied_rig_rotate[root_index][0]
        rotate_X = rotate_tuple[0]
        rotate_Y = rotate_tuple[1]
        rotate_Z = rotate_tuple[2]
        
        # Select joint to set keyframes and values for it
        cmds.select(root)
        
        # Setting the value and keyframes for the joint at the current frame in the viewport
        cmds.setKeyframe(value=translate_X, attribute='translateX')
        cmds.setKeyframe(value=translate_Y, attribute='translateY')
        cmds.setKeyframe(value=translate_Z, attribute='translateZ')
        cmds.setKeyframe(value=rotate_X, attribute='rotateX')
        cmds.setKeyframe(value=rotate_Y, attribute='rotateY')
        cmds.setKeyframe(value=rotate_Z, attribute='rotateZ')
        
        # Update for the next joint 
        new_root_index = root_index + 1
        
        # Get all children of current joint
        children = cmds.listConnections(root, type="joint", source=False)
        
        # Recursively run this function on child joints
        if (children):
            for child in children:
                new_root_index = self.copy_pose_to_rig(new_root_index, child)
        
        # The new index for the next recursion
        return new_root_index


"""
Run Copy Pose Tool Window
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