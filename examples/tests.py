# Tests to verify that the code works correctly

from phystools import *

#############################

# unit conversion tests
def test_units ():
	# Length
	print "Doing length tests:"
	aLength = PhysNum(2, 1, MetreLengthUnit());
	print "\tOriginal aLength: ", aLength
	
	bLength= aLength.convertUnits(MillimetreLengthUnit());
	print "\tNew bLength (after mm conversion): ", bLength
	
# unit comparisons test
def test_unitMatching ():
	print "Doing type equality checks:"
	x = MetreLengthUnit;
	y = MillimetreLengthUnit;
	
	print "- Method 1"
	a = MetreLengthUnit();
	b = MetreLengthUnit();
	c = MillimetreLengthUnit();
	
	print "\t Type A, B, C: ", type(a), type(b), type(c) 
	print "\t A == B", type(a) == type(b)
	print "\t A == C", type(a) == type(c)
	
	
	print "- Method 2"
	a = x();
	b = x();
	c = y();
	
	print "\t Type A, B, C: ", type(a), type(b), type(c) 
	print "\t A == B", type(a) == type(b)
	print "\t A == C", type(a) == type(c)
	
	print "- Method 3"
	a = MetreLengthUnit();
	b = MetreLengthUnit();
	c = MillimetreLengthUnit();
	
	print "\t A == B", isinstance(a, b.__class__);
	print "\t A == C", isinstance(a, c.__class__);
	
# no units testing
def test_NoUnits ():
	pass;

#############################

# uncomment the tests we want to perform...
#test_units();
test_unitMatching();
