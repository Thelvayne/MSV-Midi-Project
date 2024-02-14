import pygame
import sys
import pygame_gui
import pygame.event
from UIHelperMethods import set_scrollable_dimensions, get_container_width, get_container_height
from UICreation import remove_old_UI_elements, create_UIPanels, draw_notes, remove_label_text

# Initiates a Pygame Display Window
pygame.init()
pygame.display.set_caption("Midi Editor")

# Setting the Window Size Properties
(WIDTH, HEIGHT) = pygame.display.get_desktop_sizes()[0]
HEIGHT-=90 
WIDTH-=10
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

# Initiating all UI Managing Tools
CLOCK = pygame.time.Clock() # --> This will be relevant for Playback speed and could cause conflicts with midi tempo/bpm
MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT), 'theme.json')

# All UI Components
LOADFILEBUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10,10),(-1,-1)),
                                              text="Load MIDI-File",
                                              manager=MANAGER,
                                              anchors={"left":"left",
                                                       "top":"top"})

ADDCOLUMNBUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2,180),(50,50)),
                                              text="+",
                                              manager=MANAGER,
                                              anchors={"left":"left",
                                                       "top":"top"})

CONVERTTOWAVBUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((160,10),(-1,-1)),
                                                  text="Convert .mid to .wav",
                                                  manager=MANAGER,
                                                  anchors={"left":"left","top":"top"})

MIDIFILENAME = pygame_gui.elements.UILabel(pygame.Rect((CONVERTTOWAVBUTTON.relative_rect.right + 10,10),(-1,-1)),
                                           text="",
                                           visible=1,
                                           manager=MANAGER,
                                           anchors={"left":"left",
                                                    "top":"top"})

def updateDisplay():
    UI_REFRESH_RATE = CLOCK.tick(60) / 1000
    MANAGER.update(UI_REFRESH_RATE)
    MANAGER.draw_ui(SCREEN)
    pygame.display.update()

def exitApp():
    pygame.quit()
    sys.exit()

def app():
    MIDIFILE=None
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitApp()
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == LOADFILEBUTTON:
                
                import MidiFileLoader
                #from mido import Message,MetaMessage

                MIDIFILE = MidiFileLoader.loadMidiFile()
                #PARTITURE:Partiture.Partiture = Partiture.Partiture(MIDIFILE)
                if MIDIFILE is not None:

                    MIDIFILE.print_tracks()

                    # UI Part:
                    # clean up screen
                    remove_old_UI_elements(MANAGER=MANAGER, SCREEN=SCREEN, WIDTH=WIDTH, ADDCOLUMNBUTTON=ADDCOLUMNBUTTON, MIDIFILENAME=MIDIFILENAME)

                    # get loaded file name
                    FILENAME = MIDIFILE.filename
                    POSITIONSLASH = FILENAME.rfind("\\")
                    MIDIFILENAME.set_text(FILENAME[POSITIONSLASH+1:])
                    TRACKS = MIDIFILE.tracks

                    # dynamic creation for UIPanels to show different channels
                    create_UIPanels(TRACKS, MANAGER=MANAGER, SCREEN=SCREEN, WIDTH=WIDTH, ADDCOLUMNBUTTON=ADDCOLUMNBUTTON)
                    
                    container_width = get_container_width(TRACKS)
                    container_height = get_container_height(TRACKS)
                    set_scrollable_dimensions(container_width, container_height, MANAGER)
                    draw_notes(TRACKS, MANAGER)

                else: 
                    remove_label_text(SCREEN=SCREEN, MIDIFILENAME=MIDIFILENAME)
                    MIDIFILENAME.set_text(f"File not found or cancelled")
                
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == CONVERTTOWAVBUTTON:
                import midiToWav
                if MIDIFILE is not None:
                    midiToWav.convertMidToWav(MIDIFILE)
                else:
                    remove_label_text(SCREEN=SCREEN, MIDIFILENAME=MIDIFILENAME)
                    MIDIFILENAME.set_text(f"Cannot convert because no MidiFile is loaded!")
     
            MANAGER.process_events(event)
        updateDisplay()            
        #SCREEN.blit(pygame.surface(HEIGHT,WIDTH), (0, 0))
app()
            