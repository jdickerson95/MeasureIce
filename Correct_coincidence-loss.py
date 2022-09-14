#This script is going to calculate the actual counts that hit the detector, correcting for coincidence loss and imperfect QE (the coincidence loss is the important part because it doesn't cancel out, thicker sample = fewer electrons = lower coincidence loss)

import numpy as np
import sys
import os
import mrcfile

material = "AuNP"
#slit = "NoSlit"
slit = "Slit"

#mod_dir = sys.argv[1]
#write_dir = sys.argv[2]

#mod_dir = f"cista1/Thickness/Blanks/Counting/"
#write_dir = f"cista1/Thickness/modMRCs/Blanks/"

#mod_dir = f"cista1/Thickness/Blanks/DPS/"
#write_dir = f"cista1/Thickness/modMRCs/DPS_blanks/"

mod_dir = f"cista1/Thickness/MotionCorr/{material}_{slit}2/{material}/{slit}/"
write_dir = f"cista1/Thickness/modMRCs/{material}/{slit}/"

#mod_dir = f"cista1/Thickness/MotionCorr/{material}_{slit}2/{material}/{slit}/Counting/"
#write_dir = f"cista1/Thickness/modMRCs/{material}/{slit}/"

if not os.path.exists(write_dir):
    os.mkdir(write_dir)
#D = 8.0 #e-/px/s  #This will be measured from image i.e each pixel multiplied individually
F = 400 #frames/s
s = 5.1459 #px^2
QE = 0.8656
exposureTime = 8.5 #s 


def getFraction(D):
    frac = np.exp(-(D/exposureTime)*s/F)*QE
    if frac < 0.1:
        frac = 1.0
    return frac

if __name__ == "__main__":
    vfunc_fraction = np.vectorize(getFraction, otypes=[np.float],cache=False)
    file_list = [f for f in os.listdir(mod_dir) if (f.endswith(".mrc") and f.endswith("_PS.mrc") == False)]
    for this_file in file_list:
        mrc =  mrcfile.open(f"{mod_dir}{this_file}", permissive=True)
        data = mrc.data
        mrc.close()
        fraction_image = vfunc_fraction(data)
        mod_data = data/fraction_image
        #now write new mrc
        with mrcfile.new(f"{write_dir}/mod_{this_file}", overwrite=True) as mrc:
            mrc.set_data(np.float32(mod_data))
        

'''
real_count = D/fraction
print(fraction/QE)
print(real_count)
'''
