I used python 3.9 to create this project

Running the program
1) py ./main.py

2) example inputs from Project 1 writeup (ctrl + c, ctrl + v ready)
YARD-1:
1 2 1 3 3 5 4 5 2 6 5 6
* e empty bca empty d
*abcde empty empty empty empty empty

YARD-2:
1 2 1 5 2 3 2 4
* d b ae c
*abcde empty empty empty empty

YARD-3:
1 2 1 3
* a b
*ab empty empty

YARD-4:
1 2 1 3 1 4
*a bc d
*abcd empty empty empty

YARD-5:
1 2 1 3 1 4
* a cb d
*abcd empty empty empty

AI Usage 
Initially, I did not use LLMs up through problem 3. However, I got a fever on Tuesday, which
made it much harder to think and stay focused. From then on, I used AI fairly extensively.
Most bugs I had were solved with AI, any refactors, and I asked it to implement most of the functionality.
I came up with the algorithms to do, mentioned the constraints, and went from there. I did also have it generate
a draw_yard function, which made it much easier for me to debug my code

===Problem 1===
    ran in main.py

===Problem 2===
    result function in yard.py

===Problem 3===
    expected_states function in yard.py

===Problem 4===
    I chose the iterative deepening DFS algorithm

    Iterative deepending DFS is optimal because it always finds the optimal
    solution through an exhaustive search at each level.

    It avoids the pitfalls of other blind searches
    -BFS: high memory usage
    -DFS: can get trapped
    -DLS: required to guess some depth limit
    

===Problem 5===
    States(c,t) represents the number of possible states for c and t
    
    States(c, t) = (c)! * C(c+t, t-1)
    C(n, k) = n! / (k! * (n-k)!) <-- binomial coefficient, n Choose k
    
    (c)! <-- ways to order all cars (including the engine)
    C(n,k) <-- ways to split car sequences among each track/allow for empty
    
    Yard 3 Example:
        yard_inputs = 1 2 1 3
        init_state = * a b
        There are 3 cars, and 3 tracks
        States(3,3) = 3! * C(5,2) = 6 * 10 = 60 states

===Problem 6===
    For the heuristic, I used 
    h(S) = sum over cars x of dist(pos(x), goal(x))
    where dist(u,v) is the shortest number of edges between tracks u and v.

    A car that is k edges away from its goal must take at least k moves. 
    Summing across cars gives a lower bound. This never overestimates, so 
    the heuristic is admissible (and consistent).

    I chose the A* algorithm, where f = g + h
    We chose A* search with f = g + h.

    A* is complete and optimal with an admissible, consistent heuristic.

    It prunes the search tree aggressively, giving a 2-3x speedup (or more) compared to IDDFS.
    If memory is too large (e.g., Yard-1), the same heuristic can be used in IDA* for optimal solutions with DFS-like memory.

    Node structure:
    Each node stores: state, parent, action_from_parent, g (path cost), and f = g+h.

===Timing and Speedup Writeup===
    Here is the output of my program based on the example inputs

    === Timing & Speedup (IDDFS vs A*) ===
    Yard 1: IDDFS 3.5067s, exp=2451876, actions=0 | A* 0.3348s, exp=22735, actions=22 | Speedup time 10.47x, nodes 107.85x
    Yard 2: IDDFS 0.6167s, exp=430662, actions=14 | A* 0.0184s, exp=2076, actions=14 | Speedup time 33.50x, nodes 207.45x
    Yard 3: IDDFS 0.0000s, exp=10, actions=2 | A* 0.0000s, exp=4, actions=2 | Speedup time 0.58x, nodes 2.50x
    Yard 4: IDDFS 0.0002s, exp=140, actions=4 | A* 0.0002s, exp=24, actions=4 | Speedup time 0.72x, nodes 5.83x
    Yard 5: IDDFS 0.0016s, exp=1260, actions=6 | A* 0.0012s, exp=130, actions=6 | Speedup time 1.28x, nodes 9.69x

    On the small yards (3–5), the difference between uninformed IDDFS and informed A* was modest. The search space is 
    so small that IDDFS can quickly find a solution, and the heuristic overhead sometimes even outweighs the benefits.

    On the larger yards (1–2), the difference was dramatic.
        Yard 1: The numbers are a bit misleading here. Based on actions=0, we know that the ID_DFS program could not
            find a solution with a max depth of 15. Even then, it took 3.5 seconds to search the 2451876 nodes. A* 
            concluded its search in only 0.3348s
        Yard 2: This is a better numerical representation. A* was ~33x faster and ~200x fewer nodes expanded.


    This shows the main strength of informed search: once the search space becomes large, 
    an admissible heuristic drastically reduces the number of nodes explored while still guaranteeing optimality.




