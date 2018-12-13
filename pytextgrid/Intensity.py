from get_named_value import *

class Intensity:
    def __init__(self, fname):
        f = open(fname)
        filetype = getstringval(f.readline(), "File type")
        objectclass = getstringval(f.readline(), "Object class")

        assert('ooTextFile' == filetype)
        assert(objectclass == 'Intensity 2')
        assert(f.readline() == "\n")
        self._values = []

        c = f.read(1)
        f.seek(-1,1)
        if c == 'x':
            self._init_from_textfile(f)
        else:
            self._init_from_short_textfile(f)

    def _init_from_textfile(self, f):
        self._xmin = getfloatval(f.readline(), 'xmin')
        self._xmax = getfloatval(f.readline(), 'xmax')
        nbvalues = getintval(f.readline(), 'nx')
        self._dx = getfloatval(f.readline(), 'dx') # hop
        self._windowsize = getfloatval(f.readline(), 'x1')
        for e in ['ymin', 'ymax', 'ny', 'dy', 'y1']:
            assert(getintval(f.readline(), e) == 1)
        assert(re.match('\s*z \[\] \[\]:', f.readline()))
        assert(re.match('\s*z \[1\]:', f.readline()))
        
        for i in xrange(1, nbvalues+1):
            # if (i % 1000) == 0:
            #     print i, '/', nbvalues
            self._values.append(getfloatval(f.readline(), 'z \[1\] \[%d\]' % i))

        #print self._values

    def _init_from_short_textfile(self, f):
        self._xmin = float(f.readline())
        self._xmax = float(f.readline())
        nbvalues = int(f.readline())
        self._dx = float(f.readline()) # hop
        self._windowsize = float(f.readline())
        for e in ['ymin', 'ymax', 'ny', 'dy', 'y1']:
            assert(int(f.readline()) == 1)
        for i in xrange(1, nbvalues+1):
            # if (i % 1000) == 0:
            #     print i, '/', nbvalues
            self._values.append(float(f.readline()))
        # print self._values



    def get_vals(self, xmin, xmax):
        #print self._values
        imin = int(round((xmin - self._windowsize) / self._dx))
        imax = 1+int(round((xmax - self._windowsize) / self._dx))
        #print imin, imax
        return self._values[imin:imax]

if __name__ == '__main__':
    test = Intensity('/home/david/my_hg_repos/corpus_gvlex/prosogram_output_2011_11_16/021_LES_FEES_A1/021_LES_FEES_A1.Intensity')
