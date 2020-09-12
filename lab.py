# NO ADDITIONAL IMPORTS!
from text_tokenize import tokenize_sentences


class Trie:
    def __init__(self):
        self.value=None
        self.children={}
        self.type=None


    def __setitem__(self, key, value):
        """
        Add a key with the given value to the trie, or reassign the associated
        value if it is already present in the trie.  Assume that key is an
        immutable ordered sequence.  Raise a TypeError if the given key is of
        the wrong type.
        """
        if self.type==None:
            self.type=type(key)
        elif type(key)!=self.type:
            raise TypeError
            
        if key=='':
            self.value=value
            return 
        if key==():
            self.value=value
            return
        if key[0:1] not in self.children:
            self.children[key[0:1]]=Trie()
            
        self.children[key[0:1]][key[1:]] =value  # same as self.children[key[0]].__setitem__(key[1::],value)
        

    def __getitem__(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        """
        if type(key)!=self.type:
            raise TypeError
            
        if key=='':
            return self.value
        if key==():
            return self.value
        if key[0:1] not in self.children:
            raise KeyError
            
        return self.children[key[0:1]][key[1:]]

    def __delitem__(self, key):
        """
        Delete the given key from the trie if it exists. If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        """
        if type(key)!=self.type:
            raise TypeError
        if key not in self:
            raise KeyError
        
        self.children[key[0:1]][key[1:]]=None
        

    def __contains__(self, key):
        """
        Is key a key in the trie? return True or False.
        """
    
        if key[0:1] not in self.children:
            return False
   
        else:
            if len(key)==1:
                if self.children[key[0:1]].value==None:
                    return False
                return True
            if key[1:] in self.children[key[0:1]]:
                return True
        return False
    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this trie and
        its children.  Must be a generator!
        """
        if self.value!=None:
            if self.type==str:
                yield ('',self.value)
            if self.type==tuple:
                yield ((),self.value)
        for child in self.children:
            for pair in self.children[child]:
                yield (child+pair[0],pair[1])
                
            


def make_word_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    words in the text, and whose values are the number of times the associated
    word appears in the text
    """
    tree=Trie()
    freqdict={}
    sentences=tokenize_sentences(text) #iterate through every sentence then every word
    for sentence in sentences:
        newsentence=sentence.split() #split creates the words
        for word in newsentence:
            if word in freqdict:
                freqdict[word]=freqdict[word]+1
            else:
                freqdict[word]=1
    for word in freqdict:
        tree.__setitem__(word, freqdict[word]) #tree[word] = freqdict[word]
        
    return tree


def make_phrase_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    sentences in the text (as tuples of individual words) and whose values are
    the number of times the associated sentence appears in the text.
    """
    
    tree=Trie()
    freqdict={}
    sentences=tokenize_sentences(text) 
    for sentence in sentences:
        splitsentence=tuple(sentence.split()) #we do the same thing as in make word
        if splitsentence in freqdict:
            freqdict[splitsentence]=freqdict[splitsentence]+1 #add to the dictionary with the values
        else:
            freqdict[splitsentence]=1
    for sentence in freqdict:
        tree.__setitem__(sentence, freqdict[sentence]) #tree[word] = freqdict[word]
    return tree

def autocomplete(trie, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is of an inappropriate type for the
    trie.
    """
    if type(prefix)!=trie.type:
        raise TypeError
    def node(trie,prefix):#helper that returnns and follows the prefix
        if len(prefix)==0:
            return trie
        else:
            if prefix[0:1] in trie.children:
                return node(trie.children[prefix[0:1]],prefix[1:])
            return None
    letter=node(trie,prefix) 
    if letter==None:
        return []
    children=list(iter(letter)) #gets all the childeren
    
    
    if max_count!=None:
        children=sorted(children, key=lambda k:k[1], reverse=True) #returns the sorted list
        children=children[0:max_count]
    result=[]
    for tupl in children:
        result.append(prefix+tupl[0])
    return result
        
def validedits(trie,prefix):
    
    alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    edits=set() #start with set so that we take care of repeats
    #insertion 
    for position in range(len(prefix)+1): 
        for letter in alphabet:
            edit=prefix[:position]+letter+prefix[position:]
            if edit in trie:
                edits.add(edit)
    #deletion
    for position in range(len(prefix)):
        edit=prefix[:position]+prefix[position+1:]
        if edit in trie:
            edits.add(edit)
    #replace
    for position in range(len(prefix)):
            for letter in alphabet:
                edit=prefix[:position]+letter+prefix[position+1:]
                if edit in trie:
                    edits.add(edit)
    #transpose
    for position in range(len(prefix)-1):
            edit=prefix[:position]+prefix[position+1]+prefix[position]+prefix[position+2:]
            if edit in trie:
                edits.add(edit)
    
    return edits

def autocorrect(trie, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    completed=autocomplete(trie, prefix,max_count) #look at the ones that don't differ
    validedit=validedits(trie,prefix) 
    validtuples=[]
    for edit in validedit: #want to sort all the edits
        validtuples.append((edit,trie.__getitem__(edit)))
    validtuples.sort(key=lambda x:x[1],reverse=True)
    
    autocorrected=[]
    if max_count==None: 
        rangee=len(validtuples) #we want all the valid edits
    elif len(completed)<max_count:
        rangee=max_count-len(completed) #only want up to max count
    else:
        return completed #otherwise we only want to return the nonedits
        
    for position in range(rangee):
        if validtuples[position][0] not in completed:
            autocorrected.append(validtuples[position][0])
    return completed+autocorrected
        
        
def word_filter(trie, pattern):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    result=set()
    
    if pattern=='': #base case that theres nothing
        if trie.value!=None:
            result.add((pattern,trie.value))
        return result
    if pattern[0]=='?': #then we only have one option of looking at the children
        for node in trie.children:
            answer=word_filter(trie.children[node],pattern[1:])
            for i in answer:
                result.add((node+i[0],i[1]))
    elif pattern[0]=='*': #we have to recursively look at the rest of the nodes and only
                            #recures on whole pattern instead of pattern[1:]
        answer=word_filter(trie,pattern[1:])
        for i in answer:
            result.add((i[0],i[1]))
       
        for node in trie.children:
            answer=word_filter(trie.children[node],pattern)
            for i in answer:
                result.add((node+i[0],i[1]))
    else: #we keep the character and look at the children
        for node in trie.children:
            if node==pattern[0]:
                answer=word_filter(trie.children[node],pattern[1:])
                for i in answer:
                    result.add((pattern[0]+i[0],i[1]))
        
        
    return list(result)


# you can include test cases of your own in the block below.
if __name__ == '__main__':
    with open("Alice's Adventures in Wonderland.txt", encoding="utf-8") as f:
        text = f.read()
    trie=make_phrase_trie(text)
    
    # print(autocomplete(trie,(),max_count=6))
    
    # print(autocorrect(trie, 'hear',max_count=12))
    # print(len(word_filter(trie, '*')))
    # count=0
    # for word in word_filter(trie, '*'):
    #     count+=word[1]
    #     print(count)
    # sentences=tokenize_sentences(text) 
    # count=0
    # for sentence in sentences:
    #     count+=1
    #     print(count)
    
    sentences=tokenize_sentences(text) 
    count=set()
    for sentence in sentences:
        count.add(sentence)
    print(len(count))
    
    with open("Metamorphosis.txt", encoding="utf-8") as f:
        text = f.read()
        trie=make_word_trie(text)
        # print(autocomplete(trie,'gre',max_count=6))
        # print(word_filter(trie, 'c*h'))
          
    with open("A Tale of Two Cities.txt", encoding="utf-8") as f:
        text = f.read()
        trie=make_word_trie(text)
        # print(word_filter(trie, 'r?c*t'))
        
        
    with open("Dracula.txt", encoding="utf-8") as f:
        text = f.read()
        trie=make_word_trie(text)
        
        # print(len(word_filter(trie, '*')))
        # count=0
        # for word in word_filter(trie, '*'):
        #     count+=word[1]
        # print(count)
        
    with open("Pride and Prejudice.txt", encoding="utf-8") as f:
        text = f.read()
        trie=make_word_trie(text)
          
        # print(autocorrect(trie, 'hear'))
          
          
          
          
          
          
          
          
          
