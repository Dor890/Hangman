#################################################################
# FILE : hangman.py
# WRITER : Dor Messica , dor.messica , 318391877
# EXERCISE : intro2cse ex4 2020
# DESCRIPTION: The program contains the game "Hangman".
#################################################################
import hangman_helper

UNDERSCORE = '_'
RESTART = hangman_helper.play_again


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


def run_single_game(words_list, score):
    """
    Runs the "Hangman" game once.
    :param words_list: list of words.
    :param score: number of the player's points.
    :return: the player's points at the end of the game.
    """
    SECRET_WORD = hangman_helper.get_random_word(words_list)
    pattern = UNDERSCORE * len(SECRET_WORD)
    wrong_guesses = []
    message = "First turn, lets begin!"
    while UNDERSCORE in pattern and score > 0:
        hangman_helper.display_state(pattern, wrong_guesses, score, message)
        choice_type, choice = hangman_helper.get_input()
        if choice_type == hangman_helper.LETTER:
            if not choice.isalpha() or len(choice) > 1\
                    or not choice.islower():
                message = "Letter is invalid"
                continue
            elif choice in wrong_guesses or choice in pattern:
                message = "The letter you entered was already guessed chosen"
                continue
            else:
                score -= 1
                if choice in SECRET_WORD:
                    pattern = update_word_pattern(SECRET_WORD, pattern, choice)
                    score += score_updater(pattern, choice)
                    message = "Successful guess!"
                    continue
                else:
                    wrong_guesses.append(choice)
                    message = "You guessed the letter wrong!"
                    continue
        elif choice_type == hangman_helper.WORD:
            score -= 1
            if choice == SECRET_WORD:
                # Receive points for all the underscores that are now revealed.
                score += score_updater(pattern, UNDERSCORE)
                pattern = SECRET_WORD
            else:
                message = "You guessed the word wrong!"
                continue
        elif choice_type == hangman_helper.HINT:
            score -= 1
            words_for_hint = filter_words_list(words_list, pattern,
                                               wrong_guesses)
            recommended_words = []
            if len(words_for_hint) > hangman_helper.HINT_LENGTH:
                for i in range(0, hangman_helper.HINT_LENGTH):
                    recommended_words.append(words_for_hint
                                             [i * len(words_for_hint) //
                                              hangman_helper.HINT_LENGTH])
                hangman_helper.show_suggestions(recommended_words)
                message = "You got a hint!"
                continue
            else:
                hangman_helper.show_suggestions(words_for_hint)
                message = "You got a hint!"
                continue
    if score > 0:
        message = "Congratulations, you won!"
    else:
        message = "You lost! The secret word was: " + SECRET_WORD
    hangman_helper.display_state(pattern, wrong_guesses, score, message)
    return score


def same_letters(word, pattern):
    """
    Checks if the pattern can be a pattern of the word.
    :param word: a word from the words list.
    :param pattern: the secret word's pattern.
    :return: a boolean value if the revealed letters of the pattern are in same
             places as in the word and aren't in other places in the word.
    """
    confirmed_letters = pattern.split('_')
    for i in range(len(pattern)):
        if (pattern[i] == '_' and word[i] in confirmed_letters) or\
                pattern[i] != '_' and pattern[i] != word[i]:
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


def main():
    words_list = hangman_helper.load_words()
    play = True
    while play:
        score = run_single_game(words_list, hangman_helper.POINTS_INITIAL)
        num_of_games = 1
        while score > 0:
            message = ("You have played {} games, and have currently {} "
                       "points. Would you like to play again?").format\
                (num_of_games, score)
            if hangman_helper.play_again(message):
                score = run_single_game(words_list, score)
                num_of_games += 1
                continue
            else:
                play = False
                break
        else:
            message = ("You have survived {} games until you lost. Would you "
                       "like to restart?").format(num_of_games)
            if hangman_helper.play_again(message):
                score = hangman_helper.POINTS_INITIAL
                num_of_games = 0
                continue
            else:
                play = False
                break


if __name__ == "__main__":
    main()
