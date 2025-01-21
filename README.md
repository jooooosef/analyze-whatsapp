# Analyze Whatsapp Logs

How to create a WhatsApp Chat Logfile:<br>
This is best done on the mobile device that you use primarily for WhatsApp. The desktop versions often have incomplete data since they dont fetch all of the old chats when opening. <br>
On IOS - when the chat is open - you tap on the top bar of the chat and scroll down. Almost at the bottom there is a 'Export chat' option. This will create a zip. <br>
On Andoid you need the press the 3 and open settings. There you can also choose a export chat option.<br>
You now have a .zip which contains a '_chat.txt' file. This is the log.<br>
<br>
Open `analyze_whatsapp.py` and insert your file_path. <br>
Only `analyze_specific_words` expects more than the filepath: a list of words to filter for and optionally a list of users to exclude. <br>
All other methods are run with doAll(). <br>