"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.hlt = False
        self.sp = 7 

        # self.branchtable = {}
        # self.branchtable[0b10000010] = 
        # self.branchtable[0b01000111] = 
        # self.branchtable[0b00000001] = 

        self.ldi = 0b10000010 
        self.prn = 0b01000111 
        self.halt = 0b00000001
        self.mul = 0b10100010
        self.push = 0b01000101
    
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    
    def load(self, file):
        """Load a program into memory."""

        address = 0


        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        with open(file) as program:
            for instruction in program:
                instruction = int(instruction, 2)
                self.ram[address] = instruction
                address += 1
               


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == self.mul:
            self.register[reg_a] *= self.register[reg_b]
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
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        
        while not self.hlt:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc +1)
            operand_b = self.ram_read(self.pc +2)
        
            if ir == self.ldi:
                self.register[operand_a] = operand_b
                self.pc += 3
            elif ir == self.prn:
                print(self.register[operand_a])
                self.pc += 2
            elif ir == self.mul:
                self.alu(self.mul, operand_a, operand_b)
                self.pc += 3
            elif ir == self.push:
                self.register[self.sp] -= 1
                reg_num = self.ram[self.pc +1]
                val = self.register[reg_num]
                self.ram[self.register[self.sp]] = val
            elif ir == self.halt:
                self.hlt = True
           
           
                
           
           
            