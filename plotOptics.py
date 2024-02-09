
from optparse import OptionParser
import numpy as np 
import matplotlib.pyplot as plt
import os
import sys


def read_phase(ff):
    with open(ff) as f: lines=f.readlines()
    f.close()
    S = [float(lines[10+i].split()[0]) for i in range(len(lines[10:]))]
    deltaph = [float(lines[10+i].split()[8]) for i in range(len(lines[10:]))]
    errdeltaph = [float(lines[10+i].split()[8]) for i in range(len(lines[10:]))]

    return S, deltaph, errdeltaph


def read_beta_amp(ff):
    with open(ff) as f: lines=f.readlines()
    f.close()
    S = [float(lines[12+i].split()[1]) for i in range(len(lines[12:]))]
    deltabet = np.array([float(lines[12+i].split()[7]) for i in range(len(lines[12:]))])*100
    errdeltabet = np.array([float(lines[12+i].split()[8]) for i in range(len(lines[12:]))])*100

    return S, deltabet, errdeltabet


def read_beta_ph(ff):
    with open(ff) as f: lines=f.readlines()
    f.close()
    S = [float(lines[15+i].split()[1]) for i in range(len(lines[15:]))]
    deltabet = np.array([float(lines[15+i].split()[10]) for i in range(len(lines[15:]))])*100
    errdeltabet = np.array([float(lines[15+i].split()[11]) for i in range(len(lines[15:]))])*100

    return S, deltabet, errdeltabet


def read_beta_cod(ff):
    with open(ff) as f: lines=f.readlines()
    f.close()
    S = [float(lines[3+i].split()[1]) for i in range(len(lines[3:]))]
    deltabetx = np.array([float(lines[3+i].split()[3]) for i in range(len(lines[3:]))])*100
    deltabety = np.array([float(lines[3+i].split()[5]) for i in range(len(lines[3:]))])*100

    return S, deltabetx, deltabety


def read_disp_cod(ff):
    with open(ff) as f: lines=f.readlines()
    f.close()
    S = [float(lines[3+i].split()[1]) for i in range(len(lines[3:]))]
    dx = np.array([float(lines[3+i].split()[2]) for i in range(len(lines[3:]))])
    dy = np.array([float(lines[3+i].split()[4]) for i in range(len(lines[3:]))])

    return S, dx, dy


def read_norm_disp(ff):
    with open(ff) as f: lines=f.readlines()
    f.close()
    S = [float(lines[10+i].split()[1]) for i in range(len(lines[10:]))]
    ndx = [float(lines[10+i].split()[5]) for i in range(len(lines[10:]))]
    errndx = [float(lines[10+i].split()[6]) for i in range(len(lines[10:]))]
    dx = [float(lines[10+i].split()[10]) for i in range(len(lines[10:]))]
    errdx = [float(lines[10+i].split()[11]) for i in range(len(lines[10:]))]

    return S, ndx, errndx, dx, errdx


def read_disp(ff):
    with open(ff) as f: lines=f.readlines()
    f.close()
    S = [float(lines[10+i].split()[1]) for i in range(len(lines[10:]))]
    dx = [float(lines[10+i].split()[9]) for i in range(len(lines[10:]))]
    errdx = [float(lines[10+i].split()[10]) for i in range(len(lines[10:]))]
    deltadx = np.array([float(lines[10+i].split()[11]) for i in range(len(lines[10:]))])*100
    errdeltadx = np.array([float(lines[10+i].split()[12]) for i in range(len(lines[10:]))])*100
    try:
        d2x = [float(lines[10+i].split()[16]) for i in range(len(lines[10:]))]
        errd2x = [float(lines[10+i].split()[17]) for i in range(len(lines[10:]))]
    except:
        d2x=[0]
        errd2x=[0]

    return S, dx, errdx, deltadx, errdeltadx, d2x, errd2x


def read_model(ff):
    with open(ff) as f: lines=f.readlines()
    f.close()
    Smdl = [float(lines[14+i].split()[2]) for i in range(len(lines[14:]))]
    betxmdl = np.array([float(lines[14+i].split()[4]) for i in range(len(lines[14:]))])
    betymdl = np.array([float(lines[14+i].split()[5]) for i in range(len(lines[14:]))])
    dxmdl = np.array([float(lines[14+i].split()[12]) for i in range(len(lines[14:]))])
    dymdl = np.array([float(lines[14+i].split()[13]) for i in range(len(lines[14:]))])
    xmdl = np.array([float(lines[14+i].split()[16]) for i in range(len(lines[14:]))])
    ymdl = np.array([float(lines[14+i].split()[17]) for i in range(len(lines[14:]))])
    
    return Smdl, betxmdl, betymdl, dxmdl, dymdl, xmdl, ymdl



