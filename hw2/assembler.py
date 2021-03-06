#Creating dictionary of opcodes to respective numeric opcodes
OPCODES = {'HALT':0, 'PUSH':1, 'RVALUE':2, 'LVALUE':3, 'POP':4, 'STO':5, 'COPY':6, 'ADD':7, 'SUB':8, 'MPY':9, 'DIV':10, 'MOD':11, 'NEG':12, 'NOT':13, 'OR':14, 'AND':15,
           'EQ':16, 'NE':17, 'GT':18, 'GE':19, 'LT':20, 'LE':21, 'LABEL':22, 'GOTO':23, 'GOFALSE':24, 'GOTRUE':25, 'PRINT':26, 'READ':27, 'GOSUB':28, 'RET':29}


# 2 256KB memories for code and data
MAX_ADDRESS = 65,535

class TwoPassAssembler:
  def __init__(self):
    self.symbolTable = {}
    self.dataCounter = 0
    self.codeCounter = 0
    self.codeInstruction = []
    self.originalSymbols = []
    self.binaryInstruction= []

  def firstPass(self, dataList, codeList): # fills in symbol table to be used in secondPass
    #initialize symbpl with data section 
    for data in dataList:
      self.symbolTable[data[0].replace(':', '') ] = {'address': self.dataCounter, 'symbolType': 'Int' }
      self.dataCounter+=1
    #Now we can go through code in our first pass to find any Labels
    for code in codeList:
      if(code[0] == 'LABEL' ): # We have arrived at label definition that needs to be added
        self.symbolTable[code[1]]= {'address': self.codeCounter, 'symbolType': 'Code' }
      self.codeCounter+=1 # increment to keep track of code address line
      
  def secondPass(self, codeList): # replace symbols with address
    for code in codeList:
      if(len(code) > 1 and code[0] != 'Section'): # check if there is a second argument (operand)
        if(not code[1].isnumeric() ): # found a symbol that needs to be replaced with address from symbol table
          self.originalSymbols.append(code[1])
          code[1] = self.symbolTable[code[1]]['address']
    #all symbols replaced with address
    self.codeInstruction=codeList

    # Bits 32-21 are ignored (in practice, filled with zeros),
    # Bits 20-16 hold the opcode, 
    # Bits 15-0 hold the operand.
    # 0000 0000 0000 0000
    # ign  opCo  operand
    # 0x 0000
    # BigEndian  binary code format
  def getBinary(self):
    opCodeByte = 0x00
    operandByte = 0x00

    for code in self.codeInstruction:
      opCodeByte = 0x00
      operandByte = 0x00
      if(not code[0] == 'Section'):
        opCodeByte = OPCODES[code[0]] * 0x10000 # get numeric op code and multiply by 64 to shift bytes over
        # print(code[0],", opcode: ", hex(OPCODES[code[0]]))
        if(len(code) > 1):  # check if there is a second argument (operand)
          if(type(code[1])== 'Int'):
            operandByte=(int(code[1]))
          else:
            operandByte= int(code[1]) #get operand 
        #   print("Operand: ", hex(operandByte))
        
       
        finalIntsruct= opCodeByte+operandByte
        # print('Final  Intruct: ',hex(finalIntsruct))
        self.binaryInstruction.append(finalIntsruct) # adding current binary to list of instructions
        # self.binaryInstruction.append(opCodeByte) # adding current binary to list of instructions
        # self.binaryInstruction.append(operandByte) # adding current binary to list of instructions

  def outputBinary(self, originialCode):
    spacing=15
    innerSpace=8
    combinedInstructions= bytearray(0x00 for i in range(len(self.binaryInstruction)*4)) # combine List of instuction in a single line of bytes
    for i in range(len(self.binaryInstruction)): #fill in every 4bytes sections
      ############# Printing formating, not important #################
      spacer=""
      neededSpacing=innerSpace-len(str(originialCode[i+1][0]))
      for space in range(neededSpacing):
        spacer+=" "
      if(len(originialCode[i+1])>1):
        formattedString= str(originialCode[i+1][0])+ spacer +str(originialCode[i+1][1])
      else:
        formattedString= str(originialCode[i+1][0])
      neededSpace=spacing-len(formattedString)
      for space in range(neededSpace):
          if(len(formattedString)<8):
            formattedString+=(" ")
          else:
            formattedString+=(".")
      print(formattedString,self.binaryInstruction[i].to_bytes(4, byteorder='big'))
      #################################################################

      #writing bigendian binary to bytearray to be written to file
      combinedInstructions[i*4:i*4+4]= self.binaryInstruction[i].to_bytes(4, byteorder='big') # convert byte to big endian
    
    # print(combinedInstructions)
    outputFile = open('a.bin', 'wb')
    outputFile.write(combinedInstructions)
    outputFile.close()
    print("Wrote binary in a.bin")


      
      

# Ask user what file to read from, If not specified, will read from simple.asm
fileName= input('Enter asm file name:\n')
if len(fileName) == 0:
  fileName='simple.asm'
inFile = open(fileName, 'r')
asmLines= inFile.readlines()
inFile.close()
print('Creating binary for input assembly file:',fileName)
#Seperate sections into code and data arrays for TwoPassAssembler to use
dataSection=[]
codeSection=[]
codePortion=False
for i in range(len(asmLines)):
  if(i!=0 and not codePortion): # Skip first line and as long as not in code section, copy into sectionData
      if (asmLines[i].split() == ['Section', '.code'] ): # If going into code section, change codePortion to true
        codePortion = True
      else:
        dataSection.append(asmLines[i].split())
  else: #Copying code section into into codeSection array
      codeSection.append(asmLines[i].split())

#Ready to use TPA
tpa = TwoPassAssembler()

tpa.firstPass(dataSection, codeSection)
tpa.secondPass(codeSection)
tpa.getBinary()
tpa.outputBinary(codeSection)



