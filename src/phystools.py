# Python utilities to perform the calculations for Physics Labs
# Copyright 2009, Joshua Leung (aligorith@gmail.com)
#
# First edition: 2009 April 27

import decimal
from decimal import Decimal as D
import decimaltools as DTools
import math

###################################
# Units - Single

# Abstract single 'unit' class
class Unit:
	# Instance Information - FOR CUSTOMISATION BY SUBCLASSES
	unit_symbol = "";		# 'symbol' to print beside values
	unit_name = "Units";	# name of unit for help info
	base = 10;				# size of steps for this type of unit
	power = 1;				# how unit compares to other ones (relative to base)
	is_SI = False;			# unit is SI unit
	
	# Return string representation for console use
	def __repr__ (self):
		return self.unit_name;
		
	# Return string representation for user output
	def __str__ (self):
		return self.unit_symbol;
		
	# check if the provided unit is the same type of measurement as us
	def sameMeasurement (self, other):
		# sanity check
		if isinstance(other, Unit) == False:
			raise TypeError, "Not a unit!";
		
		# if base step is not equal, and/or units are of not same type of measurement
		# no conversion needed, so conversion factor is simply 1
		if isinstance(self, MassUnit):
			return isinstance(other, MassUnit);
		elif isinstance(self, LengthUnit):
			return isinstance(other, LengthUnit);
		elif isinstance(self, TimeUnit):
			return isinstance(other, TimeUnit);
			
		# not the same type
		return False;
		
	# Get conversion factor, given another unit, to convert from that unit to us
	# XXX we may have reversed the order of the naming vs usage :/
	def conversionFactor (self, other):
		# check if same type of measurement
		if self.sameMeasurement(other) == False:
			return D(1);
		
		# assume valid types that need converting now (base units should be the same)
		if self.power != other.power:
			return D(other.base ** other.power) / D(self.base ** self.power); 
		else:
			return D(1); # no conversion needed...

# dummy unit - placeholder which does nothing
class DummyUnit(Unit):
	pass;

# -------------------

# Unit for Mass
class MassUnit(Unit):
	# Type Information
	unit_name = "Mass";		# name of unit for help info
	base = 10;				# size of steps for this type of unit
	

# kilograms (SI)
class KilogramMassUnit(MassUnit):
	# Type Information
	unit_symbol = "kg";			# 'symbol' to print beside values
	unit_name = "Mass (kg)";	# name of unit for help info
	power = 3;					# how unit compares to other ones
	is_SI = True;				# unit is SI unit
	
# grams
class GramMassUnit(MassUnit):
	# Type Information
	unit_symbol = "g";			# 'symbol' to print beside values
	unit_name = "Mass (g)";		# name of unit for help info
	power = 0;					# how unit compares to other ones
	
# -------------------

# Unit for Length
class LengthUnit(Unit):
	# Type Information
	unit_name = "Length";	# name of unit for help info
	base = 10;				# size of steps for this type of unit
	

# kilometres
class KilometreLengthUnit(LengthUnit):
	# Type Information
	unit_symbol = "km";			# 'symbol' to print beside values
	unit_name = "Length (km)";	# name of unit for help info
	power = 7;					# how unit compares to other ones
	
# meters (SI)
class MetreLengthUnit(LengthUnit):
	# Type Information
	unit_symbol = "m";			# 'symbol' to print beside values
	unit_name = "Length (m)";	# name of unit for help info
	power = 3;					# how unit compares to other ones
	is_SI = True;				# unit is SI unit
	
# centimetres
class CentimetreLengthUnit(LengthUnit):
	# Type Information
	unit_symbol = "cm";			# 'symbol' to print beside values
	unit_name = "Length (cm)";	# name of unit for help info
	power = 1;					# how unit compares to other ones
	
# millimetres
class MillimetreLengthUnit(LengthUnit):
	# Type Information
	unit_symbol = "mm";			# 'symbol' to print beside values
	unit_name = "Length (mm)";	# name of unit for help info
	power = 0;					# how unit compares to other ones
	
