from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'Twoj_Sekretny_Klucz'

def init_game():
    session['board'] = [''] * 9
    session['turn'] = 'X'
    session['message'] = ''

def check_winner(board):
    wins = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] and board[a] != '':
            return board[a]
    if '' not in board:
        return 'Draw'
    return None

def bot_move():
    board = session['board']
    empty = [i for i, val in enumerate(board) if val == '']
    if empty:
        choice = random.choice(empty)
        board[choice] = 'O'
        session['turn'] = 'X'

@app.route('/')
def index():
    if 'board' not in session:
        init_game()
    return render_template('index.html', board=session['board'], message=session.get('message', ''))

@app.route('/move/<int:cell>')
def move(cell):
    board = session['board']
    if board[cell] == '' and session['turn'] == 'X':
        board[cell] = 'X'
        session['turn'] = 'O'
        winner = check_winner(board)
        if winner:
            session['message'] = 'Remis!' if winner == 'Draw' else f'Wygrywa {winner}!'
        else:
            bot_move()
            winner = check_winner(board)
            if winner:
                session['message'] = 'Remis!' if winner == 'Draw' else f'Wygrywa {winner}!'
    return redirect(url_for('index'))

@app.route('/restart')
def restart():
    init_game()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
