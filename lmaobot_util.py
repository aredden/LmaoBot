from __future__ import absolute_import, print_function, unicode_literals, division
import os
os.environ['SC2READER_CACHE_DIR'] = "./cache"
import sc2reader
import time
from sc2reader import factories, engine
from sc2reader.events import ChatEvent
from sc2reader.objects import Participant
import json
from datetime import datetime, timedelta

def GetTime(sec):
    sec = int(sec*0.71428571428)
    d = datetime(1,1,1,hour=int(sec/3600),minute=int(sec/60),second=sec%60)
    if d.second < 10:
        secs = "0"+str(d.second)
    else:
        secs = str(d.second)

    if d.minute < 10:
        mins = "0"+str(d.minute)
    else:
        mins = str(d.minute)
    return ("%s:%s" % (mins, secs))


races = dict([["Zerg","<:zerg:748309706178822206>"],["Protoss","<:protoss:748309678710325398>"],["Terran","<:terran:748309692660318240>"]])

def parse_replay(filename):
    
    # dir = os.getenv('SC2READER_CACHE_DIR')
    # max_size = os.getenv('SC2READER_CACHE_MAX_SIZE')
    reader = sc2reader.SC2Reader()
    starttime = time.time_ns()
    replay = reader.load_replay(source=filename)

    event_names = set([event.name for event in replay.events])

    events_of_type = {name: [] for name in event_names}
    for event in replay.events:
        events_of_type[event.name].append(event)


    chat_events = events_of_type['ChatEvent']
    chat_event_str = ''
    for event in chat_events:
        if event.name == 'ChatEvent':
            human: Participant = replay.humans[event.pid]
            event: ChatEvent = event
            chat_event_str += "`{1}`({3}) *T{4}* | **{0}**: {2}\n".format(human.name, GetTime(event.second), event.text, races[human.play_race], human.team_id)
            # print( "`{1}|{0}|T{4}` ({3}):  {2}\n".format(human.name, GetTime(event.second), event.text, races[human.play_race], human.team_id))

            print()
    endtime = time.time_ns()
    print("Parse time in nanoseconds: {0}".format(endtime-starttime))

    return chat_event_str


def chunk_string(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))


def fancy_chunk_string(input_str: str):
    chunks = []
    LIMIT = 2000
    not_chunked_text = input_str
    while not_chunked_text:
        if len(not_chunked_text) <= LIMIT:
            chunks.append(not_chunked_text)
            break
        split_index = not_chunked_text.rfind("\n", 0, LIMIT)
        if split_index == -1:
            # The chunk is too big, so everything until the next newline is deleted
            try:
                not_chunked_text = not_chunked_text.split("\n", 1)[1]
            except IndexError:
                # No "\n" in not_chunked_text, i.e. the end of the input text was reached
                break
        else:
            chunks.append(not_chunked_text[:split_index+1])
            not_chunked_text = not_chunked_text[split_index+1:]
    return chunks