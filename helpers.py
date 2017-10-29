from enum import Enum


class Operation(Enum):
    """Operations"""

    DELETED = 1
    INSERTED = 2
    SUBSTITUTED = 3

    def __str__(self):
        return str(self.name.lower())


def distances(a, b):
    """Calculate edit distance from a to b"""
    cost = []

    # Fill list with len(a) + 1 number of lists to act as the rows
    for row in range(len(a) + 1):
        cost.append([])

        # Fill rows with default data
        if row == 0:
            cost[row].append((row, None))
        else:
            cost[row].append((row, Operation.DELETED))

    # Fill each column in row 0 with default data
    for col in range(1, len(b) + 1):
        cost[0].append((col, Operation.INSERTED))

    # Call recursive helper method for the bottom right corner and return the matrix
    calc_dist(cost, a, b, len(a), len(b))
    return cost


def calc_dist(cost, a, b, i, j):
    # Base case where we are at default data, return that entry
    if i == 0 or j == 0:
        return cost[i][j]

    # If we have already calculated that operation, return it
    if i < len(cost) and j < len(cost[i]):
        return cost[i][j]

    # Calculate the deletion, insertion, and substitution costs
    deletion_cost = calc_dist(cost, a, b, i - 1, j)[0] + 1
    insertion_cost = calc_dist(cost, a, b, i, j - 1)[0] + 1
    substitution_cost = calc_dist(cost, a, b, i - 1, j - 1)[0]

    if not a[i - 1] == b[j - 1]:
        # Add one to substitution cost if the letters do not already match
        substitution_cost += 1

    # Set final to correct tuple of cost and operation
    if deletion_cost <= insertion_cost and deletion_cost <= substitution_cost:
        # Deletion is the best choice
        final = (deletion_cost, Operation.DELETED)
    elif insertion_cost <= deletion_cost and insertion_cost <= substitution_cost:
        # Insertion is best choice
        final = (insertion_cost, Operation.INSERTED)
    else:
        # Substitution is best choice
        final = (substitution_cost, Operation.SUBSTITUTED)

    # Add the tuple to the array and return the tuple for subsequent recursion
    cost[i].append(final)
    return final
