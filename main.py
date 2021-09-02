from pathlib import Path
import hashlib
import os
from progress.bar import IncrementalBar
from some_service_api import Counter
import argparse

quiet = False
output = False
files = []
parser = argparse.ArgumentParser(description='*write description*')
mode = parser.add_mutually_exclusive_group(required=True)
parser.add_argument('-q', '--quiet', action='store_true', help='print quiet')
parser.add_argument('-o', '--output', action='store', help='file output mode')
parser.add_argument('-p', '--path', action='store', help='path for directory of files', required=True)
mode.add_argument('-d', '--duplicates', action='store_true', help='search duplicates')
mode.add_argument('-l', '--large', action='store', help='search large file')
mode.add_argument('-t', '--type', action='store', help='search file extension (images, txt, docx, and other', default=None)
mode.add_argument('--old', action='store_true', help='search old file')

args = parser.parse_args()


def scan_files(path):
    if not os.path.exists(path):
        raise FileNotFoundError("Path not exist")
    else:
        global files
        files = [x for x in list(Path(path).glob("**/*"))]


def check_size(file):
    return os.stat(file).st_size


def search_extension(extension):
    bar = IncrementalBar('Progress', max=len(files))
    search_result = []
    counter = Counter()
    for file_path in files:
        if str(file_path).endswith(extension):
            search_result.append(file_path)
            counter.loop_counter()
        if not quiet:
            bar.next()
    bar.finish()
    return search_result, counter.get_counter()


def search_more_extension(specific_type=None):
    bar = IncrementalBar('Progress', max=len(files))
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
        elif specific_type is not None and str(file_path).endswith(specific_type):
            specific.append(file_path)
        if not quiet:
            bar.next()
    bar.finish()
    return jpg, png, jpg_counter.get_counter(), png_counter.get_counter()


def search_large(size):
    bar = IncrementalBar('Progress', max=len(files))
    size = int(size) * 1048576
    large = []
    large_counter = Counter()
    for file in files:
        if Path(file).stat().st_size > size:
            large.append([file, Path(file).stat().st_size])
            large_counter.loop_counter()
        if not quiet:
            bar.next()
    return large, large_counter.get_counter()


def check_len_duplicates():
    size_list = []
    for i in range(len(files)):
        size_list.append(Path(files[i]).stat().st_size)
    size_set = set(size_list)
    if not len(size_list) == len(size_set):
        dublicates = []
        for i in range(0, len(files)):
            for j in range(i + 1, len(files)):
                if Path(files[i]).stat().st_size == Path(files[j]).stat().st_size:
                    dublicates.append([Path(files[i]), Path(files[j].absolute())])
    return dublicates


def compare_hash(duplicates):
    for i in range(len(duplicates)):
        file1 = str(duplicates[1][0])
        print(file1)
        file2 = str(duplicates[1][1].absolute())
        with open(file1) as file_to_check:
            file1_data = file_to_check.read()
            file1_hash = hashlib.md5(file1_data).hexdigest()
        with open(file2) as file_to_check:
            file2_data = file_to_check.read()
            file2_hash = hashlib.md5(file2_data).hexdigest()
        if file1_hash == file2_hash:
            print('tutu')


if __name__ == '__main__':
    if args.quiet:
        quiet = True
        print('silent mode')
        print('SHHHH!')
        if args.output is None:
            print('maybe you forgot -o "filename"?')

    if args.path:
        scan_files(args.path)

    if args.duplicates:
        compare_hash(check_len_duplicates())

    elif args.large:
        large = search_large(args.large)
        searched_large = large[0]
        if not quiet:
            print("\nSearched %s files large of %s mb" % (args.large, large[1]))
            for i in range(len(searched_large)):
                print(i+1, end='. ')
                print(Path(searched_large[i][0]).name, round(searched_large[i][1]/1048576), 'mb')

    elif args.type:
        if args.type == 'images':
            searched_ext = search_more_extension()
            if not quiet:
                print('\nsearched %s images:' % (searched_ext[2]+searched_ext[3]))
                print('png (%s):' % searched_ext[3])
                if not len(searched_ext[1]) == 0:
                    for i in range(len(searched_ext[1])):
                        print(i+1, end='. ')
                        print(Path(searched_ext[1][i]))
                else:
                    print("Nothing found")
                print('jpg (%s):' % searched_ext[2])
                if not len(searched_ext[0]) == 0:
                    for i in range(len(searched_ext[0])):
                        print(i+1, end='. ')
                        print(Path(searched_ext[0][i]))
                else:
                    print("Nothing found")
        else:
            searched_ext = search_extension(args.type)
            print('searched %s %s' % (searched_ext[1], args.type))
            if not searched_ext[1] == 0:
                for i in range(searched_ext[1]):
                    print(i + 1, end='. ')
                    print(Path(searched_ext[0][i]))

    elif args.old:
        pass

    else:
        print('how did you do that? -_-')

    if args.output:
        print("file out(coming soon)")
