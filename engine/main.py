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


class Actor:
  def __init__(self, id, name, appearance):
    self.id = id
    self.name = name
    self.appearance = appearance

  def __repr__(self):
    return f"{self.id}: {self.name} - {self.appearance}"


class ActorRepo:
  def __init__(self, existing_actors=None):
    self._actors = existing_actors or []

  def of_id(self, actor_id):
    return Actor(actor_id, "John Smith", "blue")


class Scene:
  def __init__(self, background: str, actors: List[int]):
    self.background = background
    self.actors = actors

  def render(self, actor_repo):
    actors = list(map(actor_repo.of_id, self.actors))
    print("Background:", self.background, "\nActors:", actors)


class Renderer(threading.Thread):
  def __init__(self, intake=queue.Queue(), actor_repo=ActorRepo()):
    super(Renderer, self).__init__()
    self.intake = intake
    self.actor_repo = actor_repo

  def run(self):
    while True:
      nextline = self.intake.get(block = True)
      sc = Scene(nextline, [1])
      sc.render(self.actor_repo)


class Engine():
  def __init__(self):
    self._renderer = Renderer(queue.Queue())
    sinks = [self._renderer.intake,]
    self._receiver = Receiver(sinks)
  
  def run(self):
    self._receiver.start()
    self._renderer.start()


if __name__ == "__main__":
  e = Engine()
  e.run()
