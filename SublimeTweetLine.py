#import sublime
import sublime_plugin


class TweetLineCommand(sublime_plugin.TextCommand):
    # ^ + ` and view.run_command('tweet_line')
    def run(self, edit):
        for region in self.view.sel():
            # region_of_line = self.view.full_line(region)  # 改行を含む
            region_of_line = self.view.full_line(region)
            print self.view.substr(region_of_line)
