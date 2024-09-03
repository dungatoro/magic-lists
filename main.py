from functools import total_ordering
import operator as op
from itertools import groupby
 
ALGEBRAIC, GEOMETRIC = "algebraic", "geometric"
etc = "..."

@total_ordering
class Inf:
    def __eq__(self, other): return isinstance(other, Inf)
    def __lt__(self, other): return False

class MagicRange:
    def __init__(self, series, lower, upper, d):
        self.__series = series
        self.__lower = lower
        self.__upper = upper
        self.__d = d
        
    def __iter__(self):
        x = self.__lower
        # the comparison is < if d is positive and > if d is negative
        comp = op.lt if self.__d >= 0 else op.gt
        while comp(x, self.__upper):
            yield x
            x = x+self.__d if self.__series == ALGEBRAIC else x*self.__d

    def __repr__(self):
        return f"MagicRange{self.__series, self.__lower, self.__upper, self.__d}"

class L:
    def __init__(self, *nums):
        nums = [None]+list(nums) # add extra element to drop
        false_ranges = []
        splits = [list(g) for k, g in groupby(nums, lambda x: x==etc) if not k]
        for i, l in enumerate(splits[1:]):
            #                    (all but first, upper bound)
            false_ranges.append( ( splits[i][1:], l[0]        ) )

        self.ranges = []
        for nums, upper in false_ranges:
            if len(nums) < 3: # we assume algebraic
                d = 1 if len(nums) == 1 else nums[-1]-nums[-2]
                self.ranges.append( MagicRange(ALGEBRAIC, nums[0], upper, d))
                continue

            elif (d := nums[-1]-nums[-2]) == nums[-2]-nums[-3]:
                series = ALGEBRAIC

            elif (d := nums[-1]/nums[-2]) == nums[-2]/nums[-3]:
                if d.is_integer(): d = int(d) 
                series = GEOMETRIC

            # traverse backwards until an element breaks the pattern
            i, broken = len(nums)-2, False
            lower = nums[-3]
            while not broken and i > 0:
                i -= 1
                if (series == ALGEBRAIC and nums[i]-nums[i-1] == d or 
                    series == GEOMETRIC and nums[i]/nums[i-1] == d   ):
                    lower = nums[i]
                else:
                    broken = True
            
            if broken: self.ranges.append(nums[:i])
            self.ranges.append(MagicRange(series, lower, upper, d))

    def __iter__(self):
        for nums in self.ranges:
            for num in nums:
                yield num
