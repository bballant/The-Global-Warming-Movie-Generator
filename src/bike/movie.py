# bike voyage psychedelique
# author: Brian Ballantine

"""
This is the code for the Global Warming Movie Generator Movie, Bike Voyage Psychedelique.
This is open source software released under the MIT license:

-------------------------------------------------------------------
Copyright (c) 2008 Brian Ballanitne

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------

Directory of files:
    namespace: gwmg.bike
        movie.py     # the main code that creates the movies
        settings.py  # global variables
        providers.py # input frames and images

     namespace: gwmg
        base.py      # the engine the whole thing is built on
        Effects.py   # mask and animation effects that do the work
"""


# gwmg.bike.movie.py

from gwmg import base
from gwmg import Effects

# local package
from settings import *
import providers
        
class Maker(base.AnimationMaker):
    def buildAnimation(self, control):
        title(control)
        act1(control)
        act2(control)
        act3(control)
        the_end(control)

def title(control):
    _range = (1, 100)
    _keeper = base.ImageKeeper(SIZE)
    control.attach(\
        Effects.FadeInOutPercent(_range, _keeper, \
            (providers.black_mask, providers.behbike_mask), \
            (30, 30, 40), base.TweenFactory().linear))
    control.attach(\
        Effects.Mask(_range, _keeper, \
            (providers.yellow, _keeper, providers.title)))
    control.attach(\
        Effects.SimpleFader((3 * _range[1] / 4, _range[1]), _keeper, \
            (_keeper, providers.white_mask), \
            base.TweenFactory().linear))
    control.attach(\
        Effects.Commit(_range, _keeper))

def act1(control):
    _range = (101, 3500 + ACT_OVERLAP)
    _keeper = base.ImageKeeper(SIZE)
    _delta = _range[1]-_range[0]
    _changeup = 66 * 25 # 66 secs into it, it changes
    # background is red bikes on yellow
    control.attach(\
        Effects.ColorScale(_range, _keeper, \
            (providers.bike,), "White", "Red"))
    # create tree mask on top of bikes
    control.attach(\
        Effects.Mask(_range, _keeper,
            (providers.sun, _keeper, providers.tree_mask)))
    # animate it in
    control.attach(\
        Effects.SliceRepeaterPercentSlide(_range, _keeper, \
            (_keeper,), (10,40,10,10,30), ((_range[1] - _range[0]) / 10)))
    # fade the whole thing in
    control.attach(\
        Effects.SimpleFader((_range[0], _range[0]+50), _keeper, \
            (providers.white, _keeper), base.TweenFactory().linear))
    # begin the girdled slice
    # first one, right hand, black to yellow
    girdledSlice(control, (_range[0]+_delta/3, _range[1]-_delta/3), _keeper, \
        providers.behbike, (providers.black, providers.yellow), \
        (10,40,10,10,30), (False,False,False,False,True))
    # second one, pink to red
    girdledSlice(control, (_changeup, _range[1]-_delta/3-_delta/6), _keeper, \
        providers.behbike, (providers.pink, providers.red), \
        (10,40,10,10,30), (False,False,False,False,True))       
    # third one - bikes in middle
    girdledSlice(control, (_changeup, _range[1]-_delta/10), _keeper, \
        providers.behbike, (providers.red, providers.black), \
        (10,40,10,10,30), (False,True,False,False,False))
    # fourth one - first pink p
    girdledSlice(control, (_range[1]-_delta/5, _range[1]-_delta/14), _keeper, \
        providers.tree, (providers.white, providers.pink), \
        (10,40,10,10,30), (False,False,True,False,False))
    # fifth one - pink bar
    girdledSlice(control, (_range[1]-_delta/8, _range[1]-_delta/13), _keeper, \
        providers.tree, (providers.white, providers.pink), \
        (10,40,10,10,30), (False,False,False,True,False))   
    #final commit
    control.attach(\
        Effects.Commit(_range, _keeper))    

