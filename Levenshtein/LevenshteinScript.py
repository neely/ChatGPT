# python script.py input.csv output.csv

import csv
import sys

def levenshtein_distance(s1, s2, num_penalty):
    s1 = s1.lower()
    s2 = s2.lower()
    
    m = len(s1) + 1
    n = len(s2) + 1
    dp = [[0 for j in range(n)] for i in range(m)]
    
    for i in range(1, m):
        dp[i][0] = i
    for j in range(1, n):
        dp[0][j] = j
    
    for i in range(1, m):
        for j in range(1, n):
            cost = 0
            if s1[i-1].isdigit() != s2[j-1].isdigit():
                cost = num_penalty
            dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)
            
    return dp[m-1][n-1]

num_penalty = 20

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, "r") as in_file, open(output_file, "w", newline='') as out_file:
    reader = csv.reader(in_file)
    writer = csv.writer(out_file)
    
    header = next(reader)
    header.append("distance")
    writer.writerow(header)
    
    for row in reader:
        s1 = row[0]
        s2 = row[1]
        distance = levenshtein_distance(s1, s2, num_penalty)
        row.append(distance)
        writer.writerow(row)
