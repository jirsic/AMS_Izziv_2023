from run_registration_func import func
import probFun
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Aneurysm registration')

    parser.add_argument('-i_1', '--input1', help='Path to the input file')
    parser.add_argument('-i_2', '--input2', help='Path to the input file')
    parser.add_argument('-o', '--output', help='Path to the output file')

    args = parser.parse_args()

    src_path = args.input1
    trg_path = args.input2
    output_path = args.output

    return src_path, trg_path, output_path

src_path, trg_path, output_path = parse_arguments()
print(src_path)
print(trg_path)

n1=func(1)


trsMatrices, sourceMesh, targetMeshes, redo=n1.load_selCases(src_path, trg_path)


resultMeshes=n1.apply_transformations(trsMatrices, sourceMesh, redo)


if trsMatrices.sprem=='DEFEKT':
    resultMeshes=probFun.correct_defect(targetMeshes, resultMeshes, trsMatrices)

n1.show_transformedMeshes(sourceMesh, targetMeshes, resultMeshes, redo)

n1.save_mesh(resultMeshes, output_path)