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

print(generate_random_list('stegano',1, 1000, 5))