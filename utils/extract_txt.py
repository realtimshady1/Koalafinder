import os
import sys

def extract_txt(folder):
    folder_list = [os.path.join(folder, file) for file in os.listdir(folder)]

    for folder in folder_list:
        if len(folder.split('.')) == 1:
            file_list = [file for file in os.listdir(folder) if file.split('.')[1]=='txt']
            with open(folder + '.csv', 'w') as f:
                # skip 00000000.txt
                if file_list[0]=='00000000.txt':
                    file_list.pop(0)
                    row = 1
                else:
                    row = 0

                for file in file_list:
                    frame = int(file.split('.')[0])
                    if frame != row:
                        f.write('\n' * (frame - row))
                        row = frame
                    with open(os.path.join(folder,file), 'r') as text:
                        content = text.readlines()
                        f.write(','.join(content))
                    row += 1
            print('Extracted: ', folder)
        else:
            print('Skipped: ', folder)

if __name__=='__main__':
    if len(sys.argv) > 1:
        folder = sys.argv[1]

    extract_txt(folder)
