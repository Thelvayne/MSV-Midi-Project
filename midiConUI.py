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
MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT), 'theme.json')

# All UI Components
LOADFILEBUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10,10),(-1,-1)),
                                              text="Load MIDI-File",
                                              manager=MANAGER,
                                              anchors={"left":"left",
                                                       "top":"top"})

#SYSTEMCOLUMN = pygame_gui.elements.UIPanel(pygame.Rect((10,60),(WIDTH-20,90)),
 #                                          manager=None,
  #                                         anchors={"left":"left","top":"top"})

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

LASTCREATEDPANELNUMBER = -1
def setLastCreatedPanelNumber(number):
    global LASTCREATEDPANELNUMBER
    LASTCREATEDPANELNUMBER = number

def createUIPanels(filetracks):
    i = 0
    for tracks in filetracks:
        SCREEN.fill(pygame.Color("black"), (ADDCOLUMNBUTTON.relative_rect.left, 
                                            ADDCOLUMNBUTTON.relative_rect.top, 
                                            ADDCOLUMNBUTTON.relative_rect.right - MIDIFILENAME.relative_rect.left, 
                                            ADDCOLUMNBUTTON.relative_rect.bottom - MIDIFILENAME.relative_rect.top))

        name = "SYSTEMCOLUMN" + str(i)
        name = pygame_gui.elements.UIPanel(pygame.Rect((10,60+i*90),(WIDTH-20,90)),
            manager=MANAGER,
            object_id=name,
            anchors={"left":"left","top":"top"})
        ADDCOLUMNBUTTON.set_relative_position((WIDTH/2, name.relative_rect.bottom + 10))
        setLastCreatedPanelNumber(i)
        i += 1
        if i == len(filetracks) - 1:
            break

def getPanel(number):
    Panel = "SYSTEMCOLUMN" + str(number)
    for element in MANAGER.get_root_container().elements:
        if isinstance(element, pygame_gui.elements.UIPanel):
            if element.object_ids[0] == Panel:
                return element


def removeOldUIElements():
    # 'löscht' alte Namen
    
    SCREEN.fill(pygame.Color("black"), (MIDIFILENAME.relative_rect.left, 
                                        MIDIFILENAME.relative_rect.top, 
                                        MIDIFILENAME.relative_rect.right - MIDIFILENAME.relative_rect.left, 
                                        MIDIFILENAME.relative_rect.bottom - MIDIFILENAME.relative_rect.top))
    # 'löscht' alte Panels
    global LASTCREATEDPANELNUMBER
    if LASTCREATEDPANELNUMBER >= 0:
        i = 0
        while i <= LASTCREATEDPANELNUMBER:
            panel = getPanel(i)
            paneltop = panel.relative_rect.top
            panelbottem = panel.relative_rect.bottom
            panelleft = panel.relative_rect.left
            panelright = panel.relative_rect.right
            if panel != None:
                panel.kill()
            SCREEN.fill(pygame.Color('black'), (panelleft,
                                                paneltop,
                                                panelright - panelleft,
                                                panelbottem - paneltop))
            i += 1

    # verschiebt +-Button
    ADDCOLUMNBUTTON.set_relative_position((WIDTH/2,180))

def app():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitApp()
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == LOADFILEBUTTON:
                
                import MidiFileLoader,Partiture
                from mido import Message,MetaMessage

                removeOldUIElements()

                MIDIFILE = MidiFileLoader.loadMidiFile()
                PARTITURE:Partiture.Partiture = Partiture.Partiture(MIDIFILE)
                MIDIFILE.print_tracks()
                
                # console output
                print(f"LENDGHT: {MIDIFILE.length}")
                x = MIDIFILE.tracks[1]
                print(type(x[0]))

                # get loaded file name
                FILENAME = MIDIFILE.filename
                POSITIONSLASH = FILENAME.rfind("\\")
                MIDIFILENAME.set_text(FILENAME[POSITIONSLASH+1:])

                # dynamic creation for UIPanels to show different channels
                createUIPanels(MIDIFILE.tracks)
                
                
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == CONVERTTOWAVBUTTON:
                import midiToWav
                midiToWav.convertMidToWav(MIDIFILE)
     
            MANAGER.process_events(event)
        updateDisplay()            
        #SCREEN.blit(pygame.surface(HEIGHT,WIDTH), (0, 0))
app()
            