import numpy as np
import os

class Decipher:

    def __init__(self):
        self.message = ""

    def getMessage(self):
        """
        # This function is an accessor to output the deciphered message to user
        Time complexity: O(1)
        Space complexity: O(1)
        Error handling: no error handle required
        :return: the deciphered message
        """
        return self.message

    def messageFind(self,textfile):
        """
        # This function uses dynamic programming to solve Longest subsequence of common alphabet problem
        Time complexity: O(nm) where my program goes through both text's character by character
        Space complexity: O(nm) where n is the size of the first text and m be the size of the second text.
        Error handling: no error handling
        Pre-requisite: the text file must contain minimum of 2 encrypted message in order to decipher actual meassage
        :param textfile: a text file that contains two encrypted messages
        :return: No return
        # Concept references from Tushar Roy on his youtube videos about LCS
        # my own implementation of codes
        """

        file = open(textfile)
        a_list = []
        for string in file:
            a_list.append(string)

        # The codes above are creating a list to hold my two encrypted text
        row = len(a_list[0])  # the first text will be at the first in my list and be the row for my matrix
        col = len(a_list[1])  # the second text will be my column for my matrix
        Matrix = np.zeros((row + 1, col + 1))  # creates a matrix with row * col number of length
        for i in range(1,row + 1):  # shifting my matrix 1 to the right, this means that my matrix starts at index 1, not 0
            for j in range(1, col + 1):  # same goes for my column starting with index 1
                if a_list[0][i - 1] == a_list[1][j - 1]:  # check if the word on my top and my left is the same number or not
                    Matrix[i][j] = Matrix[i - 1][j - 1] + 1  # if they are the same, then we will use the diagonal value + 1
                else:  # else if top and left value is not the same, then pick the largest top or left value
                    if Matrix[i - 1][j] > Matrix[i][j - 1]:
                        Matrix[i][j] = Matrix[i - 1][j]
                    elif Matrix[i - 1][j] < Matrix[i][j - 1]:
                        Matrix[i][j] = Matrix[i][j - 1]
                    else:
                        Matrix[i][j] = Matrix[i - 1][j]

                        # if top and left value is the same, then i prioritize the top value
                        # set my current Matrix[i][j] value same as the top value


        # The below codes function as my backtracking program to backtrack my values from the Matrix in order to get my result
        # output as a string rather than return only the value
        String = ""
        i = row
        j = col
        # Starting from the very last index and backtrack till it reaches starting point 0
        while Matrix[i][j] > 0:
            # check if my current value is equal to left and top value, if they are the same
            # if they are, then I prioritize my top value by moving up to the top row
            if Matrix[i][j] == Matrix[i - 1][j] and Matrix[i][j - 1]:
                i -= 1

            elif Matrix[i][j] == Matrix[i][j - 1]:
                j -= 1

            elif Matrix[i][j] == Matrix[i - 1][j]:
                i -= 1
            # else when both of the top and left value is not the same with my current value
            # then current value must be taken from its diagonal value + 1
            # Before moving my pointer to the diagonal position, it means that my word contains the current alphabet
            # the String variable will store my string output but in reversed form
            else:
                String += a_list[0][i - 1]
                i -= 1
                j -= 1

        # The words that i obtained from my backtracking is in reversed order, reversing back will get the correct string result
        for i in reversed(range(0, len(String))):
            self.message += String[i]


    # Task 2
    def wordBreak(self,textfile):
        """
        # This function separate each alphabet and forms a substring of words and compare with the dictionary
        # if the substring words is in the dictionary, then it will consider the whole word
        # else if invalid alphabet will form a word as well, but it does not exist in the diciontary
        # dynamic programming is used to find the valid words, backtracking is used to retrieve valid words
        # backtracking is also used to form invalid words that does not exist in the dictionary
        Time complexity: O(kM * NM), where my k is my size of input message
                         M is my maximum size of the word in dictionary
                         N is number of words in dictionary
        Space complexity: O(kM + NM)
        Error handling: no error handling
        Pre-requisite: dictionary should contains at least 1 word or this function would not be called
        :param textfile: a dictionary file that contains valid words to compare with the deciphered message
        :return: No return
        """
        a_list = []
        file = open(textfile)
        for word in file:
            word = word.rstrip()
            a_list.append(word)


        length_of_word = len(self.message)

        longest = 0
        # find dictionary's longest word
        # M will be consider as dictionary's longest word length
        for i in range(0, len(a_list)):
            if len(a_list[i]) > longest:
                longest = len(a_list[i])

        # creating a kM matrix, where my k is the size of the message and M will be the maximum word length from dict
        # k is implement as row for my matrix
        # m will be implement as column for my matrix
        ListOfList = np.zeros((length_of_word, longest))

        # initialise my matrix from zero to -1
        # where -1 represents that my current alphabet or substring cannot form an valid word (word in dictionary)
        for i in range(0, length_of_word):
            for j in range(longest):
                ListOfList[i][j] = -1

        # the outer loop is iterating M times where each i represents that I can form substring's of size i
        # the inner loop is iterating k times where it loops through the k number of deciphered message
        #
        for i in range(1, longest + 1):
            for j in range(0, length_of_word - i + 1):
                k = j + i - 1
                String = self.message[j:k + 1]
                for word in range(0, len(a_list)):
                    if String == a_list[word]:
                        ListOfList[k][i - 1] = j
        # the below function is my backtracking function to find back the valid words and concatenate invalid substrings
        # it start from the last row of the matrix and it will loop through m times to find at that row, is there exist value that is not -1
        # if it exists, then min will store that value. min value will be used to indicate where my valid word start's index
        # self.message[int(min):int(last)] is consider the word that exist in the dictionary
        # then my row indicator (variable named "last") will jump to min - 1 row, if min value contains not -1 value
        # if min is -1, then it means the particular alphabet or substring is not found in dictionary
        # concatenate the unknown substrings until min is found as not - 1. then append the word
        min = -1
        Word = []
        word_1 = ""
        word_2 = ""
        res = ""
        last = length_of_word - 1
        while last >= 0:
            for i in range(0, longest):
                if ListOfList[int(last)][i] != -1:
                    min = ListOfList[int(last)][i]

            if min != -1:
                if len(word_2) != 0:
                    for x in reversed(range(0, len(word_2))):  # concatenate unknown words are in reverse form, this is to reverse it back to the correct order
                        res += word_2[x]
                    Word.append(res)
                    word_2 = ""
                    res = ""
                word_1 = self.message[int(min):int(last) + 1]
                Word.append(word_1)
                last = min - 1
                min = -1
            else:
                word_2 += self.message[int(last):int(last) + 1]
                last -= 1
                min = -1

        # this is to check if exiting the while loop, if there still exist any word that is stored in word_2 (unknown words will be stored here)
        if len(word_2) != 0:
            for x in reversed(range(0, len(word_2))): # concatenate unknown words are in reverse form, this is to reverse it back to the correct order
                res += word_2[x]
            Word.append(res)
            word_2 = ""
            res = ""

        # words that are formed after backtracking are in reversed order
        # this loop is to reverse the words back to form the correct result
        result = ""
        for i in reversed(range(0, len(Word))):
            if i == 0:
                result += Word[i]
            else:
                result += Word[i] + " "
        self.message = result


if __name__ == "__main__":
    user_input = input("The name of the file, contains two encrypted texts: ")
    if len(user_input) == 0:
        print("No input file found !")

    else:
        user_input_1 = input("The name of the dictionary file: ")
        a = Decipher()
        a.messageFind(user_input)
        str_1 = a.getMessage()
        print("--------------------------------------------------------------------")
        print("Deciphered message is " + str(str_1))
        if len(user_input_1) == 0:
            print("True message is " + a.getMessage())
            print("--------------------------------------------------------------------")
            print("Program End")
        elif os.stat(user_input_1).st_size != 0:
            a.wordBreak(user_input_1)
            print("True message is " + a.getMessage())
            print("--------------------------------------------------------------------")
            print("Program End")
        else:
            print("True message is " + str_1)
            print("--------------------------------------------------------------------")
            print("Program End")