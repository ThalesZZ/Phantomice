from datetime import datetime
from typing import NamedTuple

import keyboard
import pyautogui as pygui

pygui.PAUSE = 0

class Event(NamedTuple):
    id: int
    point: pygui.Point
    delay: float


evt_count = 0

initial_timestamp = last_timestamp = datetime.now().timestamp()
actual_event = Event(id = evt_count, point = pygui.position(), delay = 0)

event_queue = [actual_event]

print("Recording...")

while(True):
    current_position = pygui.position()

    # mouse moved
    if actual_event.point != current_position:
        evt_count += 1
        
        event_id = evt_count + 1
        event_point = pygui.Point(current_position.x, current_position.y)
        event_timestamp = datetime.now().timestamp()
        event_delay =  event_timestamp - last_timestamp

        event = Event(id = event_id, point = event_point, delay = event_delay)
        last_timestamp = event_timestamp
        actual_event = event

        event_queue.append(event)

    if keyboard.is_pressed('space'):
        break



print('Registered {evt_count} events in {duration} seconds.'.format(evt_count = len(event_queue), duration = last_timestamp - initial_timestamp))
print('Replaying...')

initial_ts_replay = datetime.now().timestamp()
for event in event_queue:
    pygui.sleep(event.delay)
    pygui.moveTo(event.point.x, event.point.y)
end_ts_replay = datetime.now().timestamp()
print('Replayed {evt_count} events in {duration} seconds.'.format(evt_count = len(event_queue), duration = end_ts_replay - initial_ts_replay))

print('Finished!')