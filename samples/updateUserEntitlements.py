import sys
sys.path.append(r"..")
from agoTools.admin import Admin
#######Enter ago org admin credentials below######
adminUsername = "org admin user"
adminPassword = "the admin user password"
######Current licensing options to use for userEntitlements######
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
userEntitlements = ["desktopAdvN","3DAnalystN","dataReviewerN","geostatAnalystN","networkAnalystN","spatialAnalystN","workflowMgrN","dataInteropN"]


agoAdmin = Admin(adminUsername,password=adminPassword)

users = agoAdmin.getUsers()
ents = agoAdmin.getEntitlements()
newUsers = []
for user in users:

    found = False
    for ent in ents:
        if user["username"] == ent["username"]:
            found = True
            break
    if found == False:
        newUsers.append(user)
       ## print user["username"]


response= agoAdmin.setEntitlements(newUsers,userEntitlements)
print response
