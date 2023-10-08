parametros="T=26\nM=6\nP=10"
linha1= "= = = = = = = = = =\n"
linha2= "= @ . * . . * . . =\n"
linha3= "= . = = = = = = . =\n"
linha4= "= . = F . . . . . =\n"
linha5= "= . = . . . . . . =\n"
linha6= "= . = . . . . . . =\n"
linha7= "= . = . . . . . . =\n"
linha8= "= * . . . . . . . =\n"
linha9= "= . . . . . . . . =\n"
linha10="= = = = = = = = = =\n"
grelha=linha1+linha2+linha3+linha4+linha5+linha6+linha7+linha8+linha9+linha10
mundoStandard=parametros + "\n" + grelha

from searchPlus import Problem
from game import *

class MedoTotal(Problem):    
    def __init__(self, situacaoInicial=mundoStandard):
        params = situacaoInicial.split("\n")
        self.conditions = GameConditions.from_list(params[:3])
        self.board = Board.from_input(params[3:])
        self.initial = GameState.from_board(self.board, self.conditions.M)
   
    def actions(self, state: GameState):
        state: GameState = state
        available_actions = GameSolver.find_valid_directions(state)
        return available_actions
        
        
    def result(self, state: GameState, action: str):
        state: GameState = state
        new = state.copy()
        return Game.apply(new, action, self.conditions.P)
    
    def path_cost(self, c: int, state1: GameState, action: str, next_state: GameState):
        pacman_next_position = next_state.pacman.get_position()

        #if state1 == next_state:
        #    return c
        
        movement_cost = state1.pacman.get_cost(pacman_next_position)        
        return c + movement_cost
    
    def goal_test(self, state: GameState):
        return state.pacman.get_steps() == self.conditions.T
    
    def executa(self,state,actions):
        """Partindo de state, executa a sequência (lista) de acções (em actions) e devolve o último estado"""
        nstate=state
        for a in actions:
            nstate=self.result(nstate,a)
        return nstate
    
    def display(self, state: GameState):
        """Devolve a grelha em modo txt"""
        return str(state.board)



	
g = MedoTotal()

print(g.board)
print(g.actions(g.initial))
