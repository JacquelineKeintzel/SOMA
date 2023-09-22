"""
Script which reads phase output and plots a colourmap of the total phase advance of each BPM.
"""
from __future__ import print_function
import os
import sys
import argparse
import pandas
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from func import BPMs_from_sdds, get_data_column, get_dict_colormap

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--axis', '-ax', dest='axis', action='store')
parser.add_argument('--optics_output_dir', '-ood', dest='optics_output_dir', action='store')
parser.add_argument('--sdds_dir', '-sd', dest='sdds_dir', action='store')
parser.add_argument('--display', '-d', action='store_true')
parser.add_argument('--when', choices=['before', 'after'])
parser.add_argument('--form', choices=['png', 'pdf'])                    
parser.add_argument('--save', '-s', action='store_true')
args = parser.parse_args()

# Definitions
axis = args.axis
sdds_dir = args.sdds_dir
optics_output_dir = args.optics_output_dir
# data = 'getphasetot' + axis.lower() + '.out'
data = 'total_phase_' + axis.lower() + '.tfs'


# List all folders in optics_output_dir
phase_folders = [ff for ff in os.listdir(optics_output_dir) if 'av' not in ff]


# List all BPMs from any sdds file
bpms = BPMs_from_sdds(os.path.join(sdds_dir, os.listdir(sdds_dir)[1]))


# Create dataframe for plotting
df = {}
for folder in phase_folders:
    df[folder] = []
    names = get_data_column(optics_output_dir, folder, data, 'NAME')
    deltaphase = get_data_column(optics_output_dir, folder, data, 'DELTAPHASE' + axis.upper())
    for bpm in bpms:
        try:
            df[folder].append(get_dict_colormap(names, deltaphase)[bpm])
        except KeyError:
            df[folder].append(np.nan)
df = pandas.DataFrame(df, index=bpms)


# Set up the plot
with open('cmap.txt','r') as f:
    lines = f.readlines()
cmatrix = []
for i in range(len(lines)):
    cmatrix.append([float(j)/255.0 for j in lines[i].split()])
cm = colors.ListedColormap(cmatrix)

hor_ax, ver_ax = np.meshgrid(
    np.linspace(0, len(bpms), len(bpms) + 1),
    np.linspace(0, len(phase_folders), len(phase_folders) + 1))
df.to_csv(optics_output_dir + '../cmapdfnoTranspose_' + axis+args.when + '.csv')
Z = df.T
fn = optics_output_dir + '../cmapdf_' + axis+args.when + '.csv'
Z.to_csv(fn)
Z = pandas.read_csv(fn, index_col=0)
Z = np.ma.masked_where(np.isnan(Z),Z)

column_length = len(df.columns.tolist())
row_length = len(bpms)
# y_posn = [i for i in range(column_length)]
# x_posn = [i for i in range(row_length)]

# Plot
size = 32
fig = plt.figure(figsize=(15, 11)) #17,11 AK
plt.pcolormesh(hor_ax, ver_ax, Z, vmin=-0.45, vmax=0.45, cmap = 'jet')#, vmin=-0.45, vmax=0.45)#, cmap = cm)
bar = plt.colorbar()
if axis.lower() == 'x': bar.set_label('$\Delta\mu_{x}$ [2$\mathregular{\pi}$]', fontsize=size)
else: bar.set_label('$\Delta\mu_{y}$ [2$\mathregular{\pi}$]', fontsize=size)
bar.ax.tick_params(labelsize=size)

plt.xlim(0, len(hor_ax)-1)
plt.ylim(0, len(ver_ax)-1)
plt.xlabel('BPM Number', fontsize=size)
plt.ylabel('Measurements', fontsize=size)
plt.xlim(0,len(bpms))
plt.tick_params('both', labelsize=size)
plt.tight_layout()



# Advanced plotting by AK
# all_meas = []
# for i in df.columns.tolist():
#     try:
#         try:
#             all_meas.append(re.match('(\S*\_[0-9]+)\.sdds', i).group(1))
#         except AttributeError:
#             all_meas.append(re.match('\S*\_avg', i).group(0))
#     except:
#         all_meas.append(i)
# ax.set_xticks([i for i in range(row_length)])
# ax.set_xticklabels(bpms, rotation='vertical', fontsize=size)
# ax.set_yticks(y_posn)
# ax.set_yticklabels(all_meas, fontsize=size)
# ax.tick_params('both', labelsize=size)
# ax.set_xlabel('BPM Number', fontsize=size)
# ax.set_ylabel('Measurements', fontsize=size)
# ax.set_xlim(0,len(bpms))
# plt.title('SuperKEKB BPM performance from T-b-T data (' + axis + '-axis, ' + args.when  + ')', fontsize=size)


if args.save == True:
    plt.savefig(optics_output_dir + '../BPMs_colourmap_'+axis.upper()+args.when+'.'+args.form)
if args.display == True:
    plt.show()
plt.close()


print(" ********************************************\n",
      "checkBPMs_colormap.py:\n",
      '"Script made it to the end, moving on..."\n',
      "********************************************")

