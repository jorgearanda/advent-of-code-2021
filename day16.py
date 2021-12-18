from loader import load_strs
from math import prod

class Packet:
    def __init__(self, binary):
        self.version = int(binary[:3], 2)
        self.type = int(binary[3:6], 2)
        self.subpackets = []
        if self.type == 4:
            self.value, self.bits_parsed = self.get_literal_value(binary[6:])
        elif binary[6] == "0":
            self.length_type = 0
            self.subpackets_length = int(binary[7:22], 2)
            self.subpackets_binary = binary[22 : 22 + self.subpackets_length]
            while len(self.subpackets_binary) > 0:
                self.subpackets.append(Packet(self.subpackets_binary))
                self.subpackets_binary = self.subpackets_binary[
                    self.subpackets[-1].bits_parsed :
                ]
            self.bits_parsed = 22 + self.subpackets_length
        else:
            self.length_type = 1
            self.subpackets_length = int(binary[7:18], 2)
            self.subpackets_binary = binary[18:]
            while len(self.subpackets) < self.subpackets_length:
                self.subpackets.append(Packet(self.subpackets_binary))
                self.subpackets_binary = self.subpackets_binary[
                    self.subpackets[-1].bits_parsed :
                ]
            self.bits_parsed = 18 + sum(
                subpacket.bits_parsed for subpacket in self.subpackets
            )

        match self.type:
            case 0:
                self.value = sum(packet.value for packet in self.subpackets)
            case 1:
                self.value = prod(packet.value for packet in self.subpackets)
            case 2:
                self.value = min(packet.value for packet in self.subpackets)
            case 3:
                self.value = max(packet.value for packet in self.subpackets)
            case 4:
                pass  # covered above
            case 5:
                self.value = 1 if self.subpackets[0].value > self.subpackets[1].value else 0
            case 6:
                self.value = 1 if self.subpackets[0].value < self.subpackets[1].value else 0
            case 7:
                self.value = 1 if self.subpackets[0].value == self.subpackets[1].value else 0

    def get_literal_value(self, binary):
        bin_value = ""
        parsed = 6
        while True:
            bin_value += binary[1:5]
            parsed += 5
            if binary[0] == "0":
                break
            binary = binary[5:]

        return int(bin_value, 2), parsed

    def version_sum(self):
        return self.version + sum(packet.version_sum() for packet in self.subpackets)


def binary_from_hex(hex):
    encode = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111",
    }
    return "".join(encode[char] for char in hex)


if __name__ == "__main__":
    data = load_strs("inputs/day16.txt")[0]
    packet = Packet(binary_from_hex(data))
    print(f"Part 1: {packet.version_sum()}")
    print(f"Part 2: {packet.value}")

# -- Tests --
def test_binary_from_hex():
    assert binary_from_hex("D2FE28") == "110100101111111000101000"
    assert (
        binary_from_hex("38006F45291200")
        == "00111000000000000110111101000101001010010001001000000000"
    )
    assert binary_from_hex("6") == "0110"


def test_literal_value():
    assert Packet("110100101111111000101000").value == 2021


def test_operator_with_length_type_0():
    packet = Packet(binary_from_hex("38006F45291200"))
    assert packet.subpackets[0].value == 10
    assert packet.subpackets[1].value == 20


def test_operator_with_length_type_1():
    packet = Packet(binary_from_hex("EE00D40C823060"))
    assert packet.subpackets[0].value == 1
    assert packet.subpackets[1].value == 2
    assert packet.subpackets[2].value == 3


def test_version_sums():
    assert Packet(binary_from_hex("8A004A801A8002F478")).version_sum() == 16
    assert Packet(binary_from_hex("620080001611562C8802118E34")).version_sum() == 12
    assert Packet(binary_from_hex("C0015000016115A2E0802F182340")).version_sum() == 23
    assert Packet(binary_from_hex("A0016C880162017C3686B18A3D4780")).version_sum() == 31


def test_part_2():
    assert Packet(binary_from_hex("C200B40A82")).value == 3
    assert Packet(binary_from_hex("04005AC33890")).value == 54
    assert Packet(binary_from_hex("880086C3E88112")).value == 7
    assert Packet(binary_from_hex("CE00C43D881120")).value == 9
    assert Packet(binary_from_hex("D8005AC2A8F0")).value == 1
    assert Packet(binary_from_hex("F600BC2D8F")).value == 0
    assert Packet(binary_from_hex("9C005AC2F8F0")).value == 0
    assert Packet(binary_from_hex("9C0141080250320F1802104A08")).value == 1
