import argparse
import run_measurments_func as fnc
import pandas as pd
import numpy as np

def parse_arguments():

    parser = argparse.ArgumentParser(description='Aneurysm segmentaton')

    parser.add_argument('-i_1', '--input1', help='Path to the input file')
    parser.add_argument('-i_2', '--input2', help='Path to the input file')
    parser.add_argument('-o', '--output', help='Path to the output file')

    args = parser.parse_args()

    src_path = args.input1
    trg_path = args.input2
    output_path = args.output

    return src_path, trg_path, output_path

src_path, trg_path, output_path = parse_arguments()

aneurysmSize1, xMaxDist, yMaxDist, zMaxDist, maxConDist, voksli=fnc.computeAneurysmVolume(src_path, [0,0,0], STEP=0.2)
aneurysmSize2, xMaxDist, yMaxDist, zMaxDist, maxConDist, voksli=fnc.computeAneurysmVolume(trg_path, [0,0,0], STEP=0.2)
aSize=np.abs(aneurysmSize1-aneurysmSize2)

measurements=[{'aneurysm size difference (in cubic milimeters):' : aneurysmSize1}]

df=pd.DataFrame([measurements])
df.to_csv(output_path)