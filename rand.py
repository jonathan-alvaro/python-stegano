import random 


def generate_random_list(key, list_length, frame_size, number_of_frame):
    key.lower()
    random_seed = 0
    for c in key:
        random_seed += ord(c)


    r = random.Random(random_seed)
    result = []
    for i in range(number_of_frame):
        result.append(r.sample(range(frame_size), list_length))
    return result

def generate_random_frames(key, number_of_frames, needed_frames):
    key.lower()
    random_seed = 0
    for c in key:
        random_seed += ord(c)

    r = random.Random(random_seed)
    result = r.sample(range(number_of_frames), number_of_frames)
    return result

#print(generate_random_list('stegano',1, 1000, 5))