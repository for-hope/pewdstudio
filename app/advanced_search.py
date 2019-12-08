import sqlite3
import re

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


def sql_search(phrase):
    con = sqlite3.connect('./app/captions.db')
    cursorObj = con.cursor()
    words = phrase.split(' ')
    for word in words:
        word = '%{}%'.format(word)
        cursorObj.execute('SELECT id, flavor FROM lines WHERE flavor LIKE ?',(word,))
    results = cursorObj.fetchall()
    con.close()
    return results

def find_phrases(phrase):
    #phrase = "tgdsfgdf hello gay i love white people"
    edited = phrase
    subphrases = [phrase]
    results = sql_search(phrase)

    last_res = ''
    res_list = list()
    res_ids = list()
    last_id = None
    while edited != '' and len(subphrases) > 0:

        found = False
        for subf in subphrases:
            s = subf
            last_res = ''
            for result in results:
                subf = str(subf)
                str_result = str(result[1])
                common_sentence = longest_common_sentence(subf, str_result)
                
                if len(common_sentence.split(' ')) > len(last_res.split()):
                    last_res = common_sentence
                    last_id = result[0]
                    found = True
                elif len(common_sentence.split(' ')) == len(last_res.split()):
                    if len(common_sentence) > len(last_res):
                        last_res = common_sentence
                        last_id = result[0]
                        found = True
            if last_res=='':
                if s in subphrases:
                    subphrases.remove(s)
                else:
                    break
                edited = edited.replace(subf,'')
                for sub in subphrases:
                    if sub == '':
                        subphrases.remove(sub)
                break
            else:
                if found:
                    res_ids.append(last_id)
                    res_list.append(last_res)
                    subphrases = edited.split('{}'.format(last_res))
                    for index, sub in enumerate(subphrases):
                        if sub.endswith(' '):
                            sub = sub[:-1]
                            subphrases[index] = sub
                        if sub.startswith(' '):
                            sub = sub[:-1]
                            subphrases[index] = sub
                        empty = True
                        for char in sub:
                            if char != ' ':
                                empty = False              
                        if not sub or sub == ' ' or sub == '' or empty:
                            subphrases.remove(subphrases[index])

                            
                    #print('sub ',subphrases)
                    edited = edited.replace(last_res,'')
                else:
                    edited = edited.replace(subf,'')
        if not found:
            break
    
    return res_list
    #print(res_list)
    #print(res_ids)
    # mat = list()
    # l = list()
    # for i,id in enumerate(res_ids):
    #     l.append(id)
    #     l.append(res_list[i])
    #     mat.append(l)
    #     l = list()
    # return mat

def strip_string(_string):
    edited_phrase = _string
    if edited_phrase.startswith(' '):
        edited_phrase = edited_phrase[1:] 
    if edited_phrase.endswith(' '):
        edited_phrase = edited_phrase[:-1]
    edited_phrase = edited_phrase.replace('  ',' ')
    return edited_phrase

def words_to_search(phrase):
    mlist = find_phrases(phrase)
    order_list = []

    for item in mlist:
        text = item
        order_list.append(phrase.find(text))


    sorted_list = [x for _,x in sorted(zip(order_list,mlist))]
    edited_phrase = phrase
    hashed_words = {}
    for item in sorted_list:
        phrase_list = edited_phrase.split(' ')

        for word in phrase_list:
            if not word in item: 
                hashed_words[word] = False
                edited_phrase = edited_phrase.replace('{}'.format(word),'')
                edited_phrase = strip_string(edited_phrase)

            else:
                hashed_words[item] = True
                edited_phrase = edited_phrase.replace('{}'.format(str(item)),'')
                edited_phrase = strip_string(edited_phrase)

                break

    return hashed_words

hashed_words = words_to_search('hello i love gay people ghfdg now')
for word in hashed_words:
    if hashed_words[word]:
        print('{}'.format(word))
    else:
        print('Doesnt exist : {}'.format(word))








                    

# s1 = 'i love cars so much man'
# s2 = 'we really love cars so much you know'
# common_sentence = longest_common_sentence(s1, s2)
# print (common_sentence)