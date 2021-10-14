from pathlib import Path
import hashlib
import os
from progress.bar import IncrementalBar
from some_service_api import Counter
import argparse
import time
import re
from some_service_api import Logger


silent = False
output = False
files = []
parser = argparse.ArgumentParser(description='*write description*')
mode = parser.add_mutually_exclusive_group(required=True)
parser.add_argument('-s', '--silent', action='store_true', help='silent mode')
parser.add_argument('-o', '--output', action='store', help='file output mode')
parser.add_argument('-p', '--path', action='store', help='path for directory of files', required=True)
mode.add_argument('-d', '--duplicates', action='store_true', help='search duplicates')
mode.add_argument('-l', '--large', action='store', help='search large file')
mode.add_argument('-t', '--type', action='store', help='search file extension (images, txt, docx, and other', default=None)
mode.add_argument('--old', action='store', help='search old file')

args = parser.parse_args()


def scan_files(path):
    if not os.path.exists(path):
        raise FileNotFoundError("Path not exist")
    else:
        global files
        files = [x for x in list(Path(path).glob("**/*"))]
        if len(files) == 0:
            raise Exception


def check_size(file):
    return os.stat(file).st_size


def search_extension(extension):
    bar = IncrementalBar('Searching', max=len(files))
    search_result = []
    counter = Counter()
    for file_path in files:
        if str(file_path).endswith(extension):
            search_result.append(Path(file_path))
            counter.loop_counter()
        bar.next()
    bar.finish()
    return search_result, counter.get_counter()


def search_more_extension(specific_type=None):
    bar = IncrementalBar('Searching', max=len(files))
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
            specific.append(Path(file_path))
        bar.next()
    bar.finish()
    return jpg, png, jpg_counter.get_counter(), png_counter.get_counter()


def search_large(size):
    bar = IncrementalBar('Searching', max=len(files))
    size = int(size) * 1048576
    large = []
    large_counter = Counter()
    for file in files:
        if Path(file).stat().st_size > size:
            large.append([file, Path(file).stat().st_size])
            large_counter.loop_counter()
        bar.next()
    return large, large_counter.get_counter()


def oldest(age_str):
    age = re.findall(r'\d+', age_str)
    out = []
    for i in age:
        age = int(i)
    if 'm' in age_str:
        age = age * 2629743.83
    if 'y' in age_str:
        age = age * 31556926

    for x in files:
        if (time.time() - Path(x).stat().st_birthtime) > age:
            out.append(x)
    return out


def check_len_duplicates():
    size_list = []
    for i in range(len(files)):
        size_list.append(Path(files[i]).stat().st_size)
    size_set = set(size_list)
    if not len(size_list) == len(size_set):
        duplicates = []
        bar = IncrementalBar('Searching duplicates', max=len(files))
        for i in range(0, len(files)):
            for j in range(i + 1, len(files)):
                if Path(files[i]).stat().st_size == Path(files[j]).stat().st_size:
                    duplicates.append([Path(files[i]).as_posix(), Path(files[j]).as_posix()])
            bar.next()
        return duplicates
    else:
        return None


def compare_hash(duplicates):
    out = []
    bar = IncrementalBar('Progress', max=len(duplicates))
    for i in range(len(duplicates)):
        file1 = duplicates[i][0]
        file2 = duplicates[i][1]
        with open(file1, "rb") as file_to_check:
            file1_data = file_to_check.read()
            file1_hash = hashlib.md5(file1_data).hexdigest()
        with open(file2, "rb") as file_to_check:
            file2_data = file_to_check.read()
            file2_hash = hashlib.md5(file2_data).hexdigest()
        if file1_hash == file2_hash:
            out.append([file1, file2])
        if not silent:
            bar.next()
    return out


if __name__ == '__main__':
    log = Logger()
    if args.silent:
        silent = True
        print('SHHHH! Silent mode')
        if args.output is None:
            log = Logger('log.txt')

    if args.output:
        print("file out mode")
        log = Logger(args.output)

    if args.path:
        scan_files(args.path)

    if args.duplicates:
        res = compare_hash(check_len_duplicates())
        if not silent:
            if not res == None:
                print('\nduplicate 1\t\t\t\t\t duplicate 2')
                for i in range(len(res)):
                    print(res[i][0], '\t', end=' ')
                    print(res[i][1], '\t')
        else:
            log.write_dual('duplicate 1\t\t\t\t\t\t\t\t\t\t duplicate 2', res)

    elif args.large:
        large = search_large(args.large)
        searched_large = large[0]
        if not silent:
            if len(searched_large) > 0:
                print("\nSearched %s files large of %s mb:" % (large[1], args.large))
                for i in range(len(searched_large)):
                    print(i+1, end='. ')
                    print(Path(searched_large[i][0]).name, round(searched_large[i][1]/1048576), 'mb')
            else:
                print("\nFiles large of %s mb not found! " % args.large)
        else:
            log.write("Searched %s files large of %s mb:" % (args.large, large[1]), searched_large)

    elif args.type:
        if args.type == 'images':
            searched_ext = search_more_extension()
            if not silent:
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
                        print(searched_ext[0][i])
                else:
                    print("Nothing found")
            if silent:
                log.write_only_title('searched %s images:' % (searched_ext[2]+searched_ext[3]))
                log.write('jpg (%s):' % searched_ext[2], searched_ext[0])
                log.write('png (%s):' % searched_ext[3], searched_ext[1])

        else:
            searched_ext = search_extension(args.type)
            if not searched_ext[1] == 0:
                if not silent:
                    print('\nsearched %s %s:' % (searched_ext[1], args.type))
                    for i in range(searched_ext[1]):
                        print(i + 1, end='. ')
                        print(searched_ext[0][i])
                elif silent:
                    log.write('searched %s %s:' % (searched_ext[1], args.type), searched_ext[0])

    elif args.old:
        old = oldest(args.old)
        if not silent:
            print("files older than %s:" % args.old)
            for i in range(len(old)):
                print(i + 1, end='. ')
                print(old[i])
        if silent:
            log.write("files older than %s:" % args.old, old)
    else:
        print('how did you do that? -_-')