def act2(control):
    _range = (3501, 5500)
    _keeper = base.ImageKeeper(SIZE)
    _delta = _range[1] - _range[0]
    #fade white background to red over halfway through
    control.attach( \
        Effects.SimpleFader((_range[0], _range[0] + _delta / 2), _keeper, \
            (providers.white, providers.red), base.TweenFactory().linear))
    # fade red background to black over halfway through
    control.attach(\
        Effects.SimpleFader((_range[0] + _delta / 2, _range[1]), _keeper, \
            (providers.red, providers.black), base.TweenFactory().linear))
    # make bike animation using mask
    mask_keeper = base.ImageKeeper(SIZE)
    control.attach(\
        Effects.FadeInOutPercent(_range, mask_keeper, \
            (providers.black_mask, providers.behbike_mask), \
            (20, 60, 20), base.TweenFactory().linear))
    # turn it yellow
    control.attach(\
        Effects.Mask(_range, _keeper,
            (providers.yellow, _keeper, mask_keeper)))
    # split it and make it two
    control.attach(\
        Effects.SliceRepeaterPercent(_range, _keeper, \
            (_keeper, providers.white), (50, 50), (True, True)))
    # reuse mask_keeper fade fountain in
    control.attach(\
        Effects.FadeInOutPercent(_range, mask_keeper, \
            (providers.black_mask, providers.fountain_mask), \
            (5, 85, 10), base.TweenFactory().linear))
    control.attach(\
        Effects.Mask(_range, _keeper, \
            (providers.fountain, _keeper, mask_keeper)))
    # do some pixel swapping
    control.attach(\
        Effects.ColorForColorPixelSwapper((_range[0],_range[0]+_delta/3), _keeper, \
        (_keeper,), (255,0,0), (116, 125, 111), 30))
    control.attach(\
        Effects.ColorForColorPixelSwapper((_range[0]+_delta/4,_range[1]), _keeper, \
        (_keeper,), (255,192,203), (192, 125, 68), 17))    
    #throw in a girdled slice
    girdledSlice(control, (_range[0]+_delta*5/8,_range[1]-_delta/4), _keeper, \
        providers.behbike, (providers.pink, providers.white), \
        (50,50), (False,True))
    # fade the whole thing in
    control.attach(\
        Effects.SimpleFader((_range[0], _range[0]+ACT_OVERLAP), _keeper, \
            (control, _keeper), base.TweenFactory().linear))
    #final commit
    control.attach(\
        Effects.Commit(_range, _keeper))

def act3(control):
    _range = (5501, 7875)
    _keeper = base.ImageKeeper(SIZE)
    _delta = _range[1] - _range[0]
    _event1 = _range[1] - 625
    _event2 = _range[1] - 350
    control.attach(\
        Effects.SliceRepeaterPercent(_range, _keeper, \
            (providers.scene, providers.black, providers.auto_mask), \
            (30, 65, 5), (True, False,True)))
    okeeper = base.ImageKeeper(SIZE)
    control.attach(\
        Effects.Mask(_range, okeeper, \
        (providers.scene, providers.black, providers.bike_mask_o)))
    control.attach(\
        Effects.FadeInOutPercent(_range, okeeper, \
            (providers.black, okeeper), \
            (60, 38, 2), base.TweenFactory().linear))
    # slow collapse
    control.attach(\
        Effects.CollapsingSquares((_event1, _range[1]), okeeper, \
        (okeeper,), 15))
    control.attach(\
        Effects.SliceRepeaterPercent(_range, _keeper, \
            (okeeper, _keeper), \
            (33, 59, 8), (False, True, False)))
    # xhock ing collapsing squares
    control.attach(\
        Effects.CollapsingSquares((_event2, _range[1]), _keeper, \
        (_keeper,), 15))
    # fade the whole thing out
    control.attach(\
        Effects.SimpleFader((_range[1]-_delta/20, _range[1]), _keeper, \
            (_keeper, providers.black), base.TweenFactory().linear))    
    #ship it!
    control.attach(\
        Effects.Commit(_range, _keeper))

def the_end(control):
    _range = (7876, 8100)
    _keeper = base.ImageKeeper(SIZE)
    control.attach(\
        Effects.SimpleFader(_range, _keeper, \
        (providers.black, providers.credits), base.TweenFactory().linear))
    #ship it!
    control.attach(\
        Effects.Commit(_range, _keeper))

def girdledSlice(control, grange, gkeeper, provider, color_providers, percents, truths, type="1"):    
    "combines some effects to create a cool masked slice I call a girdled slice"
    # make a  keepers, building two separate things, then put htem together
    mask_keeper = base.ImageKeeper(SIZE)
    foreground_keeper = base.ImageKeeper(SIZE)
    # bikes that fade in then out
    control.attach(\
        Effects.FadeInOutPercent(grange, mask_keeper, \
            (providers.white, provider), \
            (10,80,10), base.TweenFactory().linear))
    control.attach(\
        Effects.SimpleFader(grange, foreground_keeper, \
            color_providers, base.TweenFactory().linear))                   
    control.attach(\
        Effects.SliceRepeaterPercent(grange, gkeeper, \
            (foreground_keeper, gkeeper, mask_keeper.getMask(True, type)), \
            percents, truths))
    
if __name__ == '__main__':
    ohmygod = Maker((1,8100), OUTPUT_FILES, SIZE)
    ohmygod.make()
