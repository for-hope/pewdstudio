import sqlite3
import re
from difflib import SequenceMatcher as sq

def longest_common_substring(s1, s2):
  m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
  longest, x_longest = 0, 0
  for x in range(1, 1 + len(s1)):
    for y in range(1, 1 + len(s2)):
      if s1[x - 1] == s2[y - 1]:
        m[x][y] = m[x - 1][y - 1] + 1
        if m[x][y] > longest:
          longest = m[x][y]
          x_longest = x
      else:
        m[x][y] = 0
  return s1[x_longest - longest: x_longest]

def longest_common_sentence(s1, s2):
    s1_words = s1.split(' ')
    s2_words = s2.split(' ')  
    return ' '.join(longest_common_substring(s1_words, s2_words))

def sql_search(word):
    con = sqlite3.connect('captions.db')
    cursorObj = con.cursor()
    word = '%{}%'.format(word)
    cursorObj.execute('SELECT flavor FROM lines WHERE flavor LIKE ?',(word,))
    results = cursorObj.fetchall()
    con.close()

    return results

def find_phrases(phrase):
    words = phrase.split(' ')
    hashed_words = {}
    for word in words:
        results = sql_search(word)
        if results:
            hashed_words[word] = results
        else:
            hashed_words[word] = []
    saved_word = ''
    last_results = ''
    list_to_search = []
    for index,word in enumerate(words):
        go = True
        co = 1
        big_word = word
        current_results = word
        while go:
            if len(hashed_words[word]) != 0:
                if index+co < len(words):
                    big_word = '{} {}'.format(big_word,words[index+co])
                    if len(sql_search(big_word)) != 0:
                        current_results = big_word
                        go = True
                        co += 1
                    else:
                        go = False
                else:
                    go = False
            else:
                go = False

        if current_results not in last_results:
            add = True
            if len(list_to_search) > 0:
                l = len(list_to_search)-1
                s1 = list_to_search[l]

                if len(current_results) > len(s1) and len(current_results.split(' ')) > len(s1.split(' ')):
                    s2 = current_results
                    match = sq(None, s1, s2).find_longest_match(0, len(s1), 0, len(s2))
                    str_match = s2[:match.b+match.size]

                    if str_match in current_results.split(' ') or (str_match in s1 and ' ' in str_match):
                        list_to_search[l] = s1.replace(str_match,'').lstrip().rstrip() 
                else:
                    s2 = current_results
                    match = sq(None, s1, s2).find_longest_match(0, len(s1), 0, len(s2))

                    str_match = s2[:match.b+match.size]
                    str_match = str_match.lstrip().rstrip()

                    #fix space in the end and beginning

                    if str_match in s1.split(' ') or (str_match in s1 and ' ' in str_match):
                        add = False

            if add:  
                if len(list_to_search) > 0:        
                    l = len(list_to_search)-1
                last_results = current_results
                list_to_search.append(current_results)
    return list_to_search


def strip_string(_string):
    edited_phrase = _string
    if edited_phrase.startswith(' '):
        edited_phrase = edited_phrase[1:] 
    if edited_phrase.endswith(' '):
        edited_phrase = edited_phrase[:-1]
    edited_phrase = edited_phrase.replace('  ',' ')
    return edited_phrase

