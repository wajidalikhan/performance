#!/usr/bin/env python
"""
DBS 3 Client Example.   This script is called

python GetDasInfo.py '/*/*Fall13-POST*/GEN-SIM'

"""
import subprocess, argparse

def run_dasgoclient(dataset, output_file):
    """
    Runs the dasgoclient command with the given dataset name,
    and saves the output to the specified file.
    """
    cmd = f"dasgoclient --query 'file dataset={dataset}'"
    output = subprocess.check_output(cmd, shell=True)
    with open(output_file, "w") as f:
        decoded_output = output.decode()
        decoded_output = decoded_output.rstrip(decoded_output[-1])
        preprocessed_output = "root://cms-xrd-global.cern.ch/" + decoded_output.replace('\n', '\nroot://cms-xrd-global.cern.ch/')
        f.write("# "+dataset+'\n')
        f.write(preprocessed_output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runs dasgoclient with the given dataset name and saves the output to a file.")
    parser.add_argument("dataset", help="the name of the dataset")
    parser.add_argument("output_file", help="the name of the output file")
    args = parser.parse_args()
    
    run_dasgoclient(args.dataset, args.output_file)
    print(f"Output saved to {args.output_file}.")
