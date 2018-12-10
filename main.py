# example input
# extract.py -i one,two,three -b 2000 (optional) -o (optional)

import argparse
import urllib2
import re
import os
import threading
import time

class Fetch():
    
    RE_IMG_SRC = r'img .*?src="(.*?)"'
    IMAGE_SEARCH = 'https://www.google.com/search?tbm=isch&q=a&ijn=2&start=200&asearch=ichunk&async=_id:rg_s,_pms:s,_fmt:pc'

    def __init__(self, terms, batch, output):
        self.terms = terms 
        self.batchSize = batch if batch != None else 100
        self.outputLocation = output + '/' if output != None else ''

    def run(self):
        for i in self.terms:
            for j in range(int(self.batchSize/100)):
                url = 'https://www.google.com/search?tbm=isch&q='+i+'&ijn='+str(j+1)+'&start='+str(j+1)+'00&asearch=ichunk&async=_id:rg_s,_pms:s,_fmt:pc'
                req = urllib2.Request(url, headers={'User-Agent' : 'Magic Browser'})
                con = urllib2.urlopen(req)
                htmlFile = con.read()
                with open('f.txt', 'w') as f:
                    f.write(htmlFile)
                matches = re.findall(self.RE_IMG_SRC,htmlFile)
                print len(matches)
                string = self.outputLocation + i
                if not os.path.isdir(string):
                    os.makedirs(string)
                for k in range(j*100,j*100+len(matches)):
                    with open(string+'/'+str(k)+'.jpeg', 'wb+') as image:
                        print matches[k-j*100]
                        image.write(urllib2.urlopen(matches[k-(j*100)]).read())
            
    def runThread(self, term, order, output):
        print term, order, output
        print 'Starting batch', order
        url = 'https://www.google.com/search?tbm=isch&q='+term+'&ijn='+str(order)+'&start='+str(order)+'00&asearch=ichunk&async=_id:rg_s,_pms:s,_fmt:pc'
        req = urllib2.Request(url, headers={'User-Agent' : 'Magic Browser'})
        con = urllib2.urlopen(req)
        htmlFile = con.read()
        matches = re.findall(self.RE_IMG_SRC, htmlFile)
        for k in range(order*100, order*100+len(matches)):
            if (k-order*100)%20 == 0:
                print 'Batch', order, 'at', str(k)+'%'
            with open(output+'/'+str(k)+'.jpeg', 'wb+') as image:
                image.write(urllib2.urlopen(matches[k-order*100]).read())
        print 'Finished batch', order

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract images from google based on search terms in batches')
    parser.add_argument('-i','--input', nargs='+', help='Search terms for images you want to find', required=True, type=str)
    parser.add_argument('-b','--batchsize', help='Number of images to fetch for every term (default: 100)', required=False, type=int)
    parser.add_argument('-o', '--output', help='Folder to output to (default: output)', required=False, type=str)
    args = parser.parse_args()
    batchsize = args.batchsize if args.batchsize != None else 100
    inputTerms = args.input
    outputLocation = args.output if args.output != None else ''
    print batchsize, inputTerms, outputLocation
    a = Fetch(inputTerms, batchsize, outputLocation)
    #a.run()
    for j in inputTerms:
        string = outputLocation+j
        if not os.path.isdir(string):
            os.makedirs(string)
        for i in range(batchsize//100):
            print i
            t = threading.Thread(target=a.runThread, args=(j, i, string,))
            t.start()
            time.sleep(0.01)