import wave
from time import sleep

LSB_SEQUENTIAL = 1
LSB_RANDOM = 0


def pack_audio_lsb_message(message, filename):
    """Inserts necessary information for decryption into the message"""
    message = str(len(message)) + ' ' + filename + ' ' + message
    return message


def sequential_audio_lsb(in_audio, out_audio, message):
    """Embeds the message into in_audio by LSB and writes it to out_audio
    
    arguments:
    in_audio : Wave_read object opened on the source audio file
    out_audio : Wave_write object already configured according to the in_audio
    message : message to embed
    """
    try:
        assert(type(in_audio) == wave.Wave_read)
        assert(type(out_audio) == wave.Wave_write)
        assert(type(message) == str)
    except AssertionError:
        type_1 = type(in_audio)
        type_2 = type(out_audio)
        type_3 = type(message)
        print("Expected Wave_read, Wave_write and string as input,"
            + " got {}, {} and {} instead".format(type_1, type_2, type_3))
        raise

    # Embed a bit to determine in which mode the LSB algorithm is applied
    new_frame = in_audio.readframes(1)
    embed_bit = LSB_SEQUENTIAL
    new_byte = new_frame[0]
    new_byte = new_byte & (~1) | embed_bit
    new_frame = bytes(chr(new_byte), 'utf-8') + new_frame[1:]
    out_audio.writeframes(new_frame)

    embedded_chars = 0
    current_char_bits = 0
    # Extract char to embed
    char = message[embedded_chars]

    for _ in range(in_audio.getnframes()):
        
        if embedded_chars < len(message):
            frame = in_audio.readframes(1)
            for i, b in enumerate(frame):

                # Extract LSB
                embed_bit = (ord(char) >> (8 - (current_char_bits + 1)) & 1)

                # Embed LSB
                modified_byte = frame[i] & (~1) | embed_bit
                frame = frame[0:i] + bytes(chr(modified_byte), 'utf-8') + frame[i+1:]

                current_char_bits += 1
                if current_char_bits == 8:
                    embedded_chars += 1
                    current_char_bits = 0
                    if embedded_chars < len(message):
                        char = message[embedded_chars]
            
            out_audio.writeframes(frame)
        
        else:
            frame = in_audio.readframes(in_audio.getnframes())
            out_audio.writeframes(frame)
            break


def extract_sequential_audio_lsb(in_audio):
    """Extracts a message embedded within a wav file
    
    arguments:
    in_audio : a Wave_read object opened on an audio file
                containing an embedded message

    returns:
    filename : original audio filename
    message : embedded message
    """

    try:
        assert(type(in_audio) == wave.Wave_read)
    except AssertionError:
        print("Expected Wave_read object")
        raise

    # Skip first frame as it is used to store LSB mode information
    in_audio.rewind()
    in_audio.readframes(1)

    frames = in_audio.readframes(in_audio.getnframes() - 1)

    current_char_bits = 0
    message = ''
    message_length = None
    filename = None
    current_char = 0

    for char in frames:
        embedded_bit = char & 1
        current_char = current_char << 1 | embedded_bit
        current_char_bits += 1
        # print(current_char)
        # sleep(1)

        if current_char_bits == 8:
            if chr(current_char) == ' ':
                if not message_length:
                    message_length = int(message)
            
                elif not filename:
                    filename = message

                message = ''
            
            else:
                message += chr(current_char)
            
            if len(message) == message_length and filename and message_length:
                break

            current_char_bits = 0
            current_char = 0

    return (filename, message)