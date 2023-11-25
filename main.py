import time
import numpy as np
import re

# instructions = re.findall('..', '030001010300020102000101020002020601020401010100010a01f511')
rom = ""

def load_instructions_file():
    """Loads an file into ROM."""
    global rom
    with open("data.rom") as file:
        rom = ''.join([re.sub('\s+', '', line) for line in file.readlines()])

load_instructions_file()
print("Loaded ROM: " + rom) # 30 bytes total

instructions = re.findall('..', rom)
print("bROM: " + ';'.join(instructions))

program_counter = 500
instruction_register = 0
eax = 0
ebx = 0
ecx = 0
edx = 0
eex = 0
efx = 0
ram = np.arange(2000)
ram.fill(0)

def load_into_memory():
    """Loads instructions into memory."""
    global eax
    eax = 500
    for instruction in instructions:
        ram[eax] = int(instruction, 16)
        eax += 1
    eax = 0

load_into_memory()

def get_register_value(num):
    """Returns the value of a specific register."""
    global eax, ebx, ecx, edx, eex, efx
    match (num):
        case 1:
            return eax
        case 2:
            return ebx
        case 3:
            return ecx
        case 4:
            return edx
        case 5:
            return eex
        case 6:
            return efx

def set_register(num, value):
    """Sets the value of a specific register."""
    global eax, ebx, ecx, edx, eex, efx
    match (num):
        case 1:
            eax = value
        case 2:
            ebx = value
        case 3:
            ecx = value
        case 4:
            edx = value
        case 5:
            eex = value
        case 6:
            efx = value

def get_memory_from_address(num):
    """Returns the value of a RAM address."""
    return ram[num]

def get_memory_argument():
    """Gets the address that is in the next 2 IBs, returns value of that, and skips count by two."""
    global program_counter
    value = get_memory_from_address(program_counter + 1) + get_memory_from_address(program_counter + 2)
    program_counter += 2
    return int(value)

def get_address_argument():
    """Gets the address *value* in the next 2 IBs and skips count by two."""
    global program_counter
    # ooh, i've been hexed!
    hexed = str(hex(get_memory_from_address(program_counter + 1)))[2:][:2] + str(hex(get_memory_from_address(program_counter + 2)))[2:][:2]
    value = int(hexed, 16)
    program_counter += 2
    return value

def get_next_argument():
    """Gets the next byte and skips count by 1."""
    global program_counter
    value = get_memory_from_address(program_counter + 1)
    program_counter += 1
    return value

def get_register_argument():
    """Gets the register value of the next byte and skips count by 1."""
    global program_counter
    value = get_register_value(get_memory_from_address(program_counter + 1))
    program_counter += 1
    return value

def set_register_argument(value):
    """Sets the register value of the next byte to a memory value and skips count by 3"""
    global program_counter
    register = get_memory_from_address(program_counter + 1)
    value = set_register(register, value)
    program_counter += 1
    return value

running = True
debug = False

def dprint(*values: object) -> None:
    if debug:
        print(*values)

while running:
    dprint([eax, ebx, ram, program_counter])
    instruction_register = get_memory_from_address(program_counter)
    print(program_counter)
    if instruction_register == 0: # noop
        dprint("noop: " + str(program_counter) + "-" + (hex(program_counter)))
        pass
    if instruction_register == 1: # move  register  into address
        address = get_memory_argument()
        register = get_register_argument()
        if address is not None:
            ram[address] = register
    if instruction_register == 2: # move address(v) into register
        address = get_memory_argument()
        set_register_argument(address)
        dprint("store: address: ", address, "eax: ", eax, "ebx: ", ebx)
    if instruction_register == 3: # hotload into address
        address = get_memory_argument()
        value = get_next_argument()
        if address is not None:
            ram[address] = value
    if instruction_register == 4:
        pass
    if instruction_register == 5:
        pass
    if instruction_register == 6: # add register and register together
        original = get_memory_from_address(program_counter + 1)
        first = get_register_argument()
        second = get_register_argument()
        set_register(original, first + second) 
        dprint("added: reg: ", original, "eax: ", first, "ebx: ", second)
    if instruction_register == 7:
        pass
    if instruction_register == 8:
        pass
    if instruction_register == 9:
        pass
    if instruction_register == 10: # GOTO
        address = get_address_argument()
        program_counter = int(address) - 1 # because at the end, program_counter gets incremented by one
    if instruction_register == 11:
        pass
    if instruction_register == 12:
        pass
    if instruction_register == 13:
        pass
    if instruction_register == 14:
        pass
    if instruction_register == 15:
        pass
    if instruction_register == 16:
        pass
    if instruction_register == 17:
        print("exit")
        exit()
    if instruction_register == 18:
        print(get_memory_from_address(get_memory_argument()))
    program_counter += 1
    time.sleep(.1)
