from yard import Yard, draw_yard_matplotlib
#https://udel.instructure.com/courses/1873574/assignments/13722856

#1-6: sections of track
#car: lowercase letter
#engine: *


def main():
    train_yard = Yard()
    train_yard.add_edge(1, 2)
    train_yard.add_edge(1, 3)
    train_yard.add_edge(3, 5)
    train_yard.add_edge(4, 5)
    train_yard.add_edge(2, 6)
    train_yard.add_edge(5, 6)

    positions = {
        1: (0, 0),
        2: (1, 0),
        3: (1, 1),
        4: (2, 2),
        5: (2, 1),
        6: (2, 0)
    }
    draw_yard_matplotlib(train_yard, positions)


if __name__ == '__main__':
    main()



