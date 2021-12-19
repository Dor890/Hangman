#################################################################
# FILE : hangman.py
# WRITER : Dor Messica , dor.messica , 318391877
# EXERCISE : intro2cse ex4 2020
# DESCRIPTION: The program contains the game "Hangman".
#################################################################
import hangman_helper

UNDERSCORE = '_'
FIRST_TURN = "First turn, lets go!"
INVALID_LETTER = "Letter is invalid"
CHOSEN_LETTER = "The letter you entered was already guessed chosen"
SUCCESSFUL_GUESS = "You guessed correctly, the pattern is updated!"
WRONG_LETTER = "This letter is not in the secret word!"
WRONG_WORD = "You guessed the word wrong!"
WINNING_MESSAGE = "Congratulations, you won!"
LOSING_MESSAGE = "You lost! The secret word was: "
HINT_RECEIVED = "You got a hint!"
AFTER_WIN = "You have played {} games, and have currently {} points." \
            " Would you like to play again?"
AFTER_LOSE = "You have survived {} games until you lost. Would you like to" \
             " restart?"

def update_word_pattern(word, pattern, letter):
    """
    Returns the updated pattern depends on the guessed word from the user.
    :param word: the secret word (string).
    :param pattern: the current pattern (string).
    :param letter: the guessed letter (string).
    :return: an updated pattern that includes the letter.
    """
    updated_pattern = ""
    for i in range(len(word)):
        if word[i] == letter:
            updated_pattern += word[i]
        else:
            updated_pattern += pattern[i]
    return updated_pattern


def score_updater(pattern, letter):
    """
    Returns the bonus points for the correct guess.
    :param pattern: The current pattern.
    :param letter: the letter that was chosen.
    :return: a number contains the bonus points for the user.
    """
    count = pattern.count(letter)  # the appearances of letter in the pattern
    bonus = count * (count+1) // 2
    return bonus


def same_letters(word, pattern):
    """
    Checks if the pattern can be a pattern of the word.
    :param word: a word from the words list.
    :param pattern: the secret word's pattern.
    :return: a boolean value if the revealed letters of the pattern are in same
             places as in the word and aren't in other places in the word.
    """
    confirmed_letters = pattern.split(UNDERSCORE)
    for i in range(len(pattern)):
        if (pattern[i] == UNDERSCORE and word[i] in confirmed_letters) or\
                pattern[i] != UNDERSCORE and pattern[i] != word[i]:
            return False
    return True


def in_wrong_guess(word, wrong_guess_lst):
    """
    Checks if the word has any letters from the wrong guesses list.
    :param word: a word from the words list.
    :param wrong_guess_lst: list contains all the wrong letters guesses.
    :return: a boolean value any of the word's letters are in the wrong letters
             guesses list.
    """
    for letter in word:
        if letter in wrong_guess_lst:
            return True
    return False


def filter_words_list(words, pattern, wrong_guess_lst):
    """
    Returns the user a list of words that can be the secret word, depends on
    the current pattern.
    :param words: list of words.
    :param pattern: the current pattern.
    :param wrong_guess_lst: the current list of wrongs guesses.
    :return: a list contains only the words from the words list that can fit
             the pattern and the wrong guesses.
    """
    returned_list = []
    for word in words:
        if len(word) == len(pattern) and same_letters(word, pattern) and not\
                in_wrong_guess(word, wrong_guess_lst):
            returned_list.append(word)
    return returned_list


def make_suggestions(words_list, pattern, wrong_guesses):
    """
    Handles the hint input functionality for the run_single_game function.
    :param words_list: the list of all words.
    :param pattern: the current pattern.
    :param wrong_guesses: list of all wrong guesses.
    :return: the updated message.
    """
    words_for_hint = filter_words_list(words_list, pattern, wrong_guesses)
    top_hints = []  # used if there are too many word in the hits list.
    if len(words_for_hint) > hangman_helper.HINT_LENGTH:
        for i in range(0, hangman_helper.HINT_LENGTH):
            top_hints.append(words_for_hint
                             [i * len(words_for_hint) //
                              hangman_helper.HINT_LENGTH])
        hangman_helper.show_suggestions(top_hints)
    else:
        hangman_helper.show_suggestions(words_for_hint)
    return HINT_RECEIVED


