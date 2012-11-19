# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import re
import libs.twitter as twitter

# import json
# import thread
api = twitter.Api(
    consumer_key        = '1uFNM4QtiqRGB1ZQGKUY8g',
    consumer_secret     = 'BeCH5j8ZPmum357xEF9tvVf1VttVWY2E8hpcfk0',
    access_token_key    = 'YOUR_TOKEN_HERE',
    access_token_secret = 'YOUR_SECRET_HERE',
    input_encoding      = 'utf8'
)


class TweetLineCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        first_region = self.view.sel()[0]
        # region_of_line = self.view.full_line(region)  # including line end
        region_of_line = self.view.line(first_region)
        line = self.view.substr(region_of_line)
        tweet_text = re.sub(r"^\s+", "", line)

        if sublime.ok_cancel_dialog("Tweet this?\n\n" + tweet_text, "Tweet"):
            tweet_text = tweet_text.encode('utf8')
            api.PostUpdate(tweet_text)
            print "complete."
        else:
            print "Cancel"
