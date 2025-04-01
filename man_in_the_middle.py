#!/usr/bin/env python3
"""
Practice 3: Backtracking Search
"""

import numpy as np
import time


def open_file(path):
    """
    Opens the file at 'path' and reads the test cases.
    Each test case consists of two lines:
      - The first line contains two integers (m, n) for the grid dimensions.
      - The second line contains the control point coordinates.
    Returns a list where each element is a list starting with the grid size followed by the coordinates.
    """
    tests = []
    with open(path, "r") as f:
        lines = f.readlines()
        for i in range(0, len(lines), 2):
            m, n = lines[i].split()
            size = [int(m), int(n)]
            figures = lines[i + 1].split()
            case_list = [size]
            for i in range(0, len(figures), 2):
                coordinates = [int(figures[i]) + 1, int(figures[i + 1]) + 1]
                case_list.append(coordinates)
            tests.append(case_list)
        return tests


def get_checkpoints(size):
    """
    Determines the control steps for a grid of dimensions [m, n].
    Returns a list of three steps: floor(m*n/4), floor(2*m*n/4) and floor(3*m*n/4).
    """
    steps = []
    for i in range(1, 4):
        steps.append(i * size[0] * size[1] // 4)
    return steps


def new_matrix(size):
    """
    Creates a matrix of dimensions (m+2) x (n+2) with a border of 1 and the interior set to 0,
    except that cell (1,1) is initialized to 1.
    """
    matrix = np.empty((size[0] + 2, size[1] + 2))
    for i in range(0, size[0] + 2):
        for j in range(0, size[1] + 2):
            if (i == 0 or j == 0 or i == size[0] + 1 or j == size[1] + 1) or (
                i == 1 and j == 1
            ):
                matrix[i][j] = 1
            else:
                matrix[i][j] = 0
    return matrix


def verify_manhattan_dist(coord, target, step, step_target):
    """
    Checks if the Manhattan distance between 'coord' and 'target' is less than or equal to (step_target - step).
    Returns True if it is, otherwise False.
    """
    dist = abs(coord[0] - int(target[0])) + abs(coord[1] - int(target[1]))
    if dist > (int(step_target) - step):
        return False
    else:
        return True


def check_connectivity(matrix):
    """
    Checks that from cell (1,1), all accessible cells (with value 0) are reachable.
    Returns True if connectivity is ensured, otherwise False.
    """
    visited = np.zeros_like(matrix)
    neighbors = [(1, 0), (0, -1), (0, 1), (-1, 0)]
    new_neighbors = []
    for i, j in neighbors:
        x = 1 + i
        y = 1 + j
        if matrix[x][y] == 0:
            new_neighbors.append((x, y))
            visited[x][y] = 2
    if not new_neighbors:
        return False
    while new_neighbors:
        x, y = new_neighbors.pop(0)
        for i, j in neighbors:
            new_x = x + i
            new_y = y + j
            if matrix[new_x, new_y] == 0 and visited[new_x, new_y] != 2:
                visited[new_x, new_y] = 2
                new_neighbors.append((new_x, new_y))
    for i in range(1, matrix.shape[0] - 1):
        for j in range(1, matrix.shape[1] - 1):
            if matrix[i][j] == 0:
                if visited[i][j] != 2:
                    return False
    return True


def create_highlighted_matrix(matrix, coord):
    """
    Creates a new matrix from 'matrix' by marking the cell at 'coord' with 1.
    """
    new_mat = np.empty((matrix.shape[0], matrix.shape[1]))
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if i == coord[0] and j == coord[1]:
                new_mat[i][j] = 1
            else:
                new_mat[i][j] = matrix[i][j]
    return new_mat


def explore_neighbors(solution, return_list, target, checkpoint, current_step):
    """
    Explores the neighbors of a partial solution to generate new solutions.
    """
    neighbors = [(1, 0), (0, -1), (0, 1), (-1, 0)]
    current_coord = solution[-2]
    matrix = solution[-1]
    for i in range(len(neighbors)):
        new_x = neighbors[i][0] + current_coord[0]
        new_y = neighbors[i][1] + current_coord[1]
        if matrix[new_x][new_y] == 0:
            if new_x == int(target[0]) and new_y == int(target[1]):
                if current_step == checkpoint:
                    new_mat = create_highlighted_matrix(matrix, (new_x, new_y))
                    if check_connectivity(new_mat):
                        new_solution = solution.copy()
                        new_solution.pop()
                        new_solution.append((new_x, new_y))
                        new_solution.append(new_mat)
                        return_list.append(new_solution)
            else:
                if verify_manhattan_dist(
                    (new_x, new_y), target, current_step, checkpoint
                ):
                    new_mat = create_highlighted_matrix(matrix, (new_x, new_y))
                    if check_connectivity(matrix):
                        new_solution = solution.copy()
                        new_solution.pop()
                        new_solution.append((new_x, new_y))
                        new_solution.append(new_mat)
                        return_list.append(new_solution)
    return return_list


def possible_paths(solution_list, targets, checkpoints_val, total_steps):
    """
    Generates all possible valid paths (solutions) that satisfy the constraints.
    """
    index = 0
    if checkpoints_val[0] == 1:
        if targets[0] != [1, 1]:
            return []
        else:
            targets.pop(0)
            checkpoints_val.pop(0)
    for i in range(2, total_steps + 1):
        if i > checkpoints_val[index]:
            index += 1
        new_list = []
        for sol in solution_list:
            new_sol = explore_neighbors(
                sol, new_list, targets[index], checkpoints_val[index], i
            )
            if new_sol:
                new_list = new_sol
        if not new_list:
            return []
        solution_list = new_list
    return new_list


def compare_solutions(list_one, list_two):
    """
    Compares two lists of solutions to extract compatible solutions.
    """
    solutions = []
    for sol_one in list_one:
        sol_one_copy = sol_one[:-1]
        for sol_two in list_two:
            sol_two_copy = sol_two[:-1]
            new_sol = sol_one_copy.copy()
            for element in reversed(sol_two_copy[1:-1]):
                if element in sol_one_copy:
                    break
                new_sol.append(element)
            else:
                solutions.append(new_sol)
    return solutions


def final_program(input_path, output_path):
    """
    Main program:
      - Opens the input file
      - Computes the possible paths according to the constraints
      - Writes the number of valid solutions and the execution time (in milliseconds)
        to the output file.
    """
    data = open_file(input_path)
    with open(output_path, "w") as f:
        f.close()
    # print("data:", data)
    for i in range(len(data)):
        start_time = time.time()
        size = data[i][0]
        matrix = new_matrix(size)
        total_steps = size[0] * size[1]
        targets = data[i][1:]
        targets.append((1, 1))
        checkpoints_val = get_checkpoints(size)
        checkpoints_val.append(total_steps + 1)
        solution_list = [[(1, 1), matrix]]
        if checkpoints_val[0] == 1:
            if targets[0] != [1, 1]:
                sol = []
            else:
                targets.pop(0)
                checkpoints_val.pop(0)
                sol = possible_paths(
                    solution_list, targets, checkpoints_val, total_steps
                )
        else:
            sol = possible_paths(solution_list, targets, checkpoints_val, total_steps)
        num_sol = len(sol)
        end_time = time.time()
        exec_time = (end_time - start_time) * 1000  # milliseconds
        # print("return", num_sol, sol)
        with open(output_path, "a") as f:
            f.write(f"{num_sol} {exec_time:.6f}\n")


if __name__ == "__main__":
    input_path = "test.txt"
    output_path = "results_man_in_the_middle.txt"
    final_program(input_path, output_path)