def invalid_letter(letter, wrong_guesses, pattern):
    """
    Handles invalid letter inputs and returns a proper message.
    :param letter: the user's checked letter.
    :param wrong_guesses: list of all wrong guesses.
    :param pattern: the current pattern. 
    :return: the updated message
    """""
    if not letter.isalpha() or len(letter) > 1 or not letter.islower():
        return INVALID_LETTER
    elif letter in wrong_guesses or letter in pattern:
        return CHOSEN_LETTER


def letter_input(score, letter, word, wrong_guesses, pattern, message):
    """
    Receives the letter entered by the user and returns the The appropriate
    message, updated score and pattern.
    :param score: the current user's score.
    :param letter: the letter was chosen by the user.
    :param word: the secret word.
    :param wrong_guesses: list of wrong guesses.
    :param pattern: the current pattern.
    :param message: the current message
    :return: a tuple with the updated message, score and pattern.
    """
    message = invalid_letter(letter, wrong_guesses, pattern)
    if not message:
        score -= 1
        if letter in word:
            pattern = update_word_pattern(word, pattern, letter)
            score += score_updater(pattern, letter)
            message = SUCCESSFUL_GUESS
        else:
            wrong_guesses.append(letter)
            message = WRONG_LETTER
    return message, score, pattern


def word_input(score, choice, secret_word, pattern):
    """
    Receives the word entered by the user and returns the The appropriate
    message, updated score and pattern.
    :param score: the current score.
    :param choice: the word was chosen by the user.
    :param secret_word: the secret word.
    :param pattern: the current pattern.
    :return: a tuple with the updated score, message and pattern.
    """
    score -= 1
    if choice == secret_word:
        # End of game
        # Receive points for all the underscores that are now revealed.
        score += score_updater(pattern, UNDERSCORE)
        pattern = secret_word
        message = ""
    else:
        message = WRONG_WORD
    return score, message, pattern


def end_of_game(score, word):
    """
    Returns a message based on the score situation.
    :param score: the current score.
    :param word: the secret word.
    :return: the updated message.
    """
    if score > 0:
        message = WINNING_MESSAGE
    else:
        message = LOSING_MESSAGE + word
    return message


def run_single_game(words_list, score):
    """
    Runs the "Hangman" game once.
    :param words_list: list of words.
    :param score: number of the player's points.
    :return: the player's points at the end of the game.
    """
    SECRET_WORD = hangman_helper.get_random_word(words_list)
    pattern = UNDERSCORE * len(SECRET_WORD) # initializing first pattern
    wrong_guesses = [] # list of all wrong letter guesses
    message = FIRST_TURN
    while UNDERSCORE in pattern and score > 0:
        hangman_helper.display_state(pattern, wrong_guesses, score, message)
        choice_type, choice = hangman_helper.get_input()
        if choice_type == hangman_helper.LETTER:
            message, score, pattern = letter_input(score, choice, SECRET_WORD,
                                                   wrong_guesses, pattern,
                                                   message)
        elif choice_type == hangman_helper.WORD:
            score, message, pattern = word_input(score, choice, SECRET_WORD,
                                                 pattern)
        elif choice_type == hangman_helper.HINT:
            score -= 1
            message = make_suggestions(words_list, pattern, wrong_guesses)
    message = end_of_game(score, SECRET_WORD)
    hangman_helper.display_state(pattern, wrong_guesses, score, message)
    return score


def main():
    words_list = hangman_helper.load_words()
    play = True  # does the player want to keep playing.
    while play:
        score = run_single_game(words_list, hangman_helper.POINTS_INITIAL)
        num_of_games = 1  # games played
        while score > 0:
            message = AFTER_WIN.format(num_of_games, score)
            if hangman_helper.play_again(message):
                score = run_single_game(words_list, score)
                num_of_games += 1
            else:
                play = False
                break
        else:
            message = AFTER_LOSE.format(num_of_games)
            if hangman_helper.play_again(message):
                # Reset score and games played.
                score = hangman_helper.POINTS_INITIAL
                num_of_games = 0
            else:
                play = False


if __name__ == "__main__":
    main()
