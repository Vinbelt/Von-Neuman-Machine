import os
import time
import main

"""
This module provides a visual simulation of a Von Neumann architecture computer.
It includes functions to set up the simulation, load instructions, and visualize the state of the system.
Global Variables:
    VonNeuman: An instance of the VonNeuman class from the logic module
    address_register: Current address register value (binary string)
    order_register: Current order register value (binary string)
    symbol: List of strings representing the ALU operation symbol
    data_register: Current data register value (binary string)
    insert_register: Current memory insert value (binary string)
Functions:
    setup(): Sets up the simulation environment and loads instructions
    charge(adress, instructions): Loads instructions from a file into the instruction list
    update_visual_data(speed): Updates the visual representation of the system state
    visualize(): Renders the current state of the system to the console
"""

"""
Este módulo proporciona una simulación visual de una computadora con arquitectura Von Neumann.
Incluye funciones para configurar la simulación, cargar instrucciones y visualizar el estado del sistema.
Variables globales:
    VonNeuman: Una instancia de la clase VonNeuman del módulo de lógica
    address_register: Valor actual del registro de dirección (cadena binaria)
    order_register: Valor actual del registro de orden (cadena binaria)
    symbol: Lista de cadenas que representan el símbolo de la operación de la ALU
    data_register: Valor actual del registro de datos (cadena binaria)
    insert_register: Valor actual de inserción en memoria (cadena binaria)
Funciones:
    setup(): Configura el entorno de simulación y carga las instrucciones
    charge(adress, instructions): Carga instrucciones desde un archivo en la lista de instrucciones
    update_visual_data(speed): Actualiza la representación visual del estado del sistema
    visualize(): Renderiza el estado actual del sistema en la consola
"""

address_register = "0000"
order_register = "00000000"
data_register = "00000000"
insert_register = "00000000"
symbol = ["       ", "       ", "       "]
VonNeuman: main.VonNeuman

def setup():
    """Sets up the Von Neumann simulation environment, including loading instructions and configuring the console.
    Returns:
        list: A list containing the instructions for the simulation
    """
    os.system('mode con: cols=90 lines=100')
    instructions = []

    
    while True:
        ##! To get changed into a n-bit mode
        instruction = input("Enter an 8-bit binary instruction (or type 'run' to execute, 'exit' to quit, 'charge' to load from file): ")
        if len(instruction) != 8 or not all(bit in '01' for bit in instruction):
            
            if instruction.lower() == 'run':
                try:
                    os.system('cls' if os.name == 'nt' 
                              else 'clear')
                    return instructions

                except Exception as e:
                    print(f"Error: {e}")
                    instruction = list()
                    print("Restarting instruction input...")
                    continue
            
            elif instruction.lower() == 'exit':
                print("Exiting program...")
                return [] # Returns None to indicate exit
            
            elif instruction.lower() == "charge":
                ##? Needed to insert the input inside function and add error management, but it works
                adress = input("Enter the address of the file: ")
                instructions = charge(adress, instructions)
                print(f"Instructions loaded from {adress}.txt")
                return instructions 
            
            else:
                print("Invalid instruction. Please enter an 8-bit binary number.")
                continue
        
        instructions.append(instruction)

def charge(adress:str, instructions = list()):
    ##! To be changed as refered in line 81
    """Loads instructions from a specified file into the instruction list.
    Args:
        adress (str): The base name of the file (without .txt extension)
        instructions (list, optional): The list to append instructions to. Defaults to an empty list.
    Returns:
        list: The updated list of instructions
    """
    with open(f"{adress}.txt", "r") as f:
        for line in f:
            instructions.append(line.strip())
    return instructions[::-1]