def plot_delta(direc, name, axis, S, delta, errdelta, pngpdf, num):
    fix = 12
    fiy = 5
    num = 1
    size=18
    caps=6
    mark=7.5

    plt.figure(num, figsize=(fix, fiy))
    plt.errorbar(np.array(S)*1e-3, delta, yerr=errdelta, fmt = 'o', ms=mark, mec= 'C0', mfc = 'None', capsize=caps, c = 'C0', label = 'Measurement')
    plt.tick_params('both', labelsize=size)
    plt.xlabel('S [km]', fontsize=size)
    if name == 'COD_beta':
        #plt.ylim(-30,30)
        plt.ylabel(r'$\Delta \beta_{x}^{cod}$/$\beta_{x}^{mdl}$ [%]', fontsize=size) if axis =='x' else plt.ylabel(r'$\Delta \beta_{y}^{cod}$/$\beta_{y}^{mdl}$ [%]', fontsize=size) 
    if name == 'phase':
        plt.ylabel(r'$\Delta \mu_{x}$ $[2 \pi]$', fontsize=size) if axis =='x' else plt.ylabel(r'$\Delta \mu_{y}$ $[2 \pi]$', fontsize=size) 
    if name == 'beta_amp':
        plt.ylabel(r'$\Delta \beta_{x}^{amp}$/$\beta_{x}^{mdl}$ [%]', fontsize=size) if axis =='x' else plt.ylabel(r'$\Delta \beta_{y}^{amp}$/$\beta_{y}^{mdl}$ [%]', fontsize=size) 
    if name == 'beta_ph':
        #plt.ylim(-25,25)
        plt.ylabel(r'$\Delta \beta_{x}^{ph}$/$\beta_{x}^{mdl}$ [%]', fontsize=size) if axis =='x' else plt.ylabel(r'$\Delta \beta_{y}^{ph}$/$\beta_{y}^{mdl}$ [%]', fontsize=size) 
    if name == 'disp':
        plt.ylabel(r'$\Delta \eta_{x}$/$\eta_{x}^{mdl}$ [%]', fontsize=size) if axis =='x' else plt.ylabel(r'$\Delta \eta_{y}$/$\eta_{y}^{mdl}$ [%]', fontsize=size) 
    plt.xlim(0, 3.016)
    plt.tight_layout()
    plt.savefig(os.path.join(direc, name+'_'+axis+'_BEAT.'+pngpdf), bbox_inches='tight')
    plt.close(num)
    num=num+1

    return num


def plot_abs(direc, name, axis, S, Smdl, val, errval, valmdl, pngpdf, num):
    fix = 10
    fiy = 4
    num = 1
    size=22
    caps=6
    mark=7.5

    plt.figure(num, figsize=(fix, fiy))
    plt.plot(np.array(Smdl)*1e-3, valmdl, c = '#1f77b4', label='Model')
    plt.errorbar(np.array(S)*1e-3, val, yerr=errval, fmt = 'o', ms=mark, mec= 'C0', mfc = 'None', capsize=caps, c = 'C0', label = 'Measurement')
    plt.tick_params('both', labelsize=size)
    plt.xlabel('S [km]', fontsize=size)
    if name == 'disp':
        plt.ylabel(r'$\eta_{x}$ [m]', fontsize=size) if axis =='x' else plt.ylabel(r'$\eta_{y}$ [m]', fontsize=size) 
    if name == 'disp2':
        plt.ylabel(r'$\eta_{x}^{(2)}$ [m]', fontsize=size) if axis =='x' else plt.ylabel(r'$\eta_{y}^{(2)}$ [m]', fontsize=size)
    if name == 'norm_disp':
        plt.ylabel(r'$\eta_{n,x}$ [$\sqrt{\mathregular{m}}$]', fontsize=size) if axis =='x' else plt.ylabel(r'$\eta_{n,y}$ [$\sqrt{\mathregular{m}}$]', fontsize=size) 
    if name == 'COD_disp':
        plt.ylabel(r'$\eta_{x}^{cod}$ [m]', fontsize=size) if axis =='x' else plt.ylabel(r'$\eta_{y}^{cod}$ [m]', fontsize=size) 
    plt.xlim(0, 3.016)
    plt.legend(loc = 9, ncol = 2, fontsize=size, bbox_to_anchor=(0.5, 1.42), fancybox=True,  numpoints=1, scatterpoints = 1)
    plt.tight_layout()
    plt.savefig(os.path.join(direc, name+'_'+axis+'_ABS.'+pngpdf), bbox_inches='tight')
    plt.close(num)
    num=num+1

    return num


