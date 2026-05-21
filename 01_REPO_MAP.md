# Helium Repository Map

## Overview
**helium** (`mherrmann/helium`) is a Python browser automation library that wraps Selenium. Version 7.0.1, requires Python 3.5+ and selenium>=4.16.0.

## Directory Structure

```
helium/
├── helium/                         # Main package
│   ├── __init__.py                 # Public API (1166 lines)
│   └── _impl/                      # Implementation details
│       ├── __init__.py             # APIImpl, GUIElementImpl, element implementations (~1317 lines)
│       ├── selenium_wrappers.py    # WebDriverWrapper, WebElementWrapper, FrameIterator
│       ├── match_type.py           # PREFIX_IGNORE_CASE and matching logic
│       └── util/                   # Utility modules
│           ├── geom.py             # Rectangle, geometry
│           ├── xpath.py            # XPath predicates and helpers
│           ├── html.py             # HTML snippet helpers
│           ├── path.py             # Path utilities
│           ├── dictionary.py        # Dictionary inverse()
│           ├── system.py           # is_windows(), get_canonical_os_name()
│           ├── lang.py              # Language utilities (TemporaryAttrValue)
│           └── inspect_.py          # repr_args
├── tests/
│   ├── api/                        # Browser automation tests (BrowserAT base class)
│   │   ├── test_gui_elements.py    # Element lookup tests
│   │   ├── test_lookup_error_message.py  # LookupError message tests
│   │   ├── test_press.py           # press() tests
│   │   ├── test_click.py           # click() tests
│   │   ├── test_write.py           # write() tests
│   │   └── data/                   # HTML test fixtures
│   └── unit/                       # Unit tests
├── docs/                           # Documentation
├── requirements/                   # Requirements files
└── setup.py                        # Package setup
```

## Key Files

### Public API (`helium/__init__.py`)
- `start_chrome()`, `start_firefox()` - Browser startup
- `go_to()`, `write()`, `press()` - Navigation and input
- `click()`, `doubleclick()`, `hover()`, `rightclick()` - Mouse actions
- `find_all()` - Find multiple elements
- `wait_until()` - Explicit waits
- `Config` - Runtime configuration (implicit_wait_secs)
- Key classes: `Button`, `TextField`, `ComboBox`, `CheckBox`, `RadioButton`, `Text`, `Link`, `Image`, `ListItem`

### Implementation (`helium/_impl/__init__.py`)
- `APIImpl` - Main implementation class (lines 67-426)
- `GUIElementImpl` - Base for element implementations (lines 630+)
- Element implementations: `ButtonImpl`, `TextImpl`, `LinkImpl`, `ComboBoxImpl`, etc.

### Selenium Wrappers (`helium/_impl/selenium_wrappers.py`)
- `WebDriverWrapper` - Wraps Selenium WebDriver, adds `is_firefox()`, `is_ie()`
- `WebElementWrapper` - Wraps WebElement with frame handling
- `FrameIterator` - Iterates through iframe hierarchy
- `FramesChangedWhileIterating` - Exception for frame changes

## Selenium Integration Points

| Selenium Component | Location | Usage |
|--------------------|----------|-------|
| Chrome/ChromeOptions | `_impl/__init__.py:18` | `start_chrome_impl()` |
| Firefox/FirefoxOptions | `_impl/__init__.py:18` | `start_firefox_impl()` |
| ServiceFirefox | `_impl/__init__.py:14` | geckodriver service |
| WebDriverWait | `_impl/__init__.py:16` | `wait_until_impl()` |
| Select | `_impl/__init__.py:17` | `select_impl()` |
| ActionChains | selenium_wrappers.py:4 | Mouse actions |
| By (XPATH, etc) | `_impl/__init__.py:13` | Element finding |
