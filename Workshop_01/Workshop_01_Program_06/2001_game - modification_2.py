"""
Workshop_01 - Program_05_Mod_2
--------------------------
2001 Game - Modification_2
--------------------------
(c) Tomas Dolejsek 2024-01-25

*** Modification 2 ***
Now try transferring your game to the server using Flask. To store information between turns, use hidden form fields.
This is not the best solution (may be prone to cheating), but we don't care about that for now. Dice selection before
the roll should be done using a form.
"""

from random import randint, choice
from flask import Flask, render_template, request, flash, session
from collections import namedtuple
app = Flask(__name__)
RoundResult = namedtuple('RoundResult', ['round', 'player', 'computer', 'winner'])
app.secret_key = "Very secret key"


def calculate_roll(who, rolls):
    flash(f"\n{who} picked D{rolls[0]} and D{rolls[1]}.")
    flash(f"{who}'s rolls: ")
    x = randint(1, rolls[0])
    y = randint(1, rolls[1])
    flash(f"{x} + {y} = {x + y}")
    return x + y


def calculate_score(points, roll, round_number):
    if round_number == 1:
        return points + roll
    if roll == 7:
        flash("Points divided by 7!")
        return points // 7
    elif roll == 11:
        flash("Points multiplied by 11!")
        return points * 11
    else:
        return points + roll


def pick_computer_dice():
    correct_dice = (3, 4, 6, 8, 10, 12, 20, 100)
    x = choice(correct_dice)
    y = choice(correct_dice)
    return x, y


def play_round(round_number, score, rolls):
    limit = 2001
    winner = None
    for member in score:
        roll = calculate_roll(member, rolls[member])
        score[member] = calculate_score(score[member], roll, round_number)
        if score[member] >= limit:
            winner = member
            break
    return RoundResult(round_number, score['Player'], score['Computer'], winner)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', round=0, player=0, computer=0)
    if request.method == 'POST':
        limit = 2001
        rolls, score = dict(), dict()
        round_number = int(request.form['round'])
        winner = request.form.get('winner')
        print(winner)
        if winner == 'None':
            round_number = 0
        player = request.form.get('player_score')
        computer = request.form.get('computer_score')
        if round_number > 0:
            dice1 = request.form.get('dice1')
            dice2 = request.form.get('dice2')
            rolls['Player'] = int(dice1), int(dice2)
            rolls['Computer'] = pick_computer_dice()
            score['Player'] = int(player)
            score['Computer'] = int(computer)
            result = play_round(round_number + 1, score, rolls)
        else:
            result = RoundResult(1, 0, 0, None)
        if result.winner:
            session['_flashes'].clear()  # clear flashes
        return render_template('game.html', winner=result.winner, round=result.round, player=result.player,
                               computer=result.computer)


if __name__ == '__main__':
    app.run()
