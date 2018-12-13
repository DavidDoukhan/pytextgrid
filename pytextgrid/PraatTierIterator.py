#!/usr/bin/env python
# -*- coding: latin-1 -*-

import exceptions
from PraatTextGrid import Interval

class PraatTierIterator:
    def __init__(self):
       raise NotImplementedError
    def __iter__(self):
        return self

class ExcludeListTierIterator:
    """
    iterate on a given praat tier and exclude intervals
    whose text is contained in a list/set given at instance creation
    """
    def __init__(self, tier, exclude_set=[]):
        #self._intervals = tier._intervals
        #self._pos = 0
        self._it = tier.__iter__()
        self._exclude_set = set(exclude_set)

    def next(self):
        res = self._it.next()
        while res._text in self._exclude_set:
            res = self._it.next()
        return res

        # intvs = self._intervals
        # while self._pos < len(intvs) and intvs[self._pos]._text in self._exclude_set:
        #     self._pos += 1
        # if self._pos >= len(intvs):
        #     raise exceptions.StopIteration
        # self._pos += 1
        # return intvs[self._pos - 1]

    # def has_next(self):
    #     return self._pos < len(self._intervals)

    # bugged!!!
    # def current(self):
    #     return self._pt._intervals[self._pos]


# class WordTierIterator:
#     # FIXME: find a more explicit name
#     def __init__(self, pt, specials=None):
#         """
#         pt is a praat tier
#         """
#         self._pt = pt
#         self._pos = 0
#         self._special=['#START', '<s>', '</s>', ',', '[silence]', '.', '...', ':', '-', '?', '!', '\"', '#', '[rire]', ';', '']

#     def __iter__(self):
#         return self

#     def next(self):
#         while self._pos < len(self._pt._intervals) and self._pt._intervals[self._pos]._text in self._special:
#             self._pos += 1
#         if self._pos >= len(self._pt._intervals):
#             raise exceptions.StopIteration
#         self._pos += 1
#         return self._pt._intervals[self._pos - 1]

#     def has_next(self):
#         return self._pos < len(self._pt._intervals)

#     def current(self):
#         return self._pt._intervals[self._pos]


# class MergeSpecialsIterator(WordTierIterator):
#     def next(self):

#         if self._pos >= len(self._wt._intervals):
#             raise exceptions.StopIteration

#         if self._wt._intervals[self._pos]._text in self._special:
#             xmin = self._wt._intervals[self._pos]._xmin
#             while self._pos < len(self._wt._intervals) - 1 and self._wt._intervals[self._pos + 1]._text in self._special:
#                 self._pos += 1
#             xmax = self._wt._intervals[self._pos]._xmax
#             text = '.'
#         else:
#             cur = self._wt._intervals[self._pos]
#             xmin = cur._xmin
#             xmax = cur._xmax
#             text = cur._text
        
#         self._pos += 1
#         return Interval(xmin=xmin,xmax=xmax,text=text)

# class MergeWordNonwordIterator(WordTierIterator):
#     """
#     return intervals corresponding to coniguous words or contiguous non words
#     """
#     def next(self):
        
#         if self._pos >= len(self._wt._intervals):
#             raise exceptions.StopIteration
        
#         if self._wt._intervals[self._pos]._text in self._special:
#             # first case, the element is non word
#             xmin = self._wt._intervals[self._pos]._xmin
#             while self._pos < len(self._wt._intervals) - 1 and self._wt._intervals[self._pos + 1]._text in self._special:
#                 self._pos += 1
#             xmax = self._wt._intervals[self._pos]._xmax
#             text = '.'
#         else:
#             # second case, the element is a word
#             xmin = self._wt._intervals[self._pos]._xmin
#             while self._pos < len(self._wt._intervals) - 1 and not(self._wt._intervals[self._pos + 1]._text in self._special):
#                 self._pos += 1
#             xmax = self._wt._intervals[self._pos]._xmax
#             text = 'W'
#         self._pos += 1
#         return Interval(xmin=xmin,xmax=xmax,text=text)
