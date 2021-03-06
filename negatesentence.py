import sublime
import sublime_plugin
import re

class NegateSentenceCommand(sublime_plugin.TextCommand):
  def description():
    "Negates a 3rd person present simple sentence"

  def find_quotes(self):
    quotes_regex = r'(\".*?\"|((?<!\\)\'.*?(?<!\\)\'))'
    iterator = re.finditer(quotes_regex, self.current_line())
    for match in iterator:
      quote_span = match.span()
      quote_span = (quote_span[0] + self.current_line_start(), quote_span[1] + self.current_line_start())
      if self.cursor_position >= quote_span[0] and self.cursor_position <= quote_span[1]:
        return (quote_span[0], quote_span[1])

  def run(self, edit):
    print("Running negate_sentence")
    self.cursor_position = self.view.sel()[0].begin()

    quote_range = self.find_quotes()
    print(quote_range)
    if not quote_range:
      show_message("No quotes found")
      return

    sentence_region = sublime.Region(quote_range[0] + 1, quote_range[1] - 1)

    input_sentence = self.string_at(sentence_region)

    negated_sentence = self.negate(input_sentence)

    self.view.replace(edit, sentence_region, negated_sentence)

  def negate(self, sentence):
    return SentenceNegator().negate(sentence)

  def current_line(self):
    return self.string_at(self.view.line(self.cursor_position))

  def current_line_start(self):
    return self.view.line(self.cursor_position).begin()

  def string_at(self, region):
    return self.view.substr(region)

class SentenceNegator:
  IRREGULAR_ES_VERB_ENDINGS = ["ss", "x", "ch", "sh", "o"]

  def negate(self, sentence):
    print("Negating sentence: {0}".format(sentence))
    # is
    if sentence.find("isn't") > -1:
      return sentence.replace("isn't", "is")

    if sentence.find("isn\\'t") > -1:
      return sentence.replace("isn\\'t", "is")

    if sentence.find("is not ") > -1:
      return sentence.replace("is not ", "is ")

    if sentence.find("is ") > -1:
      return sentence.replace("is ", "is not ")

    # has
    if sentence.find("does not have") > -1:
      return sentence.replace("does not have", "has")

    if sentence.find("doesn't have") > -1:
      return sentence.replace("doesn't have", "has")

    if sentence.find("doesn\\'t have") > -1:
      return sentence.replace("doesn\\'t have", "has")

    if sentence.find("has ") > -1:
      return sentence.replace("has ", "does not have ")

    # should
    if sentence.find("shouldn't") > -1:
      return sentence.replace("shouldn't", "should")

    if sentence.find("shouldn\\'t") > -1:
      return sentence.replace("shouldn\\'t", "should")

    if sentence.find("should not") > -1:
      return sentence.replace("should not", "should")

    if sentence.find("should") > -1:
      return sentence.replace("should", "should not")

    # must
    if sentence.find("mustn't") > -1:
      return sentence.replace("mustn't", "must")

    if sentence.find("mustn\\'t") > -1:
      return sentence.replace("mustn\\'t", "must")

    if sentence.find("must not") > -1:
      return sentence.replace("must not", "must")

    if sentence.find("must ") > -1:
      return sentence.replace("must ", "must not ")

    # can
    if sentence.find("can't") > -1:
      return sentence.replace("can't", "can")

    if sentence.find("can\\'t") > -1:
      return sentence.replace("can\\'t", "can")

    if sentence.find("cannot") > -1:
      return sentence.replace("cannot", "can")

    if sentence.find("can ") > -1:
      return sentence.replace("can ", "cannot ")

    # doesn't work -> works
    doesnt_regex = r'(doesn\'t|doesn\\\'t|does not) (?P<verb>\w+)'

    if re.search(doesnt_regex, sentence):
      def replace_doesnt(matchobj):
        verb = matchobj.group(2)

        if verb.endswith("y") and self.__is_consonant(verb[-2]):
          return "{0}ies".format(verb[0:-1])

        for ending in self.IRREGULAR_ES_VERB_ENDINGS:
          if verb.endswith(ending):
            return "{0}es".format(verb)

        return "{0}s".format(verb)

      return re.sub(doesnt_regex, replace_doesnt, sentence, 1)

    verb_regex = r'(It |it |)(?P<verb>\w+)s( |$)'

    # works -> does not work
    def replace_verb(matchobj):
      subject = matchobj.group(1)
      verb = matchobj.group(2)
      whitespace = matchobj.group(3)

      # flies -> fly, but not die -> dy
      if verb.endswith("ie") and len(verb) > 3:
        verb = "{0}y".format(verb[0:-2])

      # stresses -> stress
      for ending in self.IRREGULAR_ES_VERB_ENDINGS:
        if verb.endswith("{0}e".format(ending)):
          verb = verb[0:-1]

      return "{0}does not {1}{2}".format(subject, verb, whitespace)

    if re.search(verb_regex, sentence):
      return re.sub(verb_regex, replace_verb, sentence, 1)

    show_message("No sentence to negate")

    return sentence

  def __is_consonant(self, letter):
    return letter not in ['a', 'e', 'i', 'o', 'u', 'y']

def show_message(message):
  print(message)
  sublime.active_window().status_message("NegateSentence: {0}".format(message))
