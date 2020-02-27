"""Golem actions"""
import time
import uuid
import os
import sys
import importlib
import string
import random as rand
from random import randint

import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException

import requests

from golem.core.exceptions import TextNotPresent, ElementNotFound
from golem import browser
from golem import execution

import imutils
import cv2
import numpy as np
import pytesseract


def _run_wait_hook():
    wait_hook = execution.settings['wait_hook']
    if wait_hook:
        time.sleep(0.3)
        start_time = time.time()
        extend_module = importlib.import_module('projects.{0}.extend'
                                                .format(execution.project))
        wait_hook_function = getattr(extend_module, wait_hook)
        wait_hook_function()
        execution.logger.debug('Wait hook waited for {} seconds'
                               .format(time.time() - start_time))


def _add_step(message):
    execution.steps.append(message)


def _capture_or_add_step(message, screenshot_on_step):
    if screenshot_on_step:
        capture(message)
    else:
        _add_step(message)


def accept_alert():
    """Accept an alert"""
    # TODO implement through browser
    step_message = 'Accept alert'
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])
    driver = browser.get_browser()
    driver.switch_to.alert.accept()


def activate_browser(browser_id):
    """Activates a browser by the browser_id

    Parameters:
    browser_id : value
    """
    step_message = 'Activate browser {}'.format(browser_id)
    browser.activate_browser(browser_id)
    _capture_or_add_step(step_message, False)


def add_cookie(cookie_dict):
    """Add a cookie to the current session.

    Required keys are: "name" and "value"
    Optional keys are: "path", "domain", "secure", "expiry"

    Note:
    * If a cookie with the same name exists, it will be overriden.
    * This function cannot set the domain of a cookie, the domain URL
    must be visited by the browser first.
    * The domain is set automatically to the current domain the browser is in.
    * If the browser did not visit any url (initial blank page) this
    function will fail with "Message: unable to set cookie"

    Parameters:
    cookie_dict : value
    """
    execution.logger.debug('Add cookie: {}'.format(cookie_dict))
    driver = browser.get_browser()
    driver.add_cookie(cookie_dict)


def assert_contains(element, value):
    """Assert element contains value
    Parameters:
    element : element
    value : value
    """
    step_message = 'Assert that {0} contains {1}'.format(element, value)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, False)
    if not value in element:
        raise Exception('Expected {} to contain {}'.format(element, value))


def assert_equals(actual_value, expected_value):
    """Assert actual value equals expected value
    Parameters:
    actual_value : value
    expected_value : value
    """
    step_message = 'Assert that {0} equals {1}'.format(actual_value, expected_value)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, False)
    if not actual_value == expected_value:
        raise Exception('Expected {} to equal {}'.format(actual_value, expected_value))


def assert_false(condition):
    """Assert condition is false
    Parameters:
    condition : value
    """
    step_message = 'Assert that {0} is false'.format(condition)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, False)
    if condition:
        raise Exception('Expected {} to be false'.format(condition))


def assert_true(condition):
    """Assert condition is true
    Parameters:
    condition : value
    """
    step_message = 'Assert that {0} is true'.format(condition)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, False)
    if not condition:
        raise Exception('Expected {} to be true'.format(condition))


def capture(message=''):
    """Take a screenshot
    Parameters:
    message (optional) : value
    """
    _run_wait_hook()
    execution.logger.info('Take screenshot {}'.format(message))
    driver = browser.get_browser()
    # store image at this point, the target directory is already
    # created since the beginning of the test, stored in golem.core.report_directory
    img_id = str(uuid.uuid4())[:8]
    img_path = os.path.join(execution.report_directory, '{}.png'.format(img_id))
    driver.get_screenshot_as_file(img_path)

    if len(message) == 0:
        message = 'Screenshot'

    full_message = '{0}__{1}'.format(message, img_id)
    step(full_message)


# def capture_crop_compare_image(base_image, x, y, h, w, tolerance_rate=0.85):
#     """Take a screenshot of current webpage, crop the screenshot by x, y coordinates,Heights, and width; then compare the cropped image with target image, finally it should return true or false
#     Parameters:
#     base_image: base_image name specifed in the base_images folder, no .png required
#     x: top left x coordinate
#     y: top left y coordinates
#     h: height of the block
#     w: width of the block
#     tolerance_rate: the image comparison tolerance rate, range from [0,1], 1 would be mean perfect match, the default value is 0.85
#     """
#     _run_wait_hook()
#     driver = browser.get_browser()
#     # store image at this point, the target directory is already
#     # created since the beginning of the test, stored in golem.core.report_directory
#     img_id = str(uuid.uuid4())[:8]
#     execution.logger.info('Take screenshot and save as {}.png'.format(img_id))
#     img_path = os.path.join(execution.report_directory, '{}.png'.format(img_id))
#     base_image_path = execution.report_directory.split('reports/')[0] + "base_images"
#     target_img_path = os.path.join(base_image_path, '{}.png'.format(base_image))
#     # Save current web page as screenshot
#     driver.get_screenshot_as_file(img_path)
#     img = cv2.imread(img_path)
#     # check the image size
#     # TODO, need to remove the hard coded image size
#     if not (img.size == 1262400):
#         resized_img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
#         crop_img = resized_img[y:y + h, x:x + w]
#     else:
#         crop_img = img[y:y + h, x:x + w]

