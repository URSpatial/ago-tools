import sys
sys.path.append(r"..")
from agoTools.admin import Admin
#######Enter ago org admin credentials below######
adminUsername = "org admin user"
adminPassword = "the admin user password"
##################################################

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


response= agoAdmin.setEntitlements(newUsers,["3DAnalystN","dataReviewerN","desktopAdvN","geostatAnalystN","networkAnalystN","spatialAnalystN","workflowMgrN"])
print response
