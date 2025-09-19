import time
import visual as visuallib

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
        directory_bus (int): Size of the directory bus in bits.
        memory_bus (int): Size of the memory bus in bits.
        direct_addressing (bool): If True, uses direct addressing mode.
        clock_size (int): Size of the clock in bits.
        clock (int): Current clock value.
        memory (list): List of binary string instructions in memory.
        data_register (list): List of current instruction and its address/data.
        acumulator (int): Accumulator for arithmetic operations.
    Exceptions:
        Missing_Setup_Arguments: Raised when directory_bus or memory_bus is less than 1
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

        self.directory_bus = dbus
        self.memory_bus = mbus
        self.direct_addressing = direct_addressing
        self.clock_size = dbus
        self.clock = 0
        self.memory = []
        self.data_register = []
        self.acumulator = 0
    
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

    def next_instruction(self) -> None:
        """Fetches the next instruction from memory into the data register.
        Raises:
            End_Of_Memory: If trying to fetch an instruction beyond memory size
        """
        if self.clock > len(self.memory):
            raise self.End_Of_Memory("No more instructions in memory")
        else:
            self. data_register.append(self.memory[self.clock])
    
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
        print(str(instruction)[4:])
        self.data_register.append(str(instruction)[4:])
    
    def execute(self) -> bool:
        """Executes the current instruction in the data register.
        Raises:
            Out_Of_Bounds: If trying to access memory out of its bounds
        Returns:
            bool: True if execution continues, False if HALT instruction is encountered
        """
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
                self.memory[int(self.data_register[1], 2)] = format(self.acumulator, f"0{self.memory_bus}b")
                self.acumulator = 0
        del self.data_register[:]
        return True
        

def main() -> int:
    """Main function to run the Von Neumann simulator with visual interface.
    Returns:
        int: Exit code (0 for success)
    """
    instructions:list
    instructions, speed = visuallib.setup()
    if speed is None:
        print("No instructions provided, exiting...")
        return 0
    vn = setup(4, 8, direct_addressing=False)
    vn = run(vn, instructions, speed+0.5) # Speed + 0.5 to ensure visual updates are noticeable

    while True:
        i = input("Press ENTER to exit...")
        if i == "":
            break
        else:
            pass
    return 0

def setup(directory_bus: int, memory_bus: int, direct_addressing=True) -> VonNeuman:
    """Sets up the Von Neumann simulator with given parameters.
    Args:
        directory_bus (int): Size of the directory bus in bits.
        memory_bus (int): Size of the memory bus in bits.
        direct_addressing (bool, optional): If True, uses direct addressing mode. Defaults to True.
    Returns:
        VNeuman: Configured Von Neumann simulator instance.
    """
    vneuman = VonNeuman(directory_bus, memory_bus, direct_addressing)
    return vneuman

def run(vneuman: VonNeuman, instructions: list, speed=1.0) -> VonNeuman:    
    """Runs the Von Neumann simulator with visual updates.
    Args:
        vneuman (VNeuman): The Von Neumann simulator instance.
        instructions (list): List of binary string instructions to load into memory.
        speed (float, optional): Speed of visual updates in seconds. Defaults to 1.0.
    Returns:
        VNeuman: The Von Neumann simulator instance after execution.
    """
    visuallib.VonNeuman = vneuman # Link the visual module to the VNeuman instance
    try:
        vneuman.set_instructions(instructions) # Load instructions into memory
    except VonNeuman.Missing_Instructions:
        print("No instructions provided, exiting...") # Exit if no instructions
        return vneuman
    while True:
        visuallib.update_visual_data(speed)
        vneuman.next_instruction()
        #First, the instruction is fetched from memory
        time.sleep(speed)
        visuallib.update_visual_data(speed)
        vneuman.interpreter()
        #Then, the instruction is interpreted
        time.sleep(speed)
        visuallib.update_visual_data(speed)
        time.sleep(speed)
        try:
            if vneuman.execute(): #Finally, the instruction is executed
                visuallib.update_visual_data(speed)
            else: # If HALT instruction, exit the loop
                print("End of program")
                print()
                for line in vneuman.show_memory():
                     # Display final memory state
                    print(line)
                print()
                break
        except VonNeuman.Out_Of_Bounds:
            # If an instruction tries to access memory out of bounds, exit the loop
            print("Address out of bounds, exiting...")
            print()
            for line in vneuman.show_memory():
                # Display final memory state
                print(line)
            print()
            break
        
        visuallib.update_visual_data(speed)
        
        try:
            time.sleep(speed)
            vneuman.tick()
        except VonNeuman.Clock_Overload:
            print("Clock overloaded")
            print()
            for line in vneuman.show_memory():
                # Display final memory state
                print(line)
            print()
            break
        time.sleep(speed)
    else:
        pass
    
    return vneuman 

if __name__ == "__main__":
    main()

##VINBELT