import sys
import os.path
import csv

sys.path.append(r"..\..")
from agoTools.admin import Admin
try:
    if len(sys.argv) > 1:
        adminUsername = sys.argv[1]
        adminPassword = sys.argv[2]

    else:
        adminUsername = "your_admin_username"
        adminPassword = "your_admin_password"
    ##2)set constrainDays to a number greater than 0 to narrow getUsers results based on the difference between current date-time and user creation date-time. Leave set to 0 in order to use default 10000 days
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

    if constrainDays:
        users=agoAdmin.getUsers(daysToCheck=constrainDays)
    else:
        users= agoAdmin.getUsers()
    print str(len(users)) + " users found."
#group=groups[0]

except Exception,e:
    print str(e)