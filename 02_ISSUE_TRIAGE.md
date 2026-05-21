# Issue Triage: Helium

## Focus Areas

### 1. Selenium Compatibility
**Status**: Requires selenium>=4.16.0 (setup.py:16, requirements/base.txt:2)

**Key Integration Points**:
- `_impl/__init__.py:18` - Direct imports: `Chrome, ChromeOptions, Firefox, FirefoxOptions`
- `selenium_wrappers.py` - WebDriverWrapper checks `browser_name` from capabilities (line 45)
- Firefox detection: `driver.is_firefox()` used at lines 39, 256

**Known Compatibility Notes**:
- Chrome 140.0.7339.185+ password leak detection handled (lines 113-120)
- Firefox requires geckodriver on PATH for older Firefox versions
- `ServiceFirefox(log_path=service_log_path)` used (line 91)

### 2. Firefox Options Path Handling

**Location**: `_impl/__init__.py:76-93`

```python
def _start_firefox_driver(self, headless, options, profile):
    firefox_options = FirefoxOptions() if options is None else options
    if headless:
        firefox_options.add_argument('--headless')
    kwargs = {'options': firefox_options}
    if profile:
        firefox_options.profile = profile  # line 89
    service_log_path = 'nul' if is_windows() else '/dev/null'
    service = ServiceFirefox(log_path=service_log_path)
    result = Firefox(service=service, **kwargs)
```

**Potential Issues**:
- `firefox_options.profile` assignment (line 89) - FirefoxProfile is set directly on options object
- No validation of profile type before assignment
- No handling for deprecated FirefoxProfile API in newer Selenium

### 3. Unicode Press Behavior

**Location**: `_impl/__init__.py:188-189`

```python
def press_impl(self, key):
    self.require_driver().switch_to.active_element.send_keys(key)
```

**Test Coverage** (`tests/api/test_press.py`):
- `test_press_single_character` - lowercase 'a'
- `test_press_upper_case_character` - uppercase 'A'
- `test_press_shift_plus_lower_case_character` - SHIFT + 'a' → 'A'

**Unicode Observations**:
- `press()` uses Selenium's `send_keys()` which handles unicode natively
- No explicit unicode handling in helium layer
- `write()` docstring mentions "one of str, unicode" (line 160)

### 4. LookupError Improvements

**Error Enhancement Pattern** (multiple locations in `_impl/__init__.py`):

```python
except LookupError:
    raise LookupError(repr(into)) from None  # lines 159-161
except LookupError:
    raise LookupError(repr(element)) from None  # lines 237-239
except LookupError:
    raise LookupError(repr(combo_box)) from None  # lines 303-305
```

**Test Coverage** (`tests/api/test_lookup_error_message.py`):
- Tests for click, hover, write, highlight, select, attach_file, drag_file
- Each test verifies error message contains the element repr (e.g., `"Button('Non-existent')"`)
- Uses `TemporaryAttrValue` to set `Config.implicit_wait_secs = .1`

**Pattern**: Catch generic `LookupError`, re-raise with `repr()` of the original element/slector

### 5. Element Lookup Tests

**Main Test File**: `tests/api/test_gui_elements.py` (275 lines)

**Test Categories**:

| Category | Elements Tested |
|----------|----------------|
| Buttons | exists, enabled, disabled, submit, input, div, title |
| TextFields | exists, editable, enabled, value, placeholder, readonly, disabled, German umlaut |
| ComboBox | exists, editable, options, select |
| CheckBox | exists, checked, unchecked, enabled, disabled, labels |
| RadioButton | exists, selected, select |
| Text | exists, free text, quotes, umlauts |
| Links | exists, title, href |
| ListItem | no text |
| Image | exists, not exists |

**Element Finding Strategy**:
- XPath-based: `HTMLElementIdentifiedByXPath` → `find_anywhere_in_curr_frame()`
- Frame-aware: `FrameIterator` handles nested iframes
- Search regions: below, to_right_of, above, to_left_of constraints
- Prefix matching: `PREFIX_IGNORE_CASE` for case-insensitive matching

**Key XPath Methods**:
- `ButtonImpl.get_xpath()` (lines 927-946) - Multiple selectors combined with `|`
- `TextImpl.get_xpath()` (lines 874-886) - Complex XPath for various text patterns
