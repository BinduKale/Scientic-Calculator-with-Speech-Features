import threading
import queue
import win32com.client

class PlayAudio:
    def __init__(self, voice='male', speakstatus=True, rate=0):
        self.voice = voice
        self.speakstatus = speakstatus
        self.rate = rate


        self.speakWords = {
            '1': 'one', '2': 'two', '3': 'three', '4': 'four',
            '5': 'five', '6': 'six', '7': 'seven', '8': 'eight',
            '9': 'nine', '0': 'zero', '+': 'plus', '-': 'minus',
            '*': 'multiply', '/': 'divide', '(': 'open parenthesis',
            ')': 'close parenthesis', 'AC': 'all clear', 'Del': 'delete',
            'π': 'pi', '√': 'square root', 'x²': 'x squared',
            'x³': 'x cubed', '1/x': 'one over x',
            'eˣ': 'e to the power of x', 'sin': 'sine', 'cos': 'cosine',
            'tan': 'tangent', 'log': 'log base 10', 'ln': 'natural log',
            'xʸ': 'x to the power of y',
            'x10³': 'x times ten to the power of three',
            '%': 'percent', '.': 'point', '00': 'double zero', '=': 'equal to'
        }

        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self._run_engine, daemon=True)
        self.thread.start()

    def _run_engine(self):
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Rate = self.rate

        
        voices = speaker.GetVoices()
        for i in range(voices.Count):
            token = voices.Item(i)
            desc = token.GetDescription().lower()
            if self.voice == 'female' and 'female' in desc:
                speaker.Voice = token
                break
            elif self.voice == 'male' and 'male' in desc:
                speaker.Voice = token
                break

        while True:
            text = self.queue.get()
            if text is None:
                break
            speaker.Speak(text)  
            self.queue.task_done()

    def speak(self, text):
        if self.speakstatus:
            word = self.speakWords.get(text, text)
            self.queue.put(word)  

    def stop(self):
        self.queue.put(None)


if __name__ == '__main__':
    import time
    ob = PlayAudio(voice='male')
    ob.speak('1')
    ob.speak('+')
    ob.speak('2')
    ob.speak('=')
    time.sleep(5) 