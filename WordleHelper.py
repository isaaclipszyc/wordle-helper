
# words in AllWords.txt comes from https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt
def getAllWords() -> list[str]:
  txtFile = open("AllWords.txt")
  content = txtFile.read().splitlines()
  txtFile.close()
  return content

# iterate through words, 
def greenFilter(allWords: list[str], guess: str) -> list[str]:
  filteredWords = []
  for i, c in enumerate(guess):
    if c != "_":
      wordsToFilter = filteredWords
      # if wordsToFilter is empty, this is the first letter found so we set wordsToFilter to allWords
      if len(wordsToFilter) == 0:
        wordsToFilter = allWords

      # create a new list and iterate through wordsToFilter, 
      # if the word contains the character we are searching for at the right index, then add to the new list
      newFilteredList = []
      for word in wordsToFilter:
        if word[i] == c:
          newFilteredList.append(word)
      
      # after each index we update what the filtered list is - it should shorten with each letter
      filteredWords = newFilteredList
      # check to see if filteredWords is empty, and if so break as this would indicate that there is no word with that letter at that position
      if len(filteredWords) == 0:
        return filteredWords

  return filteredWords

# iterate through words, check if all potential letters is contained in the word, if so append to output
def yellowFilter(words: list[str], potentialLetters) -> list[str]:
  filteredWords = []
  for word in words:
    containsAllPotential = True
    for letter in potentialLetters:
      if letter not in word:
        containsAllPotential = False
        break
    
    if containsAllPotential:
      filteredWords.append(word)
  
  return filteredWords

# iterate through words, if any wrongLetter is found in the word, do not add it to the filtered words.
def filterFunction(word: str, wrongLetters: str) -> bool:
  for letter in wrongLetters:
    if letter in word:
      return False
  return True

def greyFilter(words: list[str], wrongLetters: str) -> list[str]:
  filtered = filter(lambda word: filterFunction(word, wrongLetters), words)
  return list(filtered)



# utility functions
def isInputValid(guess) -> bool:
  return True if len(guess) == 5 else False

def formatInput(letters: str) -> str:
  formatted = letters.replace(",", "")
  return formatted

def allUnderscore(guess: str) -> bool:
  for c in guess:
    if c != "_":
      return False
  return True



def main():
  # get all 5 letter words
  allWords = getAllWords()

  # get user input
  validInput = False
  greens = ""
  while not validInput:
    print("Please enter your guess with unknown letters marked as an underscore (_):")
    greens = input("==>")
    if isInputValid(greens):
      validInput = True
    else:
      print("Invalid input, guess must be 5 characters long. ")

  print("Any letters in incorrect position? If so please enter them in one line (comma seperated), or, hit enter to ignore: ")
  yellows = input("==>")

  if yellows:
    yellows = formatInput(yellows)

  print("Any letters not in the word? If so please enter them in one line (comma seperated), or, hit enter to ignore: ")
  greys = input("==>")

  if greys:
    greys = formatInput(greys)

  #filter words using found letters (letters in correct position)
  # filtered words from greenFilter is used as the base for the next filtering.
  potentialWords = greenFilter(allWords, greens)

  # if user inputs all underscores, then use allWords for next filtering step.
  if allUnderscore(greens) == True:
    potentialWords = allWords
  
  # filter words using potential letters (letters in incorrect position)
  potentialWords = yellowFilter(potentialWords, yellows)

  # filter words using letters not found in word
  potentialWords = greyFilter(potentialWords, greys)

  # output to user
  print("Potential words:")
  print(potentialWords)

main()



 