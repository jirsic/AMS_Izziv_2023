import argparse
import run_measurments_func as fnc
import pandas as pd

def parse_arguments():

    parser = argparse.ArgumentParser(description='Aneurysm segmentaton')

    parser.add_argument('-i', '--input', help='Path to the input file')
    parser.add_argument('-o', '--output', help='Path to the output file')

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    return input_path, output_path

input_path, output_path = parse_arguments()
print(input_path)
print(output_path)

aneurysmSize, xMaxDist, yMaxDist, zMaxDist, maxConDist, voksli=fnc.computeAneurysmVolume(input_path, [0,0,0], STEP=0.2)

measurements=[{'aneurysm size (in cubic milimeters):' : aneurysmSize},
              {'absolute distance in x coordinates (in milimeters)' : xMaxDist},
              {'absolute distance in y coordinates (in milimeters)' : yMaxDist},
              {'absolute distance in z coordinates (in milimeters)' : zMaxDist},
              {'Maximum number of connected voxels in x direction': maxConDist[0]},
              {'Maximum number of connected voxels in y direction': maxConDist[1]},
              {'Maximum number of connected voxels in z direction': maxConDist[2]}]

df=pd.DataFrame([measurements])
df.to_csv(output_path)