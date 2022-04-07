def main():
    import lib
    import os.path
    from time import time
    from copy import deepcopy
    print('Welcome to MazeGenerator!')
    print('Possible commands:')
    print('(1) generate maze with random DFS')
    print('(2) generate maze with random Kruskal algorithm')
    print('(3) generate maze with random binary tree')
    print('(4) open maze, generated with MazeGenerator')
    command = None
    print('If command is invalid you should retry')
    while not command in ('1', '2', '3', '4'):
        command = input('Enter your command: ').strip()
    if command == '4':
        print('If path is invalid you should retry')
        path = str(time())
        while not os.path.exists(path):
            path = input('Enter path to maze: ')
        grid = lib.Grid.load_from_file(path)
    else:
        size = ('a', 'a')
        while not (len(size) == 2 and \
            size[0].isdigit() and size[1].isdigit() and \
            int(size[0]) >= 0 and int(size[1]) >= 0):
            size = input('Enter <height> <width>: ').strip().split()
        grid = lib.Grid(height=int(size[0]), width=int(size[1]))
        if command == '1':
            lib.random_depth_first_search(grid)
        elif command == '2':
            lib.random_kruskal(grid)
        else:
            lib.random_binary_tree(grid)
    print(grid)
    print('Do you want MazeGenerator to find the path in this maze?')
    print('Enter \'y\', if you want, \'n\', if you don\'t')
    command = input('Enter your command: ').strip()
    if command == 'y':
        start = ('a', 'a')
        while not (len(start) == 2 and \
            start[0].isdigit() and start[1].isdigit() and \
            grid.is_cell_empty(*map(int, start))):
            start = input('Enter start cell (<height> <width>): ')
            start = start.strip().split()
        finish = ('a', 'a')
        while not (len(finish) == 2 and \
            finish[0].isdigit() and finish[1].isdigit() and \
            grid.is_cell_empty(*map(int, finish))):
            finish = input('Enter finish cell (<height> <width>): ')
            finish = finish.strip().split()
        copied_grid = deepcopy(grid)
        start = tuple(map(int, start))
        finish = tuple(map(int, finish))
        lib.mark_path(copied_grid, start, finish)
        print(copied_grid)
    print('Do you want to save this maze?')
    print('Enter \'y\', if you want, \'n\', if you don\'t')
    command = input('Enter your command: ').strip()
    if command == 'y':
        saved_path = f'maze{time()}'
        grid.save(saved_path)
        print(f'Maze has been saved in file {saved_path}')

if __name__ == '__main__':
    main()
