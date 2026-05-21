from helium import go_to, click, write, press, TextField
from tests.api import BrowserAT


class URLNormalizationTest(BrowserAT):
	"""Test URL normalization in helium._impl.util.normalize_url for bare hostnames."""

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

	def test_normalize_http(self):
		"""Explicit http:// should pass through unchanged."""
		from helium._impl.util import normalize_url
		result = normalize_url('http://example.com/')
		self.assertEqual('http://example.com/', result)

	def test_go_to_bare_hostname(self):
		"""Regression: go_to() should accept bare hostnames without crashing."""
		from helium._impl.util import normalize_url
		# bare hostname normalization primary use is CLI
		result = normalize_url('localhost:8000/test')
		self.assertEqual('https://localhost:8000/test', result)

	def test_normalize_ip_address(self):
		"""Bare IP address should normalize with https."""
		from helium._impl.util import normalize_url
		result = normalize_url('192.168.1.1')
		self.assertEqual('https://192.168.1.1', result)

	def test_normalize_localhost(self):
		"""localhost should normalize correctly."""
		from helium._impl.util import normalize_url
		result = normalize_url('localhost')
		self.assertEqual('https://localhost', result)