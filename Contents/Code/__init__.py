# This agent populates metadata from a text file.
#
# Typically cast data is already populated from sites such as IMDb, The Movie Database, The TV Db, etc.. This is fine for
# commercial films or TV shows. In the case of home videos, this obviously will not work, as there is no entry for your
# videos on these sites. You also wouldn't want to add an entry for them on these sites. For home videos, you may want to include
# your family members as "Cast Members" (thus allowing you to click on their names in the UI to see a filtered view of all
# other home movies they're in.) This currently cannot be done through the Plex metadata editor. The inability to edit cast data
# directly is the main motivation behind this Agent. Like the initial post in this thread to vote for this functionality to
# be added: https://forums.plex.tv/discussion/comment/1333388
#
# This Agent was based off of ZeroQI's starter template, found here: https://github.com/ZeroQI/Hama.bundle/releases
#
# Some code was taken from a reply provided by agentplex007 in https://forums.plex.tv/discussion/comment/901785#Comment_901785

import re
import os
from datetime import datetime

def Start():
  HTTP.CacheTime             = CACHE_1DAY
  HTTP.Headers['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)'

class TextFileMetadataAgent(Agent.Movies):
  TITLE_KEY = "TITLE"
  CAST_KEY = "CAST"
  DESCRIPTION_KEY = "DESCRIPTION"
  STUDIO_KEY = "STUDIO"
  COLLECTION_KEY = "TAGS"
  DATE_KEY = "DATE"

  name = 'Text File Metadata Agent'
  primary_provider = False
  accepts_from = ['com.plexapp.agents.localmedia']
  
  @staticmethod
  def parseFile(file_contents):
    '''
    Parses the file into a map
    '''
    file_metadata={}
    for line in file_contents:
      k, v = line.split('=')
      file_metadata[k.strip()] = v.strip()
    Log("file_metadata: '%s'" % (file_metadata))
    return file_metadata
  
  # This method was grabbed from https://forums.plex.tv/discussion/comment/901785#Comment_901785 . Thanks @agentplex007!
  @staticmethod
  def readFile(filename):    
    '''Read a file and return its content
    This is used when running under Agent as open() is not available for use.
    @param filename  file to read
    @return          file content or None
    '''
    size = os.path.getsize(filename)
    fd = os.open(filename, os.O_RDONLY)
    data = os.read(fd, size)
    os.close(fd)
    return data

  def processCast(self, metadata, cast):
    '''
    Sets the cast
    '''
    if (cast == None) or (cast.strip() == ''):
      return

    metadata.roles.clear()
    castmembers = cast.split(', ')
    for c in castmembers:
      c_stripped = c.strip()
      if (c_stripped != ''):
        metadata.roles.new().name = c_stripped
        Log("cast member: '%s'" % (c_stripped))

  def processDescription(self, metadata, description):
    '''
    Sets the description
    '''
    if (description == None) or (description.strip() == ''):
      return
    metadata.summary=description
    Log("description: '%s'" % (description))

  def processDate(self, metadata, date):
    '''
    Sets the originally available at date
    '''
    if (date == None) or (re.match("^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}$", date.strip()) is None):
      return
    d = datetime.strptime(date.strip(), '%Y-%m-%d')
    metadata.originally_available_at = d
    Log("originally available at: '%s'" % (d))

  def processTitle(self, metadata, title):
    '''
    Sets the title
    '''
    if (title == None) or (title.strip() == ''):
      return
    title_stripped = title.strip()
    metadata.title=title_stripped
    Log("title: '%s'" % (title_stripped))

  def processStudio(self, metadata, studio):
    '''
    Sets the studio
    '''
    if (studio == None) or (studio.strip() == ''):
      return
    metadata.studio = studio
    Log("studio: '%s'" % (studio))

  def processCollection(self, metadata, collection):
    '''
    Sets the collection (tags)
    '''
    if (collection == None) or (collection.strip() == ''):
      return

    metadata.collections.clear()
    tags = collection.split('|')
    for t in tags:
      t_stripped = t.strip()
      if (t_stripped != ''):
        metadata.collections.add(t_stripped)
        Log("tag: '%s'" % t_stripped)

  def search(self, results, media, lang, manual=True):
    results.Append(MetadataSearchResult(id = 'null', score = 100))

  def update(self, metadata, media, lang, force=True):
    file_components=os.path.split(media.items[0].parts[0].file)
    filename=file_components[1]
    path=file_components[0]    
    txtfile=path+"/"+filename+".txt"

    if (os.path.isfile(txtfile)):
      Log("filenames: '%s', '%s'" % (filename, txtfile))

      metamap = TextFileMetadataAgent.parseFile(TextFileMetadataAgent.readFile(txtfile).splitlines())

      self.processCast(metadata, metamap.get(self.CAST_KEY))
      self.processDescription(metadata, metamap.get(self.DESCRIPTION_KEY))
      self.processStudio(metadata, metamap.get(self.STUDIO_KEY))
      self.processTitle(metadata, metamap.get(self.TITLE_KEY))
      self.processCollection(metadata, metamap.get(self.COLLECTION_KEY))
      self.processDate(metadata, metamap.get(self.DATE_KEY))
      