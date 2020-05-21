"""CPU functionality."""

import sys


LDI = 0b10000010
PRN = 0b01000111 
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110 

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.hlt = False
        self.sp = 0xF4
     

    
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

        with open(file) as program:     #iterates over the program files that are passed in
            for instruction in program: # intitally instruction looks similar to this '10000010 # LDI R0,8\n' and int() will not work
                instruction = int(instruction.split('#')[0][:-1], 2) #split gets rid of everything from the hash down and ', 2' lets it know that the number is base 2
                self.ram[address] = instruction
                address += 1 

               


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
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
        
        while not self.hlt:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc +1)
            operand_b = self.ram_read(self.pc +2)

            if ir == HLT:
                #stops the program
                self.hlt = True
            elif ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif ir == MUL:
                #pass in the required args to alu for mul to run
                self.alu(MUL, operand_a, operand_b)
                self.pc += 3
            elif ir == PUSH:
                self.sp = self.sp-1
                self.ram[self.sp] = self.reg[operand_a]
                self.pc += 2
            elif ir == POP:
                if self.sp == 0xF4:
                    return 'stack is empty'
                self.reg[operand_a] = self.ram[self.sp]
                self.sp = self.sp + 1
                self.pc += 2
         
           
                
           
           
            