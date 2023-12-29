import pygame
import sys
import pygame_gui
import pygame.event

# Initiates a Pygame Display Window
pygame.init()
pygame.display.set_caption("Midi Editor")

# Setting the Window Size Properties
(WIDTH, HEIGHT) = pygame.display.get_desktop_sizes()[0]
HEIGHT-=90 
WIDTH-=10
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

# Initiating alle UI Managing Tools
CLOCK = pygame.time.Clock() # --> This will be relevant for Playback speed and could cause conflicts with midi tempo/bpm
MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT))

# All UI Components
LOADFILEBUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10,10),(50,50)),
                                              text="Load MIDI-File",
                                              manager=MANAGER)

def updateDisplay():
    UI_REFRESH_RATE = CLOCK.tick(60) / 1000
    MANAGER.update(UI_REFRESH_RATE)
    MANAGER.draw_ui(SCREEN)
    pygame.display.update()

def exitApp():
    pygame.quit()
    sys.exit()
    
def app():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitApp()
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == LOADFILEBUTTON:
                print("LOAD MIDI FILE")
            MANAGER.process_events(event)
        updateDisplay()            
        #SCREEN.blit(pygame.surface(HEIGHT,WIDTH), (0, 0))
app()
            