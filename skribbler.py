import argparse
from selenium import webdriver
from selenium.webdriver.support.ui import Select

class Skribbler:
    def __init__(self, difficulty, numWords):
        self.difficulty = difficulty
        self.numWords = numWords
        self.driver = webdriver.Chrome("/Applications/chromedriver")
        self.driver.implicitly_wait(10)
        self.output = open("out.txt", "w")
        self.selectedWords = set()

    def run(self):
        self.driver.get("https://randomwordgenerator.com/pictionary.php")
        self.__setBatchSize()
        self.__selectDifficulty()
        self.__generateAndSelectWords()
        self.__cleanUp()

    def __setBatchSize(self):
        self.batchSize = self.driver.find_element_by_id("qty")
        self.batchSize.clear()
        self.batchSize.send_keys("50")

    def __selectDifficulty(self):
        self.difficultySelect = Select(self.driver.find_element_by_id("category"))
        value = None
        if self.difficulty == "easy":
            value = "6"
        elif self.difficulty == "medium":
            value = "7"
        elif self.difficulty == "hard":
            value = "8"
        elif self.difficulty == "harder":
            value = "9"
        self.difficultySelect.select_by_value(value)

    def __generateAndSelectWords(self):
        self.generateButton = self.driver.find_element_by_id("btn_submit_generator")
        
        while True:
            self.generateButton.click()
            wordList = self.driver.find_element_by_id("result")
            wordContainers = wordList.find_elements_by_tag_name("span")
            for wordContainer in wordContainers:
                word = wordContainer.text
                if word not in self.selectedWords and len(word) <= 30:
                    self.selectedWords.add(word)
                    self.output.write("{}, ".format(word))
                    if len(self.selectedWords) >= self.numWords:
                        return

    def __cleanUp(self):
        self.driver.quit()
        self.output.close()

parser = argparse.ArgumentParser(description="select difficulty of words")
parser.add_argument("difficulty", choices=["easy", "medium", "hard", "harder"])
parser.add_argument("-n", "--num_words", type=int, default=200, choices=range(4, 300))
args = parser.parse_args()

skribbler = Skribbler(args.difficulty, args.num_words)
skribbler.run()
