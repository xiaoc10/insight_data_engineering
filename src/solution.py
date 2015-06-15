__author__ = 'Zhong Zhang'

import fnmatch
import os
import re
import operator
import heapq
import sys

class stream_median:
    def __init__(self):
        self.min_heap = []
        self.max_heap = []
        self.count = 0

    def insert(self, num):
        if self.count % 2 == 0:
            heapq.heappush(self.max_heap, -1*num)
            self.count = self.count + 1
            if len(self.min_heap) > 0:
                if -1*self.max_heap[0] > self.min_heap[0]:
                    max_left = -1*heapq.heappop(self.max_heap)
                    min_right = heapq.heappop(self.min_heap)
                    heapq.heappush(self.max_heap, -1*min_right)
                    heapq.heappush(self.min_heap, max_left)
        else:
            max_left = -1*heapq.heappushpop(self.max_heap, -1*num)
            heapq.heappush(self.min_heap, max_left)
            self.count = self.count + 1

    def get_median(self):
        if self.count % 2 == 0:
            return (-1*self.max_heap[0] + self.min_heap[0]) / 2.0
        else:
            return -1*self.max_heap[0]

class word_counter:
    def __init__(self, src_fullfiles):
        #self.list_txtfiles(src_dir)
        self.fullfiles = src_fullfiles

    def count_word(self):
        word_and_counts = {}

        for fullfile in self.fullfiles: #per file
            with open(fullfile, "r") as file_stream:
                for line in file_stream: #per line
                    line1 = re.sub(r'[^a-zA-Z0-9\s]+', "", line).lower().strip()
                    for word in line1.split(): #per word
                        if word not in word_and_counts:
                            word_and_counts[word] = 1
                        else:
                            word_and_counts[word] = word_and_counts[word] + 1

        return word_and_counts

class insight_data_engineering_solver:
    def __init__(self, src_dir, dest_file_q1, dest_file_q2):
        self.src_dir = src_dir
        self.dest_file_q1 = dest_file_q1
        self.dest_file_q2 = dest_file_q2
        self.txtfiles = self.list_txtfiles(src_dir)
        self.fullfiles = [os.path.join(self.src_dir, txtfile) for txtfile in self.txtfiles ]
        #print(self.fullfiles)

    def list_txtfiles(self, src_dir):
        txtfiles = []
        for file in os.listdir(src_dir):
            if fnmatch.fnmatch(file, '*.txt'):
                txtfiles.extend([file])
        return txtfiles

    def word_count(self):
        #src_fullfiles = [os.path.join(self.src_dir, txtfile) for txtfile in self.txtfiles ]
        counter = word_counter(self.fullfiles)
        word_and_counts = counter.count_word()
        sorted_word_and_counts = sorted(word_and_counts.items(), key=operator.itemgetter(0))

        #output word counting results
        #destfile = os.path.join(self.src_dest, "wc_result.txt")
        destfile = self.dest_file_q1
        with open(destfile, "w") as file_stream:
            for item in sorted_word_and_counts:
                file_stream.write("{0}\t{1}\n".format(item[0], item[1]))
                #file_stream.write("{0}\t{1}" % item[0], item[1])
        #print(sorted_x)

    def running_median(self):
        median_calculator = stream_median()
        #destfile = os.path.join(self.src_dest, "med_result.txt")
        destfile = self.dest_file_q2
        with open(destfile, "w") as output_stream:
            for fullfile in self.fullfiles: #per file
                with open(fullfile, "r") as file_stream:
                    for line in file_stream: #per line
                        line1 = re.sub(r'[^a-zA-Z0-9\s]+', "", line).lower().strip()
                        word_size = len(line1.split()) #eliminate empty line
                        #print(word_size)
                        median_calculator.insert(word_size)
                        median = median_calculator.get_median()
                        output_stream.write("{0}\n".format(int(median*10)/10.0))
                        #print(format())
                        #print("%.*f" % (median_calculator.get_median(), 1))

def solver(src_dir, dest_file_q1, dest_file_q2):
    #solver = insight_data_engineering_solver("..\wc_input", "..\wc_output")
    #print(src_dir, dest_file_q1, dest_file_q2)
    ide_solver = insight_data_engineering_solver(src_dir, dest_file_q1, dest_file_q2)
    ide_solver.word_count()
    ide_solver.running_median()

if __name__ == "__main__":
    params=sys.argv[1:]
    solver(*params)

#solver("..\wc_input", "..\wc_output\wc_result.txt", "..\wc_output\med_result.txt")

'''
counter = word_counter("..\wc_input")
word_and_counts = counter.count_word()
sorted_x = sorted(word_and_counts.items(), key=operator.itemgetter(0))
print(sorted_x)
'''
'''
def word_count(src_files):
def print_result():
#txt_files = []
for file in os.listdir('../wc_input'):
    if fnmatch.fnmatch(file, '*.txt'):
        #word_count(file, dest_file)
        #txt_files.extend([file])
        txt_files = txt_files + [file]
word_count(txt_files)
print(txt_files)
'''
