# gwmg.Effects.py

import base
import Image, ImageOps

class Effect(base.Observer):
    def __init__(self, frame_range, keeper, providers):
        self.frameRange = frame_range
        self.keeper = keeper
        self.providers = providers
        self.currentFrame = 0
        self.frameCount = frame_range[1] - frame_range[0]
    
    def update(self, controller):
        self.currentFrame += 1
        
    def inRange(self, frame_num):
        if frame_num >= self.frameRange[1]:
            return False
        elif frame_num < self.frameRange[0]:
            return False
        else:
            return True

class ColorScale(Effect):
    "make a colorized version of something"
    
    def __init__(self, frame_range, keeper, providers, background_color, foreground_color):
        print frame_range
        Effect.__init__(self, frame_range, keeper, providers)
        self.backImage = Image.new("RGB", providers[0].size, background_color)
        self.foreImage = Image.new("RGB", providers[0].size, foreground_color)
        
    def update(self, control):
        Effect.update(self, control)
        image_in = self.providers[0].getImage(self.currentFrame)
        image_mask = image_in.convert('L')
        image_out = Image.composite(self.backImage, self.foreImage, image_mask)
        self.keeper.setImage(image_out)

  
class Mask(Effect):
    """mask providers given (foreground, background, mask)
    was regular mask"""

    def __init__(self, frame_range, keeper, providers):
        Effect.__init__(self, frame_range, keeper, providers)
        self.foregroundProvider = providers[0]
        self.backgroundProvider = providers[1]
        self.maskProvider = providers[2]
        
    def update(self, control):
        Effect.update(self, control)
        fore = self.foregroundProvider.getImage(self.currentFrame)
        bg = self.backgroundProvider.getImage(self.currentFrame)
        mask = self.maskProvider.getImage(self.currentFrame)
        bg.paste(fore, (0,0,mask.size[0], mask.size[1]), mask)
        self.keeper.setImage(bg)

class FadeInOutPercent(Effect):
    """fade in and then out via percentages (in,hold,out)
    used to be FaderPercentAnimation"""
    
    def __init__(self, frame_range, keeper, providers, percents, tween):
        Effect.__init__(self, frame_range, keeper, providers)
        self.alpha = 0
        self.percents = percents 
        self.tweenIn = tween(1, self.frameCount * float(percents[0]) / 100) 
        self.tweenOut = tween(1, self.frameCount * float(percents[2]) / 100) 
        self.phases = (self.frameCount * float(percents[0]) / 100, \
                        self.frameCount - (self.frameCount * float(percents[2]) / 100),\
                        self.frameCount)
        self.tweenOutFrame = self.phases[0]

    def update(self, control):
        Effect.update(self, control)
        image2 = self.providers[1].getImage(self.currentFrame)
        if self.currentFrame <= self.phases[0] :
            "fade in"
            image1 = self.providers[0].getImage(self.currentFrame)
            self.alpha += self.tweenIn.getStep(self.currentFrame)
            img = Image.blend(image1, image2, self.alpha)
        if self.currentFrame > self.phases[0] and self.currentFrame <= self.phases[1]:
            "remain the same"
            self.alpha = 1
            img = image2
        if self.currentFrame > self.phases[1] :
            "fade out"
            self.tweenOutFrame += 1
            image1 = self.providers[0].getImage(self.tweenOutFrame)
            self.alpha -= self.tweenOut.getStep(self.tweenOutFrame)
            img = Image.blend(image1, image2, self.alpha)
        #print "alpha " + str(self.alpha)
        self.keeper.setImage(img) 
                

class SliceRepeaterPercentSlide(Effect):
    """"repeates a number of vertical slices"""
    
    def __init__(self, frame_range, keeper, providers, percentages, slide_frame_count):
        Effect.__init__(self, frame_range, keeper, providers)
        self.percentages = percentages
        self.sliceCount = len(percentages)
        self.pixels = []
        total_pixels = 0
        # determine the number of pixels in a slice
        deltaP = 0
        for i in range(self.sliceCount):
            pix = (float(deltaP)/float(100)) * providers[0].size[0]
            self.pixels.append(pix)
            total_pixels += pix
            deltaP += percentages[i]
        self.__step_size = float(total_pixels) / slide_frame_count 
        self.__x = 0
        self.__end_x = providers[0].size[0]
        self.__current_slice = self.sliceCount - 1
    
    def update(self, control):
        Effect.update(self, control)
        img = Image.new("RGB", self.providers[0].size)
        src_img = self.providers[0].getImage(self.currentFrame)
        size = self.providers[0].size
        x = 0
        for i in range(self.sliceCount):
            w = int(size[0] * (float(self.percentages[i]) / float(100)))
            l = x
            x += w
            r = x
            if i > self.__current_slice:
                tmpimg = ImageOps.fit(src_img, (w,img.size[1]))
                img.paste(tmpimg, (l,0,r,tmpimg.size[1]))
            if i == self.__current_slice + 1:
                self.__end_x = l 
        if self.__current_slice >= 0:
            start_x = int(self.__x)
            # paste left half
            tmpimg = ImageOps.fit(src_img, (start_x, img.size[1]))
            img.paste(tmpimg, (0,0,start_x, tmpimg.size[1]))
            # paste right half
            tmpimg = ImageOps.fit(src_img, ((self.__end_x - start_x), img.size[1]))
            img.paste(tmpimg, (start_x, 0, self.__end_x, tmpimg.size[1]))
            #self.__x += int(self.step_size[self.__current_slice])
            self.__x += self.__step_size
            if self.__x >= self.pixels[self.__current_slice]:
                self.__x = 0.00
                self.__current_slice -= 1
        self.keeper.setImage(img)

