from VideoIO import VideoFile
from VideoIO import VideoFrame
import vigenere_cipher as vigenere
import math
import rand
import stegano_avi

def main():
    # MAIN FILE
    print("Pilih mode program:")
    print("1.Penyisipan Pesan") 
    print("2.Ekstraksi")

    mode = int(input("Masukkan nomor pilihanmu : "))
    if(mode == 1):
        plaintext_file = input("Masukan nama file input plaintext: ")
    video_filename = input("Masukkan nama file yang akan diproses : ")
    lsb_size = int(input("Masukkan ukuran LSB yang diubah (bit) : "))
    stegano_key = input("Masukkan kunci steganografi : ")
    is_encypted = input("Apakah pesan dienkripsi? (y/n) : ") == 'y'

    #Inisiasi Video
    video_file = VideoFile(video_filename,'r')

    #Get Frames
    frame_list = []
    video_frame = video_file.get_frame()
    while video_frame:
        frame_list.append(video_frame)
        video_frame = video_file.get_frame()

    #Debug, check whether frame are taken
    #print(len(frame_list))

    if (mode == 1):
        ## BACA FILE PLAINTEKS
        f = open(plaintext_file, 'r')
        text = f.read()
        f.close()
        ## ENKRIPSI PESAN
        if is_encypted:
            text = text.upper()
            text = vigenere.remove_symbols(text)
            text = text.replace(" ", "")
            stegano_key = stegano_key.upper()
            stegano_key = vigenere.remove_symbols(stegano_key)
            stegano_key = stegano_key.replace(" ", "")
            text = vigenere.standard_vigenere_cipher(text, stegano_key, True)

        ## PENYISIPAN PESAN
        is_frame_random = input("Apakah frame ingin dipilih secara acak? (y/n) : ") == 'y'
        is_pixel_random = input("Apakah pixel ingin dipilih secara acak? (y/n) : ") == 'y'

        width, height = video_file.resolution
        total_pixels = width * height
        length_per_frame = int(math.ceil(1.0 * len(text) / len(frame_list)))
        MAX_LENGTH_PER_FRAME = ((total_pixels - 1) * 3) / 8

        ## SIMPAN INFO STEGANO
        stegano_avi.insert_stegano_info(frame_list[0], lsb_size, is_frame_random, is_pixel_random)

        if (not is_frame_random):
            # FRAME SEKUENSIAL
            if (not is_pixel_random):
                # FRAME SEKUENSIAL, PIXEL SEKUENSIAL
                frame_no = 1
                for i in range(0, len(text), length_per_frame):
                    message = text[i:(i+length_per_frame)]
                    stegano_avi.sequential_image_stegano(frame_list[frame_no], message, lsb_size, width, height)
                    frame_no = frame_no + 1

                #print("fsps")
            else:
                # FRAME SEKUENSIAL, PIXEL RANDOM
                pixel_list = rand.generate_random_list(stegano_key, length_per_frame * 8, total_pixels, len(frame_list))
                frame_no = 1
                for i in range(0, len(text), length_per_frame):
                    message = text[i:(i+length_per_frame)]
                    stegano_avi.seeded_image_stegano(frame_list[frame_no], message, lsb_size, size_x, size_y, pixel_list[frame_no])
                    frame_no = frame_no + 1

                #print("fspr")
        else:
            # FRAME RANDOM
            length_per_frame = length_per_frame * 10
            used_frames = rand.generate_random_frames(stegano_key, len(frame_list), int(math.ceil(1.0 * len(frame_list) /10)))
            if (not is_pixel_random):
                # FRAME RANDOM, PIXEL SEKUENSIAL
                frame_no = 1
                for i in range(0, len(text), length_per_frame):
                    message = text[i:(i+length_per_frame)]
                    stegano_avi.sequential_image_stegano(frame_list[used_frames[frame_no]], message, lsb_size, width, height)
                    frame_no = frame_no + 1
                #print("frps")
            else:
                # FRAME RANDOM, PIXEL RANDOM
                pixel_list = rand.generate_random_list(stegano_key, length_per_frame * 8, total_pixels, len(used_frames))
                frame_no = 1
                for i in range(0, len(text), length_per_frame):
                    message = text[i:(i+length_per_frame)]
                    stegano_avi.seeded_image_stegano(frame_list[used_frames[frame_no]], message, lsb_size, size_x, size_y, pixel_list[frame_no])
                    frame_no = frame_no + 1
                #print("frpr")

        output_filename = input("Masukkan nama file output : ")
        output_video = VideoFile(output_filename,'w')
        resolution = (height, width)
        output_video.configure_output(output_filename, 20, resolutions)
        for frame in frame_list:
            output_video.write_frame(frame)

        print("Message successfully hidden")
    elif(mode == 2):
        ## EKSTRAKSI

        is_frame_random, is_pixel_random, lsb_value = stegano_avi.extract_stegano_info(frame_list[0])
        text = ""

        if (not is_frame_random):
            # FRAME SEKUENSIAL
            if (not is_pixel_random):
                # FRAME SEKUENSIAL, PIXEL SEKUENSIAL
                for frame_no in range(1, len(frame_list)):
                    message = stegano_avi.extract_sequential(frame_list[frame_no], lsb_value, width, height)
                    text.append(message)

                #print("fsps")
            else:
                # FRAME SEKUENSIAL, PIXEL RANDOM
                pixel_list = rand.generate_random_list(stegano_key, length_per_frame * 8, total_pixels, len(frame_list))
                for frame_no in range(1, len(frame_list)):
                    message = stegano_avi.extract_seeded(frame_list[frame_no], lsb_value, width, height, pixel_list)
                    text.append(message)

                #print("fspr")
        else:
            # FRAME RANDOM
            length_per_frame = length_per_frame * 10
            used_frames = int(rand.generate_random_frames(stegano_key, len(frame_list), math.ceil(1.0 * len(frame_list) /10)))
            if (not is_pixel_random):
                # FRAME RANDOM, PIXEL SEKUENSIAL
                for frame_no in used_frames:
                    message = stegano_avi.extract_sequential(frame_list[frame_no], lsb_value, width, height)
                    text.append(message)
                #print("frps")
            else:
                # FRAME RANDOM, PIXEL RANDOM
                pixel_list = rand.generate_random_list(stegano_key, length_per_frame * 8, total_pixels, len(frame_list))
                for frame_no in used_frames:
                    message = stegano_avi.extract_seeded(frame_list[frame_no], lsb_value, width, height, pixel_list)
                    text.append(message)
                #print("frpr")

        ## Langsung Ekstraksi aja boi
        ##print("Extracting")
        output_filename = input("Masukkan nama file output : ")
        f = open(output_filename, 'wb')
        f.write(text)
        f.close()


if __name__ == "__main__":
    main()