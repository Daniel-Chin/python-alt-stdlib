'''
Add overlaping notes to a midi file, automatically creating new tracks when necessary.  
'''
import typing as tp

import pretty_midi

class TrackStillBusy(Exception): pass

class MidiMultiplex:
    '''
    This implementation is only efficient if the notes are added in order of their start time.
    '''
    def __init__(self) -> None:
        self.midi = pretty_midi.PrettyMIDI()
        self.tracks: tp.List[Track] = []

    def add(self, note: pretty_midi.Note):
        for track in self.tracks:
            try:
                track.add(note)
            except TrackStillBusy:
                pass
            else:
                return
        track = Track(self.midi)
        track.add(note)
        self.tracks.append(track)
    
    def get(self):
        return self.midi

class Track:
    def __init__(self, midi: pretty_midi.PrettyMIDI) -> None:
        self.instrument = pretty_midi.Instrument(0) # piano
        self.busy_until = [0.0] * 128
        midi.instruments.append(self.instrument)
    
    def add(self, note: pretty_midi.Note):
        if note.start < self.busy_until[note.pitch]:
            raise TrackStillBusy()
        self.busy_until[note.pitch] = note.end
        self.instrument.notes.append(note)