#     # Generate the image path for saving the cropped image
#     img_id_2 = str(uuid.uuid4())[:8]
#     img_path_2 = os.path.join(execution.report_directory, '{}.png'.format(img_id_2))

#     # Save the cropped image in local report dir
#     b = cv2.imwrite(img_path_2, crop_img)
#     execution.logger.info('Being able to save cropped image? {0} \n And Crop the image and save as {1}.png'.format(b, img_id_2))
#     target_img = cv2.imread(target_img_path)

#     # convert the images to gray and do comparison
#     gray_crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
#     gray_target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
#     (score, diff) = compare_ssim(gray_crop_img, gray_target_img, full=True)
#     # diff = (diff * 255).astype("uint8")
#     execution.logger.info("The score value are: score {0}".format(score))

#     # Make sure the image comparison score is higher than the tolerance value
#     if score >= tolerance_rate:
#         execution.logger.info("Great! The score value ({0}) is higher than the tolerance rate ({1})".format(score, tolerance_rate))
#         return True
#     else:
#         execution.logger.info("Oh no! The score value ({0}) is lower than the tolerance rate ({1}). Please check why the two images is not matching".format(score, tolerance_rate))
#         return False


def verify_element_exist_by_coordinates(base_image, default_image_size=1262400, threshold=0.8):
    """Take a screenshot of current webpage, and make the base image compare to do a template matching to the scaled screenshot, then finally get the coordinates for the where the template image is in the screenshot
    Parameters:
    base_image : image name for base image
    default_image_size: the default image size is 1262400 when the web window is limited to 800 * 600
    threshold: the threshold for determing whether the element exist or not
    """
    _run_wait_hook()
    driver = browser.get_browser()
    # store image at this point, the target directory is already
    # created since the beginning of the test, stored in golem.core.report_directory
    img_id = str(uuid.uuid4())[:8]
    execution.logger.info('Take screenshot and save as {}.png'.format(img_id))
    img_path = os.path.join(execution.report_directory, '{}.png'.format(img_id))

    # Save current web page as screenshot
    driver.get_screenshot_as_file(img_path)

    # Create direcotory for finding the target base image for template matching in base images folder
    base_image_path = execution.report_directory.split('reports/')[0] + "base_images"
    target_img_path = os.path.join(base_image_path, '{}.png'.format(base_image))

    # load the base image, convert it to grayscale, and detect edges
    template = cv2.imread(target_img_path)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template = cv2.Canny(template, 50, 200)
    (tH, tW) = template.shape[:2]
    execution.logger.info('The heigh and width of the base image are (Height: {0}, Width: {1})'.format(tH, tW))

    # load the screenshot and convert it to gray scale
    image = cv2.imread(img_path)
    height, width = image.shape[:2]
    execution.logger.info('The heigh and width of the screenshot are (Height: {0}, Width: {1})'.format(height, width))
    # Convert the screenshot to Gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    found = None
    flag = False
    # loop over the scales of the image
    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        # Resize the image according to the scale, and keep track of ratio of the resizing
        resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
        r = gray.shape[1] / float(resized.shape[1])

        # if the resized image is smaller than the template, then break from the loop
        if resized.shape[0] < tH or resized.shape[1] < tW:
            break

        # detect edges in the resized, grayscale image and apply template
        # matching to find the template in the image
        edged = cv2.Canny(resized, 50, 200)
        result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

        # if we have found a new maximum correlation value, then update
        # the bookkeeping variable
        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)
        for i in result:
            if i.any() > threshold:
                flag = True
    # unpack the bookkeeping varaible and compute the (x, y) coordinates
    # of the bounding box based on the resized ratio
    (_, maxLoc, r) = found
    print((_, maxLoc, r))
    (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
    execution.logger.debug('The start coordinate for the element is (startX: {}, startY: {})'.format(startX, startY))
    (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
    execution.logger.debug('The end coordinate for the element is (endX: {}, endY: {})'.format(endX, endY))

    matched_image = cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
    matched_img_path = os.path.join(execution.report_directory, 'matched_{}.png'.format(img_id))
    save_matched_image = cv2.imwrite(matched_img_path, matched_image)
    # cv2.imshow("Image", image)
    execution.logger.info('Save the matched result as matched_{}.png'.format(img_id))

    if (image.size > default_image_size):
        ratio = math.sqrt(image.size / default_image_size)
        x_coordinate = (startX + endX) / (2 * ratio)
        y_coordinate = (startY + endY) / (2 * ratio)
        store('element_x_coordinate', x_coordinate)
        store('element_y_coordinate', y_coordinate)
        execution.logger.info('the element coordinate on the current screen is (x: {}, y: {})'.format(x_coordinate, y_coordinate))
    else:
        x_coordinate = (startX + endX) / 2
        y_coordinate = (startY + endY) / 2
        store('element_x_coordinate', x_coordinate)
        store('element_y_coordinate', y_coordinate)
        execution.logger.info('the element coordinate on the current screen is (x: {}, y: {})'.format(x_coordinate, y_coordinate))
    print(flag)
    return flag


def extract_text_from_image(image_path):
    """Extract the text from a target image using tesseract
    Parameters:
    image path: full image path ending with file name
    """
    _run_wait_hook()
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    image_text = pytesseract.image_to_string(gray)
    execution.logger.info('The text reads from the {0} is \' {1} \''.format(image_path, image_text))
    return image_text


def verify_element_exist_by_text(target_text):
    """Take a screenshot of current webpage, extract the text from current webpage, and do a string matching to see whether the target text is existed in current webpage.
    Parameters:
    target_text: target text for comparison
    """
    _run_wait_hook()
    driver = browser.get_browser()
    # store image at this point, the target directory is already
    # created since the beginning of the test, stored in golem.core.report_directory
    img_id = str(uuid.uuid4())[:8]
    execution.logger.info('Take screenshot and save as {}.png'.format(img_id))
    img_path = os.path.join(execution.report_directory, '{}.png'.format(img_id))

    # Save current web page as screenshot
    driver.get_screenshot_as_file(img_path)

    # load the screenshot and extract the text from the screenshot
    screenshot_text = extract_text_from_image(img_path)
    execution.logger.info('The text in current webpage are printed as {}'.format(screenshot_text))

    # Verify the target text exist in the screenshot text
    if target_text in screenshot_text:
        execution.logger.info('Congrats! We find the {0} exists in current Webpage'.format(target_text))
        return True
    else:
        execution.logger.info('Ooops! We could not find the {0} exists in current Webpage..please try again'.format(target_text))
        return False


def wait_while_text_element_present(target_text, timeout=60):
    """Wait while the element text is present on the current webpage
    After timeout this won't throw an exception.
    Parameters:
    target_text : the target text for comparison
    timeout (optional, default: 60) : value
    """
    try:
        timeout = int(timeout)
    except:
        raise Exception('Timeout should be digits only')
    _run_wait_hook()
    execution.logger.info('Waiting while element text \' {} \' is visible'.format(target_text))
    start_time = time.time()
    timed_out = False
    while verify_element_exist_by_text(target_text) and not timed_out:
        execution.logger.info('Element text {} is still present, waiting..'.format(target_text))
        time.sleep(0.5)
        if time.time() - start_time > timeout:
            timed_out = True
    execution.logger.info('We successfully finished waiting while the element text {0} is visible, while do we reach the timeout? {1} '.format(target_text, timed_out))


def clear(element):
    """Clear an input
    Parameters:
    element : element
    """
    _run_wait_hook()
    webelement = browser.get_browser().find(element)
    step_message = 'Clear {0} element'.format(webelement.name)
    execution.logger.info(step_message)
    webelement.clear()
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])


