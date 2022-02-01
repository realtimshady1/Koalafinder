import os
import sys
import multiprocessing as mp

def write_file(file_details):
    name, content = file_details
    with open(name, 'w') as text:
        text.write(content)

def extract_csv(folder):
    file_list = [os.path.join(folder, file) for file in os.listdir(folder)]
    extracted_list = []
    for file in file_list:
        if os.path.splitext(file)[1] == '.csv':
            folder = file.split('.')[0]

            try:
                os.mkdir(folder)
            except FileExistsError:
                pass

            with open(file, 'r') as f:
                contents = f.readlines()

            arr = [[os.path.join(folder, str(idx).zfill(8)+'.txt'), x.replace(',', '')] for (idx, x) in enumerate(contents) if x != '\n']

            with mp.Pool(mp.cpu_count()) as p:
                p.map(write_file, arr)

            extracted_list.append(os.path.basename(file))
            print('Extracted: ', file)
        else:
            print('Skipped: ', file)

    return extracted_list

if __name__=='__main__':
    if len(sys.argv) > 1:
        folder = sys.argv[1]

    extract_csv(folder)
