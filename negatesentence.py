import sublime
import sublime_plugin
import re

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

class NegateSentenceCommand(sublime_plugin.TextCommand):
  def description():
    "Negates a sentence (present simple only)"

  def run(self, edit):
    print("Running negate_sentence")
    self.cursor_position = self.view.sel()[0].begin()

    quote_start = self.find_quote_start()
    quote_end = self.find_quote_end()

    in_quotes = (quote_start and quote_end)

    word_region = sublime.Region(quote_start + 1, quote_end - 1) if in_quotes else sublime.Region(self.current_line_start(), self.current_line_end())

    input_sentence = self.string_at(word_region)

    negated_sentence = self.negate(input_sentence)

    self.view.replace(edit, word_region, negated_sentence)

  def negate(self, sentence):
    # is
    if sentence.find(" isn't ") > -1:
      return sentence.replace(" isn't ", " is ")

    if sentence.find(" is not ") > -1:
      return sentence.replace(" is not ", " is ")

    if sentence.find(" is ") > -1:
      return sentence.replace(" is ", " is not ")

    # has
    if sentence.find(" doesn't have ") > -1:
      return sentence.replace(" doesn't have ", " has ")

    if sentence.find(" has ") > -1:
      return sentence.replace(" has ", " does not have ")

    # should
    if sentence.find(" shouldn't ") > -1:
      return sentence.replace(" shouldn't ", " should ")

    if sentence.find(" should not ") > -1:
      return sentence.replace(" should not ", " should ")

    if sentence.find(" should ") > -1:
      return sentence.replace(" should ", " should not ")

    if sentence.find(" does not do ") > -1:
      return sentence.replace(" does not do ", " does ")

    # doesn't work -> works
    doesnt_regex = r'(doesn\'t|does not) (?P<verb>\w+)'

    if re.search(doesnt_regex, sentence):
      def replace_doesnt(matchobj):
        verb = matchobj.group(2)
        return "{0}s".format(verb)
      return re.sub(doesnt_regex, replace_doesnt, sentence, 1)

    if sentence.find(" does ") > -1:
      return sentence.replace(" does ", " does not do ")

    # works -> does not work
    def replace_verb(matchobj):
      subject = matchobj.group(1)
      verb = matchobj.group(2)
      whitespace = matchobj.group(3)
      return "{0}does not {1}{2}".format(subject, verb, whitespace)
    verb_regex = r'(It |it |)(?P<verb>\w+)s( |$)'
    if re.search(verb_regex, sentence):
      return re.sub(verb_regex, replace_verb, sentence, 1)

    return sentence

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
