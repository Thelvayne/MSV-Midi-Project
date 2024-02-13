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

def createUIPanels(filetracks):
    i = 0

    length = 0
    for item in filetracks[0]:
        if hasattr(item, 'time'):
            length += item.time
    
    print(length)

    amountPanels = len(filetracks) - 1

    scrollableContainer_name = "CONTAINER" + str(i)
    scrollableContainer_left_top = (10,60)
    scrollableContainer_width_height = (WIDTH-20,amountPanels*100+10)
    scrollableContainer_rect = pygame.Rect(scrollableContainer_left_top, scrollableContainer_width_height)

    scrollableContainer = pygame_gui.elements.UIScrollingContainer(
        relative_rect=scrollableContainer_rect,
        manager=MANAGER,
        starting_height=1,
        object_id=scrollableContainer_name,
        anchors={"left":"left","top":"top"}
    )

    SCREEN.fill(pygame.Color("black"), (ADDCOLUMNBUTTON.relative_rect.left, 
                                        ADDCOLUMNBUTTON.relative_rect.top, 
                                        ADDCOLUMNBUTTON.relative_rect.right - ADDCOLUMNBUTTON.relative_rect.left, 
                                        ADDCOLUMNBUTTON.relative_rect.bottom - ADDCOLUMNBUTTON.relative_rect.top))
    
    while i < len(filetracks) - 1:
        
        panel_name = "PANEL" + str(i)
        panel_left_top = (0,i * 100)
        panel_width_height = (length,90)
        panel_rect = pygame.Rect(panel_left_top, panel_width_height)
        
        panel = pygame_gui.elements.UIPanel(
            relative_rect=panel_rect,
            starting_height=2,
            manager=MANAGER,
            parent_element=scrollableContainer,
            container=scrollableContainer,
            object_id=panel_name,
            anchors={"left":"left","top":"top"})
        
        i += 1
    
    ADDCOLUMNBUTTON.set_relative_position((WIDTH/2, scrollableContainer.relative_rect.bottom + 10))

def setScrollableDimensions(Width, Height):
    i = 0
    while getContainer(i) != None:
        scrollableContainer = getContainer(i)
        scrollableContainer.set_scrollable_area_dimensions((Width, Height))
        i += 1

def getContainer(number):
    scrollableContainer = "CONTAINER" + str(number)
    for element in MANAGER.get_root_container().elements:
        if isinstance(element, pygame_gui.elements.UIScrollingContainer):
            if element.object_ids[0] == scrollableContainer:
                return element
    print(f"No UIScrollingContainer found with object_ids: {scrollableContainer}")  # <-- add this line
    return None
            
def getPanel(containernr, panelnr):
    panel = "PANEL" + str(panelnr)
    container = getContainer(containernr)
    if container == None:
        return None
    for element in container.scrollable_container.elements:
        if isinstance(element, pygame_gui.elements.UIPanel):
            if element.object_ids[1] == panel:
                return element

def removeLabeltext():
    # 'löscht' Labeltext
    SCREEN.fill(pygame.Color("black"), (MIDIFILENAME.relative_rect.left, 
                                        MIDIFILENAME.relative_rect.top, 
                                        MIDIFILENAME.relative_rect.right - MIDIFILENAME.relative_rect.left, 
                                        MIDIFILENAME.relative_rect.bottom - MIDIFILENAME.relative_rect.top))

def removeOldUIElements():
    
    removeLabeltext()

    # löscht alte Panels
    i = 0
    container = getContainer(i)
    while container != None:
        panel = getPanel(containernr=0, panelnr=i)
        if panel == None:
            break
        panel.kill()
        SCREEN.fill(pygame.Color('black'), (container.relative_rect.left,
                                                container.relative_rect.top,
                                                container.relative_rect.right - container.relative_rect.left,
                                                container.relative_rect.bottom - container.relative_rect.top))
        i += 1

    if container != None:
        container.kill()

    # verschiebt +-Button
    SCREEN.fill(pygame.Color('black'), (ADDCOLUMNBUTTON.relative_rect.left,
                                        ADDCOLUMNBUTTON.relative_rect.top,
                                        ADDCOLUMNBUTTON.relative_rect.right - ADDCOLUMNBUTTON.relative_rect.left,
                                        ADDCOLUMNBUTTON.relative_rect.bottom - ADDCOLUMNBUTTON.relative_rect.top))
    ADDCOLUMNBUTTON.set_relative_position((WIDTH/2,180))

