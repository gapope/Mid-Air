import sys

sys.path.append('/Users/Greg/Leap/lib')

import Leap, thread, time

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

from leapListener import *

import matplotlib.pyplot as plt
import tempfile, requests, json

from PIL import Image

from config import *

url = endpoint + 'vision/v2.0/read/core/asyncBatchAnalyze'
#url = endpoint + 'vision/v2.0/ocr'

securityHeaders = {'Ocp-Apim-Subscription-Key': subscription_key}

def main():
    # Create a sample listener and controller
    listener = LeapListener()
    controller = Leap.Controller()

    waiting = True
    line = ''

    plt.rcParams['figure.figsize'] = [4, 3]

    while 'x' not in line:

        # Keep this process running until Enter is pressed
        print "Press Enter to start/stop, x to quit..."
        try:
            line = sys.stdin.readline()
        except KeyboardInterrupt:
            pass
        finally:
            if waiting:
                listener.reset_vals()
                
                # Turn on listener
                controller.add_listener(listener)
            else:
                # Turn off listener
                controller.remove_listener(listener) 

                #print str(listener.pointList)
                if listener.pointLists != []:

                    plt.clf()
                    plt.axis('off')

                    for pointList in listener.pointLists:
                        plt.plot(pointList[0], pointList[1], 'k', lw=5)

                    temp = tempfile.TemporaryFile('w+b')

                    plt.savefig(temp, format='png', quality=100)

                    temp.seek(0)

                    plotImg = Image.open(temp)
                    plotSize = plotImg.size

                    borderedSize = (8000, 6000)
                    borderedImg = Image.new("RGB", borderedSize, (255, 255, 255))
                    borderedImg.paste(plotImg, ((borderedSize[0] - plotSize[0]) / 2, (borderedSize[1] - plotSize[1]) / 2))

                    borderedImg.show()

                    temp.close()
                    temp = tempfile.TemporaryFile('w+b')

                    borderedImg.save(temp, 'png')

                    temp.seek(0)

                    try:
                        headers = securityHeaders
                        headers.update({'Content-Type': 'application/octet-stream'})

                        response = requests.post(url, headers=headers, data=temp.read())
                        response.raise_for_status()
                    except Exception as e:
                        print str(e)
                        exit()

                    getUrl = response.headers['Operation-Location']

                    
                    try:
                        response = requests.get(getUrl,headers=securityHeaders)
                        response.raise_for_status()
                        print json.dumps(response.json(), indent=4)

                        while response.json()['status'] not in ['Succeeded', 'Failed']:
                            time.sleep(1)

                            response = requests.get(getUrl,headers=securityHeaders)
                            response.raise_for_status()
                            print json.dumps(response.json(), indent=4)

                    except Exception as e:
                        print str(e)
                        exit()

                    #

            waiting = not waiting

if __name__ == "__main__":
    main()