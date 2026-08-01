import time
import os
import visual as visual_lib
from json import load as json_load

"""Von Neumann architecture simulator with visual representation.
This module defines the VonNeuman class, which simulates a simple Von Neumann architecture.
It includes methods for setting up memory, fetching and executing instructions, and handling the clock.
The main function initializes the simulator and runs it with a visual interface.
"""

"""Simulador de arquitectura Von Neumann con representación visual.
Este módulo define la clase VonNeuman, que simula una arquitectura Von Neumann simple.
Incluye métodos para configurar la memoria, obtener y ejecutar instrucciones, y manejar el reloj.
La función principal inicializa el simulador y lo ejecuta con una interfaz visual.
"""

class VonNeuman:
    """A simple Von Neumann architecture simulator.
    Attributes:
        dbus (int): Size of the directory bus in bits.
        memory_bus (int): Size of the memory bus in bits.
        direct_addressing (bool): If True, uses direct addressing mode.
        clock_size (int): Size of the clock in bits.
        clock (int): Current clock value.
        memory (list): List of binary string instructions in memory.
        data_register (list): List of current instruction and its address/data.
        acumulator (int): Accumulator for arithmetic operations.
    Exceptions:
        Missing_Setup_Arguments: Raised when dbus or memory_bus is less than 1
        Missing_Instructions: Raised when no instructions are provided to set_instructions
        End_Of_Memory: Raised when trying to fetch an instruction beyond memory size
        Out_Of_Bounds: Raised when trying to access memory out of its bounds
        Clock_Overload: Raised when the clock exceeds its maximum value
    Methods:
        show_memory(): Returns a formatted string representation of the memory
        tick(): Increments the clock by 1, raises Clock_Overload if max value exceeded
        set_instructions(instructions): Sets the memory with a list of binary string instructions
        next_instruction(): Fetches the next instruction from memory into the data register
        read_memory(address): Reads the instruction at the given memory address
        interpreter(): Interprets the current instruction in the data register
        execute(): Executes the current instruction in the data register
    """
    class Missing_Setup_Arguments(Exception):
        pass

    class Missing_Instructions(Exception):
        pass

    class End_Of_Memory(Exception):
        pass

    class Out_Of_Bounds(Exception):
        pass

    class Clock_Overload(Exception):
        pass

    def __init__(self, dbus: int, mbus: int, direct_addressing=True):
        if dbus < 1 or mbus < 1:
            raise self.Missing_Setup_Arguments("Directory bus and Memory bus must be at least 1 bit")
        
        # Initialize attributes

        self.dbus = dbus
        self.mbus = mbus
        self.direct_addressing = direct_addressing
        self.clock_size = dbus
        self.clock = 0
        self.memory = []
        self.pointer=-1
        self.acumulator = 0
        self.symbol=[]
        self.data_register = []  #ojo, este tiene un trato especial
        self.address_register=0
        self.order_register=0
        self.insert_register=0
        self.speed=1.0
        self.status=''
    
    def show_memory(self) -> list:
        """Returns a formatted string representation of the memory.
        Returns:
            list: List of strings representing the memory state
        """
        memory = list()
        for i in range(len(self.memory)):
            if i == 0:
                memory.append(f"""                ┌──────────┬───────────────────────────┐║║
                    │Direccion │Data                       │║║
                    ├──────────┼───────────────────────────┤║║
                    │ {format(0, f'0{self.clock_size}b')}     │ {self.memory[0]}                  │╝║
                    ├──────────┼───────────────────────────┤ ║""")
            elif i < len(self.memory)-1:
                memory.append(f"""                │ {format(i, f'0{self.clock_size}b')}     │ {self.memory[i]}                  │ ║
                ├──────────┼───────────────────────────┤ ║""")
            else:
                memory.append(f"""                │ {format(i, f'0{self.clock_size}b')}     │ {self.memory[i]}                  │ ║
                └──────────┴───────────────────────────┘ ║""")
        return memory

            
    
    def tick(self) -> None:
        """Increments the clock by 1, raises Clock_Overload if max value exceeded.
        Raises:
            Clock_Overload: If the clock exceeds its maximum value based on clock_size
        """
        if self.clock == int("1"*self.clock_size, 2):
            raise self.Clock_Overload("Clock has reached its maximum value")
        else:
            self.clock += 1

    def set_instructions(self, instructions: list) -> None:
        """Sets the memory with a list of binary string instructions.
        Args:
            instructions (list): List of binary string instructions to load into memory
        Raises:
            Missing_Instructions: If no instructions are provided
        """
        if len(instructions) < 1:
            raise self.Missing_Instructions("No instructions provided")
        else:    
            self.memory = instructions

    
    ##! To be merged with read_memory
    def next_instruction(self) -> None:
        """Fetches the next instruction from memory into the data register.
        Raises:
            End_Of_Memory: If trying to fetch an instruction beyond memory size
        """
        self.pointer+=1
        self.status='fetch  '
        del self.data_register[:]
        self.data_register.append(self.memory[self.pointer])

    
    def read_memory(self, address: int) -> str:
        """Reads the instruction at the given memory address.
        Args:
            address (int): Memory address to read from
        Raises:
            Out_Of_Bounds: If the address is out of memory bounds
        Returns:
            str: The binary string instruction at the given address
        """
        if address >= len(self.memory):
            raise self.Out_Of_Bounds("Address out of memory bounds")
        else:
            return self.memory[address]
        
    def interpreter(self) -> None:
        """Interprets the current instruction in the data register.
        Raises:
            Out_Of_Bounds: If the address/data part of the instruction is out of memory bounds
        """
        self.status='decode '
        instruction = self.data_register[0]
        del self.data_register[0]
        interpretation = ""
        match str(instruction)[:4]:
            case "0000": #ADD
                interpretation = "ADD"
            case "0001": #SUBTRACT
                interpretation = "SUB"
            case "0010": #PRODUCT
                interpretation = "PRD"
            case "0011": #POWER
                interpretation = "PWR"
            case "0100": #AND
                interpretation = "AND"
            case "0101": #OR
                interpretation = "OR"
            case "0110": #MOVE
                interpretation = "MOV"
            case "0111": #HALT
                interpretation = "HAL"
        self.data_register.append(interpretation)
        print("instrucción:",str(instruction)[4:])
        self.data_register.append(str(instruction)[4:])
    
    def execute(self) -> bool:
        """Executes the current instruction in the data register.
        Raises:
            Out_Of_Bounds: If trying to access memory out of its bounds
        Returns:
            bool: True if execution continues, False if HALT instruction is encountered
        """
        self.status='execute'
        if self.data_register[0] == "HAL":
            print("Halting execution")
            return False
        if self.direct_addressing:
            data = int(self.data_register[1], 2)
        else:
            data = int(self.read_memory(int(self.data_register[1], 2)), 2)

        match self.data_register[0]:
            case "ADD":
                self.acumulator += data
            case "SUB":
                self.acumulator -= data
            case "PRD":
                self.acumulator *= data
            case "PWR":
                self.acumulator **= data
            case "AND":
                self.acumulator &= data
            case "OR":
                self.acumulator |= data
            case "MOV":
                self.memory[int(self.data_register[1], 2)] = format(self.acumulator, f"0{self.mbus}b")
                self.acumulator = 0
        #del self.data_register[:]
        return True

