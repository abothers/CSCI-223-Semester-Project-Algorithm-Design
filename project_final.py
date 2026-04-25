import nltk
nltk.download('brown')                                         
from nltk.corpus import brown 

class TrieNode:
    def __init__(self):
        self.children = [None] * 26  # creates 26 empty slots (one for every letter)
        self.is_end_of_word = False # gets marked if this node completes a word

    def has_character(self, char):
        index = ord(char.lower()) - ord('a') #converts characters to 0 to 25
        return 0 <= index < 26 and self.children[index] is not None
    
    def get_character(self, char):
        return self.children[ord(char.lower()) - ord('a')] #follows pointer to code 
    
    def set_character(self, char, newNode):
        self.children[ord(char.lower()) - ord('a')] = newNode #puts new node in the right slot 

class Trie: 
    def __init__(self):
        self.root = TrieNode() #starting point of the node
    
    def insert(self, word): 
        #starts at top, goes through each letter, if slot is empty, 
        #it will create a new node there, and continue to move onto next node, 
        #once last letter is reach the word is marked complete
        current = self.root 
        for char in word:
            if not current.has_character(char):
                current.set_character(char, TrieNode())
            current = current.get_character(char)
        current.is_end_of_word = True
    
    def search(self, prefix): 
        #starts at top, goes through each letter of the prefix, 
        # if letter is not found, then the prefix doesnt exist in trie, 
        # moves down to next node, returns the node where prefix ends
        current = self.root
        for char in prefix:
            if not current.has_character(char):
                return None 
            current = current.get_character(char)
        return current

class AutocompleteEngine:
    def __init__(self, max_results=15):
        self.trie = Trie() #creates the trie to store words
        self.max_results = max_results #caps at 15 so there isnt an overload

    def put_dictionary(self, word_list):
        for word in word_list:
            if word.isalpha(): #doesnt take words with numbers of symbols
                self.trie.insert(word.lower()) 

    def get_possibilities(self, prefix):
        start_node = self.trie.search(prefix.lower()) #find where prefix ends in trie
        if start_node is None: #prefix isnt found, return empty list
            return []
        results = []
        self.collect_words(start_node, prefix.lower(), results) #gets all words from that point
        return results
    
  
    def collect_words(self, node, current_word, results):
        if len(results) >= self.max_results: #stop once limit is hit 
            return

        if node.is_end_of_word: #node completes a word add it to the results
            results.append(current_word)
      
        for i in range(26): #check all 26 
            if node.children[i] is not None: #if the child exists convert the index back to the letter
                char = chr(i + ord('a')) 
                self.collect_words(node.children[i], current_word + char, results)


if __name__ == "__main__":
    engine = AutocompleteEngine(max_results=15)
    word_library = list(set(w.lower() for w in brown.words() if w.isalpha()))   #loads all nltk words into a list 
    engine.put_dictionary(word_library) #gets them into the trie 
    
    user_input = input("Search: ")
    suggestions = engine.get_possibilities(user_input)
    
    print("\nSuggestions:")
    for s in suggestions:
        print(f"- {s}")