# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import re
import libs.twitter as twitter
import libs.AccessTokenFactory as factory
import json


class TweetLineCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        self.settings = Settings()
        if not self.settings.settings['token_key']:
            self.view.window().run_command('input_pincode')
            return

        api = twitter.Api(
            consumer_key        = '1uFNM4QtiqRGB1ZQGKUY8g',
            consumer_secret     = 'BeCH5j8ZPmum357xEF9tvVf1VttVWY2E8hpcfk0',
            access_token_key    = self.settings.settings['token_key'],
            access_token_secret = self.settings.settings['token_secret'],
            input_encoding      = 'utf8'
        )

        first_region = self.view.sel()[0]
        # region_of_line = self.view.full_line(region)  # including line end
        region_of_line = self.view.line(first_region)
        line = self.view.substr(region_of_line)
        tweet_text = re.sub(r"^\s+", "", line)

        if sublime.ok_cancel_dialog("Tweet this?\n\n" + tweet_text, "Tweet"):
            tweet_text_utf8 = tweet_text.encode('utf8')
            try:
                api.PostUpdate(tweet_text_utf8)
                print "complete."
                sublime.status_message('tweet complete! "' + tweet_text + '"')
            except:
                print "error"
                sublime.status_message('tweet error :(')
        else:
            print "Cancel"


class InputPincodeCommand(sublime_plugin.WindowCommand):
    def __init__(self, window):
        self.window = window
        self.settings = Settings()

    def run(self):
        self.window.show_input_panel('input pincode:', '', self.on_input_pin, None, None)
        self.tokenFactory = factory.AccessTokenFactory()
        import webbrowser
        webbrowser.open(self.tokenFactory.getTempToken())

    def on_input_pin(self, text):
        try:
            pincode = int(text)
            keys = self.tokenFactory.getAccessToken(pincode)
        except ValueError:
            print 'Invalid pincode?, try again'
            return
        except:
            print 'Error, try again please'
            sublime.status_message('Error, try again please')
            return

        self.access_token_key, self.access_token_secret = keys
        self.settings.settings['token_key'] = self.access_token_key
        self.settings.settings['token_secret'] = self.access_token_secret
        self.settings.saveAll()
        sublime.status_message('You are authorized!')

class Settings:
    def __init__(self, filename='SublimeTweetLine.settings'):
        self.defaults = {
            'token_key': None,
            'token_secret': None,
        }
        self.filename = sublime.packages_path() + '/User/' + filename
        self.settings = self.loadAll()

    def loadAll(self):
        try:
            setting_json = open(self.filename).read()
            return json.loads(setting_json)
        except:
            return self.defaults

    def saveAll(self):
        try:
            with open(self.filename, 'w') as f:
                f.write(json.dumps(self.settings, sort_keys=True, indent=2))
        except:
            print 'save error'
