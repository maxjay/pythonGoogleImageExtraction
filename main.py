from argparse import ArgumentParser
from urllib2 import Request, urlopen
from re import findall
from threading import Thread
from time import sleep
from os import path, makedirs

class Fetch():
    
    RE_IMG_SRC = r'img .*?src="(.*?)"'
    IMAGE_SEARCH = 'https://www.google.com/search?tbm=isch&q={0}&ijn={1}&start={1}00&asearch=ichunk&async=_id:rg_s,_pms:s,_fmt:pc'

    def __init__(self, terms, batch, output):
        self.terms = terms 
        self.batchSize = batch if batch != None else 100
        self.outputLocation = output if output != None else ''

    def runMainThread(self):
        for j in self.terms:
            Thread(target=self.runParentThread, args=(j,)).start()
            sleep(0.01)
    
    def runParentThread(self, term):
        term = term.replace('_', ' ')
        if self.outputLocation != '':
            string = self.outputLocation + '/' + term
        else:
            string = self.outputLocation+term
        if not path.isdir(string):
            makedirs(string)
        for i in range(self.batchSize//100):
            Thread(target=self.runChildThread, args=(term, i, string,)).start()
            sleep(0.01)

    def runChildThread(self, term, order, output):
        print 'Starting batch', order
        url = self.IMAGE_SEARCH.format(term, order)
        req = Request(url, headers={'User-Agent' : 'Dab on them Haters Browser'})
        htmlFile = urlopen(req).read()
        matches = findall(self.RE_IMG_SRC, htmlFile)
        for k in range(order*100, order*100+len(matches)):
            if k%20 == 0:
                print 'Batch', order, 'at', str(k-order*100)+'%'
            with open(output+'/'+str(k)+'.jpeg', 'wb+') as image:
                image.write(urlopen(matches[k-order*100]).read())
        print 'Finished batch', order


if __name__ == '__main__':
    parser = ArgumentParser(description='Extract images from google based on search terms in batches')
    parser.add_argument('-i','--input', nargs='+', help='Search terms for images you want to find', required=True, type=str)
    parser.add_argument('-b','--batchsize', help='Number of images to fetch for every term (default: 100)', required=False, type=int)
    parser.add_argument('-o', '--output', help='Folder to output to (default: output)', required=False, type=str)
    args = parser.parse_args()
    a = Fetch(args.input, args.batchsize, args.output)
    a.runMainThread()