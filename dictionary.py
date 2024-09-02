from collections import defaultdict, deque

def find_path(dictionary, start_word, end_word):
    #adds the dictionary txt file to a set
    wordSet = set(dictionary)
    #keys of dictionary from patterns formed changing 1 character in word at a time
    def create_graph(words):
        graph = defaultdict(list)
        for word in words:
            for i in range(len(word)):
                pattern_match = word[:i] + '*' + word[i+1:]
                graph[pattern_match].append(word)
        return graph
    
    graph = create_graph(dictionary)
    
    #initialises BFS with a queue with starting word and a visited word set
    queue = deque([(start_word, [start_word])])
    visited = set()
    visited.add(start_word)
    
    #for each character position in current word, creates pattern
    #by replacing with '*' to look up neighbour words (words 1 character change away)
    #if neighbour word is end word, returns current path and end word
    #else if neighbour word not visited and exists in wordSet, marks visited adds to queue with path
    while queue:
        word, path = queue.popleft()
        for i in range(len(word)):
            pattern_match = word[:i] + '*' + word[i+1:]
            for neighbour in graph[pattern_match]:
                if neighbour == end_word:
                    return path + [end_word]
                if neighbour not in visited and neighbour in wordSet:
                    visited.add(neighbour)
                    queue.append((neighbour, path + [neighbour]))
    return []

def read_dictionaryfile(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

dictionary_path = "Dictionary.txt"
dictionary = read_dictionaryfile(dictionary_path)