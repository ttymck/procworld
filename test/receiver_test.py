import queue
from engine.main import Receiver

def test_enqueue():
  q = queue.Queue()
  rec = Receiver(q)
  