import sublime, sublime_plugin

class TweetLineCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.insert(edit, 0, "TweetLine!")
