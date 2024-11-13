Subsets
-------
Author: kari.kujansuu@gmail.com<br>
November 2024<br>

This is a SuperTool script, see https://www.gramps-project.org/wiki/index.php/Addon:Isotammi_addons#SuperTool and https://github.com/Taapeli/isotammi-addons/tree/master/source/SuperTool.

The script finds all the non-connected subsets (or "partitions") in the database. The script will display the number of people in each subset and a sample person from each set. The code is based on the “Not Related” tool (https://gramps-project.org/wiki/index.php/Gramps_5.2_Wiki_Manual_-_Tools#Not_Related).

The connectedness is defined by relationships: a person's parents, children and spouses belong to the same subsets. 

For example, for the sample database the script finds 105 separate partitions. The largest one has 1844 individuals:

![subsets](subsets.png)

The script chooses the sample person as the person with the alphabetically lowest ID in the subset.

Double-clicking on a row will open the person editor for the sample person. 

See e.g. the discussion here: https://gramps.discourse.group/t/list-of-tree-snippets/6425/7


