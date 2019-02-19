import cv2 as cv
import numpy as np

class VideoFrame:
    """Represents a single frame of a video"""

    def __init__(self, pixel_array):
        """Accepts a 3D array representing an image"""

        self._pixels = np.asarray(pixel_array)
        self._shape = self._pixels.shape
        try:
            assert(len(self._shape) == 3)
        except AssertionError:
            print("Expected 3D array, received "
                    + "{}D array instead".format(len(self._shape)))
            raise


    @property
    def pixels(self):
        """Returns all the pixel of the frame in a matrix"""
        return self._pixels


    def get_pixel(self, x, y):
        """Returns the RGB values of a pixel at location (x, y)
        
        As with OpenCV, (0, 0) is the top left corner of the frame"""
        return self._pixels[y, x]

    
    def write_pixel(self, x, y, rgb_array):
        """Writes the RGB value into pixel at location (x, y)

        rgb_array -- a 1D array of length 3 containing RGB values
        """
        try:
            assert(len(rgb_array) == 3)
        except AssertionError:
            print("Expected 3D array for RGB values, "
                    + "got {}D values intead".format(len(rgb_array)))
                    
        self._pixels[y, x] = rgb_array

class VideoFile:
    """Class for I/O operations on a video file"""

    def __init__(self, filename, mode='r'):
        """Opens given file as a video source
        
        Keyword arguments:
        mode -- open in read or write mode ('r' is default, 'w' for write)
        """
        self._mode = mode
        if self._mode == 'r':
            self._video = cv.VideoCapture(filename)
        elif self._mode == 'w':
            self._codec = cv.VideoWriter_fourcc(*'XVID')
            self._video = cv.VideoWriter("videos/" + filename, self._codec
                                            , 20.0, (1080, 1920))
        else:
            print("Failed to open video file: mode not recognized")
            raise AssertionError
            
        self._current_frame = 0


    def get_frame(self):
        """Returns the next frame from the video as a VideoFrame object

        Return None if no more frame is available
        """

        try:
            assert(self._mode == 'r')
        except AssertionError:
            print("Cannot get frame, file is opened in write mode")
            raise

        ret, frame = self._video.read()

        if ret:
            self._current_frame += 1
            return VideoFrame(frame)
        else:
            return None

    
    def configure_output(self, filename, framerate, size):
        """Configures the properties of the output video

        filename -- name of output video (v.avi by default)
        framerate -- framerate for output video (20.0 by default)
        size -- video resolution ((1080, 1920) by default)
        """
        self._video.open(filename, self._codec, framerate, size)


    def write_frame(self, frame):
        """Writes a single frame into the video file

        Remember to call configure_output method before writing

        frame -- VideoFrame object
        """

        try:
            assert(self._mode == 'w')
        except AssertionError:
            print("Cannot write frame, file is opened in read mode")
            raise
        
        self._video.write(frame.pixels)


    @property
    def resolution(self):
        return(self._video.get(cv.CAP_PROP_FRAME_WIDTH), self._video.get(cv.CAP_PROP_FRAME_HEIGHT))