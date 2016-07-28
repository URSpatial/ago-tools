import sys
sys.path.append(r"C:\Users\matthew_flewelling\Documents\GitHub")
from agoTools.admin import Admin
if sys.argv[1]=='css':
    agoAdmin = Admin("CenterSpatialStudiesUoR",password="Redlands!1")
    searchString='@'
if sys.argv[1]=='sb':
    agoAdmin = Admin("spatialstudies_business",password="bulld0gsGIS")
    searchString='redlands.edu'
##search = utilities.searchPortal(myAgo.user.portalUrl, query='owner: matthew_flewelling', token=myAgo.user.token)
users= agoAdmin.getUsers()

for user in users:
    if searchString in user["fullName"]:


        userName=user["username"]
        nameSplit= userName.split("@")
        nameSplit=nameSplit[0]
        fullNameList=nameSplit.split("_", 1)
        fullNameList[1].replace("_", "-")
        fullNameString=""
        i=0
        for name in fullNameList:
            if i==0:
                fullNameString+=name.title()
                i+=1

            else:
                fullNameString+= " " + name.title()
        print userName
        print user["fullName"]
        print fullNameString
        agoAdmin.setUserFullName(userName, fullNameString)

