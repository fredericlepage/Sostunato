import mido

INPUT_DEVICE = ###
OUTPUT_PORT = ###

in_port = mido.open_input(INPUT_DEVICE)
out_port = mido.open_output(OUTPUT_PORT)

notes = []              # Notes pressed while the sostunato pedal is not pressed
notes_2 = []            # Notes pressed while the sostunato pedal is held
relased_notes = []      # Notes released while the sostunato pedal is held

pedal = False

def main():
    for msg in in_port:
        if msg.type == 'note_on':
            if not pedal:
                notes.append(msg.note)
            else:
                notes_2.append(msg.note)
                if msg.note in released_notes:
                    released_notes.remove(msg.note)
            out_port.send(msg)

        if msg.type == 'note_off':
            if not pedal:
                out_port.send(msg)
                if msg.note in notes:
                    notes.remove(msg.note)
            if pedal:
                if msg.note in notes_2:
                    notes_2.remove(msg.note)
                if msg.note in notes:
                    released_notes.append(msg.note)
                else:
                    out_port.send(msg)
        
        try:
            if msg.control == 64:
                if msg.value >= 64:
                    pedal = True
                    released_notes = []
                else:
                    pedal = False
                    notes = notes + notes_2
                    notes_2 = []
                    
                    for note in released_notes:
                        print(note)
                        notes.remove(note)
                        out_port.send(mido.Message('note_off', note=note))     
        except AttributeError:
            # If msg has no attribute "control"
            pass

main()
