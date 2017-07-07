import sys
import os
sys.path.append(r"..")
from agoTools.admin import Admin
##try:
    ##1) Enter ago org admin credentials as comandline parameter or enter them below######
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
##4) Define which products to grant entitlements for.######

arcGISPro=True
geoPlanner= False
appStudio=False
communityAnalyst=True
businessAnalyst=True

##5) If setting entitlements for a specific group, set the third comand line parameter to the name of the AGO group OR set userGroup equal to the title of the AGO group as string
try:
    userGroup = sys.argv[3]
except:
    userGroup=None

####################################
agoAdmin = Admin(adminUsername,password=adminPassword)

products = []
if arcGISPro:
    products.append("pro")
if geoPlanner:
    products.append("geo")
if appStudio:
    products.append("app")
if communityAnalyst:
    products.append("cao")
if businessAnalyst:
    products.append("bao")

if constrainDays:
    users=agoAdmin.getUsers(daysToCheck=constrainDays, groupName=userGroup)
else:
    users= agoAdmin.getUsers(groupName=userGroup)

#print str(len(users)) + " users found."

productsReturn = agoAdmin.getEntitlements(products)
#print productsReturn

AddUsers = {}
print "setting entitlements for " + str(products)
for product in products:
    newUsers = []
    print product
    print product + " new users:"

    for user in users:

        found = False
        for productUser in productsReturn[product]:
            if user["username"] == productUser["username"]:
                found = True
                break
        if found == False:
            newUsers.append(str(user["username"]))
           # print user["username"]
    AddUsers[product]=newUsers
    print newUsers


response= agoAdmin.setEntitlements(AddUsers)
print response

##except Exception,e:
##    print str(e)
##    exc_type, exc_obj, exc_tb = sys.exc_info()
##    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
##    print(exc_type, fname, exc_tb.tb_lineno)