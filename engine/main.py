import os, sys, json
import threading, queue
from typing import List


class Receiver(threading.Thread):
  def __init__(self, sinks: List[queue.Queue], stream=sys.stdin):
    super(Receiver, self).__init__()
    self.__stream = stream
    self.sinks = sinks

  def run(self):
    for line in self.__stream:
      if line.strip() != "":
        for sink in self.sinks:
          sink.put(line.strip())


class Scene(threading.Thread):
  def __init__(self, intake=queue.Queue()):
    super(Scene, self).__init__()
    self.intake = intake

  def run(self):
    while True:
      nextline = self.intake.get(block = True)
      print(nextline)


class Engine():
  def __init__(self):
    self._scene = Scene(queue.Queue())
    sinks = [self._scene.intake,]
    self._receiver = Receiver(sinks)
  
  def run(self):
    self._receiver.start()
    self._scene.start()


if __name__ == "__main__":
  e = Engine()
  e.run()
