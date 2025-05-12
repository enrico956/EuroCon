import sys
import random

def sampling_data(datas, sample_num):
    if sample_num > len(datas):
        # print("Warnings: Sample number is greater than the size of the data list.", file=sys.stderr)
        random.shuffle(datas)
        return datas
    return random.sample(datas, min(len(datas), sample_num))

# # Example usage:
# data_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# sampled_data = sampling_data(data_list, 3)
# print(sampled_data)
