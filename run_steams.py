import pyautogui as pag
import random
import cv2
from matplotlib import pyplot as plt
import time
import numpy as np


# global counter for number of runs to be used in determining when to pull stam pots, glory rings, and binding necklaces
# from bank and when to hit NPC contact
run_count = 0

def main():
    global run_count
    runs = {}
    while True:
        st = time.monotonic()
        base_run()
        et = time.monotonic()
        runs[run_count] = int(et - st)

        print("RUN[{}]: {}".format(run_count, runs[run_count]))
        run_count += 1


def screengrab():
    bank_grab = pag.screenshot().convert('LA')
    bank_grab.save('C:\\Users\\jsp4k\\Desktop\\smdev\\grab.PNG', 0)
    bank_grab = cv2.imread('C:\\Users\\jsp4k\\Desktop\\smdev\\grab.PNG', 1)
    # os.remove('C:\\Users\\jsp4k\\Desktop\\smdev\\bank_grab.PNG')

    return bank_grab

# in: path for template image
# out: bounding box in form of (x1, y1), (x2, y2)
# this method takes in a template subimage and matches it to the current OSRS client graphic, returning the location
# of the subimage within the window
def locate_temp(path):
    template = cv2.imread(path, 1)

    window = screengrab()

    meth = 'cv2.TM_SQDIFF_NORMED'
    method = eval('cv2.TM_CCOEFF')

    # Apply template Matching
    res = cv2.matchTemplate(window, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    w, h, _ = template.shape
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    # debug UI showing template match bounding box overlayed with screengrab of OSRS client
    cv2.rectangle(window, (top_left[0] + w, top_left[1] + h), (bottom_right[0] - w, bottom_right[1] - h), (255, 100, 100), 20)
    plt.subplot(121),plt.imshow(res,cmap = 'gray')
    plt.title('Matching Rresult'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(window,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)
    plt.show()

    return top_left, bottom_right


# a single run of a steam rune route
def base_run():
    delay(500)

    # open inventory
    pag.press('f1')


    # locate where the bank is in the minimap and click in the top half of the bank
    start, stop, step = (.9, 1.0, .05)
    off = random.choice(list(np.arange(start, stop, step)))

    top_left, bottom_right = locate_temp('C:\\Users\\jsp4k\\Desktop\\smdev\\chest_temp.PNG')
    xoff = int((bottom_right[0] - top_left[0]) * .45 * off)
    yoff = int((bottom_right[1] - top_left[1]) / 2)
    top_left = top_left[0] + xoff, top_left[1]
    bottom_right = bottom_right[0] - xoff, bottom_right[1] - yoff

    target_box(top_left, bottom_right)
    delay(700)
    target_box((1000, 1000), (1200, 1300), clicktype='', intensity=5)
    pag.scroll(1400)
    delay()

    # locate where the chest is and right click on it
    top_left, bottom_right = locate_temp('C:\\Users\\jsp4k\\Desktop\\smdev\\bank_temp.PNG')

    start, stop, step = (.9, 1.2, .05)
    off = random.choice(list(np.arange(start, stop, step)))

    xoff = int((bottom_right[0] - top_left[0]) / 3 * off)
    yoff = int((bottom_right[1] - top_left[1]) / 3 * off)
    top_left = top_left[0] + xoff, top_left[1] + yoff
    bottom_right = bottom_right[0] - xoff, bottom_right[1] - yoff

    # rc on bank
    target_box(top_left, bottom_right, clicktype="right", )
    delay()
    pag.moveRel(yOffset=80 + random.random() * 10)
    delay(int(random.random() * 140))
    pag.click()
    delay(int(random.random() * 240))

    delay(270)

    #empty inv
    target_box((1384,1280),(1400, 1345), intensity=100)

    # withdraw stamina pot
    if run_count % 2 == 0:
        target_box((1185, 1108), (1235, 1164), clicktype='right', intensity=210)
        delay(int(11 * random.random()))
        pag.moveRel(yOffset=110 + random.random() * 10)
        delay(int(14 * random.random()))
        pag.click()
        delay(int(10 * random.random()))

    # withdraw dueling ring
    if run_count % 4 == 0:
        target_box((1045, 1110), (1100, 1150), clicktype='right', intensity=210)
        delay(int(25 * random.random()))
        pag.moveRel(yOffset=110 + random.random() * 10)
        delay(int(10 * random.random()))
        pag.click()
        delay(int(5 * random.random()))

    # withdraw binding necklace
    if run_count % 8 == 0:
        target_box((890, 1080), (930, 1155), clicktype='right', intensity=210)
        delay(int(14 * random.random()))
        pag.moveRel(yOffset=110 + random.random() * 10)
        delay(int(8 * random.random()))
        pag.click()
        delay(int(25 * random.random()))


    #grab ess
    target_box((1330,1104),(1390, 1165), intensity=210)

    # x bank4
    target_box((1525, 85),(1580, 140), intensity=100)

    # cast NPC contact
    if run_count % 10 == 0:
        pag.press('f5')
        delay(16)
        target_box((1960, 920), (2000, 960), clicktype='right', intensity=210)
        delay(int(14 * random.random()))
        pag.moveRel(yOffset=110 + random.random() * 10)
        delay(int(8 * random.random()))
        pag.click()
        delay(16, deterministic=True)
        pag.press('f1')
        delay(int(500 * random.random()))
        delay(int(500 * random.random()))
        pag.press('space')
        delay(23)
        pag.press('space')
        delay(23)
        pag.press('space')

    # consume stamina pot
    if run_count % 2 == 0:
        target_box((2080, 900), (2140, 970), intensity=15)

    # equip dueling ring
    if run_count % 4 == 0:
        target_box((2220, 900), (2270, 960), intensity=12)

    # equip binding necklace
    if run_count % 8 == 0:
        target_box((2100, 1000), (2140, 1080), intensity=5)

    # fill pouches
    target_box((1960,900),(2020, 970), intensity=15)
    target_box((1820,1010),(1900, 1080), intensity=30)
    target_box((1960,1025),(2020, 1075), intensity=27)

    # reopen bank
    target_box((1000, 960), (1100, 1030), intensity=27)
    #target_box((1320, 1280), (1400, 1345), intensity=210)

    #grab ess
    target_box((1330,1104),(1390, 1165), intensity=210)

    # x bank
    target_box((1525, 85),(1580, 140), intensity=100)


    # open armor and telport to duel arena via dueling ring
    pag.press('f2')
    target_box((2210, 1390), (2255, 1445), clicktype='right', intensity=210)

    delay(int(300 * random.random()))
    pag.moveRel(yOffset=110 + random.random() * 10)
    delay()
    pag.click()
    delay(250)

    # click on bottom portion of minimap to approach altar
    target_box((2100, 526), (2120, 545))
    delay(24 * random.random())
    pag.press('f2')
    delay(24 * random.random())
    target_box((1000, 1000), (1100, 1500), clicktype='')
    delay(10)
    # zoom out to normalize the following template matching process
    pag.scroll(-2000)


    time.sleep(8)
    delay(84)

    # locate altar on screen
    top_left, bottom_right = locate_temp('C:\\Users\\jsp4k\\Desktop\\smdev\\da_temp.PNG')
    random.choice(list(np.arange(start, stop, step)))
    xoff = int((bottom_right[0] - top_left[0]) * .4 * off)
    yoff = int((bottom_right[1] - top_left[1]) * .4 * off)
    top_left = top_left[0] + xoff, top_left[1] + yoff
    bottom_right = bottom_right[0] - xoff, bottom_right[1] - yoff

    target_box(top_left, bottom_right)

    delay(200)

    target_box((1000, 1000), (1500, 1200), clicktype='')

    delay(79)

    # open inventory
    pag.press('f1')



    # select water rune
    target_box((1830, 900), (1900, 950))
    delay(20)
    # select fire altar
    target_box((640, 325), (740, 390))
    delay(67, deterministic=True)
    # open magic menu
    pag.press('f5')
    # select magic imbue
    delay(20, deterministic=True)
    target_box((1815, 1072), (1850, 1100))
    delay(13, deterministic=True)
    # open inventory
    pag.press('f1')
    delay(55, deterministic=True)

    # empty pouches
    pag.keyDown('shift')
    delay(2, deterministic=True)
    target_box((1960,900),(2020, 970), intensity=random.random() * 4, deterministic=True)
    target_box((1820,1010),(1900, 1080), intensity=random.random() * 4, deterministic=True)
    target_box((1960,1025),(2020, 1075), intensity=2)
    delay(2, deterministic=True)
    pag.keyUp('shift')
    delay(2, deterministic=True)

    # select water altar
    target_box((1830, 900), (1900, 950), deterministic=True)
    delay(10, deterministic=True)
    target_box((1070, 820), (1190, 920), deterministic=True)

    # open armor
    pag.press('f2')
    target_box((2210, 1390), (2255, 1445), clicktype='right')

    # teleport to castle wars
    # teleport to castle wars
    delay(int(20 * random.random()))
    pag.moveRel(yOffset=180 + random.random() * 10)
    delay()
    pag.click()


# random delay function
def delay(intensity=42, deterministic=False):
    intensity = int(intensity)
    amp = random.choice(
        [.1, .13, .42, .1, .13, .14, .134, 1.67, .167, .2, .23, .25, .1, .1]) * random.random() * .042

    if intensity == 0:
        if amp < .000075 and deterministic == False:
            time.sleep(random.choice([10, 12, 13, 13, 50, 25, 10, 19, 20, 10, 10, 10, 12, 8, 19, 20, 30,
                                      21]) * random.random())  # super rare 'interrupt'
        time.sleep(amp)
    else:
        time.sleep(amp)
        delay(intensity-1, deterministic)

def target_box(top_left, bottom_right, intensity=81, clicktype="left", deterministic=False):
    x, y = random.choice(range(top_left[0], bottom_right[0])), random.choice(range(top_left[1], bottom_right[1]))

    delay()
    pag.moveTo(x, y, duration=random.random() + .142)
    if clicktype:
        delay(intensity, deterministic)
        pag.click(button=clicktype)


if __name__ == "__main__":
    main()