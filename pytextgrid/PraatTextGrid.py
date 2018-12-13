###!/usr/bin/python3
#### -*- coding: utf-8 -*-

#TODO
# while writing text, we should duplicated the double quotes
# while reading text, we should take into account
# the fact that 2 consecutive double quotes means there is only
# one double quote => the regexp used in getstringval may not be enough

# import re
#import exceptions
import codecs
from .get_named_value import *

class Point:
    def __init__(self, fd=None, time=None, mark=''):
        self._mark = mark
        self._time = time
        if fd:
            assert(re.match(r'\s*points\s*\[\d+\]:\s*', fd.readline()))
            self._time = getfloatval(fd.readline(), 'time')
            self._mark = getstringval(fd.readline(), 'mark')

    def save(self, fd):
        fd.write('\t\t\t time = %f\n' % self._time)
        fd.write('\t\t\t mark = "%s"\n' % self._mark)

    def copy(self):
        return Point(mark=self._mark, time=self._time)


class RealPoint:
    def __init__(self, fd=None, time=None, value=None):
        self._value = value
        self._time = time
        if fd:
            assert(re.match(r'\s*points\s*\[\d+\]:\s*', fd.readline()))
            self._time = getfloatval(fd.readline(), 'time')
            self._value = getfloatval(fd.readline(), 'value')

    def save(self, fd):
        fd.write('\t\t\t time = %f\n' % self._time)
        fd.write('\t\t\t value = "%f"\n' % self._value)

    def __str__(self):
        return '<RealPoint time=%.2f value=%.2f/>' % (self._time, self._value)
    
    def copy(self):
        return RealPoint(time=self._time, value=self._value)

class Interval:
    def __init__(self, xmin=None,xmax=None,text=''):
        self._xmin = xmin
        self._xmax = xmax
        self._text = text
    
    @classmethod
    def loadfromfd(cls, fd):
        fdline = fd.readline()
        assert(re.match(r'\s*intervals\s*\[\d+\]:?\s*', fdline))
        xmin = getfloatval(fd.readline(), "xmin")
        xmax = getfloatval(fd.readline(), "xmax")
        text = getstringval(fd.readline(), "text")
        return Interval(xmin, xmax, text)

    def length(self):
        return self._xmax - self._xmin

    def save(self, fd):
        fd.write('\t\t\t xmin = %f\n' % self._xmin)
        fd.write('\t\t\t xmax = %f\n' % self._xmax)
        fd.write('\t\t\t text = "%s"\n' % self._text)

    def __le__(self, other):
        return self._xmin <=  other._xmin

    def __lt__(self, other):
        return self._xmin <  other._xmin

    def __str__(self):
        return '<intv xmin=%.3f xmax=%.3f text=%s>' % (self._xmin, self._xmax, self._text)

    def copy(self):
        ret = Interval(self._xmin, self._xmax, self._text)
        if hasattr(self, 'data'):
            ret.data = self.data[:]
        return ret