def click(element):
    """Click an element
    Parameters:
    element : element
    """
    _run_wait_hook()
    webelement = browser.get_browser().find(element)
    step_message = 'Click {0}'.format(webelement.name)
    execution.logger.info(step_message)
    webelement.click()
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])


def close():
    """Close a browser. Closes the current active browser"""
    execution.logger.info('Close driver')
    driver = get_browser()
    driver.quit()
    execution.browser = None


def debug():
    """Enter debug mode"""
    if not execution.settings['interactive']:
        execution.logger.info('the -i flag is required to access interactive mode')
        return

    try:
        # optional, enables Up/Down/History in the console
        # not available in windows
        import readline
    except:
        pass
    import code

    def console_exit():
        raise SystemExit

    def console_help():
        msg = ('# start a browser and find an element:\n'
               'navigate(\'http://..\')\n'
               'browser = get_browser()\n'
               'browser.title\n'
               'element = browser.find(id=\'some-id\')\n'
               'element.text\n'
               '\n'
               '# use Golem actions\n'
               'actions.send_keys(element, \'some text\')\n'
               '\n'
               '# import a page from a project\n'
               'from projects.project_name.pages import page_name\n'
               '\n'
               '# get test data (when run from a test)\n'
               'execution.data')
        print(msg)
    vars_copy = globals().copy()
    vars_copy.update(locals())
    vars_copy['exit'] = console_exit
    vars_copy['help'] = console_help
    actions_module = sys.modules[__name__]
    vars_copy['actions'] = actions_module
    banner = ('Entering interactive mode\n'
              'type exit() to stop\n'
              'type help() for more info')
    shell = code.InteractiveConsole(vars_copy)
    try:
        shell.interact(banner=banner)
    except SystemExit:
        pass


