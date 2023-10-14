from problem.searchPlus import Problem
from pacman.game.common import GameConditions, GameState
from pacman.game.solvers import GameSolver
from pacman.game.board import Board
from pacman.elements.common import Element

parametrosB="T=26\nM=6\nP=10"
linha1B= "= = = = = = = = = =\n"
linha2B= "= @ . * . . * . . =\n"
linha3B= "= . = = = = = = . =\n"
linha4B= "= . = F . . . . . =\n"
linha5B= "= . = . . . . . . =\n"
linha6B= "= . = . . . . . . =\n"
linha7B= "= . = . . . . . . =\n"
linha8B= "= * . . . . . . . =\n"
linha9B= "= . . . . . . . . =\n"
linha10B="= = = = = = = = = =\n"
grelhaB=linha1B+linha2B+linha3B+linha4B+linha5B+linha6B+linha7B+linha8B+linha9B+linha10B
mundoStandard=parametrosB + "\n" + grelhaB

class PacmanProblem(Problem):    
    def __init__(self, situacaoInicial=mundoStandard):
        params = situacaoInicial.split("\n")
        self.conditions = GameConditions.from_list(params[:3])
        self.board = Board.from_input(params[3:])
        self.initial = GameState.from_board(self.board, self.conditions.M)
   
    def actions(self, state: GameState):
        state: GameState = state
        pacman, ghost, supergums, board = state
        fear_needed = self.conditions.T - (pacman.get_steps() + ghost.get_fear())

        if fear_needed > 0:
            if not len(supergums):
                return []
            
            _, distant_to_closest_gum = board.find_closest(pacman.get_position(), Element.SUPER_GUM)
            if distant_to_closest_gum > ghost.get_fear():
                return []
            
            if distant_to_closest_gum + (len(supergums) * self.conditions.P) < self.conditions.T - pacman.get_steps():
                return []
    
        available_actions = GameSolver.find_valid_directions(state)
        return available_actions
        
        
    def result(self, state: GameState, action: str):
        state: GameState = state
        new = state.copy()
        return GameSolver.apply(new, action, self.conditions.P)
    
    def path_cost(self, c: int, state1: GameState, action: str, next_state: GameState):
        pacman_next_position = next_state.pacman.get_position()

        if state1 == next_state:
            return c
        
        movement_cost = state1.pacman.get_cost(pacman_next_position)        
        return c + movement_cost
    
    def goal_test(self, state: GameState):
        return state.pacman.get_steps() == self.conditions.T
    
    def executa(p,estado,accoes,verbose=False):
        """Executa uma sequência de acções a partir do estado devolvendo o triplo formado pelo estado, 
        pelo custo acumulado e pelo booleano que indica se o objectivo foi ou não atingido. Se o objectivo for atingido
        antes da sequência ser atingida, devolve-se o estado e o custo corrente.
        Há o modo verboso e o não verboso, por defeito."""
        custo = 0
        for a in accoes:
            seg = p.result(estado,a)
            custo = p.path_cost(custo,estado,a,seg)
            estado = seg
            objectivo=p.goal_test(estado)
            if verbose:
                print(f"Applying action {a}....")
                print(f"{estado}")
                print(p.display(estado))
                print('Custo Total:',custo)
                print('Atingido o objectivo?', objectivo)
            if objectivo:
                break
        return (estado,custo,objectivo)
    
    def display(self, state: GameState):
        """Devolve a grelha em modo txt"""
        return str(state.board)