def config_pull() -> dict:
    """Pulls configuration parameters from config.json file.
    Returns:
        dict: Configuration parameters as a dictionary
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "..", "config.json")
    with open(config_path, "r") as config_file:
        config = json_load(config_file)
    return config["main"]

CONFIG = config_pull() 

def main() -> int:
    """Main function to run the Von Neumann simulator with visual interface.
    Returns:
        int: Exit code (0 for success)
    """
    global CONFIG
    instructions: list
    instructions = visual_lib.setup()
    VN_machine = setup(4, 8, direct_addressing=False)
    run(VN_machine, instructions, CONFIG["speed"]+0.5) #modificado julio2026

    while True:
        i = input("Press ENTER to exit...")
        if i == "":
            break
        else:
            pass
    return 0

def setup(dbus: int, mbus: int, direct_addressing=True) -> VonNeuman:
    """Sets up the Von Neumann simulator with given parameters.
    Args:
        dbus (int): Size of the directory bus in bits.
        mbus (int): Size of the memory bus in bits.
        direct_addressing (bool, optional): If True, uses direct addressing mode. Defaults to True.
    Returns:
        VN_machine (VonNeuman): Configured Von Neumann simulator instance.
    """
    try:
        VN_machine = VonNeuman(dbus, mbus, direct_addressing)
    except VonNeuman.Missing_Setup_Arguments:
        print("Invalid setup parameters, exiting...")
        ##? Need to define exit codes, but for now just exit with 1 to indicate an error
        exit(1)
    return VN_machine

def run(VN_machine: VonNeuman, instructions: list, speed=1.0)-> None:    
    """Runs the Von Neumann simulator with visual updates.
    Args:
        VN_machine (VonNeuman): The Von Neumann simulator instance.
        instructions (list): List of binary string instructions to load into memory.
        speed (float, optional): Speed of visual updates in seconds. Defaults to 1.0.
    Returns:
        VN_machine (VonNeuman): The Von Neumann simulator instance after execution.
    """
    
    visual_lib.VonNeuman = VN_machine # Link the visual module to the VNeuman instance
    
    try:
        VN_machine.set_instructions(instructions) # Load instructions into memory
    except VonNeuman.Missing_Instructions:
        print("No instructions provided, exiting...") # Exit if no instructions
        ##? Need to define exit codes, but for now just exit with 1 to indicate an error
        exit(1)
    while True:
        fetch1(VN_machine)
        espera()
        VN_machine.tick()  
        fetch2(VN_machine)
        espera()
        VN_machine.tick()  
        decode(VN_machine)
        espera()
        VN_machine.tick()  
        execute(VN_machine)
        if VN_machine.data_register[0]=='HAL':
            print("End of program")
            print()
            ##! To be moved to visual module
            for line in VN_machine.show_memory():
                # Display final memory state
                print(line)
                print()
            break   
        espera()
        VN_machine.tick()   
    return #modificado julio2026


def fetch1(VN_machine: VonNeuman)-> None:   
    VN_machine.next_instruction()  # es la instruccion
    #First, the instruction is fetched from memory
    visual_lib.update_visual_data(VN_machine.speed)
    
def fetch2(VN_machine: VonNeuman)-> None: 
    #nada
    visual_lib.update_visual_data(VN_machine.speed)

def decode(VN_machine: VonNeuman)-> None:
    VN_machine.interpreter() #Then, the instruction is interpreted
    visual_lib.update_visual_data(VN_machine.speed)

def execute(VN_machine: VonNeuman)-> None:   
    if VN_machine.execute(): #Finally, the instruction is executed
        visual_lib.update_visual_data(VN_machine.speed)

def espera() -> None:
    while True:
        i = input("Press ENTER to CONTINUE...")
        if i == "":
            break
        else:
            pass  

if __name__ == "__main__":
    main()

##VINBELT