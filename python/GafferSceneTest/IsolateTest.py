##########################################################################
#
#  Copyright (c) 2013, Image Engine Design Inc. All rights reserved.
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

import Gaffer
import GafferScene
import GafferSceneTest

class IsolateTest( GafferSceneTest.SceneTestCase ) :

	def testPassThrough( self ) :

		sphere = IECore.SpherePrimitive()
		input = GafferSceneTest.CompoundObjectSource()
		input["in"].setValue(
			IECore.CompoundObject( {
				"bound" : IECore.Box3fData( sphere.bound() ),
				"children" : {
					"groupA" : {
						"bound" : IECore.Box3fData( sphere.bound() ),
						"children" : {
							"sphereAA" : {
								"bound" : IECore.Box3fData( sphere.bound() ),
								"object" : sphere,
							},
							"sphereAB" : {
								"bound" : IECore.Box3fData( sphere.bound() ),
								"object" : sphere,
							},
						},
					},
					"groupB" : {
						"bound" : IECore.Box3fData( sphere.bound() ),
						"children" : {
							"sphereBA" : {
								"bound" : IECore.Box3fData( sphere.bound() ),
								"object" : sphere,
							},
							"sphereBB" : {
								"bound" : IECore.Box3fData( sphere.bound() ),
								"object" : sphere,
							},
						},
					},
				},
			} ),
		)

		isolate = GafferScene.Isolate()
		isolate["in"].setInput( input["out"] )

		self.assertSceneValid( input["out"] )
		self.assertSceneValid( isolate["out"] )

		# with no filter applied, nothing should be isolated so we should have a perfect pass through

		self.assertScenesEqual( input["out"], isolate["out"] )
		self.assertSceneHashesEqual( input["out"], isolate["out"] )
		self.assertTrue( input["out"].object( "/groupA/sphereAA", _copy = False ).isSame( isolate["out"].object( "/groupA/sphereAA", _copy = False ) ) )

		# and even with a filter applied, we should have a perfect pass through if the node is disabled.

		filter = GafferScene.PathFilter()
		filter["paths"].setValue( IECore.StringVectorData( [ "/*" ] ) )
		isolate["filter"].setInput( filter["out"] )

		isolate["enabled"].setValue( False )

		self.assertScenesEqual( input["out"], isolate["out"] )
		self.assertSceneHashesEqual( input["out"], isolate["out"] )
		self.assertTrue( input["out"].object( "/groupA/sphereAA", _copy = False ).isSame( isolate["out"].object( "/groupA/sphereAA", _copy = False ) ) )

	def testIsolation( self ) :

		sphere = IECore.SpherePrimitive()
		input = GafferSceneTest.CompoundObjectSource()
		input["in"].setValue(
			IECore.CompoundObject( {
				"bound" : IECore.Box3fData( sphere.bound() ),
				"children" : {
					"groupA" : {
						"bound" : IECore.Box3fData( sphere.bound() ),
						"children" : {
							"sphereAA" : {
								"bound" : IECore.Box3fData( sphere.bound() ),
								"object" : sphere,
							},
							"sphereAB" : {
								"bound" : IECore.Box3fData( sphere.bound() ),
								"object" : sphere,
							},
						},
					},
					"groupB" : {
						"bound" : IECore.Box3fData( sphere.bound() ),
						"children" : {
							"sphereBA" : {
								"bound" : IECore.Box3fData( sphere.bound() ),
								"object" : sphere,
							},
							"sphereBB" : {
								"bound" : IECore.Box3fData( sphere.bound() ),
								"object" : sphere,
							},
						},
					},
				},
			} ),
		)

		isolate = GafferScene.Isolate()
		isolate["in"].setInput( input["out"] )

		filter = GafferScene.PathFilter()
		filter["paths"].setValue( IECore.StringVectorData( [ "/groupA/sphereAB" ] ) )
		isolate["filter"].setInput( filter["out"] )

		self.assertNotEqual( isolate["out"].childNamesHash( "/groupA" ), input["out"].childNamesHash( "/groupA" ) )
		self.assertEqual( isolate["out"].childNames( "/groupA" ), IECore.InternedStringVectorData( [ "sphereAB" ] ) )
		self.assertEqual( isolate["out"].childNames( "/" ), IECore.InternedStringVectorData( [ "groupA" ] ) )

		filter["paths"].setValue( IECore.StringVectorData( [ "/groupA/sphereAA" ] ) )
		self.assertEqual( isolate["out"].childNames( "/groupA" ), IECore.InternedStringVectorData( [ "sphereAA" ] ) )
		self.assertEqual( isolate["out"].childNames( "/" ), IECore.InternedStringVectorData( [ "groupA" ] ) )


	def testAdjustBounds( self ) :

		sphere1 = IECore.SpherePrimitive()
		sphere2 = IECore.SpherePrimitive( 2 )
		input = GafferSceneTest.CompoundObjectSource()
		input["in"].setValue(
			IECore.CompoundObject( {
				"bound" : IECore.Box3fData( sphere2.bound() ),
				"children" : {
					"group" : {
						"bound" : IECore.Box3fData( sphere2.bound() ),
						"children" : {
							"sphere1" : {
								"bound" : IECore.Box3fData( sphere1.bound() ),
								"object" : sphere1,
							},
							"sphere2" : {
								"bound" : IECore.Box3fData( sphere2.bound() ),
								"object" : sphere2,
							},
						},
					},
				},
			} ),
		)

		isolate = GafferScene.Isolate()
		isolate["in"].setInput( input["out"] )

		filter = GafferScene.PathFilter()
		filter["paths"].setValue( IECore.StringVectorData( [ "/group/sphere1" ] ) )
		isolate["filter"].setInput( filter["out"] )

		self.assertEqual( isolate["out"].bound( "/" ), sphere2.bound() )
		self.assertEqual( isolate["out"].bound( "/group" ), sphere2.bound() )
		self.assertEqual( isolate["out"].bound( "/group/sphere1" ), sphere1.bound() )

		isolate["adjustBounds"].setValue( True )

		self.assertEqual( isolate["out"].bound( "/" ), sphere1.bound() )
		self.assertEqual( isolate["out"].bound( "/group" ), sphere1.bound() )
		self.assertEqual( isolate["out"].bound( "/group/sphere1" ), sphere1.bound() )

	def testSets( self ) :

		light1 = GafferSceneTest.TestLight()
		light2 = GafferSceneTest.TestLight()

		group = GafferScene.Group()
		group["in"][0].setInput( light1["out"] )
		group["in"][1].setInput( light2["out"] )

		lightSet = group["out"].set( "__lights" )
		self.assertEqual( set( lightSet.value.paths() ), set( [ "/group/light", "/group/light1" ] ) )

		isolate = GafferScene.Isolate()
		isolate["in"].setInput( group["out"] )

		lightSet = isolate["out"].set( "__lights" )
		self.assertEqual( set( lightSet.value.paths() ), set( [ "/group/light", "/group/light1" ] ) )

		filter = GafferScene.PathFilter()
		isolate["filter"].setInput( filter["out"] )

		lightSet = isolate["out"].set( "__lights" )
		self.assertEqual( set( lightSet.value.paths() ), set( [] ) )

		filter["paths"].setValue( IECore.StringVectorData( [ "/group/light" ] ) )
		lightSet = isolate["out"].set( "__lights" )
		self.assertEqual( set( lightSet.value.paths() ), set( [ "/group/light" ] ) )

		filter["paths"].setValue( IECore.StringVectorData( [ "/group/light*" ] ) )
		lightSet = isolate["out"].set( "__lights" )
		self.assertEqual( set( lightSet.value.paths() ), set( [ "/group/light", "/group/light1" ] ) )

	def testGlobalsDoNotDependOnScenePath( self ) :

		pathFilter = GafferScene.PathFilter()
		pathFilter["paths"].setValue( IECore.StringVectorData( [ "/grid/borderLines" ] ) )

		grid = GafferScene.Grid()

		isolate = GafferScene.Isolate()
		isolate["in"].setInput( grid["out"] )
		isolate["filter"].setInput( pathFilter["out"] )

		c = Gaffer.Context()
		with c :
			h1 = isolate["out"]["globals"].hash()
			c["scene:path"] = IECore.InternedStringVectorData( [ "grid" ] )
			h2 = isolate["out"]["globals"].hash()
			c["scene:path"] = IECore.InternedStringVectorData( [ "grid", "centerLines" ] )
			h3 = isolate["out"]["globals"].hash()

		self.assertEqual( h1, h2 )
		self.assertEqual( h2, h3 )

	def testFrom( self ) :

		# - group1
		#	- group2
		#		- light1
		#		- light2
		#	- light3
		# - plane

		light1 = GafferSceneTest.TestLight()
		light1["name"].setValue( "light1" )
		light2 = GafferSceneTest.TestLight()
		light2["name"].setValue( "light2" )
		light3 = GafferSceneTest.TestLight()
		light3["name"].setValue( "light3" )

		group1 = GafferScene.Group()
		group1["name"].setValue( "group1" )
		group2 = GafferScene.Group()
		group2["name"].setValue( "group2" )

		group1["in"][0].setInput( group2["out"] )
		group1["in"][1].setInput( light3["out"] )
		group2["in"][0].setInput( light1["out"] )
		group2["in"][1].setInput( light2["out"] )

		plane = GafferScene.Plane()

		parent = GafferScene.Parent()
		parent["parent"].setValue( "/" )
		parent["in"].setInput( group1["out"] )
		parent["child"].setInput( plane["out"] )

		isolate = GafferScene.Isolate()
		isolate["in"].setInput( parent["out"] )

		self.assertSceneValid( isolate["out"] )
		self.assertEqual( isolate["out"].childNames( "/" ), IECore.InternedStringVectorData( [ "group1", "plane" ] ) )
		self.assertEqual( isolate["out"].childNames( "/group1" ), IECore.InternedStringVectorData( [ "group2", "light3" ] ) )
		self.assertEqual( isolate["out"].childNames( "/group1/group2" ), IECore.InternedStringVectorData( [ "light1", "light2" ] ) )

		filter = GafferScene.PathFilter()
		filter["paths"].setValue( IECore.StringVectorData( [ "/group1/group2/light1" ] ) )

		isolate["filter"].setInput( filter["out"] )

		self.assertSceneValid( isolate["out"] )
		self.assertEqual( isolate["out"].childNames( "/" ), IECore.InternedStringVectorData( [ "group1" ] ) )
		self.assertEqual( isolate["out"].childNames( "/group1" ), IECore.InternedStringVectorData( [ "group2" ] ) )
		self.assertEqual( isolate["out"].childNames( "/group1/group2" ), IECore.InternedStringVectorData( [ "light1" ] ) )

		isolate["from"].setValue( "/group1" )

		self.assertSceneValid( isolate["out"] )
		self.assertEqual( isolate["out"].childNames( "/" ), IECore.InternedStringVectorData( [ "group1", "plane" ] ) )
		self.assertEqual( isolate["out"].childNames( "/group1" ), IECore.InternedStringVectorData( [ "group2" ] ) )
		self.assertEqual( isolate["out"].childNames( "/group1/group2" ), IECore.InternedStringVectorData( [ "light1" ] ) )

		isolate["from"].setValue( "/group1/group2" )

		self.assertSceneValid( isolate["out"] )
		self.assertEqual( isolate["out"].childNames( "/" ), IECore.InternedStringVectorData( [ "group1", "plane" ] ) )
		self.assertEqual( isolate["out"].childNames( "/group1" ), IECore.InternedStringVectorData( [ "group2", "light3" ] ) )
		self.assertEqual( isolate["out"].childNames( "/group1/group2" ), IECore.InternedStringVectorData( [ "light1" ] ) )

	def testIsolateNothing( self ) :

		sphere = GafferScene.Sphere()
		sphere["sets"].setValue("sphereSet")

		i = GafferScene.Isolate()
		i["in"].setInput( sphere["out"] )
		pathFilter = GafferScene.PathFilter()
		i["filter"].setInput( pathFilter["out"] )
		pathFilter["paths"].setValue( IECore.StringVectorData( [ "/sphere" ] ) )

		self.assertEqual( i["out"].childNames("/"), IECore.InternedStringVectorData( [ "sphere" ] ) )
		self.assertEqual( i["out"].set( "sphereSet" ).value.paths(), ["/sphere"] )

		pathFilter["paths"].setValue( IECore.StringVectorData() )

		self.assertEqual( i["out"].set( "sphereSet" ).value.paths(), [] )
		self.assertEqual( i["out"].childNames("/"), IECore.InternedStringVectorData() )


if __name__ == "__main__":
	unittest.main()