def delete_cookie(name):
    """Delete a cookie from the current session

    Parameters:
    name: value
    """
    execution.logger.debug('Delete cookie "{}"'.format(name))
    driver = browser.get_browser()
    cookie = driver.get_cookie(name)
    if not cookie:
        raise Exception('Cookie "{}" was not found'.format(name))
    else:
        driver.delete_cookie(name)


def delete_all_cookies():
    """Delete all cookies from the current session.

    Note: this only deletes cookies from the current domain.
    """
    execution.logger.debug('Delete all cookies')
    driver = browser.get_browser().delete_all_cookies()


def dismiss_alert():
    """Dismiss an alert"""
    # TODO implement through browser
    step_message = 'Dismiss alert'
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])
    driver = browser.get_browser()
    driver.switch_to.alert.dismiss()


def get(url):
    """Navigate to the given URL
    Parameters:
    url : value
    """
    navigate(url)


def get_browser():
    """Get the current active browser"""
    return browser.get_browser()


def get_cookie(name):
    """Get a cookie by its name.
    Returns the cookie if found, None if not.
    Parameters:
    name : value
    """
    execution.logger.debug('Get cookie "{}"'.format(name))
    driver = browser.get_browser()
    return driver.get_cookie(name)


def get_cookies():
    """Returns a list of dictionaries, corresponding to cookies
    visible in the current session.
    """
    execution.logger.debug('Get all current cookies')
    driver = browser.get_browser()
    return driver.get_cookies()


def get_current_url():
    """Return the current browser URL
    """
    return browser.get_browser().current_url


def get_current_title():
    """Return the current browser title
    """
    return browser.get_browser().title


def switch_window(window_name):
    """switch window by name
    """
    browser.get_browser().switch_to_window(window_name)


def window_number_gen(number, window_name):
    """Give different window different name
    """
    a = browser.get_browser().window_handles[number]
    store(window_name, a)


def mouse_hover(element):
    """Hover an element with the mouse
    Parameters:
    element : element
    """
    _run_wait_hook()
    driver = browser.get_browser()
    webelement = driver.find(element)
    step_message = 'Mouse hover element \'{0}\''.format(webelement.name)
    execution.logger.info(step_message)
    ActionChains(driver).move_to_element(webelement).perform()
    #_capture_or_add_step(step_message, execution.settings['screenshot_on_step'])


def click_on_target_area_with_coordinates(area_name, base_element, x_coordinate, y_coordinate):
    """Move to an base_element and then move the mouse to the offset location with the mouse and then click on specified area
    Parameters:
    area_name : specify the element name in certain area
    base_element : the base element for moving the mouse left and right
    x_coordinate: x coordinate of the target element
    y_coordinate: int
    """
    _run_wait_hook()
    driver = browser.get_browser()
    webelement = driver.find(base_element)
    e_location = webelement.location
    print("The element location is {}".format(e_location))
    step_message = 'Mouse hover to base_element \'{0}\' and then move to coordinates (x: {1}, y: {2},) and then click on the specified area with name as {3} '.format(webelement.name, x_coordinate, y_coordinate, area_name)
    execution.logger.info(step_message)
    move_x = x_coordinate - e_location['x']
    move_y = y_coordinate - e_location['y']
    move_to_target_area = ActionChains(driver).move_to_element_with_offset(webelement, move_x, move_y)
    move_to_target_area.click().perform()
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])


def get_current_window_rect():
    """Gets the x, y coordinates of the window as well as height and width of the current window.
    Parameters:
    """
    driver = browser.get_browser()
    a = driver.get_window_rect()
    step_message = 'Get current window\'s x y coordinates, height and width as {}'.format(a)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])


def get_element_location(element):
    """Gets the x, y coordinates, height, and width of the webelement
    Parameters:
    element: element
    """
    _run_wait_hook()
    driver = browser.get_browser()
    webelement = driver.find(element)
    location = webelement.location
    size = webelement.size
    step_message = 'get_element_location x y coordinates as: {0}, height and width as: {1}'.format(location, size)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])


