# gwmg.base.py

import Image, ImageOps

    
class Subject(object):
    "Base Subject"

    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
    
    def notify(self, modifier=None):
        for observer in self._observers:
            if modifier != observer:
                observer.update(self)


class Observer(object):
    "Base Observer - does nothing, but define an interface"

    def update(self, subject):
        pass


class Controller(Subject):
    """
    Base Controller
    Attach animations to a controller
    """    

    def __init__(self, frame_range):
        Subject.__init__(self)
        self.frameNum = frame_range[0] - 1
        self.frameRange = frame_range
        self.frame = None

    def notify(self, modifier=None):
        self.frameNum += 1
        for observer in self._observers:
            if modifier != observer and \
                    observer.inRange(self.frameNum):
                observer.update(self)
    
    def getImage(self, frame_num=None):
        "can be used as a FrameProvider"
        return self.frame.copy()
        

class Animation(Observer):
    """
    Base Animation
    keep track of local frameNum and range
    """

    def __init__(self, frame_range):    
        self.__frameRange = frame_range
        self.currentFrame = 0
    
    def update(self, controller):
        self.currentFrame += 1
     
    def inRange(self, frame_num):
        if frame_num >= self.__frameRange[1]:
            return False
        elif frame_num < self.__frameRange[0]:
            return False
        else:
            return True


class ImageProvider(object):
    """
    ImageProvider is wicket
    """

    def __init__(self, size, default=None):
        self.size = size
        if default:
            self.__default = Image.open(default)
            if self.__default.mode != "RGB":
                self.__default = self.__default.convert("RGB")
            if self.__default.size != size:
                self.__default = ImageOps.fit(self.__default,self.size)
                
    def getImage(self, frameNum):
        if not(self.__default):
            return Image.new("RGB", self.size, "White")
        else:
            return self.__default.copy()


class FrameProvider(ImageProvider):
    "provide a frame based on src string"

    def __init__(self, size, src):
        ImageProvider.__init__(self, size)
        self.__src = src
        self.__offset = 0 #how much to subtract from frame_num

    def getImage(self, frame_num):
        """ try helps us loop to begining of sequence
        if we reach the end start providing frames from the begining"""
        try:
            image = Image.open(self.__src % (frame_num - self.__offset))
        except IOError:
            self.__offset = frame_num - 1
            image = Image.open(self.__src % (frame_num - self.__offset))
        return ImageOps.fit(image, self.size)


class ControlFrameProvider(ImageProvider):
    "provides the control frame"
    
    def __init__(self, size, control):
        ImageProvider.__init__(self, size)
        self.__control = control
    
    def getImage(self, frame_num=None):
        return self.__control.frame.copy()


class ColorProvider(ImageProvider):
    "provides a singel color image"

    def __init__(self, size, color, type="RGB"):
        ImageProvider.__init__(self, size)
        self.__image = Image.new(type, size, color)
    
    def getImage(self, frameNum=None):
        return self.__image.copy()


class MaskImageProvider(ImageProvider):
    "Provides a mask"
    
    def __init__(self, size, src, invert, type="L"):
        ImageProvider.__init__(self, size, src)
        self.__invert = invert
        self.__type = type
    
    def getImage(self, frame_num=None):
        img = ImageProvider.getImage(self, frame_num)
        if self.__invert:
            img = ImageOps.invert(img)
        img = img.convert(self.__type)
        return ImageOps.fit(img, self.size)

class MaskProvider(FrameProvider):
    "Provides a mask"
    
    def __init__(self, size, src, invert, type="L"):
        FrameProvider.__init__(self, size, src)
        self.__invert = invert
        self.__type = type
    
    def getImage(self, frame_num=None):
        img = FrameProvider.getImage(self, frame_num)
        if self.__invert:
            img = ImageOps.invert(img)
        img = img.convert(self.__type)
        return ImageOps.fit(img, self.size)

class ImageKeeper(ImageProvider):
    """special kind of image provider that also saves image
    this allows for the layering of patterns in parallel."""
    
    def __init__(self, size):
        ImageProvider.__init__(self, size)
        self._image_fn = self.getRegularImage
         
    def getImage(self, frameNum=None):
        return self._image_fn()

    def getRegularImage(self):
        return self.__image.copy()
    
    def getMaskImage(self):
        if self._invert:
            self.__image = ImageOps.invert(self.__image)
        img = self.__image.convert(self._type)
        return img
    
    def setImage(self, image):
        self.__image = image
    
    def getMask(self, invert=False, type="L"):
        self._invert = invert
        self._type = type
        self._image_fn = self.getMaskImage
        return self
        

class TweenFactory(object):
    "return the tween of my asking"
    def linear(self, total_change, number_of_steps):
        return LinearTween(total_change, number_of_steps)        


class Tween(object):
    "tween interface"
    def getStep(self, frame_num):
        return 0

    
class LinearTween(Tween):
    "provide tween step, default is linear"
    
    def __init__(self, total_change, number_of_steps):
        Tween.__init__(self)
        if total_change == 0 or number_of_steps == 0:
            self.step = 0
        else:
            self.step = float(total_change) / number_of_steps
    
    def getStep(self, frame_num=None):
        return self.step

        
class AnimationMaker(object):
    """
    Runs the show
    To use, Override and Implement buildAnimation(self, animation) only
    """

    def __init__(self, frame_range, dest, size=(720,480)):
        """
        frameCount - how many to process
        params src, dest - where to grab frames, where to put 'em,
        base is the base filenames for source and dest
        """
        self.frameRange = frame_range
        self.frameCount = frame_range[1] - frame_range[0]
        self.dest = dest
        self.size = size

    def writeFrame(self, frameNum, img):
        """
        Writes frame image to file.
        """
        # use me pattern in for dest
        frameFilename =  self.dest % frameNum
        print "write " + frameFilename
        # write file
        if not(img):
            img = Image.new("RGB", self.size, "White")
        img.save(frameFilename, 'PNG')
    
    def buildAnimation(self, control):
        "override me and attach!"
        print "override me and attach!"
    
    def make(self): 
        "Get goin yee dogs!" 
        main_control = Controller((self.frameRange[0], self.frameRange[1] + 1))
        self.buildAnimation(main_control) 
        for i in range(self.frameRange[0], self.frameRange[1] + 1): 
            # create image 
            main_control.notify()
            self.writeFrame(i, main_control.frame) 
