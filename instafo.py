import numpy as np
from adbkit import ADBTools
from time import sleep
import random


def get_uiautomator_frame(screenshotfolder="c:\\ttscreenshots"):
    adb.aa_update_screenshot()
    return adb.aa_get_all_displayed_items_from_uiautomator(
        screenshotfolder=screenshotfolder,  # screenshots will be saved here
        max_variation_percent_x=10,
        # used for one of the click functions, to not click exactly in the center - more information below
        max_variation_percent_y=10,  # used for one of the click functions, to not click exactly in the center
        loung_touch_delay=(
            1000,
            1500,
        ),  # with this settings longtouch will take somewhere between 1 and 1,5 seconds
        swipe_variation_startx=10,  # swipe coordinate variations in percent
        swipe_variation_endx=10,
        swipe_variation_starty=10,
        swipe_variation_endy=10,
        sdcard="/storage/emulated/0/",
        # sdcard will be used if you use the sendevent methods, don't pass a symlink - more information below
        tmp_folder_on_sd_card="AUTOMAT",  # this folder will be created in the sdcard folder for using sendevent actions
        bluestacks_divider=32767,
        # coordinates must be recalculated for BlueStacks https://stackoverflow.com/a/73733261/15096247 when using sendevent
    )


def downswipe():
    adb.aa_swipe(random.randint(400, 600),
                 random.randint(1000, 1800),
                 random.randint(400, 600),
                 random.randint(400, 800),
                 random.uniform(0.4, 1.5))


def upswipe():
    adb.aa_swipe(random.randint(400, 600),
                 random.randint(400, 800),

                 random.randint(400, 600),
                 random.randint(1000, 1800),

                 random.uniform(0.4, 1.5))


ADBTools.aa_kill_all_running_adb_instances()
adb_path = r"C:\ProgramData\chocolatey\bin\adb.exe"
deviceserial = 'localhost:5555'
adb = ADBTools(adb_path=adb_path,
               deviceserial=deviceserial)

adb.aa_start_server()
sleep(3)
adb.aa_connect_to_device()
swipe = ([True] * 9) + [False]
like = ([False] * 3) + [True]
while True:
    downswipe() if random.choice(swipe) else upswipe()
    sleep(random.uniform(0.5, 4))
    if random.choice(like):
        while True:
            df = get_uiautomator_frame()
            if df.empty:
                continue
            dfm = df.loc[(df.bb_area > 1630) & (df.bb_area < 1690)]
            print(dfm)
            if not dfm.empty:
                dfm = dfm.drop_duplicates(subset='bb_bounds')
                dfm = dfm.loc[~dfm.bb_screenshot.apply(
                    lambda x: np.any(np.where((x[..., 2] == 255)
                                              & (x[..., 1] == 48) & (x[..., 0] == 64))))]
                if not dfm.empty:
                    dfm.ff_bb_tap_exact_center.iloc[0]()

            break
