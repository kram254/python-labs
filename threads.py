import sys
import time
import threading
import os
from random import randint, random



if len(sys.argv) < 4:
    print('Arguments not enough..')
    exit(0)

num_files = int(sys.argv[1])
num_values = int(sys.argv[2])
mode = int(sys.argv[3])
folder = "files"

if not os.path.exists(folder):
    os.mkdir(folder)
else:
    for f in os.listdir(folder):
        os.remove(os.path.join(folder, f))


def generate_file():
    filename = str(random())+".txt"
    file = open(os.path.join(folder, filename), 'w')
    for i in range(1, num_values+1):
        file.write(str(randint(100, 999))+" ")

        if i % 30 == 0:
            file.write("\n")
    file.close()



def sumFile(filename):
    file = open(os.path.join(folder, filename))
    total = 0

    for line in file:
        total = total + sum([int(x) for x in line.split()])
    time.sleep(0.00001)
    return total


start_time = time.time()
for _ in range(num_files):
    generate_file()
end_time = time.time()

print('Duration to generate %d files with %d values each is %.4f seconds' %
      (num_files, num_values, end_time-start_time))


def process_sequential():
    start_time = time.time()
    for filename in os.listdir(folder):
        sumFile(filename)

    end_time = time.time()
    print('Time to sum data from %d files is %.4f seconds' %
          (num_files, end_time-start_time))


def process_parallel():
    start_time = time.time()
    thread_list = []
    for filename in os.listdir(folder):
        th = threading.Thread(target=sumFile, args=(filename,))
        th.start()
        thread_list.append(th)
    for th in thread_list:
        th.join()

    end_time = time.time()
    print('Time to sum data from %d files is %.4f seconds' %
          (num_files, end_time-start_time))


if mode == 0:
    print('Executing program in serial mode')
    process_sequential()
elif mode == 1:
    print('Executing program in parallel mode')
    process_parallel()
else:
    print('Invalid mode')