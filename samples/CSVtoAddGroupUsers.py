import sys
import os.path
import csv

sys.path.append(r"..\..")
from agoTools.admin import Admin
print sys.argv[0]
if sys.argv[1]=='css':
    print 'bing'
    agoAdmin = Admin( "user_name_here",password="password")
    folder= r'agoGroupAdminCSVs\*AddFolderforCSVs*'
    tag= u"_univredlands"
if sys.argv[1]=='sb':
    agoAdmin = Admin("user_name_here",password="password")
    folder= r'agoGroupAdminCSVs\*AddFolderforCSVs*'
    tag= u"_redlandsbusiness"

# User parameters:
orgUsers= agoAdmin.getUsers()

#group=groups[0]

for filename in os.listdir(folder):
    isFile = os.path.isfile(folder+ "\\" + filename)
    if isFile == True:
        users=[]
        groupName = filename.split('.')[0]
        try:
            groupid= agoAdmin.findGroup(groupName)['id']
            print groupName
            filePath= folder + "\\" + filename
            with open(filePath, "rU") as csvfile:
                reader= csv.reader(csvfile, delimiter = " ", quotechar = "|")
                for row in reader:
                    userEmail = row[0]
                    userEmail=userEmail.replace("-", "_")
                    print userEmail
                    if "," in userEmail:
                        print "Whoa"
                    if "@" in userEmail:
                        mailDomain= userEmail.split('@')
                        mailDomain= str(mailDomain[1])
                        #print mailDomain
                        if mailDomain.lower() == 'redlands.edu':

                            #print tag
                            userName= userEmail + tag
                            #print userName
                            users.append(userName)
                        else:
                            print"ding"
                            users.append(userEmail)

                    else:
                        print userEmail
                        print "dong"
                        users.append(userEmail)
            #print users[0]
            agoAdmin.addUsersToGroups(users, [groupid])
        except Exception as e:
            print "\r\nRuh roh, there was an issue on line {}: ".format(sys.exc_info()[-1].tb_lineno) + str(e) +" \r\n"

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
