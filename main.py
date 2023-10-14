from problem.pacmanProblem import PacmanProblem
from problem.searchPlus import depth_first_graph_search, depth_first_graph_search_count


	
gx = PacmanProblem()
result, expanded = depth_first_graph_search_count(gx)
if result:
    print(f"Solution Prof-prim (graph) with cost {result.path_cost}: {result.solution()}")
else:
    print('No solution')
print(f"Expanded = {expanded}")