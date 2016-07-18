import sys
sys.path.append(r"..")
from agoTools.admin import Admin
if sys.argv[1]=='css':
    agoAdmin = Admin("user_name_here",password="password")
if sys.argv[1]=='sb':
    agoAdmin = Admin("user_name_here",password="password")
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