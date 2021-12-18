import operator
from functools import reduce

def hex2bin(s):
    b = bin(int(s, 16))[2:]
    return b.zfill(4)


def literal_values(s: str):
    val = ''
    last_group = False
    while not last_group:
        start_bit, packet = s[0], s[1:5]
        val += packet
        last_group = start_bit == '0'
        s = s[5:]

    return int(val, 2), s


with open(r'./input.txt') as f:
    msg = f.readline().strip()

b_msg = ''
for c in msg:
    b_msg += hex2bin(c)


def parse_message(s, vsum=0):
    packet_version = int(s[:3], 2)
    vsum += packet_version
    type_id = int(s[3:6], 2)

    s = s[6:]
    if type_id == 4:  # literal values
        val, s = literal_values(s)
        return s, val, vsum

    length_type_id = s[0]
    if length_type_id == '0':  # next 15 bits
        length_in_bits = int(s[1:16], 2)
        s = s[16:]
        subpackets = s[:length_in_bits]
        subpacket_vals = []
        while subpackets:
            subpackets, subpacket_val, vsum = parse_message(subpackets, vsum)
            subpacket_vals.append(subpacket_val)

        s = s[length_in_bits:]
    else:  # next 11 bits
        num_sub_packets = int(s[1:12], 2)
        s = s[12:]
        subpacket_vals = []
        for i in range(num_sub_packets):
            s, subpacket_val, vsum = parse_message(s, vsum)
            subpacket_vals.append(subpacket_val)

    result = 0
    if type_id == 0:
        result = sum(subpacket_vals)
    elif type_id == 1:
        result = reduce(operator.mul, subpacket_vals)
    elif type_id == 2:
        result = min(subpacket_vals)
    elif type_id == 3:
        result = max(subpacket_vals)
    elif type_id == 5:
        result = int(subpacket_vals[0] > subpacket_vals[1])
    elif type_id == 6:
        result = int(subpacket_vals[0] < subpacket_vals[1])
    elif type_id == 7:
        result = int(subpacket_vals[0] == subpacket_vals[1])

    return s, result, vsum


_, answer2, answer1 = parse_message(b_msg)
print(answer1)
print(answer2)
