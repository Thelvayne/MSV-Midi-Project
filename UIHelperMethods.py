import pygame_gui

def get_min_max_notes(tracks):
    minnote = None
    maxnote = None
    for trk in tracks:
            for item in trk:
                if item.type == 'note_on':
                    note = item.note
                    if minnote == None or note < minnote:
                        minnote = note
                    if maxnote == None or note > maxnote:
                        maxnote = note
    return (minnote, maxnote)

def get_y_placement_for_note(note, minnote):
    notediff = note - minnote + 1  
    return notediff * 10

def get_container(number, MANAGER):
    scrollableContainer = "CONTAINER" + str(number)
    for element in MANAGER.get_root_container().elements:
        if isinstance(element, pygame_gui.elements.UIScrollingContainer):
            if element.object_ids[0] == scrollableContainer:
                return element
    return None
            
def get_panel(containernr, panelnr, MANAGER):
    panel = "PANEL" + str(panelnr)
    container = get_container(containernr, MANAGER)
    if container == None:
        return None
    for element in container.scrollable_container.elements:
        if isinstance(element, pygame_gui.elements.UIPanel):
            if element.object_ids[1] == panel:
                return element

def set_scrollable_dimensions(Width, Height, MANAGER):
    i = 0
    while get_container(i, MANAGER) != None:
        scrollableContainer = get_container(i, MANAGER)
        scrollableContainer.set_scrollable_area_dimensions((Width, Height))
        i += 1

def get_container_width(tracks):
    container_width = 0
    for item in tracks[0]:
        if hasattr(item, 'time'):
            container_width += item.time
    return container_width

def get_container_height(TRACKS):
    minnote, maxnote = get_min_max_notes(TRACKS)
    steps = maxnote - minnote + 1
    amount_panels = (len(TRACKS) - 1)
    return (amount_panels * (steps*10)) + (amount_panels - 1) * 10