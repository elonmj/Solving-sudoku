from typing import Dict, Tuple
from ortools.sat.python import cp_model

from sudoku.models.board import Board 

class SudokuSolver:
    def __init__(self, board: Board):
        self.board = board
        self.initial_grid = board.grid
        
    def solve(self) -> Dict[Tuple[int, int], int]:
        """
        Résout le Sudoku et retourne un dictionnaire des solutions.
        
        :return: Dictionnaire avec les coordonnées en clé et la valeur solution en valeur
        """
        # Créer le modèle CP
        model = cp_model.CpModel()
        
        # Variables de décision
        variables = {}
        for (row, col), value in self.initial_grid.items():
            if value == 0:
                variables[(row, col)] = model.NewIntVar(1, 9, f'cell_{row}_{col}')
            else:
                variables[(row, col)] = model.NewConstant(value)
        
        # Contraintes de ligne
        for row in range(9):
            row_vars = [variables[(row, col)] for col in range(9)]
            model.AddAllDifferent(row_vars)
        
        # Contraintes de colonne
        for col in range(9):
            col_vars = [variables[(row, col)] for row in range(9)]
            model.AddAllDifferent(col_vars)
        
        # Contraintes de sous-grille 3x3
        for block_row in range(0, 9, 3):
            for block_col in range(0, 9, 3):
                block_vars = [
                    variables[(row, col)] 
                    for row in range(block_row, block_row + 3)
                    for col in range(block_col, block_col + 3)
                ]
                model.AddAllDifferent(block_vars)
        
        # Résolution
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        
        # Retourner les solutions trouvées
        solutions = {}
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            for (row, col), var in variables.items():
                solutions[(row, col)] = solver.Value(var)
                
        return solutions

def solve_sudoku(board: Board) -> Dict[Tuple[int, int], int]:
    """
    Fonction utilitaire pour résoudre un Sudoku.
    
    :param board: Grille de Sudoku à résoudre 
    :return: Dictionnaire des solutions trouvées
    """
    solver = SudokuSolver(board)
    return solver.solve()