import sys
import os.path
import csv
sys.path.append(r"..\..")
from agoTools.admin import Admin
try:
    ##1) Enter ago org admin credentials as comandline parameter or enter them below in after the else######
    if len(sys.argv) > 1:
        adminUsername = sys.argv[1]
        adminPassword = sys.argv[2]
        folder= sys.argv[3]
        tag= sys.argv[4]
        emailDomain= sys.argv[5]
    else:
        adminUsername = "your_admin_username"
        adminPassword = "your_admin_password"
        folder= r'agoGroupAdminCSVs\*AddFolderforCSVs*'
        tag= u"your_org_tag_here"
        emailDomain= "yourDomain.com"


    agoAdmin = Admin(adminUsername,password=adminPassword)


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

                        if "@" in userEmail:
                            userMailDomain= userEmail.split('@')
                            userMailDomain= str(userMailDomain[1])

                            if userMailDomain.lower() == emailDomain.lower():

                                userName= userEmail + tag

                                users.append(userName)
                            else:

                                users.append(userEmail)

                        else:


                            users.append(userEmail)
                #print users[0]
                agoAdmin.addUsersToGroups(users, [groupid])
            except Exception as e:
                print "\r\nRuh roh, there was an issue on line {}: ".format(sys.exc_info()[-1].tb_lineno) + str(e) +" \r\n"


except Exception as e:
    print e