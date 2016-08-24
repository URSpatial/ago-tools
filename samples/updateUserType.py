import sys
sys.path.append(r"..\..\ago-tools")
from agoTools.admin import Admin
try:
    ##1) Enter ago org admin credentials as comandline parameter or enter them below######
    if len(sys.argv) > 1:
        adminUsername = sys.argv[1]
        adminPassword = sys.argv[2]

    else:
        adminUsername = "your_admin_username"
        adminPassword = "your_admin_password"

    ##2) set userType to 'both' to enable Esri Access or 'arcgisonly' to disable
    userType = "both"


    ##2) Set constrainDays to a number greater than 0 to narrow getUsers results based on the difference between
    ##   current date-time and user creation date-time in days. Leave set to 0 in order to use default 10000 days
    constrainDays = 0

    ##3) Update & overwrite licenses for everyone or just assign to users with no current entitlements
    overwriteAll = False

    ##4) Modify licensing options in userEntitlements list if necessary.######
    ##PRO (pick one):
    ##  Basic = desktopBasicN
    ##  Standard = destkopStdN
    ##  Advanced = desktopAdvN
    ##Extensions (add all that apply):
    ##   Spatial Analyst = SpatialAnalystN
    ##   3D Analyst = 3DAnalystN
    ##   Network Analyst = 3DnetworkAnalystN
    ##   Geostatistical Analyst = geostatAnalystN
    ##   Data Reviewer: dataReviewerN
    ##   Workflow Manager: workflowMgrN
    ##   Data Interoperability: dataInteropN



    ####################################
    agoAdmin = Admin(adminUsername,password=adminPassword)
    ##users = agoAdmin.getUsers()
    if constrainDays:
        users=agoAdmin.getUsers(daysToCheck=constrainDays)
    else:
        users= agoAdmin.getUsers()


    print str(len(users)) + " users found."
## Set splitString to the character or string that is used to find defualt-formated fullName. splitString will be used as the point at which the username string is split on parsing.
    for user in users:


        userName=user["username"]


        print userName

        response=agoAdmin.setUserType(userName, userType)
except Exception as e:
    print e
