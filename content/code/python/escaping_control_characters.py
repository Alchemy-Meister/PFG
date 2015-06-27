def process_control_char_word_break(self, text):
      p = re.compile(ur'-\n', re.UNICODE)
      processed_text = re.sub(p, u'', text)
      processed_text = processed_text.replace('\\', '\\\\')
      processed_text = processed_text.replace('\n', ' ')
      processed_text = processed_text.replace('\"', '\\"')
      processed_text = processed_text.replace('\r', '')
      processed_text = processed_text.replace('\t', '')
      processed_text = processed_text.replace('\b', '')
      processed_text = processed_text.replace('\f', '')

      return processed_text