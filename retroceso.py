#!/usr/bin/env python3
"""
Practice 3: Backtracking Search
"""

import numpy as np
import time


def open_file(path):
    """
    Open the file at 'path' and read the test cases.
    Each test case consists of two lines:
      - The first line contains two integers (m, n) representing the grid dimensions.
      - The second line contains the control points' coordinates (space-separated).
    Returns a list where each element is a list containing the grid size followed by the coordinates.
    """
    tests = []
    with open(path, "r") as f:
        lines = f.readlines()
        # print(lines)
        for i in range(0, len(lines), 2):
            m, n = lines[i].split()
            size = [int(m), int(n)]
            figures = lines[i + 1].split()
            case_list = [size]
            for i in range(0, len(figures), 2):
                coords = [int(figures[i]) + 1, int(figures[i + 1]) + 1]
                case_list.append(coords)
            tests.append(case_list)
        return tests


def checkpoints(size):
    """
    Determine the checkpoint steps for a grid of size [m, n].
    Returns a list of three steps calculated as floor(m*n/4), floor(2*m*n/4), and floor(3*m*n/4).
    """
    steps = []
    for i in range(1, 4):
        steps.append(i * size[0] * size[1] // 4)
    return steps


def new_matrix(size):
    """
    Create a matrix of dimensions (m+2) x (n+2) with a border of 1 and inner cells set to 0,
    except cell (1,1) is initialized to 1.
    """
    matrix = np.empty((size[0] + 2, size[1] + 2))
    for i in range(size[0] + 2):
        for j in range(size[1] + 2):
            if (i == 0 or j == 0 or i == size[0] + 1 or j == size[1] + 1) or (
                i == 1 and j == 1
            ):
                matrix[i][j] = 1
            else:
                matrix[i][j] = 0
    return matrix


def verify_manhattan_dist(coord, point, current_step, total_steps):
    """
    Check if the Manhattan distance between 'coord' and 'point' is less than or equal to (total_steps - current_step).
    Returns True if so, otherwise False.
    """
    dist = abs(coord[0] - int(point[0])) + abs(coord[1] - int(point[1]))
    if dist > (int(total_steps) - current_step):
        return False
    else:
        return True


def verify_connectivity(matrix):
    """
    Check that all accessible cells (0s) in the grid can be reached from cell (1,1).
    Returns True if all accessible cells are reachable, otherwise False.
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


def create_marquee_matrix(matrix, coord):
    """
    Create a new matrix from 'matrix' by marking the cell at 'coord' with 1.
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
    Explore the neighbors of a partial solution to generate new solutions.
    """
    neighbors = [(1, 0), (0, -1), (0, 1), (-1, 0)]
    new_solutions = []
    current_coords = solution[-2]
    matrix = solution[-1]
    for i in range(len(neighbors)):
        x = neighbors[i][0] + current_coords[0]
        y = neighbors[i][1] + current_coords[1]
        if matrix[x][y] == 0:
            if x == int(target[0]) and y == int(target[1]):
                if current_step == checkpoint:
                    new_mat = create_marquee_matrix(matrix, (x, y))
                    if verify_connectivity(new_mat):
                        sol_copy = solution.copy()
                        sol_copy.pop()  # Remove matrix from end
                        sol_copy.append((x, y))
                        sol_copy.append(new_mat)
                        return_list.append(sol_copy)
            else:
                if verify_manhattan_dist((x, y), target, current_step, checkpoint):
                    new_mat = create_marquee_matrix(matrix, (x, y))
                    if verify_connectivity(matrix):
                        sol_copy = solution.copy()
                        sol_copy.pop()
                        sol_copy.append((x, y))
                        sol_copy.append(new_mat)
                        return_list.append(sol_copy)
    return return_list


def possible_paths(solutions, targets, checkpoints_list, total_steps):
    """
    Generate all possible paths that respect the target steps and checkpoints.
    """
    index = 0
    for step in range(2, total_steps + 1):
        if step > checkpoints_list[index]:
            index += 1
        new_list = []
        for solution in solutions:
            new_sol = explore_neighbors(
                solution, new_list, targets[index], checkpoints_list[index], step
            )
            if new_sol:
                new_list = new_sol
        if not new_list:
            return []
        solutions = new_list
    return new_list


def compare_solutions(list_one, list_two):
    """
    Compare two lists of solutions to extract compatible solutions.
    """
    solutions = []
    for sol1 in list_one:
        sol1_copy = sol1[:-1]
        for sol2 in list_two:
            sol2_copy = sol2[:-1]
            new_sol = sol1_copy.copy()
            for element in reversed(sol2_copy[1:-1]):
                if element in sol1_copy:
                    break
                new_sol.append(element)
            else:
                solutions.append(new_sol)
    return solutions


def final_program(input_path, output_path):
    """
    - Opens the input file
    - Calculates the possible paths according to the constraints
    - Writes the number of valid paths and the execution time to the output file
    """
    data = open_file(input_path)
    # Clear output file
    with open(output_path, "w") as f:
        f.close()
    # print("data:", data)
    for i in range(len(data)):
        start_case = time.time()
        size = data[i][0]
        matrix = new_matrix(size)
        total_steps = size[0] * size[1]
        targets = data[i][1:]
        targets.append((1, 1))
        checkpoint_steps = checkpoints(size)
        checkpoint_steps.append(total_steps + 1)
        solution_list = [[(1, 1), matrix]]
        if checkpoint_steps[0] == 1:
            if targets[0] != [1, 1]:
                solution = []
            else:
                targets.pop(0)
                checkpoint_steps.pop(0)
                solution = possible_paths(
                    solution_list, targets, checkpoint_steps, total_steps
                )
        else:
            solution = possible_paths(
                solution_list, targets, checkpoint_steps, total_steps
            )
        num_sol = len(solution)
        end_case = time.time()
        execution_time = end_case - start_case
        # print("return", num_sol, solution)
        with open(output_path, "a") as f:
            f.write(f"{num_sol} {execution_time:.6f}\n")


if __name__ == "__main__":
    input_path = "test.txt"  # file at project root
    output_path = "results.txt"  # file at project root
    total_start = time.time()
    final_program(input_path, output_path)
    total_end = time.time()
    total_exec_time = total_end - total_start
    # print(f"Total execution time: {total_exec_time:.6f} seconds")
