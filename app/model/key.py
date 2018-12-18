import random

# create_key create 128 bits entropy
def create_entropy():
    hex_str = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    entropy_str = ""
    for _ in range(32):
        # create interger in range [1,15]
        num = random.randint(0,15)
        entropy_str += hex_str[num]
    return entropy_str


# def entropy_to_mnemonic(entropy_str):

#     return mnemonic_str
