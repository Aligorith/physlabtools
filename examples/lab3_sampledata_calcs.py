# Use our utilities to perform series of calculations required for data 
# for Lab3 Formal Report using Sample Data given

import sys
import os
from phystools import *

##################################
# globals 

# ---
# Measurement instances 

mmDim= MillimetreLengthUnit();
mDim= MetreLengthUnit();

gDim= GramMassUnit();
kgDim= KilogramMassUnit();

sDim= SecondTimeUnit();

# ---

P= PhysNum;	# NOTE: class reference, not value reference

##################################

# calculate average wire radius
def calc_AverageWireRadius (values):
	global mDim;
	
	# convert from diameter to radius
	wire_radii = [];
	for val in values:
		# firstly, make sure we're in standard units
		val.changeUnits(mDim);
		
		# now append to list
		wire_radii.append(val/2);
	
	# return the average
	return phys_average(wire_radii);
	
# calculate moment of inertia of sphere
def calc_SphereInertia (mass, diameter):
	global mDim, kgDim;
	
	# convert values to SI-units
	mass.changeUnits(kgDim);
	diameter.changeUnits(mDim);
	
	# convert diameter to radius
	radius= diameter / 2;
	
	# use the formula:
	# 	I = 2/5 * m * r^2
	return (mass * radius**2) * (D(2) / D(5));
	
# calculate moment of inertia of heart-disk
def calc_HeartInertia(Is, T1s, T2h):
	return T2h/T1s * Is;

# calculate value of T for the given values (assumes only 3 of them)
def calc_T (t_values):
	# convert the t values (i.e. time for 20 oscillations) to T values
	T_values = [t/20 for t in t_values];
	
	# calculate the 'average' T value
	# TODO: in the lab specs, we should just set the uncertainty to be the
	#	 largest diff for T_values from T
	T = phys_average(T_values);
	
	# return T
	return T;
	
# calculate value of n - modulus of rigidity
def calc_n (Inertia, Slope, radius):
	# n = (8PI I) / (S r4)
	return (Inertia * ( D(8)*D(str(math.pi)) )) / (Slope * radius**4);

##################################

# run program
#	str: (string) string to print before running command
#	cmd: (string) command-line to execute
def Run_Program (str, cmd):
	if str != None: 
		print str
	
	status = os.system(cmd)
	
	if status: 
		print "$$$ Error No: ", status
		raise "Runtime Error"
	
# ----

# write latex file of the raw data
def write_latex_results (fileN, labels, format, data, caption):
	# open the nominated file for datafile writing
	f= file(fileN+".tex", 'w');
	
	# write prefactory stuff
	f.write("\\begin{table}[h]\n");
	f.write("\\begin{tabular}{ %s }\n" % ( " | ".join(["c" for x in labels]) ));
	f.write("%s \\\\ \hline \n" % ( " & ".join(labels) ));
	
	# loop over data, adding the specific columns we require
	for entry in data:	
		f.write( " & ".join(format(entry)) );
		if entry != data[-1]:
			f.write("\\\\ \n");
		else:
			f.write("\n");
	
	# write finishing stuff
	f.write("\\end{tabular}\n");
	if caption: f.write("\\caption{%s}\n" % (caption));
	f.write("\\end{table}\n");
	
	# close the file now
	f.close();
	
# ----
	
# write the given data set to the named files in standard gnuplot plotting format
def write_gnuplot_datafile (fileN, data):
	# open the nominated file for datafile writing
	f= file(fileN+".dat", 'w');
	
	# loop over data, adding the specific columns we require
	for entry in data:
		# x y xdelta ydelta
		x= entry['L'].getValue();
		xd= entry['L'].getUncertainty_Absolute();
		y= entry['T^2'].getValue();
		yd= entry['T^2'].getUncertainty_Absolute();
		
		f.write("%s %s %s %s\n" % (x, y, xd, yd));
	
	# close the file now
	f.close();
	
	
	# open the nominated file for plotting commands writing
	f= file(fileN+".plt", 'w');
	#f.write("set terminal latex\n");
	f.write("set output \"%s\"\n" % (fileN+".tex"));
	f.write("set size 3.5/5, 3/3.\n");	# xxx
	f.write("set ylabel \"T^2 (s^2)\"\n");
	f.write("set xlabel \"L (m)\"\n");
	f.write("set grid \n");
	f.write("set title \"T^2 (Torsional Oscillation Period in Seconds Square) vs L (Length in m) for Solid Sphere \"\n");
	
	f.write("plot '%s' with xyerrorbars\n" % (fileN+".dat"));
	f.write("plot '%s' using $1:$2:$4 with yerrorbars\n" % (fileN+".dat"));
	
	# close the file now
	f.close();
	
# request slope from user
# TODO: just request the rise/run info?
def ui_GetSlope ():
	print "\n\n@ Run gnuplot on the graph file!!!"
	print "Then specify the appropriate values for the best-fitslope (S) and worst-fit slope (S')"
	
	S_dy = raw_input(">>> Slope (S) - Rise (dy): ");
	S_dx = raw_input(">>> Slope (S) - Run (dx): ");
	Sw_dy= raw_input(">>> Slope Worst (S') - Rise (dy): ");
	Sw_dx= raw_input(">>> Slope Worst (S') - Run (dx): ");
	
	S = D(S_dy) / D(S_dx);
	Sw = D(Sw_dy) / D(Sw_dx);
	dS = abs(S - Sw); # uncertainty is the difference
	
	# no units for now
	return P(S, dS, DummyUnit());
	
# ----

##################################

