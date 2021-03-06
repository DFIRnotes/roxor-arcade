#Binary Scavenger Hunt
#A game developed by Xeno Kovah for the class "The Life of Binaries"
#(my first largish program written in python. be kind. rewind)
# This game is meant to reinforce the materials covered in the class
# by giving them hands-on experience using tools to determine
# particular attributes of PE binaries
#Class material and videos available at:
#http://OpenSecurityTraining.info/LifeOfBinaries.html
#This game licensed Creative Commons, Share-Alike w/ Attribution
#http://creativecommons.org/licenses/by-sa/3.0/
# Special thanks to Ero Carrera for creating the pefile python library,
# without which, making this game would have taken much longer

#This is Round 3 and will cover questions on the IMAGE_SECTION_HEADER
#and about the sections in the binary

import os
import random
import pefile
from time import time
from rounds.helpers import CheckAnswerNum, CheckAnswerString, RandomizeSectionNames
import rounds.helpers

#This function asks questions about the basic field values in IMAGE_SECTION_HEADER
#but asks it for a random section, after randomizing their names
#This shows that the naming conventions have no actual bearing on the execution
def R3Q0(questionCounter):
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR3
  Qs = ["What is the value of IMAGE_SECTION_HEADER.VirtualAddress?",
        "What is the RVA this section will be loaded at?",
        "What is the VA this section will be loaded at?",
        "What is the value of IMAGE_SECTION_HEADER.Misc.VirtualSize?",
        "How much virtual memory will this section occupy?",
        "What is the RVA of the first byte of memory after this section?",
        "What is the VA of the first byte of memory after this section?",
        "What is the value of IMAGE_SECTION_HEADER.PointerToRawData?",
        "How far into the file on disk is the data for this section?",
        "What is the file offset for this section's data?",
        "What is the value of IMAGE_SECTION_HEADER.SizeOfRawData?",
        "How much space does this section's data occupy on disk?",
        "What is the file offset for the first byte of data after this section?"]
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR3

  x = random.randint(0,3)
  if x == 0:
    pe = pefile.PE('../template32.exe')
    suffix = ".exe"
  elif x == 1:
    pe = pefile.PE('../template64.exe')
    suffix = ".exe"
  elif x == 2:
    pe = pefile.PE('../template32.dll')
    suffix = ".dll"
  else:
    pe = pefile.PE('../template64.dll')
    suffix = ".dll"

  RandomizeSectionNames(pe)
  
  #FIXME: what's the more graceful way of doing this?
  error = 1
  while error:
    try:
      #write out the modified file
      outFileName = "Round3Q" + str(questionCounter) + suffix
      pe.write(filename=outFileName)
      error = 0
    except IOError:
      questionCounter+=1
  
  #pick a random section
  randSectIndex = random.randint(0,len(pe.sections)-1)
  #Print the question
  q = random.randint(0,len(Qs)-1)
  print "For binary R3Bins/%s..." % outFileName
  print "For section '%s'..." % pe.sections[randSectIndex].Name
  print Qs[q]
  answer = raw_input("Answer: ")

  if q == 0 or q == 1:
    CheckAnswerNum(answer, pe.sections[randSectIndex].VirtualAddress)
  if q == 2:
    CheckAnswerNum(answer, pe.OPTIONAL_HEADER.ImageBase + pe.sections[randSectIndex].VirtualAddress)
  if q == 3 or q == 4:
    CheckAnswerNum(answer, pe.sections[randSectIndex].Misc_VirtualSize)
  if q == 5:
    CheckAnswerNum(answer, (pe.sections[randSectIndex].VirtualAddress + pe.sections[randSectIndex].Misc_VirtualSize))
  if q == 6:
    CheckAnswerNum(answer, (pe.OPTIONAL_HEADER.ImageBase + pe.sections[randSectIndex].VirtualAddress + pe.sections[randSectIndex].Misc_VirtualSize))
  if q == 7 or q == 8 or q == 9:
    CheckAnswerNum(answer, pe.sections[randSectIndex].PointerToRawData)
  if q == 10 or q == 11:
    CheckAnswerNum(answer, pe.sections[randSectIndex].SizeOfRawData)
  if q == 12:
    CheckAnswerNum(answer, (pe.sections[randSectIndex].PointerToRawData + pe.sections[randSectIndex].SizeOfRawData))    

