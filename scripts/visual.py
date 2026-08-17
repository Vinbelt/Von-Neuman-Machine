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
    os.system('cls' if os.name == 'nt' 
            else 'clear')
    
    while True:
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
    """Loads instructions from a specified file into the instruction list.
    Args:
        adress (str): The base name of the file
        instructions (list, optional): The list to append instructions to. Defaults to an empty list.
    Returns:
        list: The updated list of instructions
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "../others", adress)
    with open(f"{config_path}", "r") as f:
        for line in f:
            instructions.append(line.strip())
    return instructions


def update_visual_data(speed=1.0):
    """Renders the current state of the Von Neumann architecture to the console.
    """
    global VonNeuman
    os.system('cls' if os.name == 'nt' 
            else 'clear')
    
    MAIN_INTERFACE = f"""
    Unidad de Control (APU)                    Unidad Aritmético Lógica (ALU)
    ╔═════════════════════════════════════╗   ╔══════════════════════════════════════╗
    ║              Inst:╔══════════╗      ║   ║ ╔════════════╗                       ║
    ║   ╔═══════╗  ╔════╣  {format(VonNeuman.pointer, f'0{VonNeuman.dbus}b').center(8)}║      ║   ║ ║            ║                       ║
    ║   ║{VonNeuman.symbol[0]}║  ║    ║  {VonNeuman.status.center(7)} ║      ║   ║ ║            ║                       ║
    ║   ║{VonNeuman.symbol[1]}«══╣    ╚══════════╝      ║   ║ ║        /───^────────────\\          ║
    ║   ║{VonNeuman.symbol[2]}║  ║    ╔══════════╗      ║   ║ ║       /      A L U       \\         ║
    ║   ╚═══════╝  ╠════« {VonNeuman.order_register.center(8)} «════════╗ ║ ║      /                    \\        ║
    ║   Decodif.   ║    ╚══════════╝      ║ ║ ║ ║     /__________/\\__________\\       ║
    ║              ║    R.Instruccins.    ║ ║ ║ ║     | {format(VonNeuman.acumulator, f'0{VonNeuman.mbus}b')} || {VonNeuman.insert_register} |       ║
    ╚══════════════║══════════════════ ═══╝ ║ ║ ║     └─^────────┘└─^────────┘       ║
    clock:         ║                        ║ ║ ╠═══════╝           ║                ║
    ╔══════════╗   ║                        ║ ╚═║═══════════════════║════════════════╝
    ║ {format(VonNeuman.clock, f'04d')}     ║   ║                        ║   ║                   ║
    ╚══════════╝  ╔╝                        ╚═══╣                   ║
                ╔═║═════════════════════════════║═══════════╗       ║
                ║ ║╔══════════╗                ╔══════════╗ ║       ║
                ║ ╚» {VonNeuman.address_register.center(8)} »═╗            ╔═» {VonNeuman.data_reg.center(8)} »═════════╝
                ║  ╚══════════╝ ║            ║ ╚══════════╝ ║
                ║  R.Dirección  ║            ║ R.Datos      ║
                ║ ╔═════════════╝            ╚═════════════╗║
                ║ ║┌──────────┬───────────────────────────┐║║
                ║ ║│Direccion │Data                       │║║
                ║ ║├──────────┼───────────────────────────┤║║  """
 
        
    print(MAIN_INTERFACE)
    
    k=int(VonNeuman.address_register,2)
    for n in range(0, len(VonNeuman.memory)):
        if n==k:
            if (VonNeuman.status=="execute" or VonNeuman.status=="decode") and VonNeuman.data_register[1]=="MOV":
                print(f"""                ║ ╠│{"\033[41m"} {format(n, f'0{VonNeuman.dbus}b')}     {"\033[0m"}│ {"\033[41m"+VonNeuman.memory[n]+"\033[0m"}                  │╣║ """)           
            else:
                print(f"""                ║ ╠│{"\033[42m"} {format(n, f'0{VonNeuman.dbus}b')}     {"\033[0m"}│ {"\033[42m"+VonNeuman.memory[n]+"\033[0m"}                  │╣║ """)           
        else:    
            print(f"""                ║ ╠│ {format(n, f'0{VonNeuman.dbus}b')}     │ {VonNeuman.memory[n]}                  │╣║ """)
        if n < len(VonNeuman.memory) - 1:
            print(f"""                ║ ║├──────────┼───────────────────────────┤║║""")
        if n == len(VonNeuman.memory) - 1:
            print(f"""                ║  └──────────────────────────────────────┘ ║
                ╚═══════════════════════════════════════════╝""")

    time.sleep(speed)            


##VINBELT