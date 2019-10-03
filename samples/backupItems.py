import urllib
import urllib2
import httplib,os
import time
import json
import contextlib
import ast
#import arcpy
import datetime
import time
orgURL ="https://univredlands.maps.arcgis.com"
username = "CenterSpatialStudiesUoR"
password = "Redlands!1"
items = ['0ac33896b5bb4b8c92b623f11660a0c9',"59f5e9d8ea4641d69893e44495a3ac48"]
def backupItems(items):
    token = get_token(orgURL,username,password)



    for itemID in items:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
        item = getItemInfo(itemID,token)
        print "processing",item["name"] + "..."
        exportItem(itemID,item["name"] + " Backup " + timestamp,"Backup","Backups",token)


def exportItem(itemID,title,tags, folder,token,eFormat="File Geodatabase"):
    folderID = getFolderID(folder,token)
    requestURL = orgURL + "/sharing/rest/content/users/" + username + "/export"
    params ={"token":token,
                "f":"json",
                "itemId":itemID,
                "title":title,
                "exportFormat":eFormat
                }
    request = urllib2.Request(requestURL, urllib.urlencode(params))
    response = urllib2.urlopen(request)
    result = response.read()
    exportResponse = json.loads(result)
    exportResponse = decode_dict(exportResponse)
    exportID = exportResponse["exportItemId"]
    jobID = exportResponse["jobId"]
    ##Wait until done exporting

    status ="processing"
    while status == "processing":
        time.sleep(5)
        requestURL = orgURL + "/sharing/rest/content/users/" + username + "/items/" + exportID + "/status"
        params ={"token":token,
                "f":"json",
                "jobId":jobID,
                "jobType":"export"
                }
        request = urllib2.Request(requestURL, urllib.urlencode(params))
        response = urllib2.urlopen(request)
        result = response.read()
        statusResponse = json.loads(result)
        statusResponse = decode_dict(statusResponse)
        status = statusResponse["status"]
    if status == "completed":
        requestURL = orgURL + "/sharing/rest/content/users/" + username + "/items/" + exportID + "/update"
        params ={"token":token,
                "f":"json",
                "tags":tags
                }
        request = urllib2.Request(requestURL, urllib.urlencode(params))
        response = urllib2.urlopen(request)
        result = response.read()
        updateResponse = json.loads(result)
        updateResponse = decode_dict(updateResponse)
        #print updateResponse
        requestURL = orgURL + "/sharing/rest/content/users/" + username + "/items/" + exportID + "/move"
        params ={"token":token,
                "f":"json",
                "folder":folderID
                }
        request = urllib2.Request(requestURL, urllib.urlencode(params))
        response = urllib2.urlopen(request)
        result = response.read()
        objResponse = json.loads(result)
        objResponse = decode_dict(objResponse)
        return objResponse
    else:
        print "Error exporting " + itemID
        return None

def getFolderID(folderName,token):
    requestURL = orgURL + "/sharing/rest/content/users/" + username
    params = {"token":token,
                "f":"json"
                }
    request = urllib2.Request(requestURL, urllib.urlencode(params))
    response = urllib2.urlopen(request)
    result = response.read()
    objResponse = json.loads(result)
    objResponse = decode_dict(objResponse)
    folders = objResponse["folders"]
    for folder in folders:
        if folder["title"] == folderName:
            return folder["id"]
    return None

def getItemInfo(itemID,token):
    itemURL = "https://univredlands.maps.arcgis.com/sharing/rest/content/items/" + itemID
    params = {"token":token,
                "f":"json"
                }
    request = urllib2.Request(itemURL, urllib.urlencode(params))
    response = urllib2.urlopen(request)
    result = response.read()
    itemInfo = json.loads(result)
    itemInfo = decode_dict(itemInfo)
    return itemInfo
def get_token(portal_url, username, password):
    """ Returns an authentication token for use in ArcGIS Online."""

    # Set the username and password parameters before
    #  getting the token.
    #
    params = {"username": username,
              "password": password,
              "referer": "http://www.arcgis.com",
              "f": "json"}

    token_url = "{}/sharing/generateToken".format(portal_url)
    request = urllib2.Request(token_url, urllib.urlencode(params))
    token_response = submit_request(request)
    if "token" in token_response:
        #print("Getting token...")
        token = token_response.get("token")
        return token
    else:
        # Request for token must be made through HTTPS.
        #
        if "error" in token_response:
            error_mess = token_response.get("error", {}).get("message")
            if "This request needs to be made over https." in error_mess:
                token_url = token_url.replace("http://", "https://")
                token = get_token(token_url, username, password)
                return token
            else:
                raise Exception("Portal error: {} ".format(error_mess))
def submit_request(request):
    """ Returns the response from an HTTP request in json format."""
    with contextlib.closing(urllib2.urlopen(request)) as response:
        job_info = json.load(response)
        return job_info
def decode_dict(dct):
    newdict = {}
    for k, v in dct.iteritems():
        k = safeValue(k)
        v = safeValue(v)
        newdict[k] = v
    return newdict

def safeValue( inVal):
    outVal = inVal
    if isinstance(inVal, unicode):
        outVal = inVal.encode('utf-8')
    elif isinstance(inVal, list):
        outVal = decode_list(inVal)
    return outVal

def decode_list(lst):
    newList = []
    for i in lst:
        i = safeValue(i)
        newList.append(i)
    return newList
backupItems(items)