class Commit(Effect):
    "commits keeper to control"
    def __init__(self, frame_range, keeper):
        Effect.__init__(self, frame_range, keeper, None)
        
    def update(self, control):
        Effect.update(self, control)
        frame = self.keeper.getImage()
        # make sure is RGB
        if frame.mode != "RGB": frame = frame.convert("RGB")
        control.frame = frame  


class ColorForColorPixelSwapper(Effect):
    "swaps a color for another color"
    
    def __init__(self, frame_range, keeper, providers, \
                    source_color, target_color, threshold, tween=None, tween_change=None):
        Effect.__init__(self, frame_range, keeper, providers)
        self.sourceColor = source_color
        self.targetColor = target_color
        self.threshold = threshold
        self.tween = None
        if tween:
            self.tween = tween(tween_change, frame_range[1] - frame_range[0])    

    def update(self, control):
        Effect.update(self, control)
        target_image = self.providers[0].getImage(self.currentFrame)
        target_pixels = list(target_image.getdata())
        # paste pixels back into picture
        width = target_image.size[0]
        height = target_image.size[1]
        if self.tween:
            self.threshold += self.tween.getStep(self.currentFrame)
        for y in range(height):
            yp = y * width
            for x in range(width):
                xy = yp + x
                p = target_pixels[xy]
                if abs(p[0] - self.targetColor[0]) < self.threshold and \
                abs(p[1] - self.targetColor[1]) < self.threshold and \
                abs(p[2] - self.targetColor[2]) < self.threshold:
                    target_pixels[xy] = self.sourceColor
        target_image.putdata(target_pixels)
        self.keeper.setImage(target_image)

class SimpleFader(Effect):
    "Fade one image provider into another"
    
    def __init__(self, frame_range, keeper, providers, tween):
        Effect.__init__(self, frame_range, keeper, providers)
        self.alpha = 0
        self.tween = tween(1, frame_range[1] - frame_range[0]) 

    def update(self, control):
        Effect.update(self, control)
        image1 = self.providers[0].getImage(self.currentFrame)
        image2 = self.providers[1].getImage(self.currentFrame)
        self.alpha += self.tween.getStep(self.currentFrame)
        img = Image.blend(image1, image2, self.alpha)
        self.keeper.setImage(img) 
        

class CollapsingSquares(Effect):
    "squares = SquaresAnimation(squares_range, act2_keeper, act2_keeper, iterations)"

    def __init__(self, frame_range, keeper, providers, iterations):
        Effect.__init__(self, frame_range, keeper, providers)
        self.__i = 0.00
        delta = frame_range[1] - frame_range[0]
        self.__step = float(iterations) / delta

    def update(self, control):
        Effect.update(self, control)
        self.__i += self.__step
        cuts = int(self.__i) * 2
        if cuts < 1:
            return
        w = self.providers[0].size[0] / cuts
        h = self.providers[0].size[1] / cuts            
        img = self.providers[0].getImage(self.currentFrame)
        keeper_img = self.keeper.getImage()
        img = ImageOps.fit(img, (w,h)) 
        for x in range(cuts):
            for y in range(cuts):
                l = x * w
                t = y * h
                r = l + w
                b = t + h
                keeper_img.paste(img, (l,t,r,b))
        self.keeper.setImage(keeper_img)

class SliceRepeaterPercent(Effect):
    "repeates a number of vertical slices - ()"
    
    def __init__(self, frame_range, keeper, providers, percents, truths=None):
        Effect.__init__(self, frame_range, keeper, providers)
        self.percents = percents
        self.sliceCount = len(percents)
        self.truths = truths
        if len(providers) == 3:
            self.maskProvider = providers[2]
        else:
            self.maskProvider = None
    
    def update(self, control):
        Effect.update(self, control)
        src_img = self.providers[0].getImage(self.currentFrame)
        img = self.providers[1].getImage(self.currentFrame)
        size = self.providers[1].size
        x = 0
        for i in range(self.sliceCount):
            w = int(size[0] * (float(self.percents[i]) / float(100)))
            l = x
            x += w
            r = x
            if not(self.truths) or (self.truths and self.truths[i]):
                tmpimg = ImageOps.fit(src_img, (w,img.size[1]))
                if self.maskProvider:
                    mask = self.maskProvider.getImage(self.currentFrame)
                    mask = ImageOps.fit(mask, tmpimg.size) 
                    img.paste(tmpimg, (l,0,r,img.size[1]), mask)
                else:
                    img.paste(tmpimg, (l,0,r,img.size[1]))
        self.keeper.setImage(img)
