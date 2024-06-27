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

    def startWritingVideo(self, filename,
                          encoding = cv2.VideoWriter_fourcc('M','J','P','G')):
        self._videoFilename = filename
        self._videoEncoding = encoding
    
    def stopWritingVideo(self):
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None
    
    # implemenation of helper method _writeVideoFrame
    def _writeVideoFrame(self):
        if not self.isWritingVideo:
            return
        if self._videoWriter is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            if fps <= 0.0:
                if self._framesElapsed < 20:
                    return
                else:
                    fps = self._fpsEstimate
            width = self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
            size = (int(width),int(height))
            self._videoWriter = cv2.VideoWriter(
                self._videoFilename, self._videoEncoding, fps, size
            )
        self._videoWriter.write(self.frame)

class WindowManager(object):
    def __init__(self, windowName, keypressCallback = None):
        self.keypressCallback = keypressCallback
        self._windowName = windowName
        self._isWindowCreated = False

    @property
    def isWindowCreated(self):
        return self.isWindowCreated
    def createWindow(self):
        cv2.nameWindow(self._windowName)
        self._isWindowCreated = True
    def show(self, frame):
        cv2.imshow(self._windowName, frame)
    def destroyWindow(self):
        cv2.destroyWindow(self._windowName)
        self._isWindowCreated = False
    def processEvents(self):
        keycode = cv2.waitKey(1)
        if self.keypressCallback is not None and keycode != -1:
            self.keypressCallback(keycode)