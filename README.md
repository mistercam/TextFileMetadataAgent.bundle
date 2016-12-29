Text File Meta Data Agent
=========================
This agent populate certain metadata fields with data provided in a text file.

Typically cast data is already populated from sites such as IMDb, The Movie Database, The TV Db, etc.. This is fine for commercial films or TV shows. In the case of home videos, this obviously will not work, as there is no entry for your videos on these sites. You also wouldn't want to add an entry for them on these sites. For home videos, you may want to include your family members as "Cast Members" (thus allowing you to click on their names in the UI to see a filtered view of all other home movies they're in.) This currently cannot be done through the Plex metadata editor. The inability to edit cast data directly is the main motivation behind this Agent. 'Like' the initial post in this thread to vote for this functionality to be added: https://forums.plex.tv/discussion/comment/1333388

This agent is designed to work with the Personal Media Movies agent.

1. Take the video file you want to create metadata for. E.g. KidsChristmasPlay2015.mp4
2. Create a text file: KidsChristmasPlay2015.mp4.txt and place it in the same directory as the movie.

Here is a fully-formed example of a text file. You only have to specify those lines you're interested in.

CAST=Sally, Bob, Eric, Lizzie
DESCRIPTION=The annual family 2015 Christmas play put on by the kids.
STUDIO=The Johnson Family

Each line must end with a line break (new line.) There must be no other new lines in the file.