#This function asks questions about IMAGE_SECTION_HEADER.Characteristics
def R3Q1(questionCounter):
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR3
  Qs = ["What is the value for this section's Characteristics?",
        "How many flags are set in the Characteristics?",
        "Does this section have the IMAGE_SCN_CTN_CODE characteristic set? (Y or N)",
        "Does this section contain code? (Y or N)",
        "Does this section have the IMAGE_SCN_CNT_INITIALIZED_DATA characteristic set? (Y or N)",
        "Does this section contain initialized data? (Y or N)",
        "Does this section have the IMAGE_SCN_CNT_UNINITIALIZED_DATA characteristic set? (Y or N)",
        "Does this section contain uninitialized data? (Y or N)",
        "Does this section have the IMAGE_SCN_MEM_NOT_CACHED characteristic set? (Y or N)",
        "Should this section not be cached? (Y or N)",
        "Does this section have the IMAGE_SCN_MEM_NOT_PAGED characteristic set? (Y or N)",
        "Should this section not be paged out to disk? (Y or N)",
        "Does this section have the IMAGE_SCN_MEM_DISCARDABLE characteristic set? (Y or N)",
        "Is this section discardable? (Y or N)",
        "Can this section be removed from memory when the loader is done with it? (Y or N)",
        "Does this section have the IMAGE_SCN_MEM_SHARED characteristic set? (Y or N)",
        "Can this section be shared between processes? (Y or N)",
        "Does this section have the IMAGE_SCN_MEM_EXECUTE characteristic set? (Y or N)",
        "Is this section executable? (Y or N)",
        "Does this section have the IMAGE_SCN_MEM_WRITE characteristic set? (Y or N)",
        "Is this section writable? (Y or N)"]
#        "Does this section have the IMAGE_SCN_MEM_READ characteristic set? (Y or N)",
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR3

  x = random.randint(0,3)
  if x == 0:
    pe = pefile.PE('../template32.exe')
    suffix = ".exe"
  elif x == 1:
    pe = pefile.PE('../template64.exe')
    suffix = ".exe"
  elif x == 2:
    pe = pefile.PE('../template32.dll')
    suffix = ".dll"
  else:
    pe = pefile.PE('../template64.dll')
    suffix = ".dll"

  #pick a random section
  randSectIndex = random.randint(0,len(pe.sections)-1)

  numFlagsSet = 0
  if random.randint(0,1) == 1:
    pe.sections[randSectIndex].Characteristics |= 0x00000020
    IMAGE_SCN_CTN_CODE = "Y"
    numFlagsSet += 1
  else:
    IMAGE_SCN_CTN_CODE = "N"
  if random.randint(0,1) == 1:
    pe.sections[randSectIndex].Characteristics |= 0x00000040
    IMAGE_SCN_CNT_INITIALIZED_DATA = "Y"
    numFlagsSet += 1
  else:
    pe.sections[randSectIndex].Characteristics &= ~0x00000040
    IMAGE_SCN_CNT_INITIALIZED_DATA = "N"
  if random.randint(0,1) == 1:
    pe.sections[randSectIndex].Characteristics |= 0x00000080
    IMAGE_SCN_CNT_UNINITIALIZED_DATA = "Y"
    numFlagsSet += 1
  else:
    pe.sections[randSectIndex].Characteristics &= ~0x00000080
    IMAGE_SCN_CNT_UNINITIALIZED_DATA = "N"
    
  if random.randint(0,1) == 1:
    pe.sections[randSectIndex].Characteristics |= 0x02000000
    IMAGE_SCN_MEM_DISCARDABLE = "Y"
    numFlagsSet += 1
  else:
    pe.sections[randSectIndex].Characteristics &= ~0x02000000
    IMAGE_SCN_MEM_DISCARDABLE = "N"
    
  if random.randint(0,1) == 1:
    pe.sections[randSectIndex].Characteristics |= 0x04000000
    IMAGE_SCN_MEM_NOT_CACHED = "Y"
    numFlagsSet += 1
  else:
    pe.sections[randSectIndex].Characteristics &= ~0x04000000
    IMAGE_SCN_MEM_NOT_CACHED = "N"

  if random.randint(0,1) == 1:
    pe.sections[randSectIndex].Characteristics |= 0x08000000
    IMAGE_SCN_MEM_NOT_PAGED = "Y"
    numFlagsSet += 1
  else:
    pe.sections[randSectIndex].Characteristics &= ~0x08000000
    IMAGE_SCN_MEM_NOT_PAGED = "N"

  if random.randint(0,1) == 1:
    pe.sections[randSectIndex].Characteristics |= 0x10000000
    IMAGE_SCN_MEM_SHARED = "Y"
    numFlagsSet += 1
  else:
    pe.sections[randSectIndex].Characteristics &= ~0x10000000
    IMAGE_SCN_MEM_SHARED = "N"

  if random.randint(0,1) == 1:
    pe.sections[randSectIndex].Characteristics |= 0x20000000
    IMAGE_SCN_MEM_EXECUTE = "Y"
    numFlagsSet += 1
  else:
    pe.sections[randSectIndex].Characteristics &= ~0x20000000
    IMAGE_SCN_MEM_EXECUTE = "N"

  if random.randint(0,1) == 1:
    pe.sections[randSectIndex].Characteristics |= 0x80000000
    IMAGE_SCN_MEM_WRITE = "Y"
    numFlagsSet += 1
  else:
    pe.sections[randSectIndex].Characteristics &= ~0x80000000
    IMAGE_SCN_MEM_WRITE = "N"

  #FIXME: what's the more graceful way of doing this?
  error = 1
  while error:
    try:
      #write out the modified file
      outFileName = "Round3Q" + str(questionCounter) + suffix
      pe.write(filename=outFileName)
      error = 0
    except IOError:
      questionCounter+=1
  
 
  #Print the question
  q = random.randint(0,len(Qs)-1)
  print "For binary R3Bins/%s..." % outFileName
  print "For section '%s'..." % pe.sections[randSectIndex].Name
  print Qs[q]
  answer = raw_input("Answer: ")

  if q == 0:
    CheckAnswerNum(answer,pe.sections[randSectIndex].Characteristics)
  elif q == 1:
    CheckAnswerNum(answer,numFlagsSet)
  elif q == 2 or q == 3:
    CheckAnswerString(answer,IMAGE_SCN_CTN_CODE)
  elif q == 4 or q == 5:
    CheckAnswerString(answer,IMAGE_SCN_CNT_INITIALIZED_DATA)
  elif q == 6 or q == 7:
    CheckAnswerString(answer,IMAGE_SCN_CNT_UNINITIALIZED_DATA)
  elif q == 8 or q == 9:
    CheckAnswerString(answer,IMAGE_SCN_MEM_NOT_CACHED)
  elif q == 10 or q == 11:
    CheckAnswerString(answer,IMAGE_SCN_MEM_NOT_PAGED)
  elif q == 12 or q == 13 or q == 14:
    CheckAnswerString(answer,IMAGE_SCN_MEM_DISCARDABLE)
  elif q == 15 or q == 16:
    CheckAnswerString(answer,IMAGE_SCN_MEM_SHARED)
  elif q == 17 or q == 18:
    CheckAnswerString(answer,IMAGE_SCN_MEM_EXECUTE)
  elif q == 19 or q == 20:
    CheckAnswerString(answer,IMAGE_SCN_MEM_WRITE)

