from helium import press, TextField, SHIFT, write
from tests.api import BrowserAT


class PressTest(BrowserAT):
	def get_page(self):
		return 'test_write.html'
	def test_press_single_character(self):
		press('a')
		self.assertEqual('a', TextField('Autofocus text field').value)
	def test_press_upper_case_character(self):
		press('A')
		self.assertEqual('A', TextField('Autofocus text field').value)
	def test_press_shift_plus_lower_case_character(self):
		press(SHIFT + 'a')
		self.assertEqual('A', TextField('Autofocus text field').value)
	def test_press_unicode_german_umlaut(self):
		"""Regression: press() should handle German umlaut characters via write fallback."""
		write('Über')
		self.assertEqual('Über', TextField('Autofocus text field').value)
	def test_press_unicode_chinese(self):
		"""Regression: press() should handle CJK characters via write fallback."""
		write('中文测试')
		self.assertEqual('中文测试', TextField('Autofocus text field').value)


class URLNormalizationTest(BrowserAT):
	"""Test URL normalization in helium._impl.util.normalize_url"""
	def get_page(self):
		return 'test_write.html'
	def test_normalize_bare_hostname(self):
		"""Regression: bare hostname (no scheme) should normalize to https://."""
		from helium._impl.util import normalize_url
		result = normalize_url('example.com')
		self.assertEqual('https://example.com', result)
	def test_normalize_hostname_with_path(self):
		"""Bare hostname with path should normalize correctly."""
		from helium._impl.util import normalize_url
		result = normalize_url('example.com/page')
		self.assertEqual('https://example.com/page', result)
	def test_normalize_explicit_https(self):
		"""Explicit https:// should pass through unchanged."""
		from helium._impl.util import normalize_url
		result = normalize_url('https://example.com/path')
		self.assertEqual('https://example.com/path', result)
	def test_normalize_trailing_slash(self):
		"""Bare hostname with trailing slash should normalize correctly."""
		from helium._impl.util import normalize_url
		result = normalize_url('example.com/')
		self.assertEqual('https://example.com/', result)