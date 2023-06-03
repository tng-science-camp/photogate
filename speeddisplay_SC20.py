#!/usr/bin/env python3
import urwid
import photogate_SC20

class SpeedDisplay:
    def __init__(self):
        self.photogate1 = photogate_SC20.Photogate_SC20(gate_0_pin=17, gate_1_pin=18, gate_distance=0.02)
        self.photogate2 = photogate_SC20.Photogate_SC20(gate_0_pin=22, gate_1_pin=23, gate_distance=0.02)

        self.palette = [
            ('highest speed', 'dark red', 'black'),
            ('current speed', 'white', 'black'),
            ('key', 'light cyan', 'dark blue', 'underline'),
            ('foot', 'dark cyan', 'dark blue', 'bold')]

        screen = urwid.raw_display.Screen()
        screen_cols, screen_rows = screen.get_cols_rows()

        w_divider = urwid.Divider()
        w_track_rows = int((screen_rows - 4)/2)
        #w_track_rows = int((screen_rows - 4 - 1)/2)

        self.speed_track1 = 0.0
        self.highest_speed_track1 = 0.0
        self.speed_track2 = 0.0
        self.highest_speed_track2 = 0.0

        self.w_speed_track1 = urwid.BigText('{:01.2f}'.format(self.speed_track1), urwid.Thin6x6Font())
        urwid.AttrMap(self.w_speed_track1, 'current speed')
        self.w_speed_track2 = urwid.BigText('{:01.2f}'.format(self.speed_track2), urwid.Thin6x6Font())
        urwid.AttrMap(self.w_speed_track2, 'current speed')

        #self.w_edit = urwid.Edit('', '0.0000')

        w_box1_body = urwid.Padding(self.w_speed_track1, 'center', None)
        w_box1_body = urwid.Filler(w_box1_body, 'middle')
        self.w_highest_speed_track1 = urwid.Text('Highest Speed: {:01.2f} m/s '.format(self.highest_speed_track1), align='right') 
        urwid.AttrMap(self.w_highest_speed_track1, 'highest speed')
        w_box1 = urwid.Frame(w_box1_body, header=self.w_highest_speed_track1)
        w_box1 = urwid.LineBox(w_box1)
        w_box1 = urwid.AttrMap(w_box1, 'line')
        w_box1 = urwid.BoxAdapter(w_box1, w_track_rows)

        w_box2_body = urwid.Padding(self.w_speed_track2, 'center', None)
        w_box2_body = urwid.Filler(w_box2_body, 'middle')
        self.w_highest_speed_track2 = urwid.Text('Highest Speed: {:01.2f} m/s '.format(self.highest_speed_track2), align='right') 
        urwid.AttrMap(self.w_highest_speed_track2, 'highest speed')
        w_box2 = urwid.Frame(w_box2_body, header=self.w_highest_speed_track2)
        w_box2 = urwid.LineBox(w_box2)
        w_box2 = urwid.AttrMap(w_box2, 'line')
        w_box2 = urwid.BoxAdapter(w_box2, w_track_rows)
        
        #urwid.connect_signal(self.w_edit, 'change', self.set_track_speeds)

        self.w_speed_display = urwid.Pile([urwid.Text('Track 1 (m/s)'), w_box1, w_divider, urwid.Text('Track 2 (m/s)'), w_box2])
        #self.w_speed_display = urwid.Pile([self.w_edit, urwid.Text('Track 1 (m/s)'), w_box1, w_divider, urwid.Text('Track 2 (m/s)'), w_box2])
        self.w_speed_display = urwid.Filler(self.w_speed_display, 'middle')

        w_footer = urwid.Text(('foot', [('key', "N"), " New Run    ", ('key', "R"), " Reset Highest Speed    ", ('key', "esc"), " quit"]))
        w_footer = urwid.AttrMap(w_footer, "foot")
        self.w_speed_display = urwid.Frame(self.w_speed_display, footer=w_footer)
        self.loop = urwid.MainLoop(self.w_speed_display, self.palette, input_filter=self.input_filter, unhandled_input=self.unhandled_input)

    def unhandled_input(self, key):
        if key in ('n', 'N'):
            self.set_speed_track1(0.0)
            self.set_speed_track2(0.0)
        if key in ('r', 'R'):
            pass
        if key in ('esc'):
            raise urwid.ExitMainLoop()

    def input_filter(self, keys, raw):
        if 'q' in keys or 'Q' in keys:
            raise urwid.ExitMainLoop()
        elif 'n' in keys or 'N' in keys:
            self.set_speed_track1(0.0)
            self.photogate1.reset()
            self.photogate2.reset()
            self.set_speed_track1(self.photogate1.measure_speed())
            self.set_speed_track2(self.photogate2.measure_speed())
        elif 'r' in keys or 'R' in keys:
            self.set_highest_speed_track1(0.0)
            self.set_highest_speed_track2(0.0)
        else:
            return keys

    def set_highest_speed_track1(self, speed):
        self.highest_speed_track1 = speed
        self.w_highest_speed_track1.set_text('Highest Speed: {:01.2f} m/s '.format(speed))

    def set_highest_speed_track2(self, speed):
        self.highest_speed_track2 = speed
        self.w_highest_speed_track2.set_text('Highest Speed: {:01.2f} m/s '.format(speed))

    def set_speed_track1(self, speed):
        self.w_speed_track1.set_text('{:01.2f}'.format(speed))
        if speed > self.highest_speed_track1:
            self.set_highest_speed_track1(speed)

    def set_speed_track2(self, speed):
        self.w_speed_track2.set_text('{:01.2f}'.format(speed))
        if speed > self.highest_speed_track2:
            self.set_highest_speed_track2(speed)

    def set_track_speeds(self, widget, text):
        try:
            speed = float(text)
            self.set_speed_track1(speed)
            self.set_speed_track2(speed)
        except ValueError:
            pass

    def get_loop(self):
        return this.loop

    def run(self):
        self.loop.run()
            

if __name__ == "__main__":
    speed_display = SpeedDisplay()
    speed_display.run()
