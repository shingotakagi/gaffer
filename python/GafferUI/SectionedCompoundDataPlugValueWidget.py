##########################################################################
#  
#  Copyright (c) 2012, John Haddon. All rights reserved.
#  
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#  
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#  
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#  
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#  
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  
##########################################################################

import GafferUI

class _Section( GafferUI.CompoundDataPlugValueWidget ) :

	def __init__( self, plug, label, names, labels, **kw ) :
	
		GafferUI.CompoundDataPlugValueWidget.__init__( self, plug, True, label, **kw )
		
		self.__names = set( names )
		self.__namesToLabels = dict( zip( names, labels ) )
				
	def _childPlugs( self ) :
	
		return [ p for p in self.getPlug().children() if p["name"].getValue() in self.__names ]

	def _label( self, name ) :
	
		return self.__namesToLabels[name]

class SectionedCompoundDataPlugValueWidget( GafferUI.PlugValueWidget ) :

	def __init__( self, plug, sections, **kw ) :
	
		column = GafferUI.ListContainer( spacing = 8 )
	
		GafferUI.PlugValueWidget.__init__( self, column, plug, **kw )
		
		with column :
			for section in sections :
				_Section(
					self.getPlug(),
					label = section[0],
					names = [ e[0] for e in section[1] ],
					labels = [ e[1] for e in section[1] ],
				)
	
	def hasLabel( self ) :
	
		return True
			
	def _updateFromPlug( self ) :
	
		pass	