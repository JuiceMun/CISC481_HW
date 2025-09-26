from yard import *
#https://udel.instructure.com/courses/1873574/assignments/13722856

#1-n: rail sections
#car: lowercase letter
#engine: *

def filter_yard_input(yard_input:str) -> list[list[int]]:
    yard_input = yard_input.replace(" ", "")
    yard_filtered: list[list[int]] = []
    for i in range(0, len(yard_input), 2):
        yard_filtered.append([
            int(yard_input[i]),
            int(yard_input[i + 1])
        ])  # convert to [[1,2],[1,3]] rail pairs
    return yard_filtered

def main():
    #Project 1 examples
    yard_inputs_input:list[str] = [
        "1 2 1 3 3 5 4 5 2 6 5 6",
        "1 2 1 5 2 3 2 4",
        "1 2 1 3",
        "1 2 1 3 1 4",
        "1 2 1 3 1 4"
    ]

    init_states_input:list[str] = [
        "* e empty bca empty d",
        "* d b ae c",
        "* a b",
        "* a bc d",
        "* a cb d"
    ]

    goal_states_input:list[str] = [
        "*abcde empty empty empty empty empty",
        "*abcde empty empty empty empty",
        "*ab empty empty",
        "*abcd empty empty empty",
        "*abcd empty empty empty"
    ]

    train_yard_1: Yard = Yard(
        filter_yard_input(yard_inputs_input[0]),
        State(init_states_input[0]),
        State(goal_states_input[0])
    )
    train_yard_2: Yard = Yard(
        filter_yard_input(yard_inputs_input[1]),
        State(init_states_input[1]),
        State(goal_states_input[1])
    )
    train_yard_3: Yard = Yard(
        filter_yard_input(yard_inputs_input[2]),
        State(init_states_input[2]),
        State(goal_states_input[2])
    )
    train_yard_4: Yard = Yard(
        filter_yard_input(yard_inputs_input[3]),
        State(init_states_input[3]),
        State(goal_states_input[3])
    )
    train_yard_5: Yard = Yard(
        filter_yard_input(yard_inputs_input[4]),
        State(init_states_input[4]),
        State(goal_states_input[4])
    )

    train_yards: list[Yard] = [
        train_yard_1,
        train_yard_2,
        train_yard_3,
        train_yard_4,
        train_yard_5,
    ]

    print("===See README for example inputs===")
    """Console Input"""
    """yard_input:str = input("Define yard:")
    yard_filtered = filter_yard_input(yard_input)

    init_state_input:str = input("Define init-state:")
    init_state:State = State(init_state_input)

    output_state_input:str = input("Define output:")
    output_state:State = State(output_state_input)

    train_yard:Yard = Yard(
        yard_filtered,
        init_state,
        output_state
    )"""

    """Output"""
    #PROBLEM 1 [10 pts] - possible_actions
    """
    Run your function 
        *on at least three different yards 
        *two different states for each yard 
        *including the two large yards and initial states described pictorially in this
        handout
    """
    """
    index:int = 0
    for ty in train_yards:
        index += 1
        actions_init: list[Action] = possible_actions(ty, ty.initial_state)
        actions_goal: list[Action] = possible_actions(ty, ty.goal_state)
        print(f"===Possible Actions: train_yard_{index} init")
        for action in actions_init:
            print("\t"+str(action))
        print(f"===Possible Actions: train_yard_{index} goal")
        for action in actions_goal:
            print("\t"+str(action))
            """

    #PROBLEM 2 [10 pts] - expected_state

    #PROBLEM 3 [10 pts] - expected_states

    #Problem 4 [30 pts] - iterative_deepening_dfs
    for idx, ty in enumerate(train_yards, start=1):
        if idx == 1:  # skip yard 1
            continue

        goal_actions: list[Action] = iterative_deepening_dfs(
            ty, ty.initial_state, ty.goal_state, 20
        )

        sim_state:State = ty.initial_state
        for action in goal_actions:
            sim_state = result(action, sim_state)

        temp_yard:Yard = Yard(ty.rail_connectivity, ty.initial_state, ty.goal_state)
        temp_yard.current_state = sim_state

        draw_yard(temp_yard)


if __name__ == '__main__':
    main()