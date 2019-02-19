from audio_stegano import *
import pyaudio

def get_message(message_file):
    """Opens message file and retrieve the message within"""
    file = open(message_file, 'r')
    message = ''
    for line in file:
        message += line

    return message


def main():
    audio_file = input("Audio File: ")
    message_file = input("Message File: ")
    stego_key = input("Stego key: ")

    in_audio = wave.open(audio_file, 'r')

    print("1. Embed Message\n2. Extract Message")
    mode = int(input("Select operation: "))

    if mode == 1:
        message = get_message(message_file)
        frame_size = len(in_audio.readframes(1))
        in_audio.rewind()
        payload_size = in_audio.getnframes() * frame_size - 80 - len(audio_file) * 8
        if len(message) * 8 > payload_size:
            print("Error, message larger than payload size")
            raise AssertionError
        out_file = input("Output Audio File: ")
        out_audio = wave.open(out_file, 'w')
        out_audio.setparams(in_audio.getparams())

        print("1. Sequential LSB\n2. Random LSB")
        lsb_mode = int(input("LSB Mode: "))
        
        if lsb_mode == 1:
            sequential_audio_lsb(in_audio, out_audio, message)
        elif lsb_mode == 2:
            seeded_audio_lsb(in_audio, out_audio, message, stego_key)
        else:
            raise AssertionError

        while True:
            print("1. Play Original Audio\n2. Play Stego-Audio\n3. Quit")
            play_audio = int(input("Choose option: "))

            player = pyaudio.PyAudio()

            if play_audio == 1:
                in_audio.rewind()
                stream = player.open(format = player.get_format_from_width(in_audio.getsampwidth()),
                                    channels = in_audio.getnchannels(),
                                    rate = in_audio.getframerate(),
                                    output = True)

                data = in_audio.readframes(1024)

                while data:
                    stream.write(data)
                    data = in_audio.readframes(1024)
                
                stream.stop_stream()
                stream.close()

            elif play_audio == 2:
                out_audio.close()
                out_audio = wave.open(out_file, 'r')
                stream = player.open(format = player.get_format_from_width(out_audio.getsampwidth()),
                                    channels = out_audio.getnchannels(),
                                    rate = out_audio.getframerate(),
                                    output = True)

                data = out_audio.readframes(1024)

                while data:
                    stream.write(data)
                    data = out_audio.readframes(1024)
                
                stream.stop_stream()
                stream.close()

            else:
                player.terminate()
                break
    
    elif mode == 2:
        lsb_mode_frame = in_audio.readframes(1)

        lsb_mode = lsb_mode_frame[0] & 1

        if lsb_mode == LSB_SEQUENTIAL:
            original_filename, message = extract_sequential_audio_lsb(in_audio)
        elif lsb_mode == LSB_RANDOM:
            original_filename, message = extract_seeded_audio_lsb(in_audio, stego_key)
        else:
            raise AssertionError

        message_file = open(message_file, 'w')
        message_file.write(message)

if __name__ == '__main__':
    main()  