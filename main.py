from controller import Controller
from cleanup import Cleanup

def main():
    """
    Current board
        [0] [1] [2] [3] [4] [5] [6] [7] [8]
    [0]  i   i   o   o   o   o   o   o
    [1]  o   o   o   o   o   o   o   o   o
    [2]  o   o   o   o   o   o   o   o   o
    [3]  o   o   o   o   o   o   o   o   o
    [4]  o   o   o   o   o   o   o   o   o
    [5]  o   o   o   o   o   o   o   o   o
    [6]  o   o   o   o   o   o   o   o   o
    [7]  o   o   o   o   o   o   o   o   o  <- [8, 7]
    [8]  o   o   o   o   o   o   o   o   o
    """
    controller_settings = {
        'id':'mk1',
        'assignments':{}
    }
    controller = Controller(controller_settings)

    def all_on():
        controller.allOn("green_bright")
    def all_off():
        controller.allOff()
    def print_assignments():
        controller.printAssignments()

    controller.addAssignment('all_on_off', [0, 0], all_on, all_off)
    controller.addAssignment('print_assignments', [1, 0], print_assignments, print_assignments)

    cleanup_settings = {
        'object_to_clean':controller
    }
    cleanup = Cleanup(cleanup_settings)

    while True:
        controller.buttonEvent()

if __name__ == "__main__":
    print("\n\n-----MAIN-----\n\n")
    main()
