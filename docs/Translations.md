# Translations in Elite Dangerous Market Connector

Translations are handled on [OneSky](https://oneskyapp.com/), specifically in [this project](https://marginal.oneskyapp.com/collaboration/project/52710).

---

## Adding A New Phrase

### Setting it up in the code

#### Call `tr.tl(...)`
If you add any new strings that appear in the application UI, e.g. new configuration options, then you should specify them as:

	tr.tl('Text that appears in UI')

In order to do this, you must add the following import: 

`from l10n import translations as tr`

`tr.tl()` is a function that then handles the translation, using its single argument, plus the configured language, to look up the appropriate text. 

If you need to specify something in the text that shouldn't be translated then use the form:

	tr.tl('Some text with a {WORD} not translated').format(WORD='word')
This way 'word' will always be used literally.

#### Add a LANG comment

Sometimes our translators may need some additional information about what a
translation is used for. You can add that information automatically by using
`# LANG: your message here` **on the line directly above your usage, or at the
end of the line in your usage**. If both comments exist, the one on the
current line is preferred over the one above

```py
from l10n import translations as tr
# LANG: this says stuff.
tr.tl('stuff')
```

#### Edit `L10n/en.template` to add the phrase

##### Hint: It is strongly recommended to use the `find_localized_strings.py` script to help automate this process!
	/* <use of this phrase> [<file it was first added in>] */
	"<text as it appears in the code>" = "<English version of the text>";
e.g.

	/* Successfully authenticated with the Frontier website. [EDMarketConnector.py] */
	"Authentication successful" = "Authentication successful";
which matches with:

	self.status['text'] = tr.tl('Authentication successful')    # Successfully authenticated with the Frontier website

and

	/* Help text in settings. [prefs.py] */
	"Tip: You can disable a plugin by{CR}adding '{EXT}' to its folder name" = "Tip: You can disable a plugin by{CR}adding '{EXT}' to its folder name";
which matches with:

	nb.Label(plugsframe, text=tr.tl("Tip: You can disable a plugin by{CR}adding '{EXT}' to its folder name").format(EXT='.disabled')).grid(     # Help text in settings
`{CR}` is handled in `l10n.py`, translating to a unicode `\n`.  See the code in`l10n.py` for any other such special substitutions.

You can even use other translations within a given string, e.g.:

	tr.tl("One or more of your enabled plugins do not yet have support for Python 3.x. Please see the list on the '{PLUGINS}' tab of '{FILE}' > '{SETTINGS}'. You should check if there is an updated version available, else alert the developer that they need to update the code for Python 3.x.\r\n\r\nYou can disable a plugin by renaming its folder to have '{DISABLED}' on the end of the name.".format(PLUGINS=tr.tl('Plugins'), FILE=tr.tl('File'), SETTINGS=tr.tl('Settings'), DISABLED='.disabled'))
	/* Popup body: Warning about plugins without Python 3.x support [EDMarketConnector.py] */
"One or more of your enabled plugins do not yet have support for Python 3.x. Please see the list on the '{PLUGINS}' tab of '{FILE}' > '{SETTINGS}'. You should check if there is an updated version available, else alert the developer that they need to update the code for Python 3.x.\r\n\r\nYou can disable a plugin by renaming its folder to have '{DISABLED}' on the end of the name." = "One or more of your enabled plugins do not yet have support for Python 3.x. Please see the list on the '{PLUGINS}' tab of '{FILE}' > '{SETTINGS}'. You should check if there is an updated version available, else alert the developer that they need to update the code for Python 3.x.\r\n\r\nYou can disable a plugin by renaming its folder to have '{DISABLED}' on the end of the name.";

## Adding it to the OneSky project

You will, of course, need admin access to the project.  Jonathan Harris (aka Maringal, aka Otis) still handles this.  Check for this email address in github commits if you need to get in touch.

1. Copy `L10n/en.template` to `en.strings` somewhere.  It needs to be this name for OneSky to accept it as an upload.
1. In [the project](https://marginal.oneskyapp.com/admin/page/list/project/52710) click the `+` next to "Files"
	1. Select the copied `en.strings` file.
	1. **Make sure that you select "Deprecate" for the "Do you want to deprecate phrases uploaded before but not in this batch? " option.**
	1. Click the "Import files now" button.
1. Check that the new phrases are listed properly on [the phrases list](https://marginal.oneskyapp.com/admin/phrase/list/project/52710).  Use the search dialogue on the 'code text' to find them.

All project admins will get a notification of the new upload.  Now you wait for translators to work on the new/changed phrases.

---

## Updating Translations In The Code

Once you have new/changed translations on OneSky you'll want to update the code to use them.

1. Navigate to the [Translation Overview](https://marginal.oneskyapp.com/admin/project/dashboard/project/52710) then click on "Download Translation" which should bring you to [Download](https://marginal.oneskyapp.com/admin/export/phrases/project/52710).
1. In "File format" select ".strings (iOS/MacOS)".
1. "All languages" should already be selected in the "Languages filter".  If not, select it.
1. Likewise "All files" should already be selected in "File Filter".
1. Click "Export".  After a short delay you should be offered a file "EDMarketConnector.zip" for download.
1. Access the contents of this zip file, extracting *all* the files into `L10n/` in the code.
1. Rename the "en.strings" file to "en.template".
1. Commit the changes to git.

---

## Adding a New Language

To add a new language to the app:

1. Add it to the OneSkyApp project:
    1. open [EDMarketConnector - Miscellaneous Manage Languages](https://marginal.oneskyapp.com/admin/project/languages/project/52710)
    1. Search for the language.
    1. Ensure you have the correct one if there are variants.
    1. Click the `+` on the right hand side to add the language.
    1. Be sure to go through and Finalize any phrases that shouldn't be translated.  See [Translations]() in the Wiki.

    Remember that until there are translations all strings will default to the English version (actually the key, which is always specified in English).
