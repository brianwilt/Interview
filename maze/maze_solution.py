from optparse import OptionParser
import sys
import random

# Solve mazes generated from http://www.delorie.com/game-room/mazes/genmaze.cgi
# Probably should make sure cells are size 2

class MazeSolver:
    maze = []
    visited = []
    person_emoji_list = [u"\U0001F600",u"\U0001F601",u"\U0001F602",u"\U0001F603",u"\U0001F604",u"\U0001F605"]

    def __init__(self, maze_file):
        print 'Loading maze ...'
        if maze_file:
            with open(maze_file, 'r') as maze_file:
                for l in maze_file:
                    self.maze.extend([l.strip()])
        else:
            # So we can run this in online code screens, hardcode in
            self.maze.extend(['+-+-+-+-+-+-+-+-+-+-+'])
            self.maze.extend(['S |       |         |'])
            self.maze.extend(['+ + +-+-+ + + +-+-+-+'])
            self.maze.extend(['|   |   |   |       |'])
            self.maze.extend(['+-+-+ + +-+-+-+-+-+ +'])
            self.maze.extend(['| |   |         |   |'])
            self.maze.extend(['+ + +-+-+ +-+-+-+ +-+'])
            self.maze.extend(['| | |     |       | |'])
            self.maze.extend(['+ + +-+-+-+ +-+-+-+ +'])
            self.maze.extend(['| |     |     |     |'])
            self.maze.extend(['+ +-+-+ + +-+ + +-+-+'])
            self.maze.extend(['|     | |   |   |   |'])
            self.maze.extend(['+-+-+ + +-+ +-+-+ + +'])
            self.maze.extend(['|     | | | |   | | |'])
            self.maze.extend(['+ +-+-+ + + + + + + +'])
            self.maze.extend(['|   |   |     |   | |'])
            self.maze.extend(['+ + + +-+-+-+-+-+-+ +'])
            self.maze.extend(['| |   |         |   |'])
            self.maze.extend(['+ +-+-+ +-+-+-+ + + +'])
            self.maze.extend(['|       |         | E'])
            self.maze.extend(['+-+-+-+-+-+-+-+-+-+-+'])
        print 'Maze loaded.'

        # Find the start of the maze
        start_location = self._find_start()
        print 'Start location: ' + str(start_location)

        solution = self.solve_maze(start_location)

        # Print the start of a solution
        self.print_maze(solution=solution) # self._get_sol(start_location))

    # Solve the maze from this point (a tuple)
    def solve_maze(self, point, current_path=[]):
        current_path.append(point)
        # End condition
        if self.maze[point[0]][point[1]] == 'E':
            return current_path

        # Look at open directions to go from here
        for dir in self._open_directions(point):
            # Can't visit old places, otherwise will loop
            if dir not in self.visited:
                self.visited.append(dir)

                # Have to slice, otherwise all recursions adding to same path
                solution = self.solve_maze(dir, list(current_path))

                if solution:
                    return solution

        return False

    # Show the maze, optionally including a (partial) solution
    def print_maze(self, solution=None):
        print 'Solution: ' + str(solution)

        # Check that solution makes sense
        if solution is not None and not self._check_solution(solution):
            raise Exception('Solution is wrong!')

        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                if solution is not None and (y,x) in solution and self.maze[y][x] == ' ':
                    # Need sys.stdout to print a char with no space or newline
                    print random.choice(self.person_emoji_list),
                else:
                    if self.maze[y][x] == 'E':
                        print u"\U0001F382",
                    else:
                        print self.maze[y][x],

            print

    # Find the location of the 'S' character
    def _find_start(self):
        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                if self.maze[y][x] == 'S':
                    return (y,x)

    def _check_solution(self, solution, check_end=False):
        # Needs to start at ... the start
        if self.maze[solution[0][0]][solution[0][1]] != 'S':
            print 'Solution needs to start at the start silly!'
            return False

        # Should end at ... the end
        if check_end and self.maze[solution[-1][0]][solution[-1][1]] != 'E':
            print 'Solution needs to end at the end silly!'
            return False

        # Each point needs to be next to each other
        # Also make sure point is in an allowable thing (' ', 'S', 'E')
        for i in range(len(solution)-1):
            if solution[i+1] not in self._open_directions(solution[i]):
                print 'The points need to be next to each other: %s and %s' % (solution[i], solution[i+1])
                return False
            if self.maze[solution[i][0]][solution[i][1]] not in (' ', 'S' , 'E'):
                print 'You can\'t travel through walls: %s' % str(solution[i])
                return False

        # Could check for backtracking but seems OK

        return True

    # Check if a point is on the map (i.e. false for (-1,-2) tuple)
    def _is_in_bounds(self, point):
        if point[0] < 0 or point[0] > len(self.maze)-1:
            return False

        if point[1] < 0 or point[1] > len(self.maze[0])-1:
            return False

        return True

    # Check if this is a legal place to go
    def _is_open_space(self, point):
        if self._is_in_bounds(point) and self.maze[point[0]][point[1]] in (' ', 'S', 'E'):
            return True

        return False

    # Return a list of points (tuples) you can go to from a point
    def _open_directions(self, point):
        open_dirs = []

        new_dir = (point[0]-1, point[1])
        if self._is_open_space(new_dir):
            open_dirs.append(new_dir)

        new_dir = (point[0]+1, point[1])
        if self._is_open_space(new_dir):
            open_dirs.append(new_dir)

        new_dir = (point[0], point[1]-1)
        if self._is_open_space(new_dir):
            open_dirs.append(new_dir)

        new_dir = (point[0], point[1]+1)
        if self._is_open_space(new_dir):
            open_dirs.append(new_dir)

        return open_dirs

def main():
    parser = OptionParser()
    parser.add_option("-f", "--maze_file", dest="config_maze_file", help="Name of the file with the maze in it")

    (options, args) = parser.parse_args()

    config_maze_file = None

    if options.config_maze_file:
        config_maze_file = options.config_maze_file

    ms = MazeSolver(config_maze_file)

if __name__ == "__main__":
    main()
