from platform import node

import nltk 
nltk.download('words')
from nltk.corpus import words

class TrieNode:
    def __init__(self):
        self.children = [None] * 26 
        self.is_end_of_word = False

    def has_character(self, char):
        return self.children[ord(char) - ord('a')] is not None
    
    def get_character(self, char):
        return self.children[ord(char) - ord('a')]
    
    def set_character(self, char):
        self.children[ord(char) - ord('a')] = TrieNode()

class Trie: 
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        current_node = self.root
        for char in word:
            if not current_node.has_character(char):
                current_node.set_character(char, TrieNode())
            current_node = current_node.get_character(char)
        current_node.is_end_of_word = True
    
    def search(self, prefix):
        current_node = self.root
        for char in prefix:
            if not current_node.has_character(char):
                return None
            current_node = current_node.get_character(char)
        return current_node
    
class AutocompleteEngine:
    def __init__(self, max_results=15):
        self.trie = Trie()
        self.max_results = max_results
        self.build_trie()

    def put_dictionary(self, word_list):
        for word in word_list:
            self.trie.insert(word)

    def get_possiblities (self, prefix):
        node = self.trie.search(prefix)
        if not node:
            return []
        results = []
        self._collect_words(node, prefix, results)
        return results[:self.max_results]
    
    def collect_words(self, node, prefix, results):
        if len(results) >= self.max_results:
            return
        if node.is_end_of_word:
            results.append(words)
        for i in range(26):
            if node.children[i] is not None:
                self.collect_words(node.children[i], prefix + chr(i + ord('a')), results)

if __name__ == "__main__":
    engine = AutocompleteEngine()
    word_list = words.words()
    engine.put_dictionary(word_list)
    prefix = input("Enter a prefix: ")
    possibilities = engine.get_possiblities(prefix)
    print("Autocomplete suggestions:")
    for suggestion in possibilities:
        print(suggestion)

engine = AutocompleteEngine(max_results=10)
engine.put_dictionary([w.lower() for w in words.words()])


while True:
    prefix = input("Type a prefix (or 'quit' to exit): ").lower()
    if prefix == "quit":
        break
    results = engine.get_possibilities(prefix)
    if results:
        print(f"Suggestions: {results}")
    else:
        print("No words found.")
