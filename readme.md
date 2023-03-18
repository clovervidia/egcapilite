# egcapilite

I wanted a way to control Elgato Game Capture from Python, so I looked into how Stream Decks are able to control it. As it turns out, the method of communication is rather simple. The two programs just take turns reading from and writing to a text file with JSON data in it. This file allows the Stream Deck to tell Game Capture to do things, like start or stop recording, and Game Capture to tell the Stream Deck about its current status, like if it's streaming or live commentary is enabled.

Here are the things Game Capture can tell the Stream Deck about its current state:

* Live Commentary is enabled
* Currently recording
* Currently running
* Currently streaming
* Total number of Stream Command scenes
* Current Stream Command scene

There's also a bitfield to share which capabilities of Game Capture are currently able to be used, like if an account has been set up for streaming, or if Flashback Recording is enabled.

Here are the commands the Stream Deck can send to Game Capture:

* Activate Live Commentary
* Deactivate Live Commentary
* Save a Flashback Recording of a given length
* Save a screenshot
* Select a given Stream Command scene
* Start recording
* Stop recording
* Start streaming
* Stop streaming

## Usage

This is a simple module that can also read from and write to this JSON file to control Game Capture. You can read Game Capture's state and send any of the commands that the Stream Deck can. I've also added some toggles for convenience if you don't want to use the start/stop pairs.

All you have to do is `import egcapilite`. All the functions will be imported and ready to use.

For example, to check if Game Capture is running:

```python
egcapilite.is_running()
```

To check if Game Capture is able to stream:

```python
egcapilite.capabilities().stream
```

To start recording:

```python
egcapilite.start_recording()
```

To save a Flashback Recording of the past 20 seconds:

```python
egcapilite.save_flashback_buffer(20)
```

## How It Works

On Windows, if you go to the following path, you should find a file named `EGCAPILite.json`:

```text
C:\Users\YOUR_USERNAME\AppData\Roaming\Elgato\GameCapture\EGCAPILite
```

That's the file in question. Game Capture sets values in the `server` section to broadcast its state, and the Stream Deck sets values in the `client` section to send commands to Game Capture.
