# shadow_dom_poc
Proof of concept for Shadow DOM Selenium issues

Demonstrates the limitations of the executeScript workaround for traversing shadow DOM elements in Selenium.

# DOM

```html
<body>
   <app-root _nghost-tuc-c18="" ng-version="11.2.6">
      <div _ngcontent-tuc-c18="">
         <app-container _ngcontent-tuc-c18="" id="container">
           #shadow-root (open)
             <app-select _nghost-tuc-c16="">
               <input _ngcontent-tuc-c16="" type="radio" id="yes" name="answer" value="yes">
               <label _ngcontent-tuc-c16="" for="yes">Yes</label><br _ngcontent-tuc-c16="">
               <input _ngcontent-tuc-c16="" type="radio" id="no" name="answer" value="no">
               <label _ngcontent-tuc-c16="" for="no">No</label><br _ngcontent-tuc-c16="">
               <input _ngcontent-tuc-c16="" type="radio" id="maybe" name="answer" value="maybe">
               <label _ngcontent-tuc-c16="" for="maybe">Maybe</label>
             </app-select>
         </app-container>
      </div>
   </app-root>
</body>
```

# Test Code

The test has 2 cases:
- Expand the shadow dom and select the "No" radio button by ID (Passes)
- Expand the shadow dom and select the "No" radio button by XPATH (Passes)


```python3
def test_execute_script_id():
    """Attempt to select the radio button for 'No' within the shadow DOM by ID"""
    driver = create_driver()
    try:
        container = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'container')))
        shadow_root = expand_shadow_element(driver, container)

        no_radio = shadow_root.find_element(By.ID, "no")
        no_radio.click()
    finally:
        time.sleep(5)
        driver.quit()


def test_execute_script_xpath():
    """Attempt to select the radio button for 'No' within the shadow DOM by XPATH"""
    driver = create_driver()
    try:
        container = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'container')))
        shadow_root = expand_shadow_element(driver, container)

        no_radio = shadow_root.find_element(By.XPATH, ".//app-select//input[@value='no']")
        no_radio.click()
    finally:
        time.sleep(10)
        driver.quit()
```

