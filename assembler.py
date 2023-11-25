byte = ""

def register_to_byte(register: str):
    match (register):
        case "eax":
            return "0" + "1"
        case "ebx":
            return "0" + "2"
        case "ecx":
            return "0" + "3"
        case "edx":
            return "0" + "4"
        case "eex":
            return "0" + "5"
        case "efx":
            return "0" + "6"

with open("rom.code") as file:
    headers = {}
    for line in file.readlines():
        args = line.strip().split(" ")
        command = args.pop(0)
        current_byte = 500
        if command.startswith(";"):
            continue
        if command.endswith(":"):
            headers[command[:-1]] = (current_byte, 123)
            continue

        if command == "noop": # noop
            byte += "00"
            current_byte += 1
        if command == "store": # move  register  into address
            byte += "01"
            byte += register_to_byte(args[0])
            byte += args[1]
            current_byte += 4
        if command == "mov": # move address(v) into register
            byte += "02"
            byte += args[0]
            byte += register_to_byte(args[1])
            current_byte += 4
        if command == "set": # hotload into address
            byte += "03"
            byte += args[0]
            byte += args[1]
            current_byte += 4
        if command == 4:
            pass
        if command == 5:
            pass
        if command == "add": # add register and register together
            byte += "06"
            byte += register_to_byte(args[0])
            byte += register_to_byte(args[1])
            current_byte += 3
        if command == 7:
            pass
        if command == 8:
            pass
        if command == 9:
            pass
        if command == "goto": # GOTO
            header_name = args[0]
            if header_name not in headers:
                print("Invalid header name: " + header_name)
                exit(1)
            else:
                byte += "0a"
                byte += "0" + hex(headers.get(args[0])[0])[2:]
                current_byte += 3
        if command == 11:
            pass
        if command == 12:
            pass
        if command == 13:
            pass
        if command == 14:
            pass
        if command == 15:
            pass
        if command == 16:
            pass
        if command == "exit": # exit
            byte += "11"
            if len(args) > 0:
                byte += args[0]
            else:
                byte += "00"
            current_byte += 2
        if command == "dout":
            byte += "12"
            byte += args[0]
            current_byte += 2

print(byte)