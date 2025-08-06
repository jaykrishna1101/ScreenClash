class Solution:
    def isValidSudoku(self, board): # List[List[str]]) -> bool:
        row = {i:set() for i in range(9)}
        col = {i:set() for i in range(9)}
        sqr = {i:set() for i in range(9)}

        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] in row[i] or board[i][j] in col[j] or board[i][j] in sqr[(i//3)*3+(j//3)]:
                    return False
                if board[i][j].isalnum():
                    row[i].add(board[i][j])
                    col[j].add(board[i][j])
                    sqr[(i//3)*3+(j//3)].add(board[i][j])
        return True
    

board = [["1","2",".",".","3",".",".",".","."],
        ["4",".",".","5",".",".",".",".","."],
        [".","9","8",".",".",".",".",".","3"],
        ["5",".",".",".","6",".",".",".","4"],
        [".",".",".","8",".","3",".",".","5"],
        ["7",".",".",".","2",".",".",".","6"],
        [".",".",".",".",".",".","2",".","."],
        [".",".",".","4","1","9",".",".","8"],
        [".",".",".",".","8",".",".","7","9"]]

a = Solution()
print(a.isValidSudoku(board))

