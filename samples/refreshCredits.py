import sys,os,smtplib
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(sys.argv[0]))))
from email.mime.text import MIMEText
from agoTools.admin import Admin
sendEmail = True
emailTemplate = r"emailtemplates\creditoverage.txt"
creditAllocation = 500
try:
    ##1) Enter ago org admin credentials as comandline parameter or enter them below######
    if len(sys.argv) > 1:
        adminUsername = sys.argv[1]
        adminPassword = sys.argv[2]

    else:
        adminUsername = "your_admin_username"
        adminPassword = "your_admin_password"
    if len(sys.argv) == 4:
        emailTemplate = sys.argv[3]
    ##2) set userType to 'both' to enable Esri Access or 'arcgisonly' to disable
    #userType = "both"


    ##2) Set constrainDays to a number greater than 0 to narrow getUsers results based on the difference between
    ##   current date-time and user creation date-time in days. Leave set to 0 in order to use default 10000 days
    constrainDays = 0


    if sendEmail:
        server = smtplib.SMTP("s-red-mgate-01.redlands.edu",25)
        fp = open(emailTemplate,"rb")
        template = fp.read()

        fp.close()

    ####################################
    print "Logging in as ",adminUsername + "..."
    agoAdmin = Admin(adminUsername,password=adminPassword)
    ##users = agoAdmin.getUsers()
    if constrainDays:
        users=agoAdmin.getUsers(daysToCheck=constrainDays)
    else:
        users= agoAdmin.getUsers()


    # print str(len(users)) + " users found."
## Set splitString to the character or string that is used to find defualt-formated fullName. splitString will be used as the point at which the username string is split on parsing.
    roles = agoAdmin.getRoles()
    roleDict ={}
    for role in roles:
        roleDict[role["id"]] = role["name"]
    resetUserCount = 0
    print "searching",len(users),"users..."
    for user in users:
        if (roleDict.get(user["role"],"") in ["Extended User","Extended Use Accounts"]):
            continue
        if user["disabled"] == True:
            continue
        if "availableCredits" not in user:
            print "Credits were set to unlimited for " + user["username"] + ". Setting to",creditAllocation
            agoAdmin.setCredits(user["username"],creditAllocation)
        else:
            if user["availableCredits"] <=1:
                print "resetting credits for",user["username"]
                resetUserCount+=1
                agoAdmin.setCredits(user["username"],creditAllocation)
                if sendEmail:
                    print "\t-sending email"
                    to = user["email"]
                    #to ="nathan_strout@redlands.edu"
                    msg = MIMEText(template.format(user["fullName"],creditAllocation))
                    msg["Subject"] = "We've refreshed your ArcGIS Online credits"
                    msg["From"] = "spatialstudies@redlands.edu"
                    msg["Cc"] ="spatialstudies@redlands.edu"
                    msg["To"] = to
                    server.sendmail("spatialstudies@redlands.edu",[to,"spatialstudies@redlands.edu"],msg.as_string())
    if resetUserCount == 0:
        print "No credit refreshes needed"

except Exception as e:
    print "error:", e
print "done"