from helium import Config
from tests.api import BrowserAT


class ConfigReprTest(BrowserAT):
	def get_page(self):
		return 'test_gui_elements.html'
	def test_config_repr_default(self):
		"Config should show its default implicit_wait_secs value"
		self.assertEqual(
			'Config(implicit_wait_secs=10)', repr(Config)
		)
	def test_config_repr_modified(self):
		"Config should reflect modified implicit_wait_secs value"
		original = Config.implicit_wait_secs
		try:
			Config.implicit_wait_secs = 5
			self.assertEqual(
				'Config(implicit_wait_secs=5)', repr(Config)
			)
		finally:
			Config.implicit_wait_secs = original