# bash$ cvt 800 480 60
# # 800x480 59.48 Hz (CVT) hsync: 29.74 kHz; pclk: 29.50 MHz
# Modeline "800x480_60.00"   29.50  800 824 896 992  480 483 493 500 -hsync +vsync
refresh, modeline = (
    59.48,
    "800 824 896 992  480 483 493 500 -hsync +vsync",
)

# bash$ cvt 1024 600 60
# # 1024x600 59.85 Hz (CVT) hsync: 37.35 kHz; pclk: 49.00 MHz
# Modeline "1024x600_60.00"   49.00  1024 1072 1168 1312  600 603 613 624 -hsync +vsync
refresh, modeline = (
    59.85,
    "1024 1072 1168 1312  600 603 613 624 -hsync +vsync",
)

# $ cvt --reduced 1024 600 60
# # 1024x600 59.69 Hz (CVT) hsync: 36.95 kHz; pclk: 43.75 MHz
# Modeline "1024x600R"   43.75  1024 1072 1104 1184  600 603 613 619 +hsync -vsync
refresh, modeline = (
    59.69,
    "1024 1072 1104 1184  600 603 613 619 +hsync -vsync",
)

# $ cvt 1024 600 30
# # 1024x600 29.80 Hz (CVT) hsync: 18.36 kHz; pclk: 23.50 MHz
# Modeline "1024x600_30.00"   23.50  1024 1056 1152 1280  600 603 613 616 -hsync +vsync
refresh, modeline = (
    29.80,
    "1024 1056 1152 1280  600 603 613 616 -hsync +vsync",
)

modeline = modeline.split()
hsync = {"-hsync": False, "+hsync": True}[modeline[-2]]
vsync = {"-vsync": False, "+vsync": True}[modeline[-1]]
(hdisplay, hsyncstart, hsyncend, htotal,
 vdisplay, vsyncstart, vsyncend, vtotal) = map(int, modeline[:-2])

print(f"\t.h_sync_polarity = {str(hsync).lower()}")
print(f"\t.h_front_porch   = {hsyncstart - hdisplay}")
print(f"\t.h_sync_width    = {hsyncend - hsyncstart}")
print(f"\t.h_back_porch    = {htotal - hsyncend}")
print(f"\t.h_active_pixels = {hdisplay}")
print()
print(f"\t.v_sync_polarity = {str(vsync).lower()}")
print(f"\t.v_front_porch   = {vsyncstart - vdisplay}")
print(f"\t.v_sync_width    = {vsyncend - vsyncstart}")
print(f"\t.v_back_porch    = {vtotal - vsyncend}")
print(f"\t.v_active_lines  = {vdisplay}")
print()
print(f"\t.bit_clk_khz     = {int(htotal * vtotal * refresh * 10 / 1000)}")
print(f"\t.bit_clk_khz     = {int(23.50 * 10 * 1000)}")
