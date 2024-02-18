import pygame
import pygame_gui

def remove_label_text(SCREEN, MIDIFILENAME):
    # 'löscht' Labeltext
    SCREEN.fill(pygame.Color("black"), (MIDIFILENAME.relative_rect.left, 
                                        MIDIFILENAME.relative_rect.top, 
                                        MIDIFILENAME.relative_rect.right - MIDIFILENAME.relative_rect.left, 
                                        MIDIFILENAME.relative_rect.bottom - MIDIFILENAME.relative_rect.top))

def remove_old_UI_elements(MANAGER, SCREEN, WIDTH, ADDCOLUMNBUTTON, MIDIFILENAME):
    
    remove_label_text(SCREEN, MIDIFILENAME)

    # löscht alte Panels
    from UIHelperMethods import get_container, get_panel
    i = 0
    container = get_container(i, MANAGER)
    while container != None:
        panel = get_panel(containernr=0, panelnr=i, MANAGER=MANAGER)
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

def create_UIPanels(filetracks, MANAGER, SCREEN, WIDTH, ADDCOLUMNBUTTON):
    from UIHelperMethods import get_min_max_notes

    p_l_t = (0,0)
    p_w_h = (0,0)
    p_rect = pygame.Rect(p_l_t, p_w_h)
    p = pygame_gui.elements.UIPanel(relative_rect=p_rect, manager=MANAGER)
    p.background_colour.r = 255
    p.background_colour.g = 255
    p.background_colour.b = 255

    i = 0

    length = 0
    for item in filetracks[0]:
        if hasattr(item, 'time'):
            length += item.time
    
    minnote, maxnote = get_min_max_notes(filetracks)
    steps = maxnote - minnote + 2
    container_height = steps * 10

    amountPanels = len(filetracks) - 1

    scrollableContainer_name = "CONTAINER" + str(i)
    scrollableContainer_left_top = (10,60)
    scrollableContainer_width_height = (WIDTH-20, amountPanels * (container_height + 10) + 10)
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
        panel_left_top = (0,i * (container_height + 10))
        panel_width_height = (length,container_height)
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
    
    p.kill()
    ADDCOLUMNBUTTON.set_relative_position((WIDTH/2, scrollableContainer.relative_rect.bottom + 10))

def draw_notes(tracks, MANAGER):
    from UIHelperMethods import get_min_max_notes, get_panel, get_y_placement_for_note

    p_l_t = (0,0)
    p_w_h = (0,0)
    p_rect = pygame.Rect(p_l_t, p_w_h)
    p = pygame_gui.elements.UIPanel(relative_rect=p_rect, manager=MANAGER)
    p.background_colour.r = 0
    p.background_colour.g = 0
    p.background_colour.b = 0

    minnote, maxnote = get_min_max_notes(tracks)

    i = 0
    while i < len(tracks) - 1:
        panel = get_panel(containernr=0, panelnr=i, MANAGER=MANAGER)

        track = tracks[i+1]

        offset = 0
        for item in track:
            if item.type == 'program_change':
                offset = item.time
                break
        i += 1

        current_position = offset     

        n = 0
        while n < len(track):
            modi = track[n]
            if modi.type == 'note_on':
                current_position += track[n].time
                x = current_position
                y = get_y_placement_for_note(note=track[n].note, minnote=minnote)
                length = track[n+1].time
                n += 2
                current_position += length

                note_position = (x,y)
                note_size = (length + 4, 10 + 4) # +4 because pygame_gui reserves some space for the border, but we have the border at 0, it still needs it for some reason
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
    p.kill()