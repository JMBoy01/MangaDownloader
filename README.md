# Manga Downloader

## Works with manga4life url's

## How to use

Always run the ui file to properly start the program!
Download the chromium zip by clicking on this link: https://download-chromium.appspot.com/dl/Win_x64?type=snapshots
Unpack the "chrome-win" folder in the same folder as the python files are located.

### Downloading a single manga chapter

In URL field always use the url of a specific chapter, for example:
https://manga4life.com/read-online/{manga_name}-chapter-{chapter_number}.html
This is the typical url structure with the parameters between {} filled in accordingly.

The filename is directly taken and used as filename of the output pdf, for example:
"Manga Chapter 001" will give "Manga Chapter 001.pdf" as output.

### Downloading multiple manga chapters

You can download multiple chapters by clicking the checkbox and giving the start and end number of the chapters you want to download. Beware that when downloading multiple chapters the program will first collect all the data for downloading it, this causes the program to be unresponsive but it's still working in the background!

You can use the url of the chapter you want the download to start at.
In URL field always use the url of a specific chapter, for example:
https://manga4life.com/read-online/{manga_name}-chapter-{start_chapter_number}.html
This is the typical url structure with the parameters between {} filled in accordingly.

When downloading multiple chapters the chapter number of the current chapter will automatically be added at the end of the filename, for example when downloading chapter 1-10:
"Manga Chapter {chapter_number}" will give "Manga Chapter 1.pdf", "Manga Chapter 2.pdf", ..., "Manga Chapter 10.pdf" as output.
