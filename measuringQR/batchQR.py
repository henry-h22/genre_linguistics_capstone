import pandas as pd
from quality_ratio_helpers import *
from scipy.signal import welch

all_data = pd.read_csv("big_capstone_data.csv")
# all_data = all_data.head(22) # for testing!! :D
refHigher = 5500
QR_list = []

for i, row in all_data.iterrows():
    samplerate, wav = readInFile(
        str(row["file"]), 
        str(row["label"]), 
        float(row["t"])
    )

    refLower = calculateLowerReference(
        float(row["F1"]), 
        float(row["B1"])
    )
    refMid = calculateMiddleReference(
        float(row["F2"]), 
        float(row["B2"]), 
        float(row["F3"]), 
        float(row["B3"]), 
    )

    QR_list.append(
        calculateQR(
            welch(wav, fs = samplerate), 
            (refLower, refMid, refHigher)
        )
    )

all_data['QR'] = QR_list
all_data.to_csv("QR_data.csv", index = False)