def navigate(url):
    """Navigate to a URL
    Parameters:
    url : value
    """
    step_message = 'Navigate to: \'{0}\''.format(url)
    driver = browser.get_browser()
    driver.get(url)
    # driver.maximize_window()
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])


def open_browser(browser_id=None):
    """Open a new browser. The param browser_id is optional
    and only used to manage more than one browser at the same time.
    Parameters:
    browser_id (optional) : value
    """
    step_message = 'Open browser'
    browser.open_browser(browser_id)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])


def press_key(element, key):
    """Press a given key in the element.
    Parameters:
    element : element
    key : value
    """
    step_message = 'Press key: {}'.format(key)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])
    webelement = get_browser().find(element)
    if key == 'RETURN' or key == 'ENTER':
        webelement.send_keys(Keys.RETURN)
    elif key == 'UP':
        webelement.send_keys(Keys.UP)
    elif key == 'DOWN':
        webelement.send_keys(Keys.DOWN)
    elif key == 'LEFT':
        webelement.send_keys(Keys.LEFT)
    elif key == 'RIGHT':
        webelement.send_keys(Keys.RIGHT)
    else:
        raise Exception('Key value {} is invalid'.format(key))


def random(value):
    """Generate a random string value.
    TODO
    Parameters:
    value : value
    """
    random_string = ''
    for char in value:
        if char == 'c':
            random_string += rand.choice(string.ascii_lowercase)
        elif char == 'd':
            random_string += str(rand.randint(0, 9))
        else:
            random_string += char
    execution.logger.info('Random value generated: {}'.format(random_string))
    return random_string


def random_with_N_digits(n):
    """Generate N digits of random numbers.
    Parameters:
    n: the number of digits you want to generate
    """
    range_start = 10**(n-1)
    range_end = (10**n) -1
    return randint(range_start, range_end)

    
def refresh_page():
    """Refresh the page."""
    _run_wait_hook()
    step_message = 'Refresh page'
    browser.get_browser().refresh()
    # get_browser().execute_script("location.reload()")
    #browser = get_browser()
    # browser.get(browser.current_url);
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])


def reload_games(element, attribute_name, expected_attribute_value, times=3):
    """Refresh the page and reload the games"""
    _run_wait_hook()
    step_message = 'reload games'
    execution.logger.info(step_message)    
    if execution.data['timed_out'] is True:
        execution.logger.info("The game is not loading after timed out")
        for i in range(times):
            execution.logger.info("refresh the game for {} time".format(str(i+1)))
            browser.get_browser().refresh()
            wait(20)
            wait_for_element_attribute_visible(element, attribute_name, expected_attribute_value)    
            if execution.data['timed_out'] is False:
                break
        assert_false(execution.data['timed_out'] is True)        
    else:
        execution.logger.info("The game seems loaded fine...skipping reload games")


def select_by_index(element, index):
    """Select an option from a select dropdown by index.
    Parameters:
    element : element
    index : value
    """
    _run_wait_hook()
    webelement = browser.get_browser().find(element)
    step_message = 'Select option of index {0} from element {1}'.format(index, webelement.name)
    select = selenium.webdriver.support.select.Select(webelement)
    select.select_by_index(index)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])


def select_by_text(element, text):
    """Select an option from a select dropdown by text.
    Parameters:
    element : element
    text : value
    """
    _run_wait_hook()
    webelement = browser.get_browser().find(element)
    step_message = 'Select \'{0}\' from element {1}'.format(text, webelement.name)
    select = selenium.webdriver.support.select.Select(webelement)
    select.select_by_visible_text(text)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])


def select_by_value(element, value):
    """Select an option from a select dropdown by value.
    Parameters:
    element : element
    value : value
    """
    _run_wait_hook()
    webelement = browser.get_browser().find(element)
    step_message = 'Select \'{0}\' value from element {1}'.format(value, webelement.name)
    select = selenium.webdriver.support.select.Select(webelement)
    select.select_by_value(value)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])


def send_keys(element, text):
    """Send keys to an input.
    Parameters:
    element : element
    text : value
    """
    _run_wait_hook()
    webelement = browser.get_browser().find(element)
    step_message = 'Write \'{0}\' in element {1}'.format(text, webelement.name)
    # TODO chrome driver drops some characters when calling send_keys
    # if execution.browser_name in ['chrome', 'chrome-headless', 'chrome-remote']:
    #     for c in text:
    #         webelement.send_keys(c)
    #         time.sleep(0.1)
    # else:
    webelement.send_keys(text)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])


