import sys
sys.path.append(r"..\..\ago-tools")
from agoTools.admin import Admin
try:
    ##1) Enter ago org admin credentials as comandline parameter or enter them below in after the else######
    if len(sys.argv) > 1:
        adminUsername = sys.argv[1]
        adminPassword = sys.argv[2]
    else:
        adminUsername = "your_admin_username"
        adminPassword = "your_admin_password"

    ##2) set userType to 'both' to enable Esri Access or 'arcgisonly' to disable
    userType = "both"
   -##3) Set constrainDays to a number greater than 0 to filter users created in the last n days. 
    ##    Leave set to 0 in to use default 10000 days
 -  constrainDays = 0
    ####################################
    agoAdmin = Admin(adminUsername,password=adminPassword)
    ##users = agoAdmin.getUsers()
    if constrainDays:
        users=agoAdmin.getUsers(daysToCheck=constrainDays)
    else:
        users= agoAdmin.getUsers()

    print str(len(users)) + " users found."
    for user in users:
        userName=user["username"]
        print userName
        response=agoAdmin.setUserType(userName, userType)
except Exception as e:
    print e
