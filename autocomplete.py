"""
autocomplete module
"""

class Node:
    """
    Node class represents a character in a Trie
    """
    ntop_words = 4

    def __init__(self, character: str, end=False):
        self.character = character
        self.children = {}
        self.top_words = []
        self.end = end

    def add_child(self, node):
        """
        add_child adds a node as child
        :param node: node to add as child
        :type node: Node
        :return: the real child node
        """
        if node.character not in self.children:
            self.children[node.character] = node
        return self.children[node.character]

    def set_top_words(self):
        """
        set_top_words recursively sets the top worlds for the node
        and all it's children
        """
        if self.end:
            self.top_words.append(self.character)
        if self.children:
            for child in self.children.values():
                child.set_top_words()
                self.top_words += [
                    self.character+top_word
                    for top_word in child.top_words]
        else:
            self.top_words = [self.character]
        self.top_words.sort()
        self.top_words = self.top_words[:self.ntop_words]


    def display(self, prefix: str = ""): # pragma: no cover
        """
        display prints the node and it's children
        """
        print(f"{prefix}Node({self.character}, top={self.top_words}, end={self.end})")
        if self.children:
            for child in self.children.values():
                child.display(prefix+"|---")


class AutoComplete:
    """
    AutoComplete represents the whole Trie for a list of words
    """
    def __init__(self, list_of_words: [str]):
        if not isinstance(list_of_words, list):
            raise ValueError("argument should be a list of string")
        self.root = Node("")
        self.construct_trie(list_of_words)

    def construct_trie(self, list_of_words: [str]):
        """
        :param list_of_words: list of world from wich the Trie will be constructed
        :type list_of_words: [str]
        """
        for word in list_of_words:
            if not isinstance(word, str):
                raise ValueError(f"element {word} should be a string not a {type(word)}")
            self.insert_word(word)
        self.root.set_top_words()

    def insert_word(self, word: str):
        """
        inserts a word in the Trie
        :param word: word to insert
        :type word: string
        """
        node = self.root
        for index, character in enumerate(word):
            is_last_character = index == (len(word)-1)
            node_child = Node(character, end=is_last_character)
            node = node.add_child(node_child)

    def autocomplete(self, prefix: str) -> [str]:
        """
        autocomplete performs the autocompletion from a prefix
        :param prefix: prefix from which the autocompletion starts
        :type prefix: string
        """
        if not isinstance(prefix, str):
            raise ValueError(f"prefix {prefix} should be a string not a {type(prefix)}")
        node = self.root
        prefix = prefix.lower() # lower the prefix to be case insensitive
        for character in prefix:
            if character not in node.children:
                return []
            node = node.children[character]
        return [prefix[:-1]+t for t in node.top_words]

    def display(self): # pragma: no cover
        """
        display the whole trie
        """
        self.root.display()


def main():  # pragma: no cover
    """
    main entry point
    """
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="text file of vocabulary with one word by line")
    parser.add_argument("prefix", help="prefix wanted for autocompletion")

    args = parser.parse_args()

    try:
        with open(args.file, "r") as file_descriptor:
            list_of_words = [word.strip() for word in file_descriptor.readlines()]
    except FileNotFoundError as exc:
        print(exc)
        sys.exit(1)

    auto = AutoComplete(list_of_words)
    print(auto.autocomplete(args.prefix))

if __name__ == "__main__":  # pragma: no cover
    main()
