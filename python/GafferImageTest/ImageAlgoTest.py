##########################################################################
#
#  Copyright (c) 2015, Image Engine Design Inc. All rights reserved.
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

import unittest

import IECore

import GafferTest
import GafferImage
import GafferImageTest

class ImageAlgoTest( GafferImageTest.ImageTestCase ) :

	def testEmpty( self ) :

		self.assertTrue( GafferImage.empty( IECore.Box2i() ) )
		self.assertTrue( GafferImage.empty( IECore.Box2i( IECore.V2i( 0 ), IECore.V2i( 0 ) ) ) )
		self.assertFalse( GafferImage.empty( IECore.Box2i( IECore.V2i( 0 ), IECore.V2i( 1 ) ) ) )

	def testIntersects( self ) :

		self.assertFalse(
			GafferImage.intersects(
				IECore.Box2i(), IECore.Box2i()
			)
		)

		self.assertFalse(
			GafferImage.intersects(
				IECore.Box2i( IECore.V2i( 0 ), IECore.V2i( 10 ) ),
				IECore.Box2i( IECore.V2i( 10 ), IECore.V2i( 20 ) ),
			)
		)

		self.assertTrue(
			GafferImage.intersects(
				IECore.Box2i( IECore.V2i( 0 ), IECore.V2i( 10 ) ),
				IECore.Box2i( IECore.V2i( 9 ), IECore.V2i( 20 ) ),
			)
		)

	def testIntersection( self ) :

		self.assertEqual(
			GafferImage.intersection(
				IECore.Box2i( IECore.V2i( 1, 2 ), IECore.V2i( 9, 10 ) ),
				IECore.Box2i( IECore.V2i( 2, 0 ), IECore.V2i( 8, 29 ) ),
			),
			IECore.Box2i(
				IECore.V2i( 2, 2 ),
				IECore.V2i( 8, 10 )
			)
		)

	def testContains( self ) :

		self.assertFalse(
			GafferImage.contains(
				IECore.Box2i(),
				IECore.V2i( 0 )
			)
		)

		self.assertFalse(
			GafferImage.contains(
				IECore.Box2i( IECore.V2i( 0 ), IECore.V2i( 0 ) ),
				IECore.V2i( 0 )
			)
		)

		self.assertFalse(
			GafferImage.contains(
				IECore.Box2i( IECore.V2i( 0 ), IECore.V2i( 1 ) ),
				IECore.V2i( 1 )
			)
		)

		self.assertTrue(
			GafferImage.contains(
				IECore.Box2i( IECore.V2i( 0 ), IECore.V2i( 1 ) ),
				IECore.V2i( 0 )
			)
		)

	def testClamp( self ) :

		self.assertEqual(
			GafferImage.clamp(
				IECore.V2i( 5, 6 ),
				IECore.Box2i( IECore.V2i( 0 ), IECore.V2i( 10 ) )
			),
			IECore.V2i( 5, 6 )
		)

		self.assertEqual(
			GafferImage.clamp(
				IECore.V2i( 10, 6 ),
				IECore.Box2i( IECore.V2i( 0 ), IECore.V2i( 10 ) )
			),
			IECore.V2i( 9, 6 )
		)

		self.assertEqual(
			GafferImage.clamp(
				IECore.V2i( 0, 6 ),
				IECore.Box2i( IECore.V2i( 0 ), IECore.V2i( 10 ) )
			),
			IECore.V2i( 0, 6 )
		)

		self.assertEqual(
			GafferImage.clamp(
				IECore.V2i( 5, -1 ),
				IECore.Box2i( IECore.V2i( 0 ), IECore.V2i( 10 ) )
			),
			IECore.V2i( 5, 0 )
		)

		self.assertEqual(
			GafferImage.clamp(
				IECore.V2i( 5, 10 ),
				IECore.Box2i( IECore.V2i( 0 ), IECore.V2i( 10 ) )
			),
			IECore.V2i( 5, 9 )
		)

	def testLayerName( self ) :

		for channelName, layerName in [
			( "R", "" ),
			( "A", "" ),
			( "Z", "" ),
			( "myFunkyChannel", "" ),
			( "left.R", "left" ),
			( "right.myFunkyChannel", "right" ),
			( "diffuse.left.R", "diffuse.left" ),
		] :
			self.assertEqual( GafferImage.layerName( channelName ), layerName )

	def testBaseName( self ) :

		for channelName, baseName in [
			( "R", "R" ),
			( "A", "A" ),
			( "Z", "Z" ),
			( "myFunkyChannel", "myFunkyChannel" ),
			( "left.R", "R" ),
			( "right.myFunkyChannel", "myFunkyChannel" ),
			( "diffuse.left.R", "R" ),
		] :
			self.assertEqual( GafferImage.baseName( channelName ), baseName )

	def testColorIndex( self ) :

		for channelName, index in [
			( "R", 0 ),
			( "G", 1 ),
			( "B", 2 ),
			( "A", 3 ),
			( "Z", -1 ),
			( "myFunkyChannel", -1 ),
			( "left.R", 0 ),
			( "left.G", 1 ),
			( "left.B", 2 ),
			( "left.A", 3 ),
			( "left.Z", -1 ),
			( "right.myFunkyChannel", -1 ),
			( "diffuse.left.R", 0 ),
			( "diffuse.left.G", 1 ),
			( "diffuse.left.B", 2 ),
			( "diffuse.left.A", 3 ),
			( "diffuse.left.Z", -1 ),
		] :
			self.assertEqual( GafferImage.colorIndex( channelName ), index )

if __name__ == "__main__":
	unittest.main()
