import time
from yard import *

def filter_yard_input(yard_input: str) -> list:
    yard_input = yard_input.replace(" ", "")
    yard_filtered = []
    for i in range(0, len(yard_input), 2):
        yard_filtered.append([int(yard_input[i]), int(yard_input[i + 1])])
    return yard_filtered

def possible_actions_to_str(yard: Yard, state: State) -> str:
    pa_ty = possible_actions(yard, state)
    return "\t".join(str(act) for act in pa_ty)

def run_problem1(yards: list):
    print("=== PROBLEM 1 [10 pts] - possible_actions ===")
    for idx, ty in enumerate(yards, start=1):
        print(f"Yard {idx}")
        print(f"INIT-STATE-{idx} {possible_actions_to_str(ty, ty.initial_state)}")
        print(f"GOAL-STATE-{idx} {possible_actions_to_str(ty, ty.goal_state)}\n")
        #draw_yard(ty)

def run_problem6(yards: list, iddfs_max_depth: int = 15):
    print("=== Timing & Speedup (IDDFS vs A*) ===")
    for idx, ty in enumerate(yards, start=1):
        # IDDFS
        t0 = time.perf_counter()
        plan_iddfs, stats_iddfs = iterative_deepening_dfs(
            ty, ty.initial_state, ty.goal_state, max_depth=iddfs_max_depth, stats={"expanded": 0}
        )
        t1 = time.perf_counter()
        t_iddfs = t1 - t0
        n_iddfs = len(plan_iddfs)
        e_iddfs = stats_iddfs["expanded"]

        # A*
        t2 = time.perf_counter()
        plan_astar, stats_astar = astar(ty, stats={"expanded": 0})
        t3 = time.perf_counter()
        t_astar = t3 - t2
        n_astar = len(plan_astar)
        e_astar = stats_astar["expanded"]

        time_speedup = (t_iddfs / t_astar) if t_astar > 0 and plan_astar else float('nan')
        exp_speedup  = (e_iddfs / e_astar)  if e_astar  > 0 and plan_astar else float('nan')

        print(f"Yard {idx}: "
              f"IDDFS {t_iddfs:.4f}s, exp={e_iddfs}, actions={n_iddfs} | "
              f"A* {t_astar:.4f}s, exp={e_astar}, actions={n_astar} | "
              f"Speedup time {time_speedup:.2f}x, nodes {exp_speedup:.2f}x")


def main():
    # Ask user if they want manual inputs
    resp = input("Enter manual inputs? (y/n): ").strip().lower()
    if resp == "y":
        # Manual single-yard mode
        yard_str = input("Define yard connectivity (e.g., '1 2 1 5 2 3 2 4'): ").strip()
        init_str = input("Define init state (e.g., '* d b ae c'): ").strip()
        goal_str = input("Define goal state (e.g., '*abcde empty empty empty empty'): ").strip()

        ty = Yard(filter_yard_input(yard_str), State(init_str), State(goal_str))

        # Problem 1 (for this single yard)
        print("=== PROBLEM 1 [10 pts] - possible_actions ===")
        print("Yard 1")
        print(f"INIT-STATE-1 {possible_actions_to_str(ty, ty.initial_state)}")
        print(f"GOAL-STATE-1 {possible_actions_to_str(ty, ty.goal_state)}\n")

        # Problem 6 (timings, nodes, speedup) for this single yard
        run_problem6([ty], iddfs_max_depth=15)
        return

    # Batch mode: run the five example yards
    yard_inputs_input = [
        "1 2 1 3 3 5 4 5 2 6 5 6",
        "1 2 1 5 2 3 2 4",
        "1 2 1 3",
        "1 2 1 3 1 4",
        "1 2 1 3 1 4",
    ]
    init_states_input = [
        "* e empty bca empty d",
        "* d b ae c",
        "* a b",
        "* a bc d",
        "* a cb d",
    ]
    goal_states_input = [
        "*abcde empty empty empty empty empty",
        "*abcde empty empty empty empty",
        "*ab empty empty",
        "*abcd empty empty empty",
        "*abcd empty empty empty",
    ]

    train_yards = [
        Yard(filter_yard_input(yard_inputs_input[0]), State(init_states_input[0]), State(goal_states_input[0])),
        Yard(filter_yard_input(yard_inputs_input[1]), State(init_states_input[1]), State(goal_states_input[1])),
        Yard(filter_yard_input(yard_inputs_input[2]), State(init_states_input[2]), State(goal_states_input[2])),
        Yard(filter_yard_input(yard_inputs_input[3]), State(init_states_input[3]), State(goal_states_input[3])),
        Yard(filter_yard_input(yard_inputs_input[4]), State(init_states_input[4]), State(goal_states_input[4])),
    ]

    # Problem 1 and 6 on the batch
    run_problem1(train_yards)
    run_problem6(train_yards, iddfs_max_depth=15)

if __name__ == '__main__':
    main()
