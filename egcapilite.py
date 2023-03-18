import dataclasses
import json
import os
import pathlib


@dataclasses.dataclass()
class Capabilities:
    stream_command: bool = False
    record: bool = False
    screenshot: bool = False
    flashback_record: bool = False
    stream: bool = False
    live_commentary: bool = False


JSON_PATH = pathlib.Path(os.getenv("APPDATA")) / "Elgato/GameCapture/EGCAPILite/EGCAPILite.json"

if not JSON_PATH.is_file():
    raise FileNotFoundError(f"Couldn't find {JSON_PATH}.")


def _read_json():
    """
    Reads EGCAPILite.json and returns its JSON data
    :return: Parsed JSON data read from file
    """
    with open(JSON_PATH) as file:
        return json.load(file)


def _write_json(json_data):
    """
    Writes JSON data to EGCAPILite.json
    :param json_data: JSON data to write
    """
    with open(JSON_PATH, "w") as file:
        json.dump(json_data, file)


def capabilities() -> Capabilities:
    """
    Returns the capabilities that Game Capture is able to use right now
    :rtype: Capabilities
    :return: Parsed capability flags
    """
    json_data = _read_json()
    flags = json_data["server"]["capabilityFlags"]
    parsed_capabilities = Capabilities()
    parsed_capabilities.stream_command = flags & 1 != 0
    parsed_capabilities.record = flags & 2 != 0
    parsed_capabilities.screenshot = flags & 4 != 0
    parsed_capabilities.flashback_record = flags & 8 != 0
    parsed_capabilities.stream = flags & 16 != 0
    parsed_capabilities.live_commentary = flags & 32 != 0
    return parsed_capabilities


def features() -> Capabilities:
    """
    Returns the features that Game Capture supports
    Game Capture sets all of these to 1/True when it starts, so there's not much point in reading these flags
    :rtype: Capabilities
    :return: Parsed feature flags
    """
    json_data = _read_json()
    flags = json_data["server"]["featureFlags"]
    parsed_features = Capabilities()
    parsed_features.stream_command = flags & 1 != 0
    parsed_features.record = flags & 2 != 0
    parsed_features.screenshot = flags & 4 != 0
    parsed_features.flashback_record = flags & 8 != 0
    parsed_features.stream = flags & 16 != 0
    parsed_features.live_commentary = flags & 32 != 0
    return parsed_features


def is_commentary_active() -> bool:
    """
    Returns whether Live Commentary is currently enabled
    :rtype: bool
    :return: State of Live Commentary
    """
    json_data = _read_json()
    return json_data["server"]["isCommentaryActive"]


def is_recording() -> bool:
    """
    Returns whether Game Capture is currently recording
    :rtype: bool
    :return: State of recording
    """
    json_data = _read_json()
    return json_data["server"]["isRecording"]


def is_running() -> bool:
    """
    Returns whether Game Capture is currently running
    :rtype: bool
    :return: State of running
    """
    json_data = _read_json()
    return json_data["server"]["isRunning"]


def is_streaming() -> bool:
    """
    Returns whether Game Capture is currently streaming
    :rtype: bool
    :return: State of streaming
    """
    json_data = _read_json()
    return json_data["server"]["isStreaming"]


def num_scenes() -> int:
    """
    Returns the number of Stream Command scenes
    Game Capture is hardcoded to have 10 scenes, so this will always be 10
    :rtype: int
    :return: Number of scenes
    """
    json_data = _read_json()
    return json_data["server"]["numScenes"]


def selected_scene_index() -> int:
    """
    Returns the index of the currently selected Stream Command scene
    :rtype: int
    :return: Current scene index
    """
    json_data = _read_json()
    return json_data["server"]["selectedSceneIndex"]


def select_scene(scene_index: int):
    """
    Switches to a different Stream Command scene
    :param scene_index: Index of the scene to select
    """
    json_data = _read_json()
    json_data["client"]["selectScene"] = True
    json_data["client"]["selectSceneIndex"] = scene_index
    _write_json(json_data)


def start_recording():
    """
    Starts recording
    """
    json_data = _read_json()
    json_data["client"]["startRecording"] = True
    _write_json(json_data)


def stop_recording():
    """
    Stops recording
    """
    json_data = _read_json()
    json_data["client"]["stopRecording"] = True
    _write_json(json_data)


def toggle_recording():
    """
    Toggles recording
    """
    if is_recording():
        stop_recording()
    else:
        start_recording()


def save_screenshot():
    """
    Saves a screenshot
    """
    json_data = _read_json()
    json_data["client"]["saveScreenshot"] = True
    _write_json(json_data)


def save_flashback_buffer(length_seconds: int):
    """
    Saves a Flashback Recording of the given length in seconds
    :param length_seconds: Length of recording
    """
    json_data = _read_json()
    json_data["client"]["saveFlashbackBuffer"] = True
    json_data["client"]["saveFlashbackBufferSeconds"] = length_seconds
    _write_json(json_data)


def start_streaming():
    """
    Starts streaming
    """
    json_data = _read_json()
    json_data["client"]["startStreaming"] = True
    _write_json(json_data)


def stop_streaming():
    """
    Stops streaming
    """
    json_data = _read_json()
    json_data["client"]["stopStreaming"] = True
    _write_json(json_data)


def toggle_streaming():
    """
    Toggles streaming
    """
    if is_streaming():
        stop_streaming()
    else:
        start_streaming()


def activate_live_commentary():
    """
    Activates Live Commentary
    """
    json_data = _read_json()
    json_data["client"]["activateCommentary"] = True
    _write_json(json_data)


def deactivate_live_commentary():
    """
    Deactivates Live Commentary
    """
    json_data = _read_json()
    json_data["client"]["deactivateCommentary"] = True
    _write_json(json_data)


def toggle_live_commentary():
    """
    Toggles Live Commentary
    """
    if is_commentary_active():
        deactivate_live_commentary()
    else:
        activate_live_commentary()