def main():
    parser = OptionParser()
    parser.add_option("-d", "--dir",  dest="dir", help="Directory of optics analysis output")
    parser.add_option("-m", "--model",  dest="model", help="Model file.")
    parser.add_option("-r", "--ring",  dest="ring", help="Ring ID, HER or LER")
    parser.add_option("-a", "--axis",  dest="axis", help="Plane, x or y")
    parser.add_option("-p", "--pngpdf",  dest="pngpdf", help="Output format, PNG oder PDF")
    (options, args) = parser.parse_args()

    
    if not os.path.exists(os.path.join(options.dir, 'average')): 
        print(" ********************************************\n",
                "Plot optics:\n",
                'I could not find an average output folder..\n',
                'I stop now. \n',    
                "********************************************")
        sys.exit()

    num = 1

    files = [ff for ff in os.listdir(os.path.join(options.dir, 'average')) if ('.tfs') in ff]
    print(files)

    Smdl, betxmdl, betymdl, dxmdl, dymdl, xmdl, ymdl = read_model(os.path.join(options.model, 'twiss.dat'))
   

    if 'COD_betxy_muxy.tfs' in files:
        S, deltabetx, deltabety = read_beta_cod(os.path.join(options.dir, 'average/COD_betxy_muxy.tfs'))
        if options.axis == 'x':
            num = plot_delta(os.path.join(options.dir, 'average'), 'COD_beta', options.axis, S, deltabetx, [0]*len(deltabetx), options.pngpdf, num)
        else: 
            num = plot_delta(os.path.join(options.dir, 'average'), 'COD_beta', options.axis, S, deltabety, [0]*len(deltabety), options.pngpdf, num)

    if 'COD_dxy.tfs' in files:
        S, dx, dy = read_disp_cod(os.path.join(options.dir, 'average/COD_dxy.tfs'))
        if options.axis == 'x':
            num = plot_abs(os.path.join(options.dir, 'average'), 'COD_disp', options.axis, S, Smdl, dx, [0]*len(dx), dxmdl, options.pngpdf, num)
        else: 
            num = plot_abs(os.path.join(options.dir, 'average'), 'COD_disp', options.axis, S, Smdl, dy, [0]*len(dx), dymdl, options.pngpdf, num)
    
    if 'phase_'+options.axis+'.tfs' in files:
        S, deltaph, errdeltaph = read_phase(os.path.join(options.dir, 'average/phase_'+options.axis+'.tfs'))
        num = plot_delta(os.path.join(options.dir, 'average'), 'phase', options.axis, S, deltaph, errdeltaph, options.pngpdf, num)

    if 'beta_amplitude_'+options.axis+'.tfs' in files:
        S, deltabet, errdeltabet = read_beta_amp(os.path.join(options.dir, 'average/beta_amplitude_'+options.axis+'.tfs'))
        num = plot_delta(os.path.join(options.dir, 'average'), 'beta_amp', options.axis, S, deltabet, errdeltabet, options.pngpdf, num)
    
    if 'beta_phase_'+options.axis+'.tfs' in files:
        S, deltabet, errdeltabet = read_beta_ph(os.path.join(options.dir, 'average/beta_phase_'+options.axis+'.tfs'))
        num = plot_delta(os.path.join(options.dir, 'average'), 'beta_ph', options.axis, S, deltabet, errdeltabet, options.pngpdf, num)
    
    if 'normalised_dispersion_'+options.axis+'.tfs' in files:
        S, ndx, errndx, dx, errdx = read_norm_disp(os.path.join(options.dir, 'average/normalised_dispersion_'+options.axis+'.tfs'))
        ndmdl = dxmdl/np.sqrt(betxmdl) if options.axis == 'x' else dymdl/np.sqrt(betymdl)
        num = plot_abs(os.path.join(options.dir, 'average'), 'norm_disp', options.axis, S, Smdl, ndx, errndx, ndmdl, options.pngpdf, num)

    if 'dispersion_'+options.axis+'.tfs' in files:
        dmdl = dxmdl if options.axis == 'x' else dymdl
        S, dx, errdx, deltadx, errdeltadx, d2x, errd2x = read_disp(os.path.join(options.dir, 'average/dispersion_'+options.axis+'.tfs'))
        num = plot_delta(os.path.join(options.dir, 'average'), 'disp', options.axis, S, deltadx, errdeltadx, options.pngpdf, num)
        num = plot_abs(os.path.join(options.dir, 'average'), 'disp', options.axis, S, Smdl, dx, errdx, dmdl, options.pngpdf, num)

        if len(d2x) > 1:
            tw_files = [ff for ff in os.listdir(options.model) if 'twiss_dp0' in ff ]
            dpp = np.arange(-1e-3, 1.1e-3, 1e-4)
            orbit=[]
            for ff in tw_files:
                valmdl = read_model(os.path.join(options.model, ff))
                orbit.append(valmdl[5]) if options.axis == 'x' else orbit.append(valmdl[6])
            orbit=np.transpose(orbit)
            
            d2mdl = []
            dmdl = []
            for i in range(len(orbit)):
                
                diff1 = np.zeros(dpp.shape,np.float)
                diff2 = np.zeros(dpp.shape,np.float)
                
                diff1[0:-1] = np.diff(orbit[i])/np.diff(dpp)
                diff1[-1] = (orbit[i][-1] - orbit[i][-2])/(dpp[-1] - dpp[-2])
                diff2[0:-1] = np.diff(diff1)/np.diff(dpp)
                diff2[-1] = (diff1[-1] - diff1[-2])/(dpp[-1] - dpp[-2])

                dmdl.append(diff1[10])
                d2mdl.append(diff2[10])

            num = plot_abs(os.path.join(options.dir, 'average'), 'disp2', options.axis, S, Smdl, d2x, errd2x, d2mdl, options.pngpdf, num)
            

if __name__ == "__main__":
    main()




