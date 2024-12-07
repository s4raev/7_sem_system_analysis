import json
from collections import defaultdict


json_a = "[1,[2,3],4,[5,6,7],8,9,10]"
json_b = "[[1,2],[3,4,5],6,7,9,[8,10]]"

def get_matrix(ranks):
    
    rank_by_user = defaultdict(int)
    for i, users in enumerate(ranks[::-1]):
        rank = i + 1 
        if isinstance(users, list):
            for user in users :
               rank_by_user[user] = rank
            continue
        rank_by_user[users] = rank

    user_count = len(rank_by_user)  
    matrix = [[0] * user_count for _ in range(user_count)]
    for i in range(user_count):
        for j in range(user_count):
            if rank_by_user[i+1] >= rank_by_user[j+1]:
                matrix[i][j] = 1
    
    return matrix


def main(json_a, json_b):
    rank_a = json.loads(json_a)
    rank_b = json.loads(json_b)

    matrix_a = get_matrix(rank_a)
    matrix_b = get_matrix(rank_b)

    count = len(matrix_a)

    matrix_ab = [[0] * count for _ in range(count)]

    for i in range(count):
        for j in range(count):
            matrix_ab[i][j] = matrix_a[i][j] * matrix_b[i][j]

    transpose_matrix_ab = [[matrix_ab[j][i] for j in range(count)] for i in range(count)]

    conflict_kernel = []
    for i in range(count):
        for j in range(i + 1, count):
            if matrix_ab[i][j] + transpose_matrix_ab[i][j] == 0:
                conflict_kernel.append([i + 1, j + 1])
    return json.dumps(conflict_kernel)

if __name__ == "__main__":
    res = main(json_a, json_b)
    print(res)
