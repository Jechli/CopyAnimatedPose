from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

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
        
        self.copied_rig_joint_names = []
        self.copied_rig_translate = []
        self.copied_rig_rotate = []
        
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
        
        self.pose_section_layout = QtWidgets.QHBoxLayout()
        self.pose_section_layout.addLayout(self.copy_pose_layout)
        self.pose_section_layout.addLayout(self.paste_pose_layout)
        
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addLayout(self.pose_section_layout)
        

    def create_connections(self):
        
        self.copy_pose_list.itemClicked.connect(self.copy_rig_item_selected)
        self.paste_pose_list.itemClicked.connect(self.paste_rig_item_selected)
        self.copy_button.clicked.connect(self.copy_pose)
        self.paste_button.clicked.connect(self.paste_pose)
        

    def update_lists(self):
        
        list_of_rigs = [jnt for jnt in cmds.ls(type='joint') if not cmds.listRelatives(jnt, parent=True,type='joint')]
        self.copy_pose_list.clear()
        self.paste_pose_list.clear()
        for rig in list_of_rigs:
            self.copy_pose_list.addItem(rig)
            self.paste_pose_list.addItem(rig)
        
        
    """
    Functionality
    """
    
    def copy_rig_item_selected(self):   
        selected_rig = self.copy_pose_list.currentItem().text()
        cmds.select(selected_rig)
        
    
    def paste_rig_item_selected(self):
        
        if len(cmds.ls(selection=True)) > 1:
            self.copy_rig_item_selected()
            
        selected_rig = self.paste_pose_list.currentItem().text()
        cmds.select(selected_rig, add=True)
        
    
    def copy_pose(self):
        
        self.copied_rig_joint_names.clear()
        self.copied_rig_translate.clear()
        self.copied_rig_rotate.clear()
        
        root = self.copy_pose_list.currentItem().text()
        self.add_joints_to_copy_list(root)
        
        print(self.copied_rig_joint_names)
        print(self.copied_rig_translate)
        print(self.copied_rig_rotate)
        

    def paste_pose(self):
        
        if (len(self.copied_rig_joint_names) and len(self.copied_rig_translate) and len(self.copied_rig_rotate)):
            root_index = 0
            root = self.paste_pose_list.currentItem().text()
            self.copy_pose_to_rig(root_index, root)
            
        
    def add_joints_to_copy_list(self, root):
        
        root_translate = cmds.getAttr(root+'.translate')
        root_rotate = cmds.getAttr(root+'.rotate')
        
        self.copied_rig_joint_names.append(root)
        self.copied_rig_translate.append(root_translate)
        self.copied_rig_rotate.append(root_rotate)
        
        children = cmds.listConnections(root, type="joint", source=False)
        
        if (children):
            for child in children:
                self.add_joints_to_copy_list(child)


    def copy_pose_to_rig(self, root_index, root):
        
        translate_tuple = self.copied_rig_translate[root_index][0]
        translate_X = translate_tuple[0]
        translate_Y = translate_tuple[1]
        translate_Z = translate_tuple[2]
        
        rotate_tuple = self.copied_rig_rotate[root_index][0]
        rotate_X = rotate_tuple[0]
        rotate_Y = rotate_tuple[1]
        rotate_Z = rotate_tuple[2]
        
        cmds.setAttr(root+'.translateX', translate_X)
        cmds.setAttr(root+'.translateY', translate_Y)
        cmds.setAttr(root+'.translateZ', translate_Z)
        cmds.setAttr(root+'.rotateX', rotate_X)
        cmds.setAttr(root+'.rotateY', rotate_Y)
        cmds.setAttr(root+'.rotateZ', rotate_Z)
        
        new_root_index = root_index + 1
        
        children = cmds.listConnections(root, type="joint", source=False)
        
        if (children):
            for child in children:
                new_root_index = self.copy_pose_to_rig(new_root_index, child)
        
        return new_root_index


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