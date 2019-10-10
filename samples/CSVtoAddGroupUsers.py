import sys
import os.path
import csv
#print "path",os.path.abspath('..\\..')
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(sys.argv[0]))))
from agoTools.admin import Admin
##print sys.argv[0]
if len(sys.argv) < 2:
    agoAdmin = Admin("CenterSpatialStudiesUoR","https://univredlands.maps.arcgis.com",password="Redlands!1")
    folder= r'\\geosrv\tools\agoGroupAdmin\CAS'
    tag= u"_univredlands"
elif sys.argv[1]=='css':
    print "logging in..."
    agoAdmin = Admin("CenterSpatialStudiesUoR",portal="https://univredlands.maps.arcgis.com",password="Redlands!1")
    folder= r'\\geosrv\tools\agoGroupAdmin\CAS'
    tag= u"_univredlands"
elif sys.argv[1]=='sb':
    agoAdmin = Admin("spatialstudies_business",password="bulld0gsGIS")
    folder= r'\\geosrv\tools\agoGroupAdmin\SOB'
    tag= u"_redlandsbusiness"

# User parameters:
print "getting users..."
orgUsers= agoAdmin.getUsers()
orgUserNames = []
for orgUser in orgUsers:
    orgUserNames.append(orgUser["username"])

#group=groups[0]

for filename in os.listdir(folder):
    isFile = os.path.isfile(folder+ "\\" + filename)
    if isFile == True:
        users=[]
        groupName = filename.split('.')[0]
        fileType = filename.split('.')[1]
        if fileType != "csv":
            print fileType+" not csv"
            continue
        print "processing group",groupName
        try:
            group = agoAdmin.findGroup(groupName)
            if group == None:
                print "**Can't find",groupName +" in AGO**"
                continue
            groupid= group['id']

##            print groupName
            groupMembers = agoAdmin.getUsersInGroup(group['id'])
            groupUsers = groupMembers['users']
            i =0
            while i < len(groupUsers):
                groupUsers[i] = groupUsers[i].lower()
                i+=1
            filePath= folder + "\\" + filename
            with open(filePath, "rU") as csvfile:
                reader= csv.reader(csvfile, delimiter = ",", quotechar = "|")
                for row in reader:
                    userEmail = row[0]
                    userEmail=userEmail.replace("-", "_")
                    userEmail = userEmail.lower().strip()
##                    #print userEmail
                    if "," in userEmail:
                        continue
                    if "@" in userEmail:
                        mailDomain= userEmail.split('@')
                        mailDomain= str(mailDomain[1])
                        #print mailDomain
                        if mailDomain.lower() == 'redlands.edu':

                            #print tag
                            userName= userEmail + tag
                            userName = userName.lower().strip()
                            #print userName
                            if userName not in groupUsers:
                                if userName not in orgUserNames:
                                    print "\t-" + userName + " is not a member of the organization"
                                else:
                                    print "\t-adding " + userName
                                    users.append(userName)

                        else:
                            #print"ding"
                            users.append(userEmail)

                    else:
                        print userEmail
                        #print "dong"
                        users.append(userEmail)
            #print users[0]
            if len(users) == 0:
                print "\t-no new users"
            else:
                agoAdmin.addUsersToGroups(users, [groupid])
        except Exception as e:
            print "**Error with",groupName +"**"
            print "\tError on line {}: ".format(sys.exc_info()[-1].tb_lineno) + str(e) +" \r\n "+ groupid

##        groupUsers= agoAdmin.getUsersInGroup(groupName)
##        groupUsers= groupUsers["users"]
##        print
##        addUsers=[]
##        print len(addUsers)
##        for user in orgUsers:
##            if not user["username"] in groupUsers:
##                print user["username"]
##                addUsers.append(user["username"])
##
##        agoAdmin.addUsersToGroups(addUsers, [groupName])
