# Copyright 2017 University of Rome La Sapienza and Battelle Energy Alliance, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
  Created on April 18, 2017
  @author: Matteo Donorio (University of Rome La Sapienza)
"""
from __future__ import division, print_function, unicode_literals, absolute_import
import warnings
warnings.simplefilter('default',DeprecationWarning)

import os
import copy
import sys
import MELCORdata
from utils import utils
from melgenInterface import MelgenApp

class MelcorApp(MelgenApp):
  """
    This class is the CodeInterface for MELCOR
  """
  def __init__(self):
    """
      Constructor
      @ In, None
      @ Out, None
    """
    MelgenApp.__init__(self)

  def generateCommand(self, inputFiles, executable, clargs=None, fargs=None):
    """
      Generate a command to run MELCOR
      Collects all the clargs and the executable to produce the command-line call.
      Returns tuple of commands and base file name for run.
      Commands are a list of tuples, indicating parallel/serial and the execution command to use.
      This method is used to retrieve the command (in tuple format) needed to launch the Code.
      @ In, inputFiles, list, List of input files (length of the list depends on the number of inputs that have been added in the Step is running this code)
      @ In, executable, string, executable name with absolute path (e.g. /home/path_to_executable/code.exe)
      @ In, clargs, dict, optional, dictionary containing the command-line flags the user can specify in the input (e.g. under the node < Code >< clargstype =0 input0arg =0 i0extension =0 .inp0/ >< /Code >)
      @ In, fargs, dict, optional, a dictionary containing the axuiliary input file variables the user can specify in the input (e.g. under the node < Code >< clargstype =0 input0arg =0 aux0extension =0 .aux0/ >< /Code >)
      @ Out, returnCommand, tuple, tuple containing the generated command. returnCommand[0] is the command to run the code (string), returnCommand[1] is the name of the output root
    """
    subReturnCommand = MelgenApp.generateCommand(self,inputFiles, executable, clargs, fargs)
    outputfile = 'GEN_OUTPUT'
    returnCommand = subReturnCommand[0],outputfile
    return returnCommand

  def finalizeCodeOutput(self,command,output,workingDir):
    """
      This method is called by the RAVEN code at the end of each run (if the method is present, since it is optional).
      In this method the MELCOR outputfile is parsed and a CSV is created
      @ In, command, string, the command used to run the just ended job
      @ In, output, string, the Output name root
      @ In, workingDir, string, current working dir
      @ Out, output, string, optional, present in case the root of the output file gets changed in this method.
    """
    outfile = os.path.join(workingDir,output+'.out')
    outputobj=MELCORdata.MELCORdata(outfile)
    outputobj.writeCsv(os.path.join(workingDir,output+'.csv'))
