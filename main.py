from pathlib import Path
import os
from progress.bar import IncrementalBar
from some_service_api import Counter
import argparse

#path = '/Users/macbook/OneDrive/LNTU/Programming'
quiet = False
output = False

parser = argparse.ArgumentParser(description='*write description*')
mode = parser.add_mutually_exclusive_group(required=True)
parser.add_argument('-q', '--quiet', action='store_true', help = 'print quiet')
parser.add_argument('-o', '--output', action='store', help='file output mode')
parser.add_argument('-p', '--path', action='store', help='path for directory of files', required=True)
mode.add_argument('-d', '--duplicates', action='store_true', help='search duplicates')
mode.add_argument('-l', '--large', action='store', help='search large file')
mode.add_argument('-t', '--type', action='store', help='search file extention (images, txt, docx, and other', default=None)
mode.add_argument('--old', action='store_true', help='search old file')

args = parser.parse_args()

def scan_files(path):
    global files
    files = [x for x in list(Path(path).glob("**/*"))]

def compare(F1, F2):
    pass

def check_size(file):
    return os.stat(file).st_size


def search_extension(extension):
    bar = IncrementalBar('Progress', max=len(files))
    searched_type = []
    counter = Counter()
    for file_path in files:
        if str(file_path).endswith(extension):
            searched_type.append(file_path)
            counter.loop_counter()
        if not quiet:
            bar.next()
    bar.finish()
    return searched_type


def search_more_extension(scecific_type = None):
    bar = IncrementalBar('Progress', max = len(files))
    jpg = []
    png = []
    specific = []
    jpg_counter = Counter()
    png_counter = Counter()
    for file_path in files:
        if str(file_path).endswith('.jpg'):
            jpg.append(file_path)
            jpg_counter.loop_counter()
        elif str(file_path).endswith('.png'):
            png.append(file_path)
            png_counter.loop_counter()
        elif scecific_type != None and str(file_path).endswith(scecific_type):
            specific.append(file_path)
        if not quiet:
            bar.next()
    bar.finish()
    return jpg, png

def search_large(size):
    bar = IncrementalBar('Progress', max=len(files))
    size = int(size) * 1048576
    large = []
    for file in files:
        if Path(file).stat().st_size > size:
            large.append([(file) ,(Path(file).stat().st_size)])
        if not quiet:
            bar.next()
    return large


if __name__ == '__main__':
    if args.quiet:
        quiet = True
        print('silent mode')
        print('SHHHH!')
        if args.output == None:
            print('maybe you forgot -o "filename"?')
    if args.path:
        scan_files(args.path)
    if args.duplicates:
        print('coming soon;)')
    elif args.large:
        searched_large = search_large(args.large)
        if not quiet:
            print("\nFiles large of", args.large, "mb:")
            for i in range(len(searched_large)):
                print(i+1,end='. ')
                print(Path(searched_large[i][0]).name)
    elif args.type:
        if args.type == 'images':
            searched_ext = search_more_extension()
            if not quiet:
                print('\nsearched images:')
                print('png:')
                if not len(searched_ext[1]) == 0:
                    for i in range(len(searched_ext[1])):
                        print(i+1, end='. ')
                        print(Path(searched_ext[1][i]))
                else:
                    print("Nothing found")
                print('jpg:')
                if not len(searched_ext[0]) == 0:
                    for i in range(len(searched_ext[1])):
                        print(i+1, end='. ')
                        print(Path(searched_ext[0][i]))
                else:
                    print("Nothing found")
        else:
            scan_files()
            print(Path(search_extension(args.type)[0]))
            pass # print help message
    elif args.old:
        
    else:
        pass
    if args.output:
        print("file out(coming soon)")