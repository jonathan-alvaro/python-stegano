import wave

LSB_SEQUENTIAL = 1
LSB_RANDOM = 0


def pack_audio_lsb_message(message, filename):
    """Inserts necessary information for decryption into the message"""
    message = filename + ' ' + len(message) + ' ' + message
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
        frame = in_audio.readframes(1)

        if embedded_chars < len(message):
            for i, b in enumerate(frame):

                # Extract LSB
                embed_bit = (char >> (8 - (i + 1)) & 1)

                # Embed LSB
                modified_byte = frame[i] & (~1) | embed_bit
                frame = frame[0:i] + bytes(chr(modified_byte), 'utf-8') + frame[i+1:]

                current_char_bits += 1
                if current_char_bits == 8:
                    embedded_chars += 1
                    current_char_bits = 0
                    char = message[embedded_chars]
            
        out_audio.writeframes(frame)


def extract_sequential_audio_lsb(audio_file):
    