def R3Q2(questionCounter):
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR3
  Qs = ["What is the section name that typically contains the program's main code?",
        "What is the section name that typically contains the program's writable global data?",
        "What is the section name that typically contains the program's read-only global data?",
        "What is the section name that typically contains the program's relocation data?",
        "What is the section name that typically contains the program's resources?",
        "Although it is commonly merged into other sections, what is a possible name for the section containing global data which is uninitialized, and therefore does not need to be stored on disk?",
        "Although it is commonly merged into other sections, what is a possible name for the section containing import data?",
        "Although it is commonly merged into other sections, what is a possible name for the section containing export data?",
        "What is the commonly used prefix for sections that can be paged to disk?",
        "What is the section name that typically contains 64 bit programs' exception handling data structures?",
        "Can a section's SizeOfRawData be larger than its VirtualSize? (Y or N)",
        "Can a section's VirtualSize be larger than its SizeOfRawData? (Y or N)"]
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR3

  #Print the question
  q = random.randint(0,len(Qs)-1)
  print Qs[q]
  answer = raw_input("Answer: ")
  
  if q == 0:
    CheckAnswerString(answer,".text")
  elif q == 1:
    CheckAnswerString(answer,".data")
  elif q == 2:
    CheckAnswerString(answer,".rdata")
  elif q == 3:
    CheckAnswerString(answer,".reloc")
  elif q == 4:
    CheckAnswerString(answer,".rsrc")
  elif q == 5:
    CheckAnswerString(answer,".bss")
  elif q == 6:
    CheckAnswerString(answer,".idata")
  elif q == 7:
    CheckAnswerString(answer,".edata")
  elif q == 8:
    CheckAnswerString(answer,"PAGE")
  elif q == 9:
    CheckAnswerString(answer,".pdata")
  elif q == 10 or q == 11:
    CheckAnswerString(answer, "Y")
    print "I want to ask you 'When will this be the case?', but I wouldn't be able to parse your reply :) So just make sure you know!"
    
