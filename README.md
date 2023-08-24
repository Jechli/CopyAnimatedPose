# CopyAnimatedPose
Created in Maya 2022.

The Copy Pose Tool copies a pose from an animated rig to a static rig in Maya. This is a quick video tutorial on using the tool:

https://github.com/Jechli/CopyAnimatedPose/assets/2565734/d2182d8b-9a85-4689-962f-97e530449e0b


HOW TO USE:

* To quickly open up the UI for the tool for testing, import the file into Maya, select all of the code in the script editor, and press Ctrl+Enter.

![copy_pose_tool](https://github.com/Jechli/CopyAnimatedPose/assets/2565734/d182ccc5-9e1d-45ef-84ba-dc637fb5f2a4)

1. In the viewport of Maya, go to the frame that you would like to copy the pose from.
2. On the left side of the tool, select in the list the rig you want to copy the pose from.
3. Click on the 'Copy Pose' button.
5. On the right side of the tool, select in the list the rig you would like to copy your pose to.
6. Click on the 'Paste Pose' button.

If any rigs have been added / deleted during the time the tool has been opened, there is a 'Refresh Lists' button at the top for updating the rig lists accordingly.


IMPROVEMENTS AND EXTENSIONS


> It is missing a check to see if the rigs are compatible to be copied and pasted between each other.
> Currently the copy and paste functions are done recursively, from the root joint to the tips of the rig without checking the naming. If one can assume that the naming of the joints will always be the same then it could be good to check the names too before copying over.
> It would be good to have an information display about which rig pose at which frame has been last copied.
> The UX can be simplified further by not having a Copy and Paste button; instead, they can be merged into one button. Since we can select both the copy-from and copy-to rigs in the UI the Copy Pose button can be a bit confusing if the user forgets to click on it before clicking on the Paste Pose button.  
> This can easily be extended to copying and pasting animation by running the copy_pose() and paste_pose() functions over all the frames in the scene. It would require that there is just one button for copying/pasting the animation so that the user doesn't have to wait one iteration through all the frames for the tool to save all the poses in the timeline before pasting it. It is also more efficient memory--wise to do so. 
