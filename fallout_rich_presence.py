import time
import psutil
import pymem
from pypresence import Presence

CLIENT_ID = "1352438694782566504" #client id for discord

GAME_EXE = "falloutwHR.exe"  #fallout 1 exe
CHECK_INTERVAL = 5  # checks every 5 seconds for game

LEVEL_ADDRESS = 0x00665220  # static address for the level 
CHARACTER_NAME_ADDRESS = 0x0056BF1C  # static address for the character name 

def is_game_running():
    """Check if Fallout 1 is running."""
    for process in psutil.process_iter(attrs=['name']):
        if process.info['name'].lower() == GAME_EXE.lower():
            return True
    return False

def get_level():
    """Get the character's level from memory."""
    pm = pymem.Pymem(GAME_EXE)  # attaches to the Fallout 1 process
    level = pm.read_int(LEVEL_ADDRESS)  #reads the address
    return level

def get_character_name():
    """Get the character's name from memory."""
    pm = pymem.Pymem(GAME_EXE)  # attaches to Fallout 1 process
    name_bytes = pm.read_bytes(CHARACTER_NAME_ADDRESS, 64)  
    character_name = name_bytes.split(b'\x00', 1)[0]  
    return character_name.decode('utf-8')  

def main():
    rpc = Presence(CLIENT_ID)
    rpc.connect()
    game_active = False

    try:
        while True:
            if is_game_running():
                if not game_active:
                    print("Fallout 1 detected! Updating Rich Presence...")
                    game_active = True
                
                #gets character level and name
                level = get_level()
                character_name = get_character_name()

                #updates Rich Presence with character name and level
                rpc.update(
                    state=f"Level {level} - {character_name}",
                    large_image="fallout1",  #
                    large_text="Fallout 1"
                )
            else:
                if game_active:
                    print("Fallout 1 closed. Clearing Rich Presence...")
                    rpc.clear()
                    game_active = False

            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\nStopping script.")
        rpc.clear()

if __name__ == "__main__":
    main()
