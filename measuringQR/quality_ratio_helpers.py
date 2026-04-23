import numpy as np
import tgt
from scipy.io import wavfile
from scipy.integrate import simpson

def readInFile(filename: str, label: str, time: float) -> tuple:
    """
    This function takes in some info from a dataframe row, and takes us all the way to the point
    where we have just the part of the wav file we want to look at as a numpy array!
    Returns a samplerate, np.array tuple
    """
    file = filename.split('.')[0].strip(' ')

    samplerate, wav = wavfile.read(f"./ALLdone/{file}.wav")
    wav = wav[:, 0] # grab left channel. whatever
    tg = tgt.read_textgrid(f"./ALLdone/{file}.TextGrid")

    text_grid_in_question = None
    for annotation in tg.tiers[1].get_annotations_by_time(time):
        if annotation.text == label:
            text_grid_in_question = annotation

    if text_grid_in_question is None:
        print('uh oh!!!')
        raise RuntimeError(f"Something went wrong while finding the correpsonding textgrid annotation for file {filename}! Womp!!")
    
    grid_start = text_grid_in_question.start_time
    grid_end = text_grid_in_question.end_time
    target_timepoint_start = grid_start + (4.5 * ((grid_end - grid_start) / 9))
    target_timepoint_end = target_timepoint_start + (2 * ((grid_end - grid_start) / 9))

    return samplerate, wav[int(target_timepoint_start * samplerate):int(target_timepoint_end * samplerate)]


def calculateLowerReference(F1: float, B1: float) -> float:
    """
    given the frequency and bandwidth of the first formant, we run a quick calc and get the lower reference! :D
    """
    return F1 - (B1 / 2)


def calculateMiddleReference(F2: float, B2: float, F3: float, B3: float) -> float:
    """
    given the frequency and bandwidth of both the second and third formants, returns the middle reference frequency
    """
    f3_under = F3 - (B3 / 2)
    f2_over = F2 + (B2 / 2)
    if f3_under > f2_over:
        return f3_under
    else:
        return (F2 + F3) / 2
    

def calculateQR(welch: tuple, refs: tuple) -> float:
    """
    given the output from scipy.signal.welch & a tuple containing the three frequency references,
    returns the quality ratio QR! yay!!
    """
    f, Pxx = welch
    # Pxx = np.log(Pxx) # source paper says to do this, why not! (DONT DO IT IT IS BAD!!!)

    i = 0
    # note we dont need x coordinates cuz we're doing a ratio! and values in f are equidistant!! yay!!!
    P12 = []
    P345 = []
    while (f[i] < refs[0]):
        i += 1
    while (f[i] < refs[1]):
        P12.append(Pxx[i])
        i += 1
    while (f[i] < refs[2]):
        P345.append(Pxx[i])
        i += 1

    return simpson(np.array(P12)) / simpson(np.array(P345))