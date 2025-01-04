## Background   

This collection of scripts, the general structure of data implied by the programs, and the functional capabilities of the commands within, exist to expand the cognitive range of motion. They constitute a journal, a calendar, a mental sounding board, data to be mined, and a means of turning will into action. By projecting self into a medium capable of acting on goals and intentions.

For the longest time, my goal has simply been to have a low latency means of recording my thoughts, and organising effortlessly. Not the longest time, but ever since LLMs came on the scene I’ve been experimenting with various note taking approaches expecting that they’ll later be fed through summarisation and data extraction processes. Early on that was creating a graphical interface for recording log entries. Quickly realised that updating the GUI everytime I wanted to add basic functionality didn’t work, and more, that making interaction simple was key. I continued to focus on audio recording, making sure it was as simple as run script and save in the right place with the right name. In addition, I began to use daily notes and then zetellkasten notes. In using the latter, I recognised that this model was what I needed with audio, an almost frictionless way to capture moment to moment thoughts. Logs, musings, memos, schedules. Collection is key, all else comes after.

---

## Version history 
### V 0.01

- Initialized repository
- Added `record_audio.py` and `transcriber.py`, as well as requirements and readme. 

---

## Modules

### record_audio.py

- When run, checks for the existence of a state file which, if non-existent, creates, and then begins recording. If state indicates recording, then recording is stopped and the state file changed. Saves recording as date-time (`recording_%Y-%m-%d_%H-%M-%S.wav`)


### transcriber.py

- Checks an index file `transcription_index.txt` against available files. Transcribes using whisper, saves as txt file in the same folder and adds names to the index. Whisper model size can be changed with speed/ quality tradeoffs. Currently specified as latest and largest - intended function is a scheduled overnight job so not worried about how long it will take. May take a while if a batch have been added in bulk. 

### summariser.py (in progress)

- summarise each entry
- saves the summaries
- create a daily summary from the collected summaries

