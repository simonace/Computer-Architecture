ADD_OP_DELAY = 2
MUL_OP_DELAY = 6

class ReservationStationEntry(object):
    def __init__(self, op, vj, vk, qj, qk):
        self.op = op
        self.vj = vj
        self.vk = vk
        self.qj = qj
        self.qk = qk
        if self.op == "add":
            self.opDelay = ADD_OP_DELAY
        elif self.op == "mul":
            self.opDelay = MUL_OP_DELAY
        self.finished = False
        self.result = 0

    def cal(self):
        if self.op == "add":
            return self.vj + self.vk
        elif self.op == "mul":
            return self.vj * self.vk
        

class SimpleTomasuloEmulator(object):

    def __init__(self, codeSeq=[]):
        self.codeSeq = codeSeq
        self.reservationStations = {}
        self.addOpIndex = 1
        self.mulOpIndex = 1
        self.regStatus = {"r1" : "0",
                          "r2" : "0",
                          "r3" : "0",
                          "r4" : "0",
                          "r5" : "0",
                          "r6" : "0",
                          "r7" : "0"}
        self.regValue =  {"r1" : 1,
                          "r2" : 2,
                          "r3" : 3,
                          "r4" : 4,
                          "r5" : 5,
                          "r6" : 6,
                          "r7" : 7 }
        self.regIdealValue = self.regValue.copy()

    def decode(self, code):
        opcode, operands = code.replace('\n', '').split(' ')
        dst, operand1, operand2 = operands.split(',')
        return (opcode.lower(), dst, operand1, operand2)

    def idealCalculate(self, code):
        opcode, operands = code.replace('\n', '').split(' ')
        dst, operand1, operand2 = operands.split(',')
        if opcode.lower() == "add":
            self.regIdealValue[dst] = self.regIdealValue[operand1] + self.regIdealValue[operand2]
        elif opcode.lower() == "mul":
            self.regIdealValue[dst] = self.regIdealValue[operand1] * self.regIdealValue[operand2]
        

    def issue(self, decodedTuple):
        opcode = decodedTuple[0]
        dst = decodedTuple[1]
        op1 = decodedTuple[2]
        op2 = decodedTuple[3]
        if opcode == "add":
            entryName = "add" + str(self.addOpIndex)
            self.addOpIndex = self.addOpIndex + 1
        elif opcode == "mul":
            entryName = "mul" + str(self.mulOpIndex)
            self.mulOpIndex = self.mulOpIndex + 1
        self.regStatus[dst] = entryName
        self.reservationStations[entryName] = ReservationStationEntry(op=opcode, vj=self.regValue[op1], vk=self.regValue[op2], qj=self.regStatus[op1], qk=self.regStatus[op2])

    def writeRegFile(self, entryName, result):
        for reg, status in self.regStatus.items():
            if status == entryName:
                self.regValue[reg] = result
                self.regStatus[reg] = "0"

    def writeReservationStations(self, entryName, result):
        for name, entry in self.reservationStations.items():
            if entry.qj == entryName:
                entry.vj = result
                entry.qj = "0"
            if entry.qk == entryName:
                entry.vk = result
                entry.qk = "0"

    def regResultCheck(self):
        hasMismatch = False
        print("Compare register file values with golden result:\n")
        for reg, value in self.regValue.items():
            if self.regIdealValue[reg] != value:
                print("ERROR: " +reg + " has value " + str(value) + ", differs from the ideal value of " + str(self.regIdealValue[reg]) + '.\n')
            else:
                print(reg + " has value " + str(value) + ", matches the ideal value.\n")
        if hasMismatch:
            print("Register file value check failed!")
        else:
            print("Register file value check passed!")

    def run(self):
        cycle = 1
        while(len(self.codeSeq)>0 or len(self.reservationStations)>0):
            if len(self.codeSeq)>0:
                fetchCode = self.codeSeq.pop(0)
                self.idealCalculate(fetchCode)
                self.issue(self.decode(fetchCode))
            for name, entry in self.reservationStations.items():
                if entry.qj=="0" and entry.qk=="0":
                    if entry.opDelay==0:
                        self.writeRegFile(name, entry.cal())
                        self.writeReservationStations(name, entry.cal())
                        entry.finished = True
                    else:
                        entry.opDelay = entry.opDelay - 1
            print(("Cycle: " + str(cycle)).ljust(80) + "\n")
            print('='*80 + '\n')
            print("Name".ljust(10) + "Finished".ljust(10) + "Op".ljust(10) + "Vj".ljust(10) + "Vk".ljust(10) + "Qj".ljust(10) + "Qk".ljust(10) + "Op Delay".ljust(10) + '\n')
            for name, entry in self.reservationStations.items():
                print(name.ljust(10) + str(entry.finished).ljust(10) + entry.op.ljust(10) + str(entry.vj).ljust(10) + str(entry.vk).ljust(10) + entry.qj.ljust(10) + entry.qk.ljust(10) + str(entry.opDelay).ljust(10) + '\n')
            print('='*80 + '\n'*2)
            cycle = cycle + 1
            tempD = dict(self.reservationStations)
            for name, entry in self.reservationStations.items():
                if entry.finished:
                    del tempD[name]
            self.reservationStations = dict(tempD)
        self.regResultCheck()
        
   

if __name__ == "__main__":
    f = open("code.txt", "r")
    tomasulo = SimpleTomasuloEmulator(f.readlines())
    tomasulo.run()
    f.close()
    
    
