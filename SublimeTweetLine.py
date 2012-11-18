import sublime
import sublime_plugin
import re


class TweetLineCommand(sublime_plugin.TextCommand):
    # ^ + ` and view.run_command('tweet_line')
    def run(self, edit):
        first_region = self.view.sel()[0]
        # region_of_line = self.view.full_line(region)  # including line end
        region_of_line = self.view.line(first_region)
        line = self.view.substr(region_of_line)
        tweet_string = re.sub(r"^\s+", "", line)
        if sublime.ok_cancel_dialog("Tweet this?\n\n" + tweet_string, "Tweet"):
            print line
        else:
            print "Cancel"
