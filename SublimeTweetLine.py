#import sublime
import sublime_plugin


class TweetLineCommand(sublime_plugin.TextCommand):
    # ^ + ` and view.run_command('tweet_line')
    def run(self, edit):
        self.view.insert(edit, 0, "TweetLine!")