def set_browser_capability(capability_key, capability_value):
    """Set a browser capability.
    Parameters:
    capability_key : value
    capability_value : value
    """
    step_message = ('Set browser cabability "{}" to "{}"'
                    .format(capability_key, capability_value))
    execution.browser_definition['capabilities'][capability_key] = capability_value
    execution.logger.debug(step_message)


def set_window_size(width, height):
    """Set the browser window size.
    Parameters:
    width : value
    height : value
    """
    _run_wait_hook()
    driver = browser.get_browser()
    step_message = 'Set browser window size to {0}x, {1}y.'.format(width, height)
    driver.set_window_size(width, height)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])


def step(message):
    """Log a step to the report.
    Parameters:
    message : value
    """
    execution.logger.info(message)
    execution.steps.append(message)


def store(key, value):
    """Store a value in data.
    Parameters:
    key : value
    value : value
    """
    execution.logger.info('Store value {} in key {}'.format(value, key))
    setattr(execution.data, key, value)


def verify_alert_is_present():
    """Verify an alert is present"""
    # TODO implement through browser
    step_message = 'Verify an alert is present'
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])
    driver = browser.get_browser()
    try:
        alert = driver.switch_to.alert
    except NoAlertPresentException:
        assert False, 'an alert was not present'


def verify_alert_is_not_present():
    """Verify an alert is not present"""
    # TODO implement through browser
    step_message = 'Verify an alert is not present'
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])
    driver = browser.get_browser()
    try:
        alert = driver.switch_to.alert
        assert False, 'an alert was present'
    except NoAlertPresentException:
        pass


def verify_cookie_value(name, value):
    """Verify the value of a cookie.

    Parameters:
    name: value
    value: value
    """
    step_message = ('Verify that cookie "{}" contains value "{}"'
                    .format(name, value))
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])
    cookie = browser.get_browser().get_cookie(name)
    if not cookie:
        raise Exception('Cookie "{}" was not found'.format(name))
    elif not 'value' in cookie:
        raise Exception('Cookie "{}" did not have "value" key'.format(name))
    elif cookie['value'] != value:
        msg = ('Expected cookie "{}" value to be "{}" but was "{}"'
               .format(name, value, cookie['value']))
        raise Exception(msg)


def verify_cookie_exists(name):
    """Verify a cookie exists in the current session.
    The cookie is found by its name.

    Parameters:
    name: value
    """
    step_message = 'Verify that cookie "{}" exists'.format(name)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])
    cookie = browser.get_browser().get_cookie(name)
    if not cookie:
        raise Exception('Cookie "{}" was not found'.format(name))


# TODO rename to verify_element_exists
def verify_exists(element):
    """Verify that en element exists.
    Parameters:
    element : element
    """
    _run_wait_hook()
    step_message = 'Verify that the element exists'
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])
    try:
        webelement = browser.get_browser().find(element, timeout=1)
    except:
        raise ElementNotFound('Element {} does not exist'.format(element))


def verify_is_enabled(element):
    """Verify an element is enabled.
    Parameters:
    element : element
    """
    _run_wait_hook()
    webelement = browser.get_browser().find(element)
    step_message = 'Verify the element \'{0}\' is enabled'.format(webelement.name)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])
    if not webelement.is_enabled():
        raise Exception('Element is enabled')


def verify_is_not_enabled(element):
    """Verify an element is not enabled
    Parameters:
    element : element
    """
    _run_wait_hook()
    webelement = browser.get_browser().find(element)
    step_message = 'Verify the element \'{0}\' is not enabled'.format(webelement.name)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])
    if webelement.is_enabled():
        raise Exception('Element is enabled')


def verify_is_not_selected(element):
    """Verify an element is not selected
    Parameters:
    element : element
    """
    _run_wait_hook()
    webelement = browser.get_browser().find(element)
    step_message = 'Verify the element \'{0}\' is not selected'.format(webelement.name)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])
    if webelement.is_selected():
        raise Exception('Element is selected')


def verify_is_not_visible(element):
    """Verify an element is not visible
    Parameters:
    element : element
    """
    _run_wait_hook()
    webelement = browser.get_browser().find(element)
    step_message = 'Verify the element \'{0}\' is not visible'.format(webelement.name)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])
    if webelement.is_displayed():
        raise Exception('Element is visible')


def verify_is_selected(element):
    """Verify an element is selected
    Parameters:
    element : element
    """
    _run_wait_hook()
    webelement = browser.get_browser().find(element)
    step_message = 'Verify the element \'{0}\' is selected'.format(webelement.name)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])
    if not webelement.is_selected():
        raise Exception('Element is not selected')


