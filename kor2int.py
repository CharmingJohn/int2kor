# -*- coding: utf-8 -*-

import re

def is_number(x):
    #if type(x) == str:
    #    x = x.replace(',', '')
    try:
        float(x)
    except:
        return False
    return True

def text2int (textnum, numwords={}):
    #units = [
    #    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
    #    'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
    #    'sixteen', 'seventeen', 'eighteen', 'nineteen',
    #]
    units = [
        '영', '일', '이', '삼', '사', '오', '육', '칠', '팔',
        '구'
    ]
    tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
    #scales = ['hundred', 'thousand', 'million', 'billion', 'trillion']
    scales = ['십', '백', '천']
    ordinal_words = {'first':1, 'second':2, 'third':3, 'fifth':5, 'eighth':8, 'ninth':9, 'twelfth':12}
    ordinal_endings = [('ieth', 'y'), ('th', '')]

    hangul = re.compile(r'[가-힣]')

    if not numwords:
        #numwords['and'] = (1, 0)
        numwords[' '] = (1, 0)
        for idx, word in enumerate(units): numwords[word] = (1, idx)
        #for idx, word in enumerate(tens): numwords[word] = (1, idx * 10)
        #for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)
        for idx, word in enumerate(scales): numwords[word] = (10 ** (idx + 1), 0)

    #textnum = textnum.replace('-', ' ')
    textnum = textnum.replace('공', '영')
    textnum = list(textnum)


    current = result = 0
    curstring = ''
    onnumber = False
    lastunit = False
    lastscale = False

    def is_numword(x):
        if is_number(x):
            return True
        if word in numwords:
            return True
        return False

    def from_numword(x):
        if is_number(x):
            scale = 0
            increment = int(x.replace(',', ''))
            return scale, increment
        return numwords[x]

    #for word in textnum.split():
    for word in textnum:
        if word in ordinal_words:
            scale, increment = (1, ordinal_words[word])
            current = current * scale + increment
            #if scale > 100:
            if scale > 10:
                result += current
                current = 0
            onnumber = True
            lastunit = False
            lastscale = False
        else:
            for ending, replacement in ordinal_endings:
                if word.endswith(ending):
                    word = "%s%s" % (word[:-len(ending)], replacement)

            if (not is_numword(word)) or (word == ' ' and not lastscale):
                if onnumber:
                    # Flush the current number we are building
                    curstring += repr(result + current) + " "
                curstring += word + " "
                result = current = 0
                onnumber = False
                lastunit = False
                lastscale = False
            else:
                scale, increment = from_numword(word)
                onnumber = True

                if lastunit and (word not in scales):
                    # Assume this is part of a string of individual numbers to
                    # be flushed, such as a zipcode "one two three four five"
                    curstring += repr(result + current)
                    result = current = 0

                if scale > 1:
                    current = max(1, current)

                current = current * scale + increment
                #if scale > 100:
                if scale > 10 :
                    result += current
                    current = 0

                lastscale = False
                lastunit = False
                if word in scales:
                    lastscale = True
                elif word in units:
                    lastunit = True

    if onnumber:
        curstring += repr(result + current)

    curstring = list(curstring)
    for i in range(len(curstring) - 1):
        if curstring[i] == ' ':
            if curstring[i+1] == ' ':
                curstring[i+1] = ''
            else:
                curstring[i] = ''

    numidx = 0

    curstring = ''.join(curstring)

    return curstring
