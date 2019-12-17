"""CPU functionality."""

import sys
# print(sys.argv)

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 255
        self.pc = 0
        self.reg = [0] * 8

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR_value, MDR_address):
        self.ram[MDR_address] = MDR_value
        return self.ram[MDR_address]

    def load(self):
        """Load a program into memory."""
        # Get File name
        filename = sys.argv[1]
        address = 0

        with open(filename) as f:
            for line in f:
                n = line.split("#")
                n[0] = n[0].strip()

                if n[0] == '':
                    continue

                val = int(n[0], 2)
                self.ram[address] = val
                print("In ram, printed:", self.ram[address])
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
             self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        # Instructions Decoded
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010

        while running or self.pc < len(self.ram):
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            print('Running CPU-RUN')
            if IR == LDI:

                # Now put value in correct register
                self.reg[operand_a] = operand_b
                self.pc += 3

            if IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2

            if IR == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            if IR == HLT:

                running = False
                return exit()

