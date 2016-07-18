import sys
sys.path.append(r"..\..")
from agoTools.admin import Admin
if sys.argv[1]=='css':
    agoAdmin = Admin("user_name_here",password="password")
    groups=['group_ID_1', 'group_ID_2', 'group_ID_3', 'group_ID_4']
if sys.argv[1]=='sb':
    agoAdmin = Admin("user_name_here",password="password")
    groups = ['group_ID_1', 'group_ID_2']   # Enter <groupIDs> of groups to which you want to add new users
# User parameters:
orgUsers= agoAdmin.getUsers()

#group=groups[0]


for group in groups:
    groupUsers= agoAdmin.getUsersInGroup(group)
    groupUsers= groupUsers["users"]

    addUsers=[]
    print len(addUsers)
    for user in orgUsers:
        if not user["username"] in groupUsers:
            print user["username"]
            addUsers.append(user["username"])

    agoAdmin.addUsersToGroups(addUsers, [group])
