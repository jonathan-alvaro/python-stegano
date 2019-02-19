from VideoIO import VideoFile

# MAIN FILE
print("Pilih mode program:")
print("1.Penyisipan Pesan") 
print("2.Ekstraksi")

mode = int(input("Masukkan nomor pilihanmu : "))
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
print(len(frame_list))

if (mode == 1):
    ## PENYISIPAN PESAN
    is_frame_random = input("Apakah frame ingin dipilih secara acak? (y/n) : ") == 'y'
    is_pixel_random = input("Apakah pixel ingin dipilih secara acak? (y/n) : ") == 'n'

    if (not is_frame_random):
        # FRAME SEKUENSIAL
        if (not is_pixel_random):
            # FRAME SEKUENSIAL, PIXEL SEKUENSIAL
            print("fsps")
        else:
            # FRAME SEKUENSIAL, PIXEL RANDOM
            print("fspr")
    else:
        # FRAME RANDOM
        if (not is_pixel_random):
            # FRAME RANDOM, PIXEL SEKUENSIAL
            print("frps")
        else:
            # FRAME RANDOM, PIXEL RANDOM
            print("frpr")
elif(mode == 2):
    ## EKSTRAKSI
    
    ## Langsung Ekstraksi aja boi
    print("Extracting")