def drawNotes(tracks):
    i = 0
    while i < len(tracks) - 1:
        panel = getPanel(containernr=0, panelnr=i)

        track = tracks[i+1]

        offset = 0
        for item in track:
            if item.type == 'program_change':
                offset = item.time
                break
        print(offset)
        i += 1

        current_position = offset

        n = 0
        while n < len(track):
            modi = track[n]
            if modi.type == 'note_on':
                current_position += track[n].time
                x = current_position
                y = get_y_placement_for_note(track[n].note)
                length = track[n+1].time
                n += 2
                current_position += length

                note_position = (x,y)
                note_size = (length, 10)
                note_rect = pygame.Rect(note_position,note_size)

                note = pygame_gui.elements.UIPanel(
                    relative_rect=note_rect,
                    starting_height=3,
                    manager=MANAGER,
                    parent_element=panel,
                    container=panel,
                    anchors={"left":"left","top":"top"} 
                )
            else:
                n += 1

def get_y_placement_for_note(note):
    if note == 67:
        return 0
    elif note == 68:
        return 5
    elif note == 69:
        return 10
    elif note == 70:
        return 15
    elif note == 71:
        return 20
    elif note == 72:
        return 25
    elif note == 73:
        return 30 
    elif note == 74:
        return 35 
    elif note == 75:
        return 40 
    elif note == 76:
        return 45 
    elif note == 77:
        return 50 
    elif note == 78:
        return 55                
    elif note == 79:
        return 60 
    elif note == 80:
        return 65 
    elif note == 81:
        return 70 
    elif note == 82:
        return 75 
    elif note == 83:
        return 80
    else:
        return 85

def app():
    MIDIFILE=None
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitApp()
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == LOADFILEBUTTON:
                
                import MidiFileLoader,Partiture
                #from mido import Message,MetaMessage
                import mido

                MIDIFILE = MidiFileLoader.loadMidiFile()
                #PARTITURE:Partiture.Partiture = Partiture.Partiture(MIDIFILE)
                if MIDIFILE is not None:

                    MIDIFILE.print_tracks()
                    tracks = MIDIFILE.tracks

                    # UI Part:
                    # clean up screen
                    removeOldUIElements()

                    # get loaded file name
                    FILENAME = MIDIFILE.filename
                    POSITIONSLASH = FILENAME.rfind("\\")
                    MIDIFILENAME.set_text(FILENAME[POSITIONSLASH+1:])

                    # dynamic creation for UIPanels to show different channels
                    createUIPanels(MIDIFILE.tracks)
                    container_width = 0
                    for item in tracks[0]:
                        if hasattr(item, 'time'):
                            container_width += item.time
                    amount_panels = (len(MIDIFILE.tracks) - 1)
                    container_height = (amount_panels * 90) + ((amount_panels - 1) * 10)
                    setScrollableDimensions(container_width,container_height)
                    updateDisplay()
                    drawNotes(tracks)

                else: 
                    removeLabeltext()
                    MIDIFILENAME.set_text(f"File not found or cancelled")
                
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == CONVERTTOWAVBUTTON:
                import midiToWav
                if MIDIFILE is not None:
                    midiToWav.convertMidToWav(MIDIFILE)
                else:
                    removeLabeltext()
                    MIDIFILENAME.set_text(f"Cannot convert because no MidiFile is loaded!")
     
            MANAGER.process_events(event)
        updateDisplay()            
        #SCREEN.blit(pygame.surface(HEIGHT,WIDTH), (0, 0))
app()
            