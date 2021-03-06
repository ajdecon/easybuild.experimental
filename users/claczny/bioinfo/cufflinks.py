# This file is an EasyBuild recipy as per https://github.com/hpcugent/easybuild
#
# Copyright:: Copyright (c) 2012 University of Luxembourg / LCSB
# Author::    Cedric Laczny <cedric.laczny@uni.lu>, Fotis Georgatos <fotis.georgatos@uni.lu>
# License::   MIT/GPL
# File::      $File$ 
# Date::      $Date$

import fileinput
import glob
import re
import os
import shutil
import sys

from easybuild.easyblocks.generic.configuremake import ConfigureMake
from easybuild.tools.modules import get_software_root

class EB_Cufflinks(ConfigureMake):
    """
    Support for building cufflinks (Transcript assembly, differential expression, and differential regulation for RNA-Seq)
    """

    def configure_step(self):
	"""
        Check for dependencies
	"""
	boost = get_software_root('Boost')
        if not boost:
            self.log.error("Dependency module Boost not loaded?")

	sam = get_software_root('SAMtools')
        if not sam:
            self.log.error("Dependency module SAMtools not loaded?")

	eigen = get_software_root('Eigen')
        if not eigen:
            self.log.error("Dependency module Eigen not loaded?")

	super(EB_Cufflinks, self).configure_step()


    def patch_step(self):
	"""
	First we need to rename a few things, s.a. http://wiki.ci.uchicago.edu/Beagle/BuildingSoftware -> "Cufflinks"
	"""
	build_dir = os.getcwd()
	source_files = build_dir + '/src/*.cpp'
	header_files = build_dir + '/src/*.h'
	files = glob.glob(source_files)
	files = files + (glob.glob(header_files))
	for fname in files:
		for line in fileinput.input(fname, inplace=1, backup='.orig'):
			line = re.sub(r'foreach', 'for_each', line, count=0)
			sys.stdout.write(line)

	for line in fileinput.input(build_dir +'/src/common.h', inplace=1, backup='.orig'):
			line = re.sub(r'#include \<boost\/for\_each.hpp\>', '#include <boost/foreach.hpp>', line, count=0)
			sys.stdout.write(line)

	super(EB_Cufflinks, self).patch_step()

