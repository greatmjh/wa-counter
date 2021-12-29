# wa-counter
Counts the number of messages sent to each person or group and puts it in a spreadsheet file

## Requirements
- Python 3.9 or higher
- `xlsxwriter` (can be installed with `pip install --user xlsxwriter`

## How to use
### Getting the message files
1. On your phone, visit `wa.me/` followed by your phone number, including country code, but without the +. If it prompts you to open WhatsApp, open it. This will open a DM with your own phone number
2. Send a message, such as `.` to this thread, to save it
3. Go through all your chats, and for each one open it, tap the ... on the top right of the screen, tap 'More' and tap 'Export Chat'. Now choose your own phone number, that was added as a chat earlier
4. Open WhatsApp Web, go to your own chat, and download all the files named `WhatsApp Chat with <name>.txt` into a folder

### Creating an alias file
If you name your contacts differently to their actual names, and want your spreadsheet to contain their actual names, create a text file formatted like so:
```
Contact Name,Alias
Other Contact,Other Alias
```
Note the lack of space after the comma

### Creating a group file
If you want to separate DMs and groups in your spreadsheet, create a text file with all the names of the groups you are in, as they appear in their export files, like so:
```
Group
Other Group
```

### Using the script
Usage:
`python count.py [-y <year to exclusively look at (optional)>] [-a <path to optional alias file>] [-g <path to optional group list>] <path to directory with exported files>`