# Test Ouput
```
============================= test session starts ==============================
platform darwin -- Python 3.9.2, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
rootdir: /Users/ngenereux/git/shadow-dom-poc/test
collected 2 items

test.py .F                                                               [100%]

=================================== FAILURES ===================================
__________________________ test_execute_script_xpath ___________________________

    def test_execute_script_xpath():
        driver = create_driver()
        try:
            container = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'container')))
            shadow_root = expand_shadow_element(driver, container)
    
>           no_radio = shadow_root.find_element(By.XPATH, ".//app-select//input[@value='no']")

test.py:41: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.9/site-packages/selenium/webdriver/remote/webelement.py:658: in find_element
    return self._execute(Command.FIND_CHILD_ELEMENT,
.venv/lib/python3.9/site-packages/selenium/webdriver/remote/webelement.py:633: in _execute
    return self._parent.execute(command, params)
.venv/lib/python3.9/site-packages/selenium/webdriver/remote/webdriver.py:321: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x110e9b400>
response = {'status': 400, 'value': '{"value":{"error":"invalid selector","message":"invalid selector: Unable to locate an elemen...fff70d48109 _pthread_start + 148\\n24  libsystem_pthread.dylib             0x00007fff70d43b8b thread_start + 15\\n"}}'}

    def check_response(self, response):
        """
        Checks that a JSON response from the WebDriver does not have an error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get('status', None)
        if status is None or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get('value', None)
            if value_json and isinstance(value_json, basestring):
                import json
                try:
                    value = json.loads(value_json)
                    if len(value.keys()) == 1:
                        value = value['value']
                    status = value.get('error', None)
                    if status is None:
                        status = value["status"]
                        message = value["value"]
                        if not isinstance(message, basestring):
                            value = message
                            message = message.get('message')
                    else:
                        message = value.get('message', None)
                except ValueError:
                    pass
    
        exception_class = ErrorInResponseException
        if status in ErrorCode.NO_SUCH_ELEMENT:
            exception_class = NoSuchElementException
        elif status in ErrorCode.NO_SUCH_FRAME:
            exception_class = NoSuchFrameException
        elif status in ErrorCode.NO_SUCH_WINDOW:
            exception_class = NoSuchWindowException
        elif status in ErrorCode.STALE_ELEMENT_REFERENCE:
            exception_class = StaleElementReferenceException
        elif status in ErrorCode.ELEMENT_NOT_VISIBLE:
            exception_class = ElementNotVisibleException
        elif status in ErrorCode.INVALID_ELEMENT_STATE:
            exception_class = InvalidElementStateException
        elif status in ErrorCode.INVALID_SELECTOR \
                or status in ErrorCode.INVALID_XPATH_SELECTOR \
                or status in ErrorCode.INVALID_XPATH_SELECTOR_RETURN_TYPER:
            exception_class = InvalidSelectorException
        elif status in ErrorCode.ELEMENT_IS_NOT_SELECTABLE:
            exception_class = ElementNotSelectableException
        elif status in ErrorCode.ELEMENT_NOT_INTERACTABLE:
            exception_class = ElementNotInteractableException
        elif status in ErrorCode.INVALID_COOKIE_DOMAIN:
            exception_class = InvalidCookieDomainException
        elif status in ErrorCode.UNABLE_TO_SET_COOKIE:
            exception_class = UnableToSetCookieException
        elif status in ErrorCode.TIMEOUT:
            exception_class = TimeoutException
        elif status in ErrorCode.SCRIPT_TIMEOUT:
            exception_class = TimeoutException
        elif status in ErrorCode.UNKNOWN_ERROR:
            exception_class = WebDriverException
        elif status in ErrorCode.UNEXPECTED_ALERT_OPEN:
            exception_class = UnexpectedAlertPresentException
        elif status in ErrorCode.NO_ALERT_OPEN:
            exception_class = NoAlertPresentException
        elif status in ErrorCode.IME_NOT_AVAILABLE:
            exception_class = ImeNotAvailableException
        elif status in ErrorCode.IME_ENGINE_ACTIVATION_FAILED:
            exception_class = ImeActivationFailedException
        elif status in ErrorCode.MOVE_TARGET_OUT_OF_BOUNDS:
            exception_class = MoveTargetOutOfBoundsException
        elif status in ErrorCode.JAVASCRIPT_ERROR:
            exception_class = JavascriptException
        elif status in ErrorCode.SESSION_NOT_CREATED:
            exception_class = SessionNotCreatedException
        elif status in ErrorCode.INVALID_ARGUMENT:
            exception_class = InvalidArgumentException
        elif status in ErrorCode.NO_SUCH_COOKIE:
            exception_class = NoSuchCookieException
        elif status in ErrorCode.UNABLE_TO_CAPTURE_SCREEN:
            exception_class = ScreenshotException
        elif status in ErrorCode.ELEMENT_CLICK_INTERCEPTED:
            exception_class = ElementClickInterceptedException
        elif status in ErrorCode.INSECURE_CERTIFICATE:
            exception_class = InsecureCertificateException
        elif status in ErrorCode.INVALID_COORDINATES:
            exception_class = InvalidCoordinatesException
        elif status in ErrorCode.INVALID_SESSION_ID:
            exception_class = InvalidSessionIdException
        elif status in ErrorCode.UNKNOWN_METHOD:
            exception_class = UnknownMethodException
        else:
            exception_class = WebDriverException
        if value == '' or value is None:
            value = response['value']
        if isinstance(value, basestring):
            if exception_class == ErrorInResponseException:
                raise exception_class(response, value)
            raise exception_class(value)
        if message == "" and 'message' in value:
            message = value['message']
    
        screen = None
        if 'screen' in value:
            screen = value['screen']
    
        stacktrace = None
        if 'stackTrace' in value and value['stackTrace']:
            stacktrace = []
            try:
                for frame in value['stackTrace']:
                    line = self._value_or_default(frame, 'lineNumber', '')
                    file = self._value_or_default(frame, 'fileName', '<anonymous>')
                    if line:
                        file = "%s:%s" % (file, line)
                    meth = self._value_or_default(frame, 'methodName', '<anonymous>')
                    if 'className' in frame:
                        meth = "%s.%s" % (frame['className'], meth)
                    msg = "    at %s (%s)"
                    msg = msg % (meth, file)
                    stacktrace.append(msg)
            except TypeError:
                pass
        if exception_class == ErrorInResponseException:
            raise exception_class(response, message)
        elif exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if 'data' in value:
                alert_text = value['data'].get('text')
            elif 'alert' in value:
                alert_text = value['alert'].get('text')
            raise exception_class(message, screen, stacktrace, alert_text)
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.InvalidSelectorException: Message: invalid selector: Unable to locate an element with the xpath expression .//app-select//input[@value='no'] because of the following error:
E       NotSupportedError: Failed to execute 'evaluate' on 'Document': The node provided is '#document-fragment', which is not a valid context node type.
E         (Session info: chrome=89.0.4389.90)

.venv/lib/python3.9/site-packages/selenium/webdriver/remote/errorhandler.py:242: InvalidSelectorException
=========================== short test summary info ============================
FAILED test.py::test_execute_script_xpath - selenium.common.exceptions.Invali...
========================= 1 failed, 1 passed in 20.74s =========================

```
