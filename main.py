from datetime import datetime
from typing import NamedTuple

import keyboard
import pyautogui

pyautogui.PAUSE = 0

class Event(NamedTuple):
    id: int
    point: pyautogui.Point
    delay: float
    type: str


evt_count = 0

initial_timestamp = last_timestamp = datetime.now().timestamp()
actual_event = Event(id = evt_count, point = pyautogui.position(), delay = 0, type = 'move')

event_queue = [actual_event]

print("Recording...")

while(True):
    if keyboard.is_pressed('space'):
        break

    current_position = pyautogui.position()
    event_type = None

    if(actual_event.point != current_position):
        event_type = 'move'

    # mouse moved
    if event_type != None:
        evt_count += 1
        
        event_id = evt_count + 1
        event_point = pyautogui.Point(current_position.x, current_position.y)
        event_timestamp = datetime.now().timestamp()
        event_delay = event_timestamp - last_timestamp

        event = Event(id = event_id, point = event_point, delay = event_delay, type = event_type)
        last_timestamp = event_timestamp
        actual_event = event

        event_queue.append(event)



print('Registered {evt_count} events in {duration} seconds.'.format(evt_count = len(event_queue), duration = last_timestamp - initial_timestamp))
print('Replaying...')

initial_ts_replay = datetime.now().timestamp()

for event in event_queue:
    pyautogui.sleep(event.delay)
    
    if event.type == 'move':
        pyautogui.moveTo(event.point.x, event.point.y)

end_ts_replay = datetime.now().timestamp()
print('Replayed in {duration} seconds.'.format(duration = end_ts_replay - initial_ts_replay))

print('Finished!')