def verify_is_visible(element):
    """Verify an element is visible
    Parameters:
    element : element
    """
    _run_wait_hook()
    webelement = browser.get_browser().find(element)
    step_message = 'Verify the element \'{0}\' is visible'.format(webelement.name)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])
    if not webelement.is_displayed():
        raise Exception('Element is not visible')


def verify_not_exists(element):
    """Verify an element does not exist
    Parameters:
    element : element
    """
    _run_wait_hook()
    step_message = 'Verify that the element'
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])
    try:
        webelement = get_browser().find(element)
        if webelement:
            raise Exception('Element {} exists and should not'
                            .format(webelement.name))
    except ElementNotFound:
        pass


def verify_selected_option(element, text):
    """Verify an element has a selected option, passed by option text.
    Parameters:
    element : element
    text : value
    """
    _run_wait_hook()
    webelement = browser.get_browser().find(element)
    select = selenium.webdriver.support.select.Select(webelement)
    step_message = ('Verify selected option of element \'{0}\''
                    ' is \'{1}\''.format(webelement.name, text))
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])
    if not select.first_selected_option.text == text:
        raise TextNotPresent('Option selected in element \'{0}\' '
                             'is not {1}'
                             .format(webelement.name, text))


def verify_text(text):
    """Verify that the given text is present anywhere in the page.
    Parameters:
    text : value
    """
    _run_wait_hook()
    driver = browser.get_browser()
    step_message = 'Verify \'{0}\' is present in page'.format(text)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])
    if text not in driver.page_source:
        raise TextNotPresent("Text '{}' was not found in the page".format(text))


def verify_text_in_element(element, text):
    """Verify the given text is present in element.
    Parameters:
    element : element
    text : value
    """
    _run_wait_hook()
    webelement = browser.get_browser().find(element)
    step_message = 'Verify element \'{0}\' contains text \'{1}\''.format(webelement.name, text)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, execution.settings['screenshot_on_step'])
    if text not in webelement.text:
        raise TextNotPresent("Text \'{0}\' was not found in element {1}. Text \'{2}\' was found."
                             .format(text, webelement.name, webelement.text))


def wait(seconds):
    """Wait for a fixed amount of seconds.
    Parameters:
    seconds (int or float) : value
    """
    execution.logger.info('Waiting for {} seconds'.format(seconds))
    try:
        to_float = float(seconds)
    except:
        raise Exception('seconds value should be a number')
    time.sleep(to_float)

# TODO
# def wait_for_element_exists(element, timeout=20):
# #     try:
# #         timeout = int(timeout)
# #     except:
# #         raise Exception('Timeout should be digits only')
# #     execution.logger.info('Waiting for element {} to not exist'.format(element))
# #     webelement = None
# #     start_time = time.time()
# #     while not webelement and (time.time() - start_time) < timeout:
# #         try:
# #             webelement = get_browser().find(element, timeout=3)
# #         except:
# #             print('wait_for_element_exists')

#     start_time = time.time()
#     still_exists = True
#     remaining_time = time.time() - start_time
#     while still_exists and remaining_time < timeout:
#         time.sleep(0.5)
#         remaining_time = time.time() - start_time
#         try:
#             webelement = get_browser().find(element, timeout=0)
#         except:
#             still_exists = False
#     # else:
#     #     execution.logger.debug('Element {} was not found, continuing...'.format(element))


# def wait_for_element_clickable(element, timeout=20):
#     browser = get_browser()
#     element = WebDriverWait(browser, timeout).until(
#         EC.element_to_be_clickable())


def wait_for_element_not_exist(element, timeout=20):
    """Wait for a webelement to stop existing in the DOM.
    If the webelement still exists after the timeout
    ended, it will not raise an exception.
    Parameters:
    element : element
    timeout (optional, default: 20) : value
    """
    try:
        timeout = int(timeout)
    except:
        raise Exception('Timeout should be digits only')
    execution.logger.info('Waiting for element {} to not exist'.format(element))
    webelement = None
    try:
        s = browser.get_browser().find(element, timeout=3)
    except:
        execution.logger.debug('Element already does not exist, continuing...')
        return
    start_time = time.time()
    still_exists = True
    remaining_time = time.time() - start_time
    while still_exists and remaining_time <= timeout:
        execution.logger.debug('Element still exists in the DOM, waiting...')
        time.sleep(0.5)
        remaining_time = time.time() - start_time
        try:
            webelement = get_browser().find(element, timeout=0)
        except:
            still_exists = False
            execution.logger.debug('Element stopped existing')


