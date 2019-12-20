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
        self.sp = 7
        self.fl = 6

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
                # print("In ram, printed:", self.ram[address])
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.reg[self.fl] = 1
            else:
                self.reg[self.fl] = 0
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
        # Set Stack Pointer
        self.reg[self.sp] = 244
        # Set Flag register
        self.reg[self.fl] = 0
        # Instructions Decoded
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        POP = 0b01000110
        PUSH = 0b01000101
        RET = 0b00010001
        CALL = 0b01010000
        ADD = 0b10100000
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        while running or self.pc < len(self.ram):
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # print('Running ---', IR)
            # print("PC = ", self.pc)
            if IR == JEQ:
                # print("Should be equal if 1:", self.reg[self.fl])
                if self.reg[self.fl] == 1:
                    # print("Jumping to:", self.reg[operand_a])
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            if IR == JNE:
                if self.reg[self.fl] == 0:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            if IR == JMP:
                self.pc = self.reg[operand_a]
            if IR == CMP:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3
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

            if IR == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3

            if IR == HLT:

                running = False
                return exit()

            if IR == POP:

                # Get value at top of stack (it's in the SP register)
                value = self.ram[self.reg[self.sp]]
                # Put that value in selected register
                self.reg[operand_a] = value
                # Increment stack pointer
                self.reg[self.sp] += 1

                self.pc += 2

            if IR == PUSH:
                # Decrement Pointer
                self.reg[self.sp] -= 1
                # The register to look in, is in operand_a
                # Get value in register
                value = self.reg[operand_a]
                # Add to ram at current spot of the stack
                self.ram[self.reg[self.sp]] = value

                self.pc += 2

            if IR == CALL:
                # push address of next instruction to stack
                # Decrement Pointer
                self.reg[self.sp] -= 1
                # Get value of next address of instruction
                value = self.pc + 2
                # Add to ram at current spot of the stack
                self.ram[self.reg[self.sp]] = value
                # Set PC to address stored in register[operand_a]
                self.pc = self.reg[operand_a]

            if IR == RET:
                 # Get value at top of stack (it's in the SP register)
                value = self.ram[self.reg[self.sp]]
                # Increment stack pointer
                self.reg[self.sp] += 1

                # Set PC to value that we popped from the stack
                self.pc = value