# -------------------

# Unit for Time
class TimeUnit(Unit):
	# Type Information
	unit_name = "Time";		# name of unit for help info
	base = 60;				# size of steps for this type of unit
	

# seconds (SI)
class SecondTimeUnit(MassUnit):
	# Type Information
	unit_symbol = "s";			# 'symbol' to print beside values
	unit_name = "Time (s)";		# name of unit for help info
	power = 0;					# how unit compares to other ones
	is_SI = True;				# unit is SI unit
	
# minutes
class MinuteTimeUnit(MassUnit):
	# Type Information
	unit_symbol = "min";		# 'symbol' to print beside values
	unit_name = "Time (min)";	# name of unit for help info
	power = 1;					# how unit compares to other ones
	
###################################
# Units - Combinations of them
	
# Measurement Unit - represents a some form of measurement 
# for use when combining multiple units
class MeasurementUnit:
	# instance stuff -----------------------------------
	
	# instance vars
	unit= None;		# unit used here
	power= 1;		# i.e. unit^power
	
	def __init__ (self, unit, power=1):
		# sanity checks
		if isinstance(unit, Unit):
			self.unit= unit;
		else:
			raise TypeError, "Unit provided must be an instance of Unit";
			
		if type(power) != int:
			raise TypeError, "Power must be an integer";
		else:
			self.power= power;
		
	# Return string representation for console use
	def __repr__ (self):
		return "MeasurementUnit(%s, %d)" % (repr(self.unit), self.power)
		
	# Return string representation for user output
	def __str__ (self):
		# unit^pow
		return "%s^%d" % (self.unit, self.power)
		
	
	# type-specific tools -------------------------------
	
	# check if unit is combinable with measurement
	def combinableUnit (self, unit):
		# firstly, the measurement type test
		if self.unit.sameMeasurement(unit) == False:
			return False;
			
		# now the specific unit type test
		if isinstance(unit, self.__class__) == False:
			# for now, not acceptable - will form result in another measurement in vars
			return False;
		
		# unit is ok
		return True;
	
	# 'add' power reference
	def add (self, other):
		self.power += 1;
		
	# 'subtract' power reference
	def subtract (self):
		self.power -= 1;
		
	# combine with another measurement
	# 	- assumes sanity checks done
	def combine (self, other):
		# simply combine the powers now, since units are the same 
		self.power += other.power;
	
# ---	

# Dummy combined unit class - just store all the provided units
class CombinedUnits:
	# class stuff ------------------------------
	def __init__ (self, initialValues=[]):
		# init storage
		self.units = [];
		
		# store provided values
		for val in initialValues:
			self.addUnit(val);
	
	def __repr__ (self):
		return "CombinedUnits(%s)" % (repr(self.units));
		
	def __str__ (self):
		# loop over measurements, getting a list of the units
		result = "";
		for unit in self.units:
			# if power is 0, don't show, since something cancelled it out
			if unit.power != 0:
				# TODO: should we do any fancy grouping around these?
				result += str(unit);
			
		return result;
	
	# tools -------------------------------------
	
	# add a unit to the list (result of multiplication) 
	def addUnit (self, unit):
		if isinstance(unit, Unit):
			# check if any existing measurement will take it
			for mUnit in self.units:
				# combine then finish off
				if mUnit.combinableUnit(unit):
					mUnit.add();
					break;
			else:
				# add a new measurement, defaulting to single power
				self.units.append(MeasurementUnit(unit));
		elif isinstance(unit, MeasurementUnit):
			# check if any existing measurement just needs some power adding
			for mUnit in self.units:
				# combine then finish off
				if mUnit.combinableUnit(unit.unit):
					mUnit.combine(unit);
					break;
			else:
				# add the given unit
				self.units.append(unit);
		else:
			raise TypeError, "Not a unit";
			
	# remove a unit (result of division)
	def remove (self, unit):
		if isinstance(unit, Unit):
			# check if any existing measurement will take it
			for mUnit in self.units:
				# combine then finish off
				if mUnit.combinableUnit(unit):
					mUnit.subtract();
					break;
			else:
				# add a new measurement, defaulting to single negative power
				self.units.append(MeasurementUnit(unit, -1));
		elif isinstance(unit, MeasurementUnit):
			# check if any existing measurement just needs some power adding
			for mUnit in self.units:
				# combine then finish off
				if mUnit.combinableUnit(unit.unit):
					mUnit.combine(unit);
					break;
			else:
				# add the given unit, but make sure that it is negative
				unit.power= -abs(unit.power);
				self.units.append(unit);
		else:
			raise TypeError, "Not a unit";
	
