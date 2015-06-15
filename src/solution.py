__author__ = 'Zhong Zhang'

'''
(1) Word Count
Idea:
use a map to store the word as the key and its associated occurrences as the value.

(2) Stream Median
Idea:
The key of the problem is how to insert the coming number into the existed array efficiently.
One of the optimal solutions is to use balanced binary search tree, insertion is O(logN) and
finding median is O(1). However, the implementation of balanced binary search tree, for example
AVL, is pretty complexity. We can achieve the same time complexity by maintaining two heaps
simultaneously, a max-heap and min-heap.

The max-heap is used to store the smallest half of the numbers and min-heap contains the largest
half which means the maximum element in the max-heap is less than the minimum element in the
min-heap. If the number of elements is even, the max-heap and min-heap contain half of the
elements separately. If the number is odd, the max-heap has one more element than the min-heap.

Zhong Zhang @ UTA @ 6/15/2015
'''
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
        if self.count % 2 == 0: #self.count % 2 == 0 ==> even ==> insert new element to max_heap
            heapq.heappush(self.max_heap, -1*num)
            self.count = self.count + 1
            if len(self.min_heap) > 0:
                if -1*self.max_heap[0] > self.min_heap[0]:     # if maximum element in max_heap >= minimum element in min_heap
                    max_left = -1*heapq.heappop(self.max_heap) # adjust max_heap and min_heap
                    min_right = heapq.heappop(self.min_heap)
                    heapq.heappush(self.max_heap, -1*min_right)
                    heapq.heappush(self.min_heap, max_left)
        else: #self.count % 2 != 0 ==> odd ==> insert new element to min_heap
            max_left = -1*heapq.heappushpop(self.max_heap, -1*num) #compare the current element with the maximum element
            heapq.heappush(self.min_heap, max_left)                #in the max_heap and the larger one is inserted to
            self.count = self.count + 1                            #min_heap

    def get_median(self):
        if self.count % 2 == 0:
            return (-1*self.max_heap[0] + self.min_heap[0]) / 2.0
        else:
            return -1*self.max_heap[0]

class word_counter:
    def __init__(self, src_fullfiles):
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

    def list_txtfiles(self, src_dir): #get all txt files in a directorys
        txtfiles = []
        for file in os.listdir(src_dir):
            if fnmatch.fnmatch(file, '*.txt'):
                txtfiles.extend([file])
        return txtfiles

    def word_count(self):
        counter = word_counter(self.fullfiles)
        word_and_counts = counter.count_word()
        sorted_word_and_counts = sorted(word_and_counts.items(), key=operator.itemgetter(0))

        destfile = self.dest_file_q1
        with open(destfile, "w") as file_stream: #output word counting results
            for item in sorted_word_and_counts:
                file_stream.write("{0}\t{1}\n".format(item[0], item[1]))

    def running_median(self):
        median_calculator = stream_median()
        destfile = self.dest_file_q2
        with open(destfile, "w") as output_stream:
            for fullfile in self.fullfiles: #per file
                with open(fullfile, "r") as file_stream:
                    for line in file_stream: #per line
                        line1 = re.sub(r'[^a-zA-Z0-9\s]+', "", line).lower().strip()
                        word_size = len(line1.split())
                        median_calculator.insert(word_size)
                        median = median_calculator.get_median()
                        output_stream.write("{0}\n".format(int(median*10)/10.0))

def solver(src_dir, dest_file_q1, dest_file_q2):
    ide_solver = insight_data_engineering_solver(src_dir, dest_file_q1, dest_file_q2)
    ide_solver.word_count()
    ide_solver.running_median()

if __name__ == "__main__":
    params=sys.argv[1:]
    solver(*params)
