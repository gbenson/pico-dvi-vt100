import sys
from enum import Enum, auto

class Timing:
    CRT = auto()
    Reduced = auto()


C_PRIME = 30
M_PRIME = 300
CLOCK_STEP = 0.25
MIN_VSYNC_BP = 550
MIN_V_PORCH_RND = 3
V_SYNC_RND = 10 # = non-standard
MIN_V_BPORCH = 6

H_PIXELS, V_LINES_RND, IP_FREQ_RQD = map(int, sys.argv[1:])
print(f"# requested: {H_PIXELS}x{V_LINES_RND} @ {IP_FREQ_RQD} Hz")

INT_RQD = False  # interlace required?
TIMING_RQD = Timing.CRT

V_FIELD_RATE_RQD = IP_FREQ_RQD
if INT_RQD:
    V_FIELD_RATE_RQD *= 2

CELL_GRAN_RND = 8
H_PIXELS_RND = (H_PIXELS // CELL_GRAN_RND) * CELL_GRAN_RND

LEFT_MARGIN = RIGHT_MARGIN = 0
TOTAL_ACTIVE_PIXELS = H_PIXELS_RND + LEFT_MARGIN + RIGHT_MARGIN

TOP_MARGIN = BOTTOM_MARGIN = 0
INTERLACE = 0.5 if INT_RQD else 0

if TIMING_RQD is Timing.CRT:
    H_PERIOD_EST = ((1 / V_FIELD_RATE_RQD)
                    -MIN_VSYNC_BP / 1000000) / (V_LINES_RND + (
                        2 * TOP_MARGIN) + MIN_V_PORCH_RND + INTERLACE) * 1000000

    V_SYNC_BP = int(MIN_VSYNC_BP / H_PERIOD_EST) + 1
    V_SYNC_BP = max(V_SYNC_BP, V_SYNC_RND + MIN_V_BPORCH)

    V_BACK_PORCH = V_SYNC_BP - V_SYNC_RND

    TOTAL_V_LINES = (V_LINES_RND + TOP_MARGIN + BOTTOM_MARGIN
                     + V_SYNC_BP + INTERLACE + MIN_V_PORCH_RND)

    IDEAL_DUTY_CYCLE = C_PRIME - (M_PRIME * H_PERIOD_EST / 1000)

    if IDEAL_DUTY_CYCLE < 20:
        H_BLANK = (int(TOTAL_ACTIVE_PIXELS * 20 / (100 - 20)
                       / (2 * CELL_GRAN_RND))
                   * (2 * CELL_GRAN_RND))
    else:
        H_BLANK = (int(TOTAL_ACTIVE_PIXELS * IDEAL_DUTY_CYCLE
                       / (100 - IDEAL_DUTY_CYCLE) / (2 * CELL_GRAN_RND))
                   * (2 * CELL_GRAN_RND))

    TOTAL_PIXELS = TOTAL_ACTIVE_PIXELS + H_BLANK

    ACT_PIXEL_FREQ = CLOCK_STEP * int(TOTAL_PIXELS / H_PERIOD_EST / CLOCK_STEP)

    ACT_H_FREQ = 1000 * ACT_PIXEL_FREQ / TOTAL_PIXELS

    ACT_FIELD_RATE = 1000 * ACT_H_FREQ / TOTAL_V_LINES

    ACT_FRAME_RATE = ACT_FIELD_RATE
    if INT_RQD:
        ACT_FRAME_RATE /= 2


print("frame rate:", ACT_FRAME_RATE)
PCLK_HZ = TOTAL_PIXELS * TOTAL_V_LINES * ACT_FRAME_RATE
BCLK_KHZ = int(PCLK_HZ / 100)

print("pixel clock:", round(PCLK_HZ))
print("bit clock khz:", BCLK_KHZ)

# round it like cvt displays it
ACT_FRAME_RATE = round(ACT_FRAME_RATE * 100) / 100
print()

print("frame rate:", ACT_FRAME_RATE)
PCLK_HZ = TOTAL_PIXELS * TOTAL_V_LINES * ACT_FRAME_RATE
BCLK_KHZ = int(PCLK_HZ / 100)

print("pixel clock:", round(PCLK_HZ))
print("bit clock khz:", BCLK_KHZ)