#Ask if the OptionalHeader.ImageSize matches the expectations based on
#the section headers (students need to know to sum the section headers to get
#the correct ImageSize). Then ask a follow up question of what the correct
#ImageSize should be
def R3Q3(questionCounter):
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR3
  Qs = ["Is the Optional Header SizeOfImage value correct? (Y or N)",
  "Does the IMAGE_OPTIONAL_HEADER.SizeOfImage match the expected value based on the number and size of sections? (Y or N)"]
  #NOTE: if you update the number of questions in this function, you need to update the boundaries in StartR3

  #Just reusing the capability from R1Q4
  randomSectionNames = [".xeno", "xeno", ".kovah", "kovah", 
                        ".boring", ".section", ".names", ".are", ".the",
                        ".new", ".normal", ".when", ".you're",
                        ".just", ".trying", ".to", 
                        ".move", ".forward", ":P", ":D", ":O",
                         "<-siht", "<-si", "<-ton", "<-a", "<-epip"]

  x = random.randint(0,3)
  if x == 0:
    pe = pefile.PE('../template32.exe')
    suffix = ".exe"
  elif x == 1:
    pe = pefile.PE('../template64.exe')
    suffix = ".exe"
  elif x == 2:
    pe = pefile.PE('../template32.dll')
    suffix = ".dll"
  else:
    pe = pefile.PE('../template64.dll')
    suffix = ".dll"

  #Created new function to insert random sections and write the file out
  numExtraSections = random.randint(1,5)
  totalNumSections = pe.FILE_HEADER.NumberOfSections + numExtraSections 
  #Since we haven't actually modified pe.FILE_HEADER.NumberOfSections in the binary yet
  #this function will know whether to add new sections based on whether the first param
  #is greater than the existing header or not
  updateSizeOfImage = random.randint(0,1)

  #FIXME: what's the more graceful way of doing this?
  error = 1
  while error:
    try:
      #write out the modified file
      outFileName = "Round3Q" + str(questionCounter) + suffix
      pe.x_modifySectionsAndWrite(totalNumSections, randomSectionNames, updateSizeOfImage, outFileName)
      #Reopen the file otherwise the pe.sections[] calculations below won't be accurate
      pe = pefile.PE(outFileName)
      error = 0
    except IOError:
      questionCounter+=1


  #Print the question
  q = random.randint(0,len(Qs)-1)
  print "For binary R3Bins/%s..." % outFileName
  print Qs[q]
  answer = raw_input("Answer: ")

  if q == 0 or q == 1:
    if updateSizeOfImage:
      CheckAnswerString(answer,"Y")
    else:
      CheckAnswerString(answer,"N")
      print "Bonus question: What should the value of SizeOfImage be?"
      answer = raw_input("Answer: ")
      CheckAnswerNum(answer, pe.sections[-1].Misc_VirtualSize + pe.sections[-1].VirtualAddress)
      
  #TODO: Are there any more questions from earlier rounds I skipped because we
  #hadn't covered sections yet which I can go back and hit now that we have?


def StartR3(seed, suppressRoundBanner, escapeScore):
  global gScore
  global gNextLevelRequiredScore
  if not suppressRoundBanner:
    print "================================================================================"
    print "Welcome to Round 3:"
    print "This round is all about IMAGE_SECTION_HEADERs (\"Section Headers\")"
    print "\nRound terminology note:"
    print "RVA = Relative Virtual Address (relative to image base)."
    print "VA = Absolute Virtual Address (base + RVA)"
    print "================================================================================\n"
  #making a directory that the files go into, just to keep things tidier
  try:
    os.mkdir("R3Bins")
  except OSError:
    pass
  os.chdir("R3Bins")
  filelist = [ f for f in os.listdir(".")]
  for f in filelist:
    try:
      os.remove(f)
    except OSError:
      pass
  roundStartTime = int(time())
  rounds.helpers.gNextLevelRequiredScore = escapeScore
  random.seed(seed)
  questionCounter = 0;
  while rounds.helpers.gScore < rounds.helpers.gNextLevelRequiredScore:
    #Now changed it so that a given R*Q* only has as many chances to be called
    #as it has calls to CheckAnswer*. This way the number of variant ways
    #to ask the question doesn't increase the probability of the question being asked
    #NOTE: if you update the number of questions in the round, you need to update these boundaries
    x = random.randint(0,47)
    if x <= 8:
      R3Q0(questionCounter)
    elif x <= 19:
      R3Q1(questionCounter)
    elif x <= 30:
      R3Q2(questionCounter)
    elif x <= 32:
      R3Q3(questionCounter)
      
    questionCounter+=1

  if not suppressRoundBanner:
    currentTime = int(time())
    roundTime = currentTime - roundStartTime
    roundMinutes = roundTime / 60
    roundSeconds = roundTime % 60
    totalElapsedTime = currentTime - rounds.helpers.gAbsoluteStartTime
    print "\nCongratulations, you passed round 3!"
    print "It took you %u minutes, %u seconds for this round." % (roundMinutes, roundSeconds)
    totalMinutes = totalElapsedTime / 60
    totalSeconds = totalElapsedTime % 60
    print "And so far it's taken you a total time of %u minutes, %u seconds." % (totalMinutes, totalSeconds) 

  os.chdir("..")