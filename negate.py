import sublime
import sublime_plugin

'''
Examples:
"it does not do stuff" -> "it does stuff"
`it does not do ${stuff}` -> `it does ${stuff}`
"it should do stuff" -> "it shouldn't do stuff"
"it has a name" -> "it does not have a name"
"it shouldn't do stuff" -> "it should do stuff"
'it should do stuff' -> 'it should not do stuff'
'it shouldn\'t do stuff' -> 'it should do stuff'
"They do stuff" -> "They don't do stuff"
'''

'''
Basic flow:
1. Find beginning of current quote. If no quote take whole line (?).
2. Find a subject and verb. If quoted string is not a sentence - quit.
3. Negate the verb taking subject's plurality into account.
4. If single quotes -> use long negation (does not) else use short (doesn't).
'''

'''
Advanded usage:
- [ ] Negate in selection
- [ ] Use with multiple selections
'''

class NegateCommand(sublime_plugin.TextCommand):
  def description():
    "Negates a sentence (present simple only)"

  def run(self, edit):
    self.cursor_position = self.view.sel()[0].begin()

    quote_start = self.find_quote_start()
    quote_end = self.find_quote_end()

    self.in_quotes = (quote_start is not None and quote_end is not None)

    self.word_region = sublime.Region(quote_start + 1, quote_end - 1) if self.in_quotes else sublime.Region(self.current_line_start(), self.current_line_end())

    print(self.string_at(self.word_region))

  def find_quote_start(self):
    current_line_start = self.current_line_start()
    i = self.cursor_position
    while i >= current_line_start:
      if self.char_at(i) == '"':
        return i
      i = i-1

    return None

  def find_quote_end(self):
    current_line_end = self.current_line_end()
    i = self.cursor_position
    while i <= current_line_end:
      if self.char_at(i) == '"':
        return i
      i = i+1

    return None

  def current_line_start(self):
    return self.view.line(self.cursor_position).begin()

  def current_line_end(self):
    return self.view.line(self.cursor_position).end()

  def char_at(self, cursor_position):
    return self.view.substr(cursor_position)

  def string_at(self, region):
    return self.view.substr(region)
