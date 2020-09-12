#!/usr/bin/env python3
"""6.009 Lab -- Six Double-Oh Mines"""

# NO IMPORTS ALLOWED!

def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f'{key}:')
            for inner in val:
                print(f'    {inner}')
        else:
            print(f'{key}:', val)


# 2-D IMPLEMENTATION
def find_nearby_nodes(num_rows,num_cols,row,column):
    """
    Given the number of rows and columns, this finds the location in (row,column) of 
    the 8 surrounding positions and eliminates the coordinate if it is out of bounds
    """
    validpositions=[]
    for r in range(row-1,row+2):
        for c in range(column-1,column+2):
            if 0<=r<num_rows and 0<=c<num_cols: #check to see if location is out of bounds
                validpositions.append((r,c))

    return validpositions

def bad_squares(game):
    """
    finds bad squares in 2-d
    """
    bombs = 0  # set number of bombs to 0
    covered_squares = 0
    for r in range(game['dimensions'][0]):
        # for each r,
        for c in range(game['dimensions'][1]):
            # for each c,
            if game['board'][r][c] == '.':
                if  game['mask'][r][c] == True:
                    # if the game mask is True, and the board is '.', add 1 to
                    # bombs
                    bombs += 1
            elif game['mask'][r][c] == False:
                covered_squares += 1
    bad_squares = bombs + covered_squares #retruns the number of bomb squares and covered squares
    return bad_squares

def coveredsquares(game):
    """
    retruns the number of covered squares and bombs in 2-d
    """
    bombs = 0
    covered_squares = 0
    for r in range(game['dimensions'][0]):
        for c in range(game['dimensions'][1]):
            if game['board'][r][c] == '.':
                if  game['mask'][r][c] == True:
                    bombs += 1
            elif game['mask'][r][c] == False:
                covered_squares += 1
    return bombs,covered_squares
def makeboardmask(num_rows,num_cols,bombs):
    """
    makes board and mask in 2d
    """
    board = []
    for r in range(num_rows):
        row = []
        for c in range(num_cols):
            if [r,c] in bombs or (r,c) in bombs: #checks if position is a bomb
                row.append('.')
            else:
                row.append(0)
        board.append(row)
    mask = []
    for r in range(num_rows):
        row = []
        for c in range(num_cols):
            row.append(False) #appends false
        mask.append(row)
    return board,mask


def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    mask:
        [False, False, False, False]
        [False, False, False, False]
    state: ongoing
    """
    #creates the board and the mask
    board,mask=makeboardmask(num_rows, num_cols, bombs)
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == 0:
                neighbor_bombs = 0
                neighbornodes=find_nearby_nodes(num_rows, num_cols, r, c)
               #iterates through the list of nearby nodes and counts for bombs
                for node in neighbornodes:
                    if board[node[0]][node[1]] == '.':
                            neighbor_bombs += 1
                            board[r][c] = neighbor_bombs
    return {
        'dimensions': (num_rows, num_cols),
        'board' : board,
        'mask' : mask,
        'state': 'ongoing'}  

def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['mask'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is visible on the board after digging (i.e. game['mask'][bomb_location] ==
    True), 'victory' when all safe squares (squares that do not contain a bomb)
    and no bombs are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    mask:
        [False, True, True, True]
        [False, False, True, True]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    mask:
        [True, True, False, False]
        [False, False, False, False]
    state: defeat
    """
    if game['state'] == 'defeat' or game['state'] == 'victory':
        game['state'] = game['state']  # keep the state the same
        return 0

    if game['board'][row][col] == '.':
        game['mask'][row][col] = True
        game['state'] = 'defeat'
        return 1

    bombs,covered_squares=coveredsquares(game)

    if bombs != 0:
        # if bombs is not equal to zero, set the game state to defeat and
        # return 0
        game['state'] = 'defeat'
        return 0
    if covered_squares == 0:
        game['state'] = 'victory'
        return 0
    #if number of covered squares if 0, then we won
    if game['mask'][row][col] != True:
        game['mask'][row][col] = True
        revealed = 1
    else:
        return 0
    #recursively digs on surrounding nodes if the node is a 0
    if game['board'][row][col] == 0:
        num_rows, num_cols = game['dimensions']
        if 0 <= row < num_rows:
             if 0 <= col < num_cols:
                nearbynodes=find_nearby_nodes(num_rows, num_cols, row, col)
                for node in nearbynodes:
                    if game['board'][node[0]][node[1]] != '.':
                            if game['mask'][node[0]][node[1]] == False:
                                revealed += dig_2d(game, node[0], node[1])
    badsquares=bad_squares(game)
    if badsquares > 0:
        game['state'] = 'ongoing'
        return revealed
    else:
        game['state'] = 'victory'
        return revealed

