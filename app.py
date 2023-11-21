import os

from arguments import validate_arguments, get_arguments

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "true"

from flowjam.audio_manager import AudioManager
from flowjam.key_event_manager import KeyEventManager
from flowjam.thresholds import calculate_thresholds

from jams.library import select_jam

audio_manager = None
key_manager = None


def welcome():
    print("Welcome to Flow Jam!\n")
    print(
        "Flow Jam is a productivity tool that encourages flow by responding to your typing.\n"
    )
    print(
        "If this is your first time running, the app will try to set up a listener for key presses. You may need to update your security settings to allow this. If you don't trust it, check out the source!\n"
    )
    input("Press ENTER to get into the flow! ")


def start_menu(args):
    while True:
        print("Curent details:")
        print(f"  Jam: {audio_manager.get_jam().get_name()}")
        print(f"  Thresholds: {audio_manager.get_thresholds()}")
        print(f"  Falloff: {key_manager.get_falloff_minutes()} minutes")
        print()
        print("Flow Jam menu:")
        print("  [q] quit")
        print("  [f+] increase falloff by one minute")
        print("  [f-] decrease falloff by one minute")
        print("  [t+] increase threshold by 50 events")
        print("  [t-] decrease threshold by 50 events")
        print("  [j] select new jam")
        input_value = input("\nEnter a command: ")

        if input_value == "q":
            break
        elif input_value == "f+":
            print("Increasing falloff by one minute...")
            key_manager.set_falloff_minutes(key_manager.get_falloff_minutes() + 1)
        elif input_value == "f-":
            print("Decreasing falloff by one minute...")
            key_manager.set_falloff_minutes(key_manager.get_falloff_minutes() - 1)
        elif input_value == "t+":
            print("Increasing threshold by 50 events...")
            thresholds = audio_manager.get_thresholds()
            threshold = thresholds[-1] + 50
            audio_manager.set_thresholds(
                calculate_thresholds(
                    threshold, len(audio_manager.get_jam().get_files())
                )
            )
        elif input_value == "t-":
            print("Decreasing threshold by 50 events...")
            thresholds = audio_manager.get_thresholds()
            threshold = thresholds[-1] - 50
            audio_manager.set_thresholds(
                calculate_thresholds(
                    threshold, len(audio_manager.get_jam().get_files())
                )
            )
        elif input_value == "j":
            choose_and_start_jam(args)


def choose_and_start_jam(args):
    audio_manager.stop()
    jam = select_jam(args)

    if jam is None:
        shutdown_and_exit(0)

    if audio_manager.get_jam() is not None:
        audio_manager.get_jam().stop()

    audio_manager.set_jam(jam)

    if audio_manager.get_thresholds() is None:
        audio_manager.set_thresholds(
            calculate_thresholds(args.threshold, len(jam.get_files()))
        )

    audio_manager.start()

    print(
        f"\nStarting the '{jam.get_name()}' jam! Start typing to get into that flow state!\n"
    )
    jam.play()


def main():
    global audio_manager
    global key_manager

    args = get_arguments()

    if not validate_arguments(args):
        shutdown_and_exit(1)

    welcome()

    key_manager = KeyEventManager(falloff_minutes=args.falloff)
    audio_manager = AudioManager(key_event_manager=key_manager)

    key_manager.start()

    choose_and_start_jam(args)
    start_menu(args)

    print("Shutting down...")
    shutdown()


def shutdown():
    global audio_manager
    global key_manager

    if audio_manager is not None:
        jam = audio_manager.get_jam()
        if jam is not None:
            jam.stop()
        audio_manager.stop()

    if key_manager is not None:
        key_manager.stop()


def shutdown_and_exit(code=0):
    shutdown()
    exit(code)


if __name__ == "__main__":
    main()
