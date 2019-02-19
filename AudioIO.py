WAV_HEADER_LENGTH = 44

class AudioFile:
    """Class for I/O operations on audio file"""

    def __init__(self, filename, mode='r'):
        """Opens given file as an audio file

        Keyword arguments:
        mode -- 'r' for read, 'w' for write
        """
        self._mode = mode
        self._filename = filename
        if self._mode == 'r':
            self._audio = open(filename, 'rb')
        elif self._mode == 'w':
            self._audio = open(filename, 'wb')
        else:
            print("Failed to open audio file, mode not recognized")
            raise AssertionError


    def skip_bytes(self, n):
        """Skips n bytes from the file"""
        self._audio.read(n)

    
    def get_byte(self):
        """Gets next byte from the audio file"""
        try:
            assert(self._mode == 'r')
        except AssertionError:
            print("File opened in write mode, cannot read")
            raise

        return self._audio.read(1)
    
    
    def write_bytes(self, new_bytes):
        """Writes bytes into the audio file"""
        try:
            assert(self._mode == 'w')
        except AssertionError:
            print("File opened in read mode, cannot write")
            raise
        
        self._audio.write(new_bytes)
