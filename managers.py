import cv2
import numpy as np
import time

class CaptureManager(object):
    def __init__(self, capture, previewWindowManager = None,
                 shouldMirrorPreview = False):
        
        self.previewWindowManager = previewWindowManager
        self.shouldMirrorPreview = shouldMirrorPreview

        self._capture = capture
        self._channel = 0
        self._enteredFrame = False
        self._frame = None
        self._imageFilename = None
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None

        self._startTime = None
        self._framesElapsed = 0
        self._fpsEstimate = None

    @property
    def channel(self):
        return self._channel
        
    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = value
            self._frame = None

    @property
    def frame(self):
        if self._enteredFrame and self._frame is None:
            _, self._frame = self._capture.retrieve(
            channel = self.chennel
                )
        return self._frame
        
    @property
    def isWritingImage(self):
        return self._imageFilename is not None
        
    @property
    def isWritingVideo(self):
        return self._videoFilename is not None
        
    # creating enterFrame() method
    def enterFrame(self):
        # But first, check that any previous frame was exited.
        assert not self._enteredFrame, \
            'previous enterFrame() had no matching exitFrame()'
        if self._capture is not None:
            self._enteredFrame = self._capture.grab()

    # create exitFrame() method
    def exitFrame(self):
        if self.frame is None:
            self._enteredFrame = False
            return
        
        if self._framesElapsed == 0:
            self._startTime = time.time()
        else:
            timeElapsed = time.time() - self._startTime
            self._fpsEstimate = self._framesElapsed / timeElapsed
        self._framesElapsed += 1

        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                mirroredFrmae = np.fliplr(self.frame).copy()
                self.previewWindowManager.show(mirroredFrmae)
            else:
                self.previewWindowManager.show(self.frame)

        if self.isWritingImage:
            cv2.imwrite(self._imageFilename, self.frame)
            self._imageFilename = None

        self._writeVideoFrame()

        self._frame = None
        self._enteredFrame = False

    '''Let's add the following
    implementations of public methods named writeImage, 
    startWritingVideo, and stopWritingVideo'''

    def writeImage(self, filename):
        self._imageFilename = filename

    
                

