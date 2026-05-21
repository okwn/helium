# PR Backlog: Helium

## High Priority

### 1. Firefox Options Path Compatibility Fix
**File**: `helium/_impl/__init__.py:89`
**Current Code**:
```python
firefox_options.profile = profile
```
**Issue**: Direct attribute assignment may break with Selenium API changes
**Suggested Fix**:
```python
if hasattr(firefox_options, 'set_preference'):
    # New Selenium API path
    pass
else:
    firefox_options.profile = profile
```
**Tests Needed**: `test_firefox_options.py` with custom profile

### 2. Unicode press() Test Coverage
**File**: `tests/api/test_press.py`
**Gap**: No Unicode character tests

**Add Tests**:
```python
def test_press_unicode_character(self):
    press('ü')
    # verify in text field

def test_press_unicode_combination(self):
    press(SHIFT + 'ü')  # May produce 'Ü' depending on keyboard
```

## Medium Priority

### 3. LookupError Message Consistency
**Current**: Various element types have LookupError tests
**Gap**: `Window`, `Alert` not covered in `test_lookup_error_message.py`

**Add Tests**:
```python
def test_window_non_existent_error_message(self):
    self._check(lambda: switch_to("Non-existent"), "'Non-existent'")
```

### 4. Firefox-Specific Element Quirks
**Location**: `_impl/__init__.py:256-262`
```python
if offset == (0, 0) and driver.is_firefox():
    # Firefox button styling workaround
    offset = (1, 1)
```
**Issue**: Comment says buttons in Firefox "have an indent in the corners"
**Enhancement**: Add comment explaining when this triggers and why

### 5. Chrome Password Leak Detection Workaround
**Location**: `_impl/__init__.py:113-120`
**Issue**: Hardcoded Chrome version check
**Enhancement**: Add comment documenting when this can be removed

## Low Priority / Improvements

### 6. press() Documentation
**Issue**: `press()` docstring doesn't mention Unicode support explicitly
**Enhancement**: Add note:
```python
"""
Presses the given key or key combination. Supports Unicode characters
via send_keys().
"""
```

### 7. Element Lookup Performance
**Observation**: `FrameIterator` uses `sys.maxsize` loop for frame discovery
**Enhancement**: Consider caching frame structure

### 8. Missing Test for aria-label Matching
**Gap**: Button can be found by aria-label but no explicit test
**Add**: `test_button_aria_label` in `test_gui_elements.py`

## Test Data Files

### HTML Fixtures Location
`tests/api/data/`

| File | Purpose |
|------|---------|
| `test_gui_elements.html` | Main element lookup tests (12KB) |
| `test_write.html` | write() and press() tests |
| `test_click.html` | click() tests |
| `test_hover.html` | hover() tests |
| `test_point.html` | Point and coordinate tests |

### HTML Fixtures to Add
- `test_unicode.html` - Unicode input elements for press() tests
- `test_firefox_profile.html` - Firefox-specific styling tests