if __name__ == '__main__':
	print "Phys113 Lab 3 Data Calculations \n"
	
	# set up the context to only use precision sufficient for accurate calcs
	decimal.getcontext().prec = 10;
	
	# calculate average thickness of wire
	print "Calculating Wire Thickness..."
	#	data
	wire_diameters = [\
		P(0.378, 0.0005, mmDim), 
		P(0.378, 0.0005, mmDim),
		P(0.379, 0.0005, mmDim),
		P(0.375, 0.0005, mmDim),
		P(0.380, 0.0005, mmDim),
	]
	#	calculate
	wire_average= calc_AverageWireRadius(wire_diameters);
	print "\tAverage Wire Radius is ", wire_average, "\n"
	#	write results
	def __doformat_wdiameter (entry):
		# L | t1/2/3
		vals = [];
		vals.append("$%s$" % (str(entry).replace("+/-", "\\pm")));
		
		return vals;
	write_latex_results("wireResults", 
		["Diameter (mm)"],
		 __doformat_wdiameter, wire_diameters,
		 "Raw data for wire diameters");
	
	
	# calculating inertia of solid sphere
	print "Calculating Inertia of Solid Sphere..."
	#	data
	sphere_mass= P(359.9, 0.1, gDim);
	sphere_diameter= P(44.48, 0.03, mmDim);
	#	calculate
	sphere_inertia= calc_SphereInertia(sphere_mass, sphere_diameter);
	print "\tSolid Sphere Inertia is ", sphere_inertia, "\n"
	
	
	# normal data - format = length, 3 times
	print "Calculating Results for Solid Sphere..."
	#	data
	sphere_data = [\
	[P(612, 1, mmDim), 	P(67.72, 0.05, sDim), P(67.62, 0.05, sDim), P(67.80, 0.05, sDim)],
	[P(481, 1, mmDim), 	P(60.28, 0.05, sDim), P(60.21, 0.05, sDim), P(60.28, 0.05, sDim)],
	[P(322, 1, mmDim),	P(50.47, 0.05, sDim), P(50.35, 0.05, sDim), P(50.56, 0.05, sDim)],
	[P(202, 1, mmDim),	P(39.50, 0.05, sDim), P(39.32, 0.05, sDim), P(32.29, 0.05, sDim)]
	]
	
	# 	calculate T values, and print those
	print "\t L |", "T |", "T^2 "
	T_vals = [];
	for sdata in sphere_data:
		# for each set of measurements, store the calculated results as dict
		# 	length first - convert units to SI-units
		T_valD = {'L':sdata[0]};
		T_valD['L'].changeUnits(mDim);
		# 	calculate T-Values, and store as separate 
		T_valD['T']= calc_T(sdata[1:]); # strip off the length var to get the data
		T_valD['T^2']= T_valD['T'] ** 2;	# square T value
		
		# print the results from this
		print '\t', T_valD['L'], '|' , T_valD['T'], '|', T_valD['T^2'];
		
		# add dict to list of results
		T_vals.append(T_valD);
		
	# 	plot graph with gnuplot
	write_gnuplot_datafile("T2_vs_L", T_vals);
	
	#	write results for latex
	def __doformat_L_3T (entry):
		# L | t1/2/3
		vals = [];
		vals.append(entry[0].toStr(latex=True));
		vals.append(entry[1].toStr(latex=True));
		vals.append(entry[2].toStr(latex=True));
		vals.append(entry[3].toStr(latex=True));
		return vals;
	write_latex_results("sphereResults", 
		["L (m)", "$t_1 (s)$", "$t_2 (s)$", "$t_3 (s)$"],
		 __doformat_L_3T, sphere_data,
		 "Raw data");
	
	def __doformat_T2_L (entry):
		# L | T^2
		vals = [];
		vals.append(entry['L'].toStr(latex=True));
		vals.append(entry['T^2'].toStr(latex=True));
		return vals;
	write_latex_results("sphereResultsA", 
		["L (m)", "$T^2 (s^2)$"], 
		__doformat_T2_L, T_vals,
		"Processed data");
	
	# 	wait for user to input the necessary data (slope value)
	S = ui_GetSlope();
	print "\tSlope of T^2 vs L is ", S
	n = calc_n(sphere_inertia, S, wire_average);
	print "\tModulus of Rigidity of Wire, n, is ", n, "\n"
	
	# inertia of heart disk
	print "Calculating Results for Heart-Shaped Disk"
	#	data
	hdisk_data= [[P(202, 1, mmDim),	P(99.41, 0.05, sDim), P(99.24, 0.05, sDim), P(99.16, 0.05, sDim)]];
	
	# do calculations
	# 	length first - convert units to SI-units
	T_valH = {'L':hdisk_data[0][0]};
	T_valH['L'].changeUnits(mDim);
	# 	calculate T-Values, and store as separate 
	T_valH['T']= calc_T(hdisk_data[0][1:]); # strip off the length var to get the data
	T_valH['T^2']= T_valH['T'] ** 2;	# square T value
	#	calculate inertia of heart disk
	hInertia= calc_HeartInertia(sphere_inertia, T_vals[-1]['T^2'], T_valH['T^2']);
	
	# print the results from this
	print '\t', "Average T = ", T_valH['T'];
	print '\t', "Average T^2 = ", T_valH['T^2'];
	print '\t', "Inertia of Heart Disk = ", hInertia		
	
	#	write results for latex
	write_latex_results("heatResults", 
		["L (m)", "$t_1 (s)$", "$t_2 (s)$", "$t_3 (s)$"],
		 __doformat_L_3T, hdisk_data,
		 "Raw data for Heart-Shaped disk");
	
	
	# done
	sys.stdin.readline();
