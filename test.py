import sys
import csv
import os


copy_to_lineEdit = ''
copy_to_lineEdit2 = 'asdasdasd, ,asdf, ,a,f as ,'

def create_address_cache():
    dir = os.path.dirname(__file__)
    csv_filename = os.path.join(dir, 'address_cache.csv')

    if not os.path.exists(csv_filename):
        with open(csv_filename, 'w'): pass

create_address_cache()

def returnNotMatches(a, b):
    a = set(a)
    b = set(b)
    return [list(b - a), list(a - b)]

def foo(L1, L2):
    t = list(set(L1) & set(L2))
    return t

def read_csv():
    dir = os.path.dirname(__file__)
    csv_filename = os.path.join(dir, 'address_cache.csv')
    ifile = open(csv_filename, "rb")
    reader = csv.reader(ifile)
    for row in reader:
        pass
    return row

def write_csv():
    copy_to = [''.join(copy_to_lineEdit2.split())]
    copy_to = copy_to[0].split(',')
    copy_to = filter(None, copy_to)
    # print(copy_to)
    dir = os.path.dirname(__file__)
    csv_filename = os.path.join(dir, 'address_cache.csv')

    if os.stat(csv_filename).st_size == 0:
        L3 = copy_to
        ifile = open(csv_filename, "wb")

        spamwriter = csv.writer(ifile, sys.stdout, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(L3)
        ifile.close()
    elif copy_to == '':
        ifile = open(csv_filename, "rb")
        ifile.close()
    elif copy_to != read_csv():

        L2 = copy_to
        a = read_csv()
        t = returnNotMatches(a, L2)
        g = [j for i in t for j in i]
        print(g)
        c = foo(read_csv(), L2)
        ifile = open(csv_filename, "wb")

        spamwriter = csv.writer(ifile, sys.stdout, delimiter=",", quoting=csv.QUOTE_NONE)
        spamwriter.writerow(c + g)
        ifile.close()
    else:
        ifile = open(csv_filename, "rb")
        ifile.close()

# print('read: ' + str(read_csv()))

# print('write: ' + str(write_csv()))

write_csv()

# print('intersection')
# print(foo(read_csv(), write_csv()))
# print(returnNotMatches(read_csv(), write_csv()))