def update_visual_data(speed=1.0):
    ##! Confusing name, to be changed
    """Updates the visual representation of the Von Neumann architecture state.
    Args:
        speed (float, optional): Delay time in seconds for visualization updates. Defaults to 1.0.
    """

    global VonNeuman
    global address_register
    global order_register
    global symbol
    global data_register
    global insert_register

    
    if len(VonNeuman.data_register) > 1:
        match VonNeuman.data_register[0]:
            case "ADD":
                symbol = [
                    "   │   ",
                    "───┼───",
                    "   │   "
                    ]
            case "SUB":
                symbol = [
                    "       ",
                    "───────",
                    "       "
                    ]
            case "PRD":
                symbol = [
                    r"  \ /  ",
                    r"   X   ",
                    r"  / \  "
                    ]
            case "PWR":
                symbol = [
                    r"  / \  "
                    r" /   \ "
                    "/     \\"
                    ]
            case "AND":
                symbol = [
                    " ┌───┐ ",
                    "─┤AND├─",
                    " └───┘ "
                    ]
            case "OR":
                symbol = [
                    " ┌───┐ ",
                    "─┤OR ├─",
                    " └───┘ "
                    ]
            case "MOV":
                symbol= [
                    r"|\   /|",
                    r"| \ / |",
                    r"|     |"
                ]
            case "HAL":
                symbol = [
                    "       ",
                    "HALT···",
                    "       "
                ]

        address_register = VonNeuman.data_register[1]

    elif len(VonNeuman.data_register) == 1:
        order_register = VonNeuman.data_register[0]
        data_register = VonNeuman.data_register[0]

    visualize()
    
    if len(VonNeuman.data_register) > 1 and VonNeuman.data_register[0] != "HAL":
        time.sleep(0.4)
        try:
            insert_register = VonNeuman.memory[int(VonNeuman.read_memory(int(VonNeuman.data_register[1], 2)), 2)]
        except Exception:
            insert_register = "ERR     "
        visualize()
    else:
        visualize()


def visualize():
    """Renders the current state of the Von Neumann architecture to the console.
    """
    global VonNeuman
    global address_register
    global order_register
    global symbol
    global data_register
    global insert_register

    os.system('cls' if os.name == 'nt' 
            else 'clear')
    try:
        print(int(VonNeuman.read_memory(int(VonNeuman.data_register[1], 2)), 2))
    except Exception:
        pass
    
    MAIN_INTEFACE = f"""
    Unidad de Control (APU)                    Unidad Aritmético Lógica (ALU)
    ╔═════════════════════════════════════╗   ╔══════════════════════════════════════╗
    ║   ╔═══════╗ Reloj ╔═«════════╗      ║   ║ ╔════════════╗                       ║
    ║   ║{symbol[0]}║       █ ║  {format(VonNeuman.clock, f'0{VonNeuman.directory_bus}b')}   «═╗   ║   ║ ║            ║                       ║
    ║   ║{symbol[1]}«══╗    ╚═»════════╝  ║   ║   ║ ║        /───^────────────\\          ║
    ║   ║{symbol[2]}║  ║    ╔══════════╗  ║   ║   ║ ║       /                  \\         ║
    ║   ╚═══════╝  ╠════« {order_register} «══║═════╗ ║ ║      /                    \\        ║
    ║   Decodif.   ║    ╚══════════╝  ║   ║ ║ ║ ║     /__________/\\__________\\       ║
    ║              ║    R.Instruccins.║   ║ ║ ║ ║     | {format(VonNeuman.acumulator, f'0{VonNeuman.memory_bus}b')} || {insert_register} |       ║
    ╚══════════════║══════════════════║═══╝ ║ ║ ║     └─^────────┘└─^────────┘       ║
                   ║                  ║     ║ ║ ╠═══════╝           ║                ║
                   ╠══════════════════╝     ║ ╚═║═══════════════════║════════════════╝
                   ║                        ║   ║                   ║
                  ╔╝                        ╚═══╣                   ║
                ╔═║═════════════════════════════║═══════════╗       ║
                ║ ║╔══════════╗                ╔^═════════╗ ║       ║
                ║ ╚» {address_register}     »═╗            ╔═» {data_register} »═════════╝
                ║  ╚══════════╝ ║            ║ ╚══════════╝ ║
                ║  R.Dirección  ║            ║ R.Datos      ║
                ║ ╔═════════════╝            ╚═════════════╗║
                ║ ║┌──────────┬───────────────────────────┐║║
                ║ ║│Direccion │Data                       │║║
                ║ ║├──────────┼───────────────────────────┤║║
                ║ ╚│ {format(0, f'0{VonNeuman.clock_size}b')}     │ {VonNeuman.memory[0]}                  │╝║
                ║  ├──────────┼───────────────────────────┤ ║"""
    
    
    print(MAIN_INTEFACE)

    for n in range(1, len(VonNeuman.memory)):
        if n < len(VonNeuman.memory) - 1:
            print(f"""                ║  │ {format(n, f'0{VonNeuman.clock_size}b')}     │ {VonNeuman.memory[n]}                  │ ║
                ║  ├──────────┼───────────────────────────┤ ║""")
        if n == len(VonNeuman.memory) - 1:
            print(f"""                ║  │ {format(n, f'0{VonNeuman.clock_size}b')}     │ {VonNeuman.memory[n]}                  │ ║
                ║  └──────────────────────────────────────┘ ║
                ╚═══════════════════════════════════════════╝""")

##VINBELT