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
    #Premade input
    yard_inputs_input:list[str] = [
        "1 2 1 3 3 5 4 5 2 6 5 6",
        "",
        "1 2 1 3",
        "1 2 1 3 1 4",
        "1 2 1 3 1 4"
    ]

    init_states_input:list[str] = [
        "* e empty bca empty d",
        "",
        "* a b",
        "*a bc d",
        "*abcd empty empty empty"
    ]

    goal_states_input:list[str] = [
        "*abcde empty empty empty empty empty",
        "",
        "*ab empty empty",
        "*abcd empty empty empty",
        "*abcd empty empty empty"
    ]


    print("===See README for example inputs===")
    """Console Input"""
    yard_input:str = "1 2 1 3"#input("Define yard:")
    yard_filtered = filter_yard_input(yard_input)

    init_state_input:str = "cd *a b"#input("Define init-state:")
    init_state:State = State(init_state_input)

    output_state_input:str = "*abcd empty empty"#input("Define output:")
    output_state:State = State(output_state_input)

    train_yard:Yard = Yard(
        yard_filtered,
        init_state,
        output_state)

    """Output"""
    #PROBLEM 1 [10 pts] - possible_actions



    #PROBLEM 2 [10 pts] - expected_results


    train_yard.left(2,1)
    for action in possible_actions(train_yard, train_yard.current_state):
        print(str(action))

    test_state:State = State("")

    print(test_state.state)

    draw_yard(train_yard)


if __name__ == '__main__':
    main()