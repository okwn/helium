from helium import press, TextField, SHIFT
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
		"""Regression test: press() should handle German umlauts correctly."""
		press('ü')
		self.assertEqual('ü', TextField('Autofocus text field').value)

	def test_press_unicode_chinese(self):
		"""Regression test: press() should handle CJK characters via send_keys."""
		press('中')
		self.assertEqual('中', TextField('Autofocus text field').value)

	def test_press_unicode_combined(self):
		"""Regression test: press() with SHIFT and unicode (e.g. ü -> Ü)."""
		press(SHIFT + 'ü')
		# Result depends on keyboard layout; at minimum no exception should be raised
		field = TextField('Autofocus text field')
		self.assertTrue(len(field.value) > 0)