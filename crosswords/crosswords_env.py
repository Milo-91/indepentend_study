import json
import parameters
import re

# board, ans, status, t, id
class CrosswordsEnv():
    def __init__(self, file_name):
        self.all_data = self.load_data(file_name)
        self.id = 0

    def get_id(self):
        self.id += 1
        return self.id - 1

    def load_data(self, file_name):
        data = None
        with open(file_name, 'r') as file:
            data = json.load(file)
        return data

    def reset(self, board = None, status = None, t = None, id = None):
        self.board = ['_'] * 25 # 25 blanks on the board
        self.ans = ['_____'] * 10 # memory each line
        self.status = [0] * 10 # 10 lines status 0: Unfilled, 1: Filled, 2: Changed
        self.t = 0 # steps
        self.id = 0
        self.data = self.all_data[parameters.idx][0]
        if board != None:
            self.board = board
            self.ans = self.get_ans(self.board)
        if status != None:
            self.status = status
        if t != None:
            self.t = t
        if id != None:
            self.id = id

    def board_render(self):
        string = 'Current Board\n'
        for i in range(5):
            string += ''.join(self.board[i * 5 : (i + 1) * 5])
            string += '\n'
        return string

    def get_lines(self, status):
        lines = list()
        # horizontal
        for i in range(5):
            #print(self.data[i])
            if status == None or self.status[i] == status:
                lines.append(f'{i + 1}. ' + self.data[i] + ': ' + ''.join(self.board[i * 5 : (i + 1) * 5]))
        # vertical
        for i in range(5):
            if status == None or self.status[i + 5] == status:
                lines.append(f'{i + 6}. ' + self.data[i + 5] + ': ' + ''.join(self.board[i::5]))
        return lines

    def get_ans(self, board):
        ans = [''] * 10
        for i in range(5):
            ans[i] = ''.join(board[i * 5 : (i + 1) * 5])
        for i in range(5):
            ans[i + 5] = ''.join(board[i::5])
        return ans

    def ans_render(self):
        string = 'Unfilled:\n'
        string += '\n'.join(self.get_lines(status = 0)) + '\n'
        if len(self.get_lines(status = 2)) > 0:
            string += '\n'.join(self.get_lines(status = 2)) + '\n'

        return string

    def change_env(self, ans):
        if ans == None:
            return
        format = r'^(\d+)\. ([a-zA-Z]{5}).*$'
        match = re.match(format, ans)
        if not match:
            return
        line_index, answer = match.group(1), match.group(2)
        l = int(line_index) - 1
        print(f'line_index = {l}')
        # board
        if l < 5:
            self.board[l * 5 : (l + 1) * 5] = [char.upper() for char in answer]
        else:
            l -= 5
            self.board[l::5] = [char.upper() for char in answer]
        # status
        for i in range(5):
            self.status[i] = 0
            if all(element != '_' for element in self.board[i * 5 : (i + 1) * 5]):
                self.status[i] = 1
        for i in range(5):
            self.status[i + 5] = 0
            if all(element != '_' for element in self.board[i::5]):
                self.status[i + 5] = 1
        # t
        self.t += 1
        #ans
        self.ans = self.get_ans(self.board)

    def board_complete(self):
        if '_' in self.board:
            return False
        else:
            return True