class Tier:
    # FIXME: fields intervals/nbintervals should be renamed in elts/nbetls:
    # since a tier could contain either intervals, either points
    def __init__(self, xmin=0.,xmax=0.,tierclass='IntervalTier', name=None):
        self._intervals = []
        self._xmin = xmin
        self._xmax = xmax
        self._name = name
        self._class = tierclass
        if tierclass not in ['IntervalTier', 'TextTier']:
            raise NotImplementedError('tierclass %s not managed' % tierclass)

    @classmethod
    def loadfromfd(cls, fd):
        """
        load from open file descriptor
        """
        assert(re.match(r'\s*item\s*\[\d+\]:\s*', fd.readline()))
        tierclass = getstringval(fd.readline(), "class")
        name = getstringval(fd.readline(), "name")
        xmin = getfloatval(fd.readline(), "xmin")
        xmax = getfloatval(fd.readline(), "xmax")
        ret = Tier(xmin=xmin, xmax=xmax, tierclass=tierclass, name=name)

        if tierclass == 'IntervalTier':
            nbintervals = getintval(fd.readline(), "intervals: size")
            for i in range(nbintervals):
                ret._intervals.append(Interval.loadfromfd(fd))
        elif tierclass == 'TextTier':
            nbintervals = getintval(fd.readline(), 'points: size')
            for i in range(nbintervals):
                ret._intervals.append(Point(fd=fd))
        return ret
    
    @classmethod
    def initfromlist(cls, l, xmin=0., xmax=0., tierclass='IntervalTier', name=''):
        l.sort()
        tier = cls(xmin=xmin, xmax=xmax, tierclass=tierclass, name=name)
        tpos = 0.
        for intv in l:
            if abs(tpos - intv._xmin) >= 0.001:
                tier.append(Interval(tpos, intv._xmin, ''))
            tier.append(intv)
            tpos = intv._xmax
        if xmax - tpos >= 0.001:
            tier.append(Interval(tpos, xmax, ''))
        return tier



    def append(self, interval):
        self._intervals.append(interval)
        if self._class == 'IntervalTier':
            self._xmax = interval._xmax ### FIXME
        else: ### TextTier or PitchTier
            self._xmax = interval._time

    def subtier(self, xmin, xmax):
        if self._class in ['TextTier', 'PitchTier']:
            return filter(lambda point: point._time >= xmin and point._time <= xmax, self._intervals)
        elif self._class != 'IntervalTier':
            raise NotImplementedError
        #print self._intervals
        return filter(lambda intv: intv._xmin >= xmin and intv._xmax <= xmax, self._intervals)

    def save(self, fd):
        fd.write('\t\tclass = \"%s\"\n' % self._class)
        fd.write('\t\tname = \"%s\"\n' % self._name)
        fd.write('\t\txmin = %f\n' % self._xmin)
        fd.write('\t\txmax = %f\n' % self._xmax)
        if self._class == 'IntervalTier':
            fd.write('\t\tintervals: size = %d\n' % len(self._intervals))
            for i in range(len(self._intervals)):
                fd.write('\t\tintervals[%d]:\n' % (i+1))
                self._intervals[i].save(fd)
        elif self._class == 'TextTier':
            fd.write('\t\tpoints: size = %d\n' % len(self._intervals))
            for i in range(len(self._intervals)):
                fd.write('\t\tpoints[%d]:\n' % (i+1))
                self._intervals[i].save(fd)
        else:
            raise NotImplementedError
    
    def __iter__(self):
        return self._intervals.__iter__()

    def copy(self):
        ret = Tier(self._xmin, self._xmax, self._class, self._name)
        for e in self._intervals:
            ret.append(e.copy())
        return ret

    def text_at_pos(self,x):
        i = 0
        while self._intervals[i+1]._xmin < x:
            i += 1
        assert(x>=self._intervals[i]._xmin and x <= self._intervals[i]._xmax)
        return self._intervals[i]._text

    def intv_containing_pos(self, t):
        #print 'intv at pos', t
        res = filter(lambda x: x._xmin < t and x._xmax > t, self._intervals)
        # raise exception if point lies on a boundary
        assert(len(res) == 1)
        #print 'found', res[0]._xmin
        return res[0]

    def text_count(self, text):
        """
        return number of tier inverval st _text == text
        """
        res = 0
        for intv in self:
            if intv._text == text:
                res += 1
        return res

    def text_cond_count(self, condition):
        """
        return number of tier intervals whose text satisfy condition
        """
        res = 0
        for intv in self:
            if condition(intv._text):
                res += 1
        return res

    def __getitem__(self, key):
        return self._intervals[key]

    def __len__(self):
        return len(self._intervals)


# class IntervalTier(Tier):
#     pass

# class TextPointTier(Tier):
#     pass

# class RealPointTier(Tier):
#     pass

