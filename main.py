from VideoIO import *
import math

# Accept video,stegano-video frame list. Also need the list of encrypted frame (index) as encrypted_index
def video_psnr (video1_frame_list, video2_frame_list, encrypted_index):
    psnr_list = []
    for i in encrypted_index:
        video1_pixels = video1_frame_list[i].pixels
        video2_pixels = video2_frame_list[i].pixels

        m = len(video1_pixels)
        n = len(video1_pixels[0])
        diff_sum = 0
        for j in range (m):
            for k in range (n):
                diff_r = video1_pixels[j][k][0] - video2_pixels[j][k][0]
                diff_g = video1_pixels[j][k][1] - video2_pixels[j][k][1]
                diff_b = video1_pixels[j][k][2] - video2_pixels[j][k][2]
                diff_sum = diff_sum + (diff_r+diff_g+diff_b)**2

        rms = math.sqrt(diff_sum/(m*n))
        if rms == 0:
            psnr = 0
        else:
            psnr = 20 * math.log10(256/rms)

        psnr_list.append(0)
    return sum(psnr_list)/len(psnr_list)

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
frame_list.append(video_frame)
video_frame = video_file.get_frame()
frame_list.append(video_frame)
video_frame = video_file.get_frame()
frame_list.append(video_frame)

# while video_frame:
#     frame_list.append(video_frame)
#     video_frame = video_file.get_frame()

print (video_psnr(frame_list,frame_list))
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