def wait_for_element_not_visible(element, timeout=20):
    """Wait for an element to stop being visible.
    After the timeout, this won't throw an exception.
    Parameters:
    element : element
    timeout (optional, default: 20) : value
    """
    try:
        timeout = int(timeout)
    except:
        raise Exception('Timeout should be digits only')
    execution.logger.info('Waiting for element {} to be not visible'.format(element))
    webelement = None
    try:
        webelement = browser.get_browser().find(element, timeout=3)
    except:
        execution.logger.debug('Element is already not visible, continuing...')
        return
    if webelement:
        start_time = time.time()
        timed_out = False
        while webelement.is_displayed() and not timed_out:
            execution.logger.debug('Element is still visible, waiting...')
            time.sleep(0.5)
            if time.time() - start_time > timeout:
                timed_out = True
                execution.logger.info('Timeout, element is still visible.')


def wait_for_element_enabled(element, timeout=20):
    """Wait for element to be enabled.
    After timeout this won't throw an exception.
    Parameters:
    element : element
    timeout (optional, default: 20) : value
    """
    execution.logger.info('Waiting for element {} to be enabled'.format(element))
    start_time = time.time()
    timed_out = False
    #webelement = None
    # try:
    webelement = browser.get_browser().find(element, timeout)
    enabled = webelement.is_enabled()
    while not enabled and not timed_out:
        execution.logger.debug('Element is not enabled, waiting..')
        time.sleep(0.5)
        enabled = webelement.is_displayed()
        if time.time() - start_time > timeout:
            timed_out = True


def wait_for_element_visible(element, timeout=20):
    """Wait for element to be visible.
    After timeout this won't throw an exception.
    Parameters:
    element : element
    timeout (optional, default: 20) : value
    """
    try:
        timeout = int(timeout)
    except:
        raise Exception('Timeout should be digits only')
    _run_wait_hook()
    execution.logger.info('Waiting for element {} to be visible'.format(element))
    start_time = time.time()
    timed_out = False
    webelement = browser.get_browser().find(element)
    while not webelement.is_displayed() and not timed_out:
        execution.logger.debug('Element is not visible, waiting..')
        time.sleep(0.5)
        if time.time() - start_time > timeout:
            timed_out = True


def wait_for_element_attribute_visible(element, attribute_name, expected_attribute_value, timeout=360):
    """Wait for element attribute to be visible.
    After timeout this won't throw an exception.
    Parameters:
    element : element
    attribute_name: The attribute name you are looking for
    expected_attribute_value: The expected attribute value for comparison
    timeout (optional, default: 30) : value
    """
    try:
        timeout = int(timeout)
    except:
        raise Exception('Timeout should be digits only')
    _run_wait_hook()
    execution.logger.info('Waiting for element\'s attribute {} to be visible'.format(attribute_name))
    start_time = time.time()
    timed_out = False
    webelement = browser.get_browser().find(element)
    attribute_value = None
    while not attribute_value == expected_attribute_value and not timed_out:
        execution.logger.debug('Element\'s attribute is not visible, waiting..')
        attribute_value = webelement.get_attribute(attribute_name)
        execution.logger.debug('The attribute value is {}'.format(attribute_value))
        time.sleep(0.5)
        if time.time() - start_time > timeout:
            timed_out = True
    store('timed_out', timed_out) 


def http_get(url, headers={}, params={}, verify_ssl_cert=True):
    """Perform an HTTP GET request to the given URL.
    Headers and params are optional dictionaries.

    Parameters:
    url : value
    headers (optional, dict) : value
    params (optional, dict) : value
    verify_ssl_cert (optional, default is True) : value
    """
    step_message = 'Make GET request to {}'.format(url)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, False)
    response = requests.get(url, headers=headers, params=params, verify=verify_ssl_cert)
    store('last_response', response)


def http_post(url, headers={}, data={}, verify_ssl_cert=True):
    """Perform an HTTP POST request to the given URL.
    Headers and data are optional dictionaries.

    Parameters:
    url : value
    headers (optional, dict) : value
    data (optional, dict) : value
    verify_ssl_cert (optional, default is True) : value
    """
    step_message = 'Make POST request to {}'.format(url)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, False)
    response = requests.post(url, headers=headers, data=data, verify=verify_ssl_cert)
    store('last_response', response)


def verify_response_status_code(response, status_code):
    """Verify the response status code.
    Parameters:
    response : value
    status_code : value
    """
    if isinstance(status_code, str):
        if status_code.isdigit():
            status_code = int(status_code)
    step_message = 'Verify response status code is {}'.format(status_code)
    execution.logger.info(step_message)
    _capture_or_add_step(step_message, False)
    if not response.status_code == status_code:
        raise Exception("Expected response status code to be {0} but was {1}"
                        .format(status_code, response.status_code))


# def verify_response_content():
#     pass