def render_2d(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring bombs).
    game['mask'] indicates which squares should be visible.  If xray is True (the
    default is False), game['mask'] is ignored and all cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A 2D array (list of lists)

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    endarray=[]
    rows=len(game['board'])
    colums=len(game['board'][0])
    for row in range(rows):
        rowlist=[]
        for column in range(colums):
            #if covered 
            if game['mask'][row][column]==False and xray==False:
                rowlist.append('_')
                #if the position is has no nearby bombs
            elif game['board'][row][column]==0:
                    rowlist.append(' ')
            else: #then we would want to append the number that is on the board
                rowlist.append(str(game['board'][row][column]))
        endarray.append(rowlist)
    return endarray
                


def render_ascii(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function 'render_2d(game)'.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A string-based representation of game

    >>> print(render_ascii({'dimensions': (2, 4),
    ...                     'state': 'ongoing',
    ...                     'board': [['.', 3, 1, 0],
    ...                               ['.', '.', 1, 0]],
    ...                     'mask':  [[True, True, True, False],
    ...                               [False, False, True, False]]}))
    .31_
    __1_
    """
    
    rowarray=''
    rows=len(game['board'])
    colums=len(game['board'][0])
    for row in range(rows):
        for column in range(colums):
            if game['mask'][row][column] or xray:#checks if the position is true or if xray is true
                
                if game['board'][row][column]=='.': #if bomb
                    rowarray+='.'
                elif game['board'][row][column]==0: #if empty
                    rowarray+=' '
                else:
                    rowarray+=str(game['board'][row][column])
            else:
                rowarray+=('_')
        rowarray+='\n'
    return rowarray[:-1] #we want to get rid of the \n at the end



# N-D IMPLEMENTATION
def find_nearby_nodes_withself(dimensions, position):
    """
    Given the number of rows and columns, this finds the location in (row,column) of 
    the 8 surrounding positions and eliminates the coordinate if it is out of bounds
    """
    
    if len(dimensions)==1: #base case if the dimension is only one
        lst=[]
        if position[0]-1>=0:#checks to see if the position is out of bounds
            lst.append((position[0]-1,)) # we want to append a tuple since the recursive case is a tuple
        lst.append(position)
        if position[0]+1<dimensions[0]:
            lst.append((position[0]+1,))
        return lst
    one_d_neighbors=find_nearby_nodes_withself(dimensions[:-1],position[:-1]) #does the recursive case on the last element
    neighbors=[]
    for neighbor in one_d_neighbors:
        if position[-1]-1>=0: #we look at the last position
            neighbors.append(neighbor+(position[-1]-1,)) #sicne neighbor is already a tuple,we have to add the uples
        neighbors.append(neighbor+(position[-1],))
        if position[-1]+1<dimensions[-1]: #checks for out of boudns
            neighbors.append(neighbor+(position[-1]+1,))
    return neighbors

def find_nearby_nodes_nd(dimensions,position):
    """
    This finds the location of all of the surrounding positions and 
    eliminates the node that is itself
    """
    neighbors=find_nearby_nodes_withself(dimensions, position)
    neighbors.remove(position)
    return  neighbors #since in find nearby ndoes,vwe need to indlude the position itself, we need to remove this value

def make_board(dimensions):
    """
    if given a dimensions, this creates an empty board with all the values set as
    false
    """
    if len(dimensions)==1: #base case if dimensions is 1
        lst=[]
        for item in range(dimensions[0]):
            lst.append(False) # we want to make a board with everything being false
        return lst
    lst=[] 
    for item in range(dimensions[0]):
        innerlst=make_board(dimensions[1:]) #then we want to recurse on everything but the first element
        lst.append(innerlst)
    return lst

def make_board_with_0(dimensions):
    """
    if given a dimensions, this creates an empty board with all the values set as
    0
    """
    if len(dimensions)==1:
        lst=[]
        for item in range(dimensions[0]):
            lst.append(0)#same as make board, but we initialize the whole board as 0
        return lst
    lst=[]
    for item in range(dimensions[0]):
        innerlst=make_board_with_0(dimensions[1:])
        lst.append(innerlst)
    return lst
def set_board(board,coordinate,value):
    """
    given a created board, a coordinate value, and a value, we can set that value to 
    the given value
    """
    if len(coordinate)==1:#basecase is when we are in one d
        board[coordinate[0]]=value
        return
    set_board(board[coordinate[0]],coordinate[1:],value) #otherwise we recursively set
    
def get_value(board,coordinate):
    """
    given a coordinate, we want to get the value
    """
    if len(coordinate)==1: #basecase is when we are in 1d
        return board[coordinate[0]]
    return (get_value(board[coordinate[0]],coordinate[1:]))

def all_positions(dimensions):
    """
    given a board, it return all the possible dimensions of the board
    """
    if len(dimensions)==1:
        lst=[]
        for value in range(dimensions[0]):
            lst.append((value,)) #we are appending a tuple
        return lst
    lst=[]
    for item in range(dimensions[0]):
        coord=(item,)
        for elem in all_positions(dimensions[1:]): #we dont start with position 0
            new=coord+elem
            lst.append(new) #appends the tuple of coordinates to list
    return lst
            
        
def game_state(game):
    """
    given a game, this returns the game state
    """
    for position in all_positions(game['dimensions']):
        maskval=get_value(game['mask'],position)
        if maskval: #if mask is true
            if get_value(game['board'],position)=='.': #if mask is true and we unveiled a bomb, then we loose
                return 'defeat'
        else:
            if not maskval and get_value(game['board'],position)!='.': #if mask is false and still a number then game still on
                return 'ongoing'
    return 'victory'
        
    
def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of lists, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: ongoing
    """
    mask=make_board(dimensions)
    board=make_board_with_0(dimensions)
    
    
    for bomb in bombs: #sets all the bombs
        set_board(board, bomb, '.')


    for bombloc in bombs: #goes thorugh every bomb and then get the neighbors and adds one to their value
        neighbors=find_nearby_nodes_nd(dimensions, bombloc)
        for neighbor in neighbors:
            if get_value(board,neighbor)!='.': #checks to see if neighbor is bomb
                set_board(board, neighbor,(get_value(board,neighbor)+1))

    
    gamestate={'dimensions':dimensions,'state':'ongoing','board':board,'mask':mask}
    return gamestate
        

def dig_nd(game, coordinates, check = True):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the mask to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are visible, and 'ongoing' otherwise.

    Args:
       coords (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: defeat
    """

    if get_value(game['mask'],coordinates): #if the value of the mask is true then it is already revealed
        return 0
     
    if game['state'] == 'defeat' or game['state'] == 'victory': #if we've already won, we dont want to dig
        return 0

    if get_value(game['board'],coordinates) == '.': #if we dig at a site and it is a bomb, then we lost
        set_board(game['mask'],coordinates,True) 
        game['state'] = 'defeat'
        return 1
    
    if get_value(game['board'],coordinates)!=0: # if the value is a number, then we dig and change the mask
        set_board(game['mask'],coordinates,True)
        if check:
            game['state'] = game_state(game)
        return 1
    
    if get_value(game['board'],coordinates)==0:
        nearbynodes=find_nearby_nodes_nd(game['dimensions'], coordinates) #we recursively dig on the nearby nodes
        set_board(game['mask'],coordinates,True) #we set the check to be true at the last step of the recursion
        summ=1
        for node in nearbynodes:
            if not get_value(game['mask'],node):
                summ+=dig_nd(game,node, False)
    if check:            
        game['state'] = game_state(game)#we check the game state at the end
    return summ
    
def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares
    neighboring bombs).  The mask indicates which squares should be
    visible.  If xray is True (the default is False), the mask is ignored
    and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    the mask

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [True, True], [True, True]],
    ...               [[False, False], [False, False], [True, True], [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    coordinates=all_positions(game['dimensions'])
    board=make_board(game['dimensions'])
    if xray==False:
        for coordinate in coordinates: #iterate through every coordinate and set accordingly
            if get_value(game['mask'], coordinate)==False:
                set_board(board, coordinate, '_')
            else:
                if get_value(game['board'],coordinate)==0:
                    set_board(board,coordinate,' ')
                else:
                    set_board(board,coordinate,str(get_value(game['board'],coordinate)))
    if xray: #if xray is true
        for coordinate in coordinates:
            if get_value(game['board'],coordinate)==0:
                set_board(board,coordinate,' ')
            else:
                set_board(board,coordinate,str(get_value(game['board'],coordinate)))
    return board 
        
        


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags) #runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d or any other function you might want.  To do so, comment
    # out the above line, and uncomment the below line of code. This may be
    # useful as you write/debug individual doctests or functions.  Also, the
    # verbose flag can be set to True to see all test results, including those
    # that pass.
    #
    #doctest.run_docstring_examples(render_2d, globals(), optionflags=_doctest_flags, verbose=False)
    # print(find_nearby_nodes_nd((10,7), (5,0)))
    