###################################
# Physics Number

# Special representation of numbers as value + absolute uncertainty + units, 
# as is required in Physics Calculations. 
class PhysNum:
	# helper utility functions for class ---------------

	# validate numeric arguments to yield 'Decimal' objects
	@staticmethod
	def _validateNumArg (arg):
		# check for decimal 
		if type(arg) == D:
			return arg;
		
		# convert standard 'number' types to decimal
		if type(arg) == int:
			return D(arg);
		if type(arg) == float:
			return D(str(arg));
			
		# if a string, try to convert to a decimal, 
		# as it may be just a number in 'disguise'
		if type(arg) == str:
			return D(arg);
			
		# non numeric types can't be used!
		raise TypeError, "Non-numeric type encountered!";
		
	# validate the other arg given to an arithmetic operator
	def _validateArithArg (self, arg):
		# action to take depends on what the type of the given data is
		if type(arg) in (int, float, D):
			# convert to a PhysNum to be able to add normally
			arg= PhysNum(arg, 0, self.getUnits());
		elif isinstance(arg, PhysNum) == False:
			# error.. cannot add
			raise TypeError, "Not a numeric type";
			
		# return the arg now that we've validated it
		return arg;
		
	# class stuff ----------------------------------
	
	# instance variables
	v= None; 		# Decimal - 'value'
	e= None;		# Decimal - 'uncertainty'
	units= None;	# Unit  - 'units'  
	
	# constructor 
	def __init__ (self, value, uncertainty=0, units=None):
		# store arguments as instance variables after validating them first
		self.v= PhysNum._validateNumArg(value);
		self.e= PhysNum._validateNumArg(uncertainty);
		self.units= units; 
	
	# console representation
	def __repr__ (self):
		return "PhysNum(%s, %s, %s)" % (self.v, self.e, repr(self.units));
		
	# user-output representation (standard representation)
	def __str__ (self):
		# get units first - they may not exist (some cases not coded yet!)
		units= self.units if self.units else "";
		return "%s%s +/- %s%s" % (self.v, units, self.e, units);
		
	# specialist user-output representation method
	#	- latex options: 0 = off, 1 = manually defined, 2 = with special macro
	# TODO: implement the precision controls
	def toStr (self, latex=0, withUnits=False, precision=28):
		# get units first - just in case they are used (but they may not exist)
		units= self.units if (self.units and withUnits) else "";
		
		# return format
		if latex:
			if latex == 2:	# special mode... TODO: need define for this!
				return "\physNum{%s}{%s}{%s}" % (self.v, self.e, units);
			else:
				return "$(%s \pm %s)%s$" % (self.v, self.e, units);
		else:
			return "%s%s +/- %s%s" % (self.v, units, self.e, units);
		
	# getters --------------------------------------
	
	# Get the absolute value of this 'number'
	#	withUnits: (boolean) if True, return a outputtable string containing the absolute value and units
	#			  otherwise, just return the Decimal() that represents this
	def getValue (self, withUnits=False):
		if withUnits:
			return "%s%s" % (self.v, self.units);
		else:
			return self.v;
		
	# Get the absolute uncertainty of this 'number'
	#	withUnits: (boolean) if True, return a outputtable string containing the absolute uncertainty and units
	#			  otherwise, just return the Decimal() that represents this
	def getUncertainty_Absolute (self, withUnits=False):
		if withUnits:
			return "%s%s" % (self.e, self.units);
		else:
			return self.e;
		
	# Get the fractional uncertainty of this 'number' as a Decimal()
	def getUncertainty_Fractional (self):
		# sanity check: if our value is 0, simply return zero instead of getting divide by zero
		if self.v == 0:
			# for safety, just return 0
			return D('0');
		else:
			# plus operator here forces rounding...
			return +(self.e / self.v);
	
	# Get the percentage uncertainty of this 'number'
	#	withUnits: (boolean) if True, return a outputtable string containing the percentage uncertainty and 'units'
	#			  (i.e. percent, %). Otherwise, just return the Decimal() that represents this
	def getUncertainty_Percentage (self, withUnits=False):
		if withUnits:
			return "%s%%" % (self.getUncertainty_Fractional() * 100)
		else:
			return self.getUncertainty_Fractional() * 100;
		
	# Get the units of this 'number' as a Unit
	def getUnits (self):
		return self.units;
	
	# assorted number ops ---------------------------
	
	# change the units of this number to the specified units
	def changeUnits (self, newUnits):
		# check if we need to do anything (i.e. not same units?)
		# 	currently, we just check this by using the representations, which we assume will be different (no typos!)
		ownUnits = self.getUnits();
		if not (ownUnits or newUnits):
			return;
		if ownUnits.sameMeasurement(newUnits) == False:
			return;
		if repr(ownUnits) == repr(newUnits):
			return;
			
		# get the conversion factor (going from own to new, so use new.conversion... )
		convFac = newUnits.conversionFactor(ownUnits);
		
		# apply the conversion to our own values
		self.v *= convFac;
		self.e *= convFac;
		
		# set the new units
		self.units= newUnits;
	
	# make a copy of this number with the units changed to the specified ones
	def convertUnits (self, newUnits):
		# check if we need to do anything (i.e. not same units?)
		# 	currently, we just check this by using the representations, which we assume will be different (no typos!)
		ownUnits = self.getUnits();
		if not (ownUnits or newUnits):
			return None;
		if repr(ownUnits) == repr(newUnits):
			return None;
			
		# get the conversion factor (going from own to new, so use new.conversion... )
		convFac = newUnits.conversionFactor(ownUnits);
		
		# apply the conversion to our own values
		val= self.v * convFac;
		err= self.e * convFac;
		
		# return the new type
		return PhysNum(val, err, newUnits);
	
	# unary arithmetic operators -------------------------
	
	# absolute value operator - same as doing getValue(), so just reference that
	__abs__ = getValue;
	
	# pos operator - this is overloaded to return the upper value allowed 
	# 	by the uncertainty as a Decimal()
	def __pos__ (self):
		return self.getValue() + self.getUncertainty_Absolute();
	
	# pos operator - this is overloaded to return the lower value allowed 
	# 	by the uncertainty as a Decimal()
	def __neg__ (self):
		return self.getValue() - self.getUncertainty_Absolute();
		
	# invert the values (i.e. 1/val) - special case of division, with top numbe == 1
	def __invert__ (self):
		# final units are combination of these units
		units= self.getUnits();
		newUnits = None; # FIXME!!!!
		
		# simply divide the absolute value
		if self.getValue() == 0:
			# for now, refuse to divide this
			#val= Decimal('0');
			raise ZeroDivisionError;
		else:
			val= Decimal('1') / self.getValue();
		
		# the new uncertainty is simply the sum of the fractional uncertainties of the top and bottom,
		# multiplied by the new value. This simplifies down to being simply the uncertainty * new value
		err= self.getUncertainty_Fractional() * val;
		
		# return a new number
		return PhysNum(val, err, newUnits);
		
	# arithmetic operators (LHS-default) ---------------------------
	
	# addition operator - returns the result as a new PhysNum
	def __add__ (self, other):
		# validate given arg
		other= self._validateArithArg(other);
		
		# change the units of the number we're adding so that they're compatible 
		# (if same type of measurement, that is)
		units= self.getUnits();
		other.changeUnits(units);
		
		# simply add the component parts, doing unit conversions on the alternate data
		val= self.getValue() + other.getValue();
		err= self.getUncertainty_Absolute() + other.getUncertainty_Absolute();
		
		# return the result
		return PhysNum(val, err, units);
		
	# subtraction operator - returns the result as a new PhysNum
	def __sub__ (self, other):
		# validate given arg
		other= self._validateArithArg(other);
		
		# change the units of the number we're subtracting so that they're compatible 
		# (if same type of measurement, that is)
		units= self.getUnits();
		other.changeUnits(units);
		
		# subtract the values, but always add the absolute uncertainties
		# doing unit conversions on the alternate data
		val= self.getValue() - other.getValue();
		err= self.getUncertainty_Absolute() + other.getUncertainty_Absolute();
		
		# return the result
		return PhysNum(val, err, units);
	
	# multiplication operator - return the result as a new PhysNum
	def __mul__ (self, other):
		# validate given arg
		other= self._validateArithArg(other);
		
		# final units are combination of these units
		units= self.getUnits();
		newUnits = units; # FIXME!!!!
		
		# change the units of the number we're multiplying with so that they're compatible 
		# (if same type of measurement, that is)
		other.changeUnits(units);
		
		# simply multiply the absolute value
		val= self.getValue() * other.getValue();
		
		# to obtain the absolute uncertainty, need to add the percentage/fractional ones,  
		# then multiply this by the new value to get the new absolute value
		err= (self.getUncertainty_Fractional() + other.getUncertainty_Fractional()) * val;
		
		# return a new number
		return PhysNum(val, err, newUnits);
		
	# power operator - basically same as multiplication, but we can't do fractional values easily...
	def __pow__ (self, other, modulo=0):
		# check if other is integer 
		# FIXME: at some point, it would be good to have this
		if type(other) is not int:
			raise NotImplemented, "Only integer powers allowed" 
			
		# check if no multiplication needed?
		if other == 0:
			# N^0 is always 1
			return PhysNum(1, 0, self.getUnits());
		elif other < 0:
			# we will need to perform a division step at end, but firstly, 
			# take the absolute value of the int to use
			other= abs(other);
			postDiv= True;
		else:
			# just multiply...
			postDiv= False;
			
		# perform a little loop, multiplying ourself by our original value multiple times
		# TODO: could optimise to only do even powers...
		result= None;
		for i in xrange(other):	
			if result:
				# keep multipling if first one has been set already
				result *= self;
			elif other == 1:
				# there's just one, so just make a copy of self
				result= eval(repr(self));
			else:
				# since this is just a starting point, this is fine...
				result = self;
		
		# if we need to invert the result
		if postDiv: 
			result = ~result;
			
		# return the resulting new number
		return result;
	
	# division operator - divide values, but add fractional uncertainties
	def __div__ (self, other):
		# validate given arg
		other= self._validateArithArg(other);
		
		# final units are combination of these units
		units= self.getUnits();
		newUnits = units; # FIXME!!!!
		
		# change the units of the number we're multiplying with so that they're compatible 
		# (if same type of measurement, that is)
		other.changeUnits(units);
		
		# simply divide the absolute value
		if other.getValue() == 0:
			# for now, refuse to divide this
			#val= Decimal('0');
			raise ZeroDivisionError
		else:
			val= self.getValue() / other.getValue();
		
		# to obtain the absolute uncertainty, need to add the percentage/fractional ones,  
		# then multiply this by the new value to get the new absolute value
		err= (self.getUncertainty_Fractional() + other.getUncertainty_Fractional()) * val;
		
		# return a new number
		return PhysNum(val, err, newUnits);
		
	# truediv is the same as div for now
	__truediv__ = __div__;
	
	
	# arithmetic operators (RHS) ---------------------------
	
	# addition operator - returns the result as a new PhysNum
	# 	same as LHS addition, since communicative result
	__radd__ = __add__;
	
	# multiplication operator - return the result as a new PhysNum
	# 	same as LHS multiplication, since communicative result
	__rmul__ = __mul__;
	
	# subtraction operator - returns the result as a new PhysNum
	#	order is different, since subtraction is not communicative
	def __rsub__ (self, other):
		# validate given arg
		other= self._validateArithArg(other);
		
		# change the units of the number we're subtracting so that they're compatible 
		# (if same type of measurement, that is)
		units= self.getUnits();
		other.changeUnits(units);
		
		# subtract the values, but always add the absolute uncertainties
		# doing unit conversions on the alternate data
		val= other.getValue() - self.getValue();
		err= self.getUncertainty_Absolute() + other.getUncertainty_Absolute();
		
		# return the result
		return PhysNum(val, err, units);
		
	# division operator - divide values, but add fractional uncertainties
	#	order is different, since subtraction is not totally communicative
	def __rdiv__ (self, other):
		# validate given arg
		other= self._validateArithArg(other);
		
		# final units are combination of these units
		units= self.getUnits();
		newUnits = units; # FIXME!!!!
		
		# change the units of the number we're multiplying with so that they're compatible 
		# (if same type of measurement, that is)
		other.changeUnits(units);
		
		# simply divide the absolute value
		if self.getValue() == 0:
			# for now, refuse to divide this
			#val= Decimal('0');
			raise ZeroDivisionError
		else:
			val= other.getValue() / self.getValue();
		
		# to obtain the absolute uncertainty, need to add the percentage/fractional ones,  
		# then multiply this by the new value to get the new absolute value
		err= (self.getUncertainty_Fractional() + other.getUncertainty_Fractional()) * val;
		
		# return a new number
		return PhysNum(val, err, newUnits);
		
	# brute-force math ------------------------------
	
	# apply the given function (requiring single parameter only) 
	# on this number to yield a new PhysNum
	# 	- uses brute-force calculation techniques
	def calcFunc (self, func):
		# the new value is simply the result of applying the function to it
		val= func(self.v);
		
		# the absolute uncertainty is half the magnitude of the difference between the
		# upper and lower bounds allowable by the absolute uncertainties
		# WARNING: binary floating point errors are introduced here, as the functions 
		# 		   called are still essentially binary :/
		ubound= D(str(func(self.v + self.e)));
		lbound= D(str(func(self.v - self.e)));
		err= (ubound - lbound) / 2;
		
		# return a new number 
		# FIXME: what about the units? I guess they're still ok?
		return PhysNum(val, err, self.units); 

###################################
# Commonly-Performed Math API
# TODO: separate into own file?

# calculate the sum of a given list of values
def phys_sum (values):
	# init vars used
	result= None;
	tot= len(values);
	
	# loop over values, summing them
	for val in values:	
		if result:
			result += val;
		elif tot == 1:
			result = eval(repr(val));
		else:
			result = val;
	
	# return the sum of the values
	return result;
	
# calculate the average value of a list of values
def phys_average (values):
	N = len(values);
	
	# get the sum of these values
	result= phys_sum(values);
	
	# divide the absolute value by N, but the uncertainty by square-root of N
	# ..tsk tsk... directly modifying PhysNum like this is bad...
	result.v /= N;
	result.e /= D(N).sqrt();	# decimal provides its own precise sqrt func
	
	# return the result
	return result;
	
###################################
# Unit Tests
# ... TODO!!! ...

if __name__ == '__main__':
	pass;
