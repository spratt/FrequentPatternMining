#!/usr/bin/env python2.6

class Dataset(object):
    def __init__(self):
        self.rows = []

    def __len__(self):
        return len(self.rows)

    def readFromFile(self,f):
        for line in f:
            canonical = line.strip().lower()
            self.rows.append(canonical.split(" "))

if __name__ == '__main__':

    import sys

    if len(sys.argv) < 2:
        print "usage: {0} [file]".format(sys.argv[0])
        sys.exit(-1)

    filename = sys.argv[1]
    ds = Dataset()
    with open(filename,'rU') as f:
        ds.readFromFile(f)
        
    print "Read {0} lines in {1}".format(len(ds),filename)