class PitchTier(Tier):
    def __init__(self, fname):
        self._class = 'PitchTier'

        f = codecs.open(fname, encoding='utf-8')
        filetype = getstringval(f.readline(), "File type")
        objectclass = getstringval(f.readline(), "Object class")

        assert('ooTextFile' == filetype)
        assert(objectclass == 'PitchTier')
        assert(f.readline() == "\n")

        self._xmin = getfloatval(f.readline(), "xmin")
        self._xmax = getfloatval(f.readline(), "xmax")

        nbvalues = getintval(f.readline(), "points: size")
        self._intervals = []
        for i in range(nbvalues):
            self._intervals.append(RealPoint(fd=f))

    # def save(self, fname):
    #     raise NotImplementedError

    # def __iter__(self):
    #     pass

    def __str__(self):
        return 'PitchTier [' + ','.join(map(str,self._intervals)) + ']'

    def copy(self):
        raise NotImplementedError

class PraatTextGrid:

    def __init__(self, xmin=0, xmax=0, ft='ooTextFile', oc='TextGrid'):
        self._filetype = ft
        self._objectclass = oc
        self._tiers = []
        self._xmin = xmin
        self._xmax = xmax
        #f = open(fname, encoding='utf-8')
        #self._filetype = getstringval(f.readline(), "File type")
        #self._objectclass = getstringval(f.readline(), "Object class")
        #assert(f.readline() == "\n")
        #self._xmin = getfloatval(f.readline(), "xmin")
        #self._xmax = getfloatval(f.readline(), "xmax")
        #assert(f.readline() == "tiers? <exists> \n") ## lorsqu'on sauvegarde, on ne mets pas d'espace, il faudrait peut être gérer ça a coup de regexp
        #nbtiers = getintval(f.readline(), "size")
        #assert(re.match(r'item \[\]:\s*', f.readline()))
        
        #for i in range(nbtiers):
        #    self._tiers.append(Tier(f))

    @classmethod
    def loadfromfile(cls, fname):
        f = codecs.open(fname, encoding='utf-8')
        assert(getstringval(f.readline(), 'File type') == 'ooTextFile')
        assert(getstringval(f.readline(), 'Object class') == 'TextGrid')
        assert(f.readline().strip() == "")
        xmin = getfloatval(f.readline(), "xmin")
        xmax = getfloatval(f.readline(), "xmax")
        assert(f.readline().strip() == "tiers? <exists>") ## lorsqu'on sauvegarde, on ne mets pas d'espace, il faudrait peut être gérer ça a coup de regexp
        nbtiers = getintval(f.readline(), "size")
        assert(re.match(r'item \[\]:\s*', f.readline()))

        tg = cls(xmin=xmin, xmax=xmax)
        for i in range(nbtiers):
            tg._tiers.append(Tier.loadfromfd(f))

        return tg

    
    def save(self, fname):
        f = codecs.open(fname, 'w', encoding='utf-8')
        f.write('File type = "%s"\n' % self._filetype)
        f.write('Object class = "%s"\n\n' % self._objectclass)
        f.write('xmin = %f\n' % self._xmin)
        f.write('xmax = %f\n' % self._xmax)
        f.write('tiers? <exists> \n')
        f.write('size = %d\n' % len(self._tiers))
        f.write('item []:\n')
        for i in range(len(self._tiers)):
            f.write('\titem [%d]:\n' % (i+1))
            self._tiers[i].save(f)
        f.close()
        
    def __getitem__(self, key):
        for t in self._tiers:
            if t._name == key:
                return t
        print('key ', key, 'not available in TextGrid')
        raise exception.KeyError

    def __iter__(self):
        return self._tiers.__iter__()

    def append(self, tier):
        self._tiers.append(tier)

    def copy(self):
        raise NotImplementedError


            
if __name__ == "__main__":
    import sys

    #getstringval('            text = "<s>" ', "text")

    #ptg = PraatTextGrid(sys.argv[1])
    #ptg.save(sys.argv[2])
    #print 'done!'


    pt = PitchTier(sys.argv[1])
    print(pt)
