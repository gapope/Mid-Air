import sys

from config import *

#Leap library path (path to lib folder of SDK)
sys.path.append(LeapPath)

import Leap, thread, time
from leapListener import *

#Create a listener and controller that will be shared by these utility functions
listener = LeapListener()
controller = Leap.Controller()

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import tempfile, requests, json

from PIL import Image

import pyperclip

#Azure connection config
url = endpoint + 'vision/v2.0/read/core/asyncBatchAnalyze'
securityHeaders = {'Ocp-Apim-Subscription-Key': subscription_key}
    
#Prints to console as well as updating message label in GUI
def output(window, mesg):
    print mesg
    window.setMessageLabel(mesg)

#Start recording data
def startLeapMotion(window):
    #Reset anything after last recording
    listener.reset_vals()

    output(window, "Recording...")

    # Turn on listener
    return controller.add_listener(listener)

#Stop the data recording, generate and analyze the image from the data
def stopLeapMotion(window):
     # Turn off listener
    controller.remove_listener(listener) 

    #Was something written by the user?
    if listener.pointLists != []:
        output(window, "Processing data...")

        #Plot data points
        imgFile = genPlot(listener.pointLists)

        #Print writing to screen for user
        window.setImageLabel(imgFile)

        #Add borders so image is usable by Azure
        submitFile = addBorders(imgFile)

        output(window, "Extracting text...")
        #Submit to Azure handwriting recognition
        text = extractText(submitFile)

        #If text was found, copy it to the clipboard
        if text != '':
            try:
                pyperclip.copy(text)

                output(window, "Copied \"" +text+ "\" to clipboard")
            except Exception as e:
                output(window, "Failed to copy to clipboard: " +str(e))
        else:
            output(window, "No text found")
    #User never triggered Leap Motion
    else:
        output("Press start to begin")

#Make plots of characters from XY data
def genPlot(pointLists):
    #Clean plot figure and remove the axes
    plt.clf()
    plt.axis('off')

    #Add data for each charater written
    for pointList in pointLists:
        plt.plot(pointList[0], pointList[1], 'k', lw=5)

    #Save image
    imgFile = 'images/userInput.png'

    plt.savefig(imgFile, format='png', quality=100)

    return imgFile

#Add large white borders to the image, effectively shrinking the plot
#Azure doesn't like to read large handwriting
def addBorders(imgFile):
    
    plotImg = Image.open(imgFile)
    plotSize = plotImg.size

    #Create a much larger white image with the same aspect ratio as the handwriting plot
    borderedSize = (6800, 5100)
    borderedImg = Image.new("RGB", borderedSize, (255, 255, 255))
    #Insert handwriting plot in the center
    borderedImg.paste(plotImg, ((borderedSize[0] - plotSize[0]) / 2, (borderedSize[1] - plotSize[1]) / 2))

    plotImg.close()

    #Save image
    submitFile = 'images/toSubmit.png'

    borderedImg.save(submitFile, 'png')

    return submitFile

#Submit an image file to azure for handwriting analysis
def extractText(submitFile):
    #Submit image
    try:
        headers = securityHeaders
        headers.update({'Content-Type': 'application/octet-stream'})

        response = requests.post(url, headers=headers, data=open(submitFile, 'rb').read())
        response.raise_for_status()
    except Exception as e:
        return "Failed to submit image: " +str(e)

    #Results available here
    getUrl = response.headers['Operation-Location']

    #Fetch results
    try:
        response = requests.get(getUrl,headers=securityHeaders)
        response.raise_for_status()
        print json.dumps(response.json(), indent=4)

        #Wait and retry for results until success (or failure)
        while response.json()['status'] not in ['Succeeded']:
            time.sleep(1)

            response = requests.get(getUrl,headers=securityHeaders)
            response.raise_for_status()

            data = response.json()

            #Total analysis failure
            assert data['status'] != 'Failed', "Extraction failed"
            
            print json.dumps(data, indent=4)

            text = ''

            #Grab exracted text
            for result in data['recognitionResults']:
                for line in result['lines']:
                    text += line['text']

            return text

    except Exception as e:
        return "Failed to fetch extraction result: " +str(e)