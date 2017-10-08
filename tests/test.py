import sublime
import sys
from unittest import TestCase

class TestNegateSentence(TestCase):
  def setUp(self):
    self.view = sublime.active_window().new_file()
    # make sure we have a window to work with
    s = sublime.load_settings("Preferences.sublime-settings")
    s.set("close_windows_when_empty", False)

  def tearDown(self):
    if self.view:
      self.view.set_scratch(True)
      self.view.window().focus_view(self.view)
      self.view.window().run_command("close_file")

  def set_text(self, string):
    self.view.run_command("insert", {"characters": string})

  def get_text(self):
    return self.view.substr(self.view.line(self.view.text_point(0, 0)))

  def test_negate_is(self):
    self.check_substitution('"The dog is black"', '"The dog is not black"')

  def test_negate_isnt(self):
    self.check_substitution('"The dog isn\'t black"', '"The dog is black"')

  def test_negate_is_not(self):
    self.check_substitution('"The dog is not black"', '"The dog is black"')

  def test_negate_has_a(self):
    self.check_substitution('"A man has a face"', '"A man does not have a face"')

  def test_negate_has_an(self):
    self.check_substitution('"A man has an animal"', '"A man does not have an animal"')

  def test_negate_doesnt_have(self):
    self.check_substitution('"A man doesn\'t have an animal"', '"A man has an animal"')

  def test_negate_shouldnt(self):
    self.check_substitution('"It shouldn\'t be red"', '"It should be red"')

  def test_negate_should_not(self):
    self.check_substitution('"It should be red"', '"It should not be red"')

  def test_negate_should_not(self):
    self.check_substitution('"It should not be red"', '"It should be red"')

  def test_negate_does_not(self):
    self.check_substitution('"It does not require a name"', '"It requires a name"')

  def test_negate_does_not_do(self):
    self.check_substitution('"It does not do tricks"', '"It does tricks"')

  def test_negate_doesnt_verb(self):
    self.check_substitution('"It doesn\'t work"', '"It works"')

  def test_negate_does_not_verb(self):
    self.check_substitution('"It does not work"', '"It works"')

  def test_negate_verb(self):
    self.check_substitution('"It replaces first occurence"', '"It does not replace first occurence"')

  def test_negate_does(self):
    self.check_substitution('"It does tricks"', '"It does not do tricks"')

  def check_substitution(self, input, expected):
    self.set_text(input)
    self.view.run_command("negate_sentence")
    self.assertEqual(self.get_text(), expected)


