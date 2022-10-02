import re

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

# iterate through words, first check if all potential letters is contained in the word, if so then check each letter is in none of the positions listed as incorrect.
def yellowFilter(words: list[str], yellows: dict) -> list[str]:
  filteredWords = []
  potentialLetters = yellows.keys()
  for word in words:
    potentialWord = True
    for letter in potentialLetters:
      if letter not in word:
        potentialWord = False
        break
      else:
        positions = yellows[letter]
        for position in positions:
          if word[position] == letter:
            potentialWord = False
    
    if potentialWord:
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
def isGreenInputValid(guess) -> bool:
  return True if len(guess) == 5 or len(guess) == 0 else False

def isYellowInputValid(input: str) -> bool:
  strs = input.split()
  for str in strs:
    valid = re.fullmatch("^[a-zA-Z]:[0-5]{1}(,([0-5]){1})*", str)
    if valid == None:
      return False
  return True

def formatGreyInput(letters: str) -> str:
  formatted = letters.replace(",", "")
  return formatted

def formatYellowInput(input: str) -> dict:
  yellowsDict = {}
  lettersAndPositions = input.split()
  for letterAndPositions in lettersAndPositions:
    split = letterAndPositions.split(":")
    letter = split[0]
    positions = [int(pos) for pos in split[1].split(",")]
    yellowsDict[letter] = positions
  return yellowsDict

def allUnderscore(guess: str) -> bool:
  for c in guess:
    if c != "_":
      return False
  return True



def main():
  # get all 5 letter words
  allWords = getAllWords()

  # get user input
  validGreenInput = False
  greens = ""
  while not validGreenInput:
    print("Please enter your guess with unknown letters marked as an underscore (_):")
    greens = input("==>")
    if isGreenInputValid(greens):
      validGreenInput = True
    else:
      print("Invalid input, guess must be 5 characters long, or, empty. ")

  validYellowInput = False
  yellows = ""
  
  while not validYellowInput:
    print("Any letters in incorrect position? If so please enter them in the form 'letter:indexes letter:indexes etc.' where the indexes are comma seperated, or, hit enter to ignore: ")
    yellows = input("==>")
    if isYellowInputValid(yellows):
      validYellowInput = True
    else:
      print("Invalid input, guess must be in the form 'letter:indexes letter:indexes etc.' where the indexes are comma seperated, or, empty. ")

  if yellows:
    yellows = formatYellowInput(yellows)

  print("Any letters not in the word? If so please enter them in one line (comma seperated), or, hit enter to ignore: ")
  greys = input("==>")

  if greys:
    greys = formatGreyInput(greys)

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



 