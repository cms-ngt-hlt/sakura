# NGT Calibration Loop

(Still a pre-Alpha version, nothing actually works)

## Instructions

Run the loop with
```
python3 NGTLoopStep2.py
```

It expects a file "running.txt" to appear in the working directory to signal the fact that we are running, and "lumisections" to appear in that same directory with name "ls*.txt". You can simulate that with:
```
sleep 5; touch running.txt; for i in `seq 1 20`; do touch ls"$i".txt; sleep 1; done; rm running.txt
```
(you have to clean up the lumisections yourself afterwards).

## TODO

- Fix the end of run logic (right now the last few lumisections are dropped)
- Actually implement methods instead of just mockups
