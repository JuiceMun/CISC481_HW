from yard import  Yard, draw_yard
#https://udel.instructure.com/courses/1873574/assignments/13722856

#1-n: rail sections
#car: lowercase letter
#engine: *

def main():
    print("===See README for example inputs===")

    yard_input:str = "1 2 1 3"#input("Define yard:")
    yard_input = yard_input.replace(" ","")
    yard_filtered:list[list[int]] = []
    for i in range(0, len(yard_input), 2):
        yard_filtered.append([
            int(yard_input[i]),
            int(yard_input[i + 1])
        ]) #convert to [[1,2],[1,3]] rail pairs

    init_state_input:str = "* a b"#input("Define init-state:")
    init_state_filtered = []
    for state in init_state_input.split():
        if state == "empty":
            init_state_filtered.append([])
        else:
            init_state_filtered.append(list(state))

    output_state_input:str = "*ab empty empty"#input("Define output:")
    output_state_filtered = []
    for state in output_state_input.split():
        if state == "empty":
            output_state_filtered.append([])
        else:
            output_state_filtered.append(list(state))

    train_yard:Yard = Yard(
        yard_filtered,
        init_state_filtered,
        output_state_filtered)
    draw_yard(train_yard)

    print(f"{yard_filtered}\n{init_state_filtered}\n{output_state_filtered}")

if __name__ == '__main__':
    main()