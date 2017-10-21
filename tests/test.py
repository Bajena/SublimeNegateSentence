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

  def move_cursor(self, position):
    pt = self.view.text_point(0, position)

    self.view.sel().clear()
    self.view.sel().add(sublime.Region(pt))

  def test_negate_is(self):
    self.check_substitution('"The dog is black"', '"The dog is not black"')

  def test_negate_isnt(self):
    self.check_substitution('"The dog isn\'t black"', '"The dog is black"')

  def test_negate_isnt_backslash(self):
    self.check_substitution("'The dog isn\\'t black'", "'The dog is black'")

  def test_negate_is_not(self):
    self.check_substitution('"The dog is not black"', '"The dog is black"')

  def test_negate_has_a(self):
    self.check_substitution('"A man has a face"', '"A man does not have a face"')

  def test_negate_has_an(self):
    self.check_substitution('"A man has an animal"', '"A man does not have an animal"')

  def test_negate_has_to(self):
    self.check_substitution('"has to be here"', '"does not have to be here"')

  def test_negate_doesnt_have_to(self):
    self.check_substitution('"A man does not have to be here"', '"A man has to be here"')

  def test_negate_doesnt_have(self):
    self.check_substitution('"A man doesn\'t have an animal"', '"A man has an animal"')

  def test_negate_doesnt_have_backslash(self):
    self.check_substitution("'A man doesn\\'t have an animal'", "'A man has an animal'")

  def test_negate_does_not_have(self):
    self.check_substitution('"A man does not have an animal"', '"A man has an animal"')

  def test_negate_shouldnt(self):
    self.check_substitution('"It shouldn\'t be red"', '"It should be red"')

  def test_negate_shouldnt_backslash(self):
    self.check_substitution("'It shouldn\\'t be red'", "'It should be red'")

  def test_negate_should_not(self):
    self.check_substitution('"It should not be red"', '"It should be red"')

  def test_negate_should(self):
    self.check_substitution('"It should be red"', '"It should not be red"')

  def test_negate_mustnt(self):
    self.check_substitution('"It mustn\'t be a snake"', '"It must be a snake"')

  def test_negate_mustnt_backslash(self):
    self.check_substitution("'It mustn\\'t be a snake'", "'It must be a snake'")

  def test_negate_must(self):
    self.check_substitution('"It must be a snake"', '"It must not be a snake"')

  def test_negate_must_not(self):
    self.check_substitution('"It must not be a snake"', '"It must be a snake"')

  def test_negate_cant(self):
    self.check_substitution('"It can\'t be true"', '"It can be true"')

  def test_negate_cant_backslash(self):
    self.check_substitution("'It can\\'t be true'", "'It can be true'")

  def test_negate_cannot(self):
    self.check_substitution('"It cannot be true"', '"It can be true"')

  def test_negate_can(self):
    self.check_substitution('"It can be a snake"', '"It cannot be a snake"')

  def test_negate_does_not(self):
    self.check_substitution('"It does not require a name"', '"It requires a name"')

  def test_negate_does_not_do(self):
    self.check_substitution('"It does not do tricks"', '"It does tricks"')

  def test_negate_doesnt_verb(self):
    self.check_substitution('"It doesn\'t work"', '"It works"')

  def test_negate_doesnt_verb_backslash(self):
    self.check_substitution("'It doesn\\'t work'", "'It works'")

  def test_negate_does_not_verb(self):
    self.check_substitution('"It does not work"', '"It works"')

  def test_negate_verb(self):
    self.check_substitution('"It replaces first occurence"', '"It does not replace first occurence"')

  # irregulars
  def test_negate_flies(self):
    self.check_substitution('"It flies"', '"It does not fly"')

  def test_negate_dies(self):
    self.check_substitution('"It dies"', '"It does not die"')

  def test_negate_kisses(self):
    self.check_substitution('"It kisses"', '"It does not kiss"')

  def test_negate_does(self):
    self.check_substitution('"It does tricks"', '"It does not do tricks"')

  def test_negate_does_not_fly(self):
    self.check_substitution('"It does not fly"', '"It flies"')

  def test_negate_does_not_die(self):
    self.check_substitution('"It does not die"', '"It dies"')

  def test_negate_does_not_kiss(self):
    self.check_substitution('"It does not kiss"', '"It kisses"')

  def test_negate_does_not_do(self):
    self.check_substitution('"It does not do"', '"It does"')

  # proper quote detection
  def test_no_replacement(self):
    self.check_substitution('"Notasentence"', '"Notasentence"')

  def test_no_quotes(self):
    self.check_substitution('It is not a quoted sentence', 'It is not a quoted sentence')

  def test_cursor_before_start_quote_substitute(self):
    self.check_substitution('"It does tricks"', '"It does not do tricks"', 0)

  def test_cursor_after_first_quote_substitute(self):
    self.check_substitution('"It does tricks"', '"It does not do tricks"', 1)

  def test_cursor_before_last_quote_substitute(self):
    self.check_substitution('"It does tricks"', '"It does not do tricks"', 15)

  def test_cursor_after_end_quote_substitute(self):
    self.check_substitution('"It does tricks"    ', '"It does not do tricks"    ', 16)

  def test_cursor_much_after_end_quote_no_substitute(self):
    self.check_substitution('"It does tricks"    ', '"It does tricks"    ', 17)

  def check_substitution(self, input, expected, cursor_position = 0):
    self.set_text(input)
    self.move_cursor(cursor_position)
    self.view.run_command("negate_sentence")
    self.assertEqual(self.get_text(), expected)


