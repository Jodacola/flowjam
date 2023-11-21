import time
import Quartz
from AppKit import NSEvent
import threading


class KeyEventManager:
    def __init__(self, falloff_minutes=2):
        self.event_times = []
        self.running = False
        self.threads = []
        self.falloff_minutes = falloff_minutes
        self.event_count = 0

    def __clear_events_after_falloff(self):
        while self.running:
            cutoff = time.time() - (60 * self.falloff_minutes)
            if len(self.event_times) > 0:
                self.event_times = [
                    event_time for event_time in self.event_times if event_time > cutoff
                ]
            self.event_count = len(self.event_times)
            time.sleep(0.2)

    def __keypress_callback(self, proxy, type_, event, refcon):
        if type_ < 0 or type_ > Quartz.kCGAnyInputEventType:
            return event

        key_event = NSEvent.eventWithCGEvent_(event)
        if key_event is None:
            return event

        if key_event.type() == Quartz.kCGEventKeyDown:
            self.event_times.append(time.time())

        return event

    def __init_tap_and_listen(self):
        print(
            "Setting up key event listener... \n\n⚠️⚠️⚠️\nNOTE: System-wide keyboard input may be unavailable for several seconds."
        )

        event_mask = 1 << Quartz.kCGEventKeyDown
        event_tap = Quartz.CGEventTapCreate(
            Quartz.kCGSessionEventTap,
            Quartz.kCGHeadInsertEventTap,
            0,
            event_mask,
            self.__keypress_callback,
            None,
        )

        if not event_tap:
            print("\nFailed to create event tap; check your security settings.\n")
            return

        run_loop_source = Quartz.CFMachPortCreateRunLoopSource(None, event_tap, 0)
        Quartz.CFRunLoopAddSource(
            Quartz.CFRunLoopGetCurrent(), run_loop_source, Quartz.kCFRunLoopDefaultMode
        )

        Quartz.CGEventTapEnable(event_tap, True)

        try:
            while self.running:
                Quartz.CFRunLoopRunInMode(Quartz.kCFRunLoopDefaultMode, 5, False)
        except KeyboardInterrupt:
            pass

    def get_event_count(self):
        return self.event_count

    def get_falloff_minutes(self):
        return self.falloff_minutes

    def set_falloff_minutes(self, falloff_minutes):
        self.falloff_minutes = falloff_minutes

    def start(self):
        self.running = True
        self.threads.append(threading.Thread(target=self.__init_tap_and_listen))
        self.threads.append(threading.Thread(target=self.__clear_events_after_falloff))
        for thread in self.threads:
            thread.start()

    def stop(self):
        print("Ending key event capture...")
        self.running = False
        for thread in self.threads:
            thread.join()
