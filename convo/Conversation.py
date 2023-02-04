import spacy
from collections import Counter
from string import punctuation
nlp = spacy.load("en_core_web_lg")

class Conversation:
    def __init__(self, prompt):
        self.prompt = ""
        self.promptHW = self.get_hotwords(prompt)
        self.prevInputHW = ""
        self.threshold = 0.6
    
    def get_hotwords(self,text):
        result = ""
        pos_tag = ['PROPN', 'ADJ', 'NOUN'] # 1
        doc = nlp(text.lower()) # 2
        for token in doc:
            # 3
            if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
                continue
            # 4
            if(token.pos_ in pos_tag):
                result += (token.text + " ")
        return nlp(result)
    
    def getPropN(self):
        result = []
        pos_tag = ['PROPN', 'NOUN']
        for token in self.prevInputHW:
            # 3
            if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
                continue
            # 4
            if(token.pos_ in pos_tag):
                result.append(token.text)
        return set(result)
         
    def compare(self, prompt, input):
        return prompt.similarity(input)

    def addTopic(self):
        print("Prompt Before: ", self.promptHW.text)
        self.promptHW = nlp(self.promptHW.text + self.prevInputHW.text)
        print("Prompt After: ", self.promptHW.text)
        self.prevInputHW = ""

    def hear_sentence(self,curInput):
        curInputHW = self.get_hotwords(curInput)
        # print("PrevInputHW: ", self.prevInputHW)
        # print("COMPARISON: ", self.compare(self.promptHW,curInputHW))
        if self.compare(self.promptHW,curInputHW) > self.threshold:
            self.prevInputHW = ""
            print("--------------------good, on topic--------------------")
            return 0
        elif self.prevInputHW != "":
            if self.compare(self.prevInputHW, curInputHW) > self.threshold:
                self.prevInputHW = curInputHW
                print("---------------two sentences on new topic: add new topic: ", self.getPropN(), "---------------")
                return 1
            print("---------------new topic1 + new topic 2 : Anyways, let's go back to our discussion.---------------")
            return 3
        else:
            self.prevInputHW = curInputHW
            print("---------------First strike on new topic---------------")
            return 2
    
    

