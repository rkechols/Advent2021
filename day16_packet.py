import os

from constants import INPUTS_DIR, UTF_8


INPUT_FILE = os.path.join(INPUTS_DIR, "input16.txt")


class Decoder:
    def __init__(self, bits: str):
        self.bits = bits
        self.index = 0
        self.version_numbers = list()

    def parse_version(self) -> int:
        version_bin = self.bits[self.index:(self.index + 3)]
        self.index += 3
        version = int(version_bin, base=2)

        self.version_numbers.append(version)

        return version

    def parse_type_id(self) -> int:
        type_id_bin = self.bits[self.index:(self.index + 3)]
        self.index += 3
        type_id = int(type_id_bin, base=2)
        return type_id

    def parse_literal(self) -> int:
        this_number_bits = list()
        while self.bits[self.index] == "1":
            self.index += 1  # move past the 1
            bit_block = self.bits[self.index:(self.index + 4)]
            this_number_bits.append(bit_block)
            self.index += 4  # move past the block
        self.index += 1  # move past the 0
        bit_block = self.bits[self.index:(self.index + 4)]
        this_number_bits.append(bit_block)
        self.index += 4  # move past the block
        # convert to decimal
        this_number = int("".join(this_number_bits), base=2)
        return this_number

    def parse_packet(self):  # START
        version = self.parse_version()
        type_id = self.parse_type_id()
        if type_id == 4:  # literal
            value = self.parse_literal()
        else:  # operator
            length_type_id = self.bits[self.index]
            self.index += 1
            sub_packets = list()  # TODO?
            if length_type_id == "0":
                bit_block = self.bits[self.index:(self.index + 15)]
                self.index += 15
                length_in_bits = int(bit_block, base=2)
                end_index = self.index + length_in_bits
                while self.index < end_index:
                    self.parse_packet()  # TODO?
            else:
                bit_block = self.bits[self.index:(self.index + 11)]
                self.index += 11
                n_sub_packets = int(bit_block, base=2)
                for _ in range(n_sub_packets):
                    self.parse_packet()  # TODO?


if __name__ == "__main__":
    bits_ = list()
    with open(INPUT_FILE, "r", encoding=UTF_8) as f:
        for line_ in f:
            line = line_.strip()
            for char in line:
                dec = int(char, base=16)
                binary = format(dec, "04b")
                bits_.extend(list(binary))
    # part 1
    decoder = Decoder("".join(bits_))
    decoder.parse_packet()
    version_sum = sum(decoder.version_numbers)
    print(f"SUM of version numbers: {version_sum}")
