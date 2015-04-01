#!/usr/bin/python

import string, sys, glob, os, shutil, getopt, mmap
import operator
from subprocess import call
#import subprocess.call
sys.argv.append( '-b' ) # for ROOT in batch mode 

#temp = sys.argv 
#print sys.argv
from ROOT import gROOT, gPad, TH1D, TFile, TCanvas, TLatex, TLegend, THStack, TVirtualMutex, kRed, kOrange, kBlue, kCyan, kGreen, kViolet, kOrange, kBlack, kMagenta
#from ROOT import *
#sys.argv = temp
#print sys.argv

global histo, h_ttbar, h_wjets, h_dyjets, h_qcd, h_t, h_tth, h_ttz, h_ttw 

def debug(line):
    print '-----'
    print line
    print '-----'

def help():
    print 'First argument analysis:'
    print './check.py CMG_TYPE_SAMPLE '
    print ' TYPE = MC, data'
    print ' SAMPLE = TTbar, WJets,'
    print ' in general: ./check.py fileDir/* [OutputDir]'
    sys.exit(0)


def get(File,what,Lfac,lineCol,lineWid,lineSty,fillCol,reb=0):
	File.cd()
	h = File.Get(what)
	h = h.Clone()                                              # prevent overwrighting
	h.SetDirectory(0)                                          # now the histo is independent of the file state (closed/open)
	h.SetLineColor(lineCol)
	h.SetLineWidth(lineWid)
	h.SetLineStyle(lineSty)
	h.SetFillColor(fillCol)
	h.Scale(Lfac)
	if reb!=0: h.Rebin(reb)
	return h.Clone()

def plot(ana,histos,h_legend,minY,maxY,minX,maxX,whatX,whatY,c1=0):
	global stack, leg, dum
#	print what
#	gROOT.SetBatch(True)                                        # suppress root window popping up #! better: sys.argv.append('b')
	gROOT.ProcessLine("gErrorIgnoreLevel = kWarning;")          # suppress standard output of the form: "Info in <TCanvas::Print>: ... has been created" and 
#                                                                                                           "Info in <TCanvas::SaveAs>: ... has been created"
	#prepare the layout
	if c1==0:
		c1=TCanvas('c1','',800,600)
	c1.SetLogy() 
	dum = histo.Clone()
#	dum.Reset()
	dum.SetMinimum(minY)
	dum.SetMaximum(maxY)
	dum.GetXaxis().SetRangeUser(minX,maxX)
#        last = dum.FindLastBinAbove(0,1)
#        last = last + 0.5 * last
#        dum.GetXaxis().SetRange(0,last+10)
	dum.GetXaxis().SetTitleSize(0.038)
	dum.GetYaxis().SetTitleSize(0.04)
	dum.GetXaxis().SetLabelSize(0.03)
	dum.GetYaxis().SetLabelSize(0.03)
	dum.GetXaxis().SetTitleOffset(1.2)
	dum.GetYaxis().SetTitleOffset(1.1)
	dum.SetXTitle(whatX)
	dum.SetYTitle(whatY)
 	dum.SetTitle('')
	dum.SetStats(0)
	dum.Draw()
        
        tex = TLatex(0.89,0.93,"#scale[0.8]{CMSSW_7_2_3}                    #scale[0.6]{ #sqrt{s} = 13 TeV, #int L dt = 4 fb^{-1}, bx = 25 ns, PU = 20}")
        tex.SetNDC()
        tex.SetTextAlign(31)
        tex.SetTextFont(42)
        tex.SetTextSize(0.047)
        tex.SetLineWidth(2)
        tex.Draw()
        #CMS_lumi_v2( c1, 14, 11 )
#        tex1 = TLatex(0.15,0.89,"CMSSW_7_2_3 ")
#        tex1.SetNDC()
#        tex1.SetTextAlign(13)
#        tex1.SetTextFont(61)
#        tex1.SetTextSize(0.045)
#        tex1.SetLineWidth(2)
#        tex1.Draw()
	# a legend
#	leg = TLegend(0.63,0.525,0.87,0.875) #for 33 TeV 
#        leg = TLegend(0.65,0.65,0.9,0.9)
        leg = TLegend(0.6545226,0.534965,0.8944724,0.8846154) #fits best 
        leg.SetBorderSize(1)
        leg.SetTextFont(62)
        leg.SetTextSize(0.035)
        leg.SetLineColor(0)
        leg.SetLineStyle(1)
        leg.SetLineWidth(1)
        leg.SetFillColor(0)
        leg.SetFillStyle(1001)
	if ana == 'TTbar':
            title=' t#bar{t}'
            leg.AddEntry(histo,title,'l')
	elif ana == 'WJets':
            leg.AddEntry(histo,'W+jets','l')
        elif ana == 'DYJets':
            leg.AddEntry(histo,'DY+jets','l')
        elif ana == 'QCD':
            leg.AddEntry(histo,'QCD','l')
        elif ana == 'SingleTop':
            leg.AddEntry(histo,'t / #bar{t}','l')
        elif ana == 'TTH':
            leg.AddEntry(histo,'ttH','l')
        elif ana == 'TTW':
            leg.AddEntry(histo,'ttW','l')
        elif ana == 'TTZ':
            leg.AddEntry(histo,'ttZ','l') 
        elif ana == 'T1tttt_1500_100':
            leg.AddEntry(histo,'T1t^{4}(1500,100)','l') 
        elif ana == 'T1tttt_1200_800':
            leg.AddEntry(histo,'T1t^{4}(1200,800)','l') 
        elif ana == 'T5tttt_1000_280':
            leg.AddEntry(histo,'T5t^{4}(1000,280)','l') 
        elif ana == 'T5tttt_1300_280':
            leg.AddEntry(histo,'T5t^{4}(1300,280)','l') 
        elif ana == 'T5tttt_1000_285':
            leg.AddEntry(histo,'T5t^{4}(1000,285)','l') 
        elif ana == 'T5tttt_1300_285':
            leg.AddEntry(histo,'T5t^{4}(1300,285)','l') 
        elif ana == 'T1ttbbWW_1300_290':
            leg.AddEntry(histo,'T1t^{2}b^{2}W^{2}(1300,290)','l') 
        elif ana == 'T1ttbbWW_1300_295':
            leg.AddEntry(histo,'T1t^{2}b^{2}W^{2}(1300,295)','l') 
        elif ana == 'T1ttbbWW_1000_715':
            leg.AddEntry(histo,'T1t^{2}b^{2}W^{2}(1000,715)','l') 
        elif ana == 'T1ttbbWW_1000_720':
            leg.AddEntry(histo,'T1t^{2}b^{2}W^{2}(1000,720)','l') 
        elif ana == 'SqGl_1300_100':
            leg.AddEntry(histo,'SqGl(1300,100)','l') 
        # bgrd stack
        if histos != 0 and h_legend != 0:
            stack = THStack('stack','')
            N=len(histos)
            for i in range(N):
                h=histos[i][0]
                stack.Add(h)
	    for i in range(N-1,-1,-1):
                h=histos[i][0]
                t=h_legend[h]
                leg.AddEntry(h,t,'f')
            # draw bgrds + signals
#            stack.Draw('samehist')
            stack.Draw('same')

        #histo.Draw('samehist')
        histo.Draw('same')
        leg.Draw("same")
        gPad.RedrawAxis()

	c1.SaveAs(dir_png_noCuts+what+".png")
	c1.SaveAs(dir_pdf_noCuts+what+".pdf")
	c1.SaveAs(dir_root_noCuts+what+".root")


### NEW functions
def trimName(fname):
    prefix = 'CMG_MC_'
    suffix = '_his.root'
    nameBegin= fname.find(prefix)
    fname = fname[nameBegin:]
    fname = fname.replace(prefix,'')
    fname = fname.replace(suffix,'')
    return fname
####################################



#####################################################################################################################
#------------------------------------------- program begin ----------------------------------------------------------

if __name__ == "__main__":

#######################        
#if len(sys.argv)>0:
#    ana = sys.argv[1]
#else:
#    help()
#######################

    # len(sys.argv) = 1 means sys.argv[0] is filled with ./script.py
    if len(sys.argv) < 2:
        help()
    elif len(sys.argv) < 3:
        inDir = sys.argv[1]
        
    elif len(sys.argv) < 4:
        inDir = sys.argv[1]
        outDir = sys.argv[2]
# !!!! outputdir makes no sense !!!!

    print 'Input Directory:', inDir
#    print 'Output Directory:', outDir

    fileList = glob.glob(inDir+'/*.root')

    print 'Found', len(fileList), 'files'
    print [trimName(x) for x in fileList]
    print 80*'#'


    production = raw_input("Which production? (i.e.: 'phys14_Iso'): ")
#    production = 'cronTest'
#    production = 'Phys14_Iso'
#    production = 'Phys14_v3'
    print "drawing histograms"

    # defining
    ## dirs
    control_dir = '/afs/desy.de/group/cms/www/html/subgroups/susy/controlPlots/'
    #control_dir = '/afs/desy.de/user/t/trippk/www/controlPlots/'
    prod_dir = control_dir+production+'/'

    """
    # merge root files
    wjetsHT=[]
    qcdHT=[]
    dyjetsHT=[]
    singletop=[]
    prefix='CMG_MC_'
    suffix='_his.root'
    pwd= '/afs/desy.de/user/t/trippk/'
    for files in fileList:
        if 'WJetsToLNu' in files:
            wjetsHT.append(files)
        if 'QCD_HT' in files:
            qcdHT.append(files)
        if 'DYJetsToLL' and 'HT' in files:
            dyjetsHT.append(files)
        if 'sch' in files:
            singletop.append(files)
        if 'tch' in files:
            singletop.append(files)
        if 'tWch' in files:
            singletop.append(files)

    os.system('hadd '+pwd+prefix+'WJets'+suffix+' '+' '.join(wjetsHT))
    os.system('hadd '+pwd+prefix+'QCD'+suffix+' '+' '.join(qcdHT))
    os.system('hadd '+pwd+prefix+'DYJets'+suffix+' '+' '.join(dyjetsHT))
    os.system('hadd '+pwd+prefix+'SingleTop'+suffix+' '+' '.join(singletop))

    # update fileList
    
    newFileList=[]
    removeList = wjetsHT + qcdHT + dyjetsHT + singletop

    print 'removeList'
    for p in removeList:
        print p
    print 'removeList end'

    for item in fileList:
        if item not in removeList:
                newFileList.append(item)

#    newFileList(map(reMove(fileList), fileList))

    print 'newFileList'
    for p in newFileList:
        print p
    print 'newFileList end'

    
    fileList.remove(pwd+'CMG_MC_TTH_his.root')
    fileList.remove('/afs/desy.de/user/t/trippk/CMG_MC_WJetsToLNu_HT100to200_his.root')
    for item in fileList:
        print item


    print 'remove'
    for item in removeList:
        print item
        #fileList.remove(item)

    print 'remove end'

    addList = [pwd+prefix+'WJets'+suffix, pwd+prefix+'QCD'+suffix, pwd+prefix+'DYJets'+suffix, pwd+prefix+'SingleTop'+suffix]
    newFileList = newFileList + addList
    
    print '$$$$$$$$$$$'
    for item in newFileList:
        print item
    print '$$$$$$$$$$$'

    """
    for ana in [trimName(x) for x in fileList]:
        print ana

        # do a loop out of this
        www_dir = prod_dir+ana+'/'
        dir_png_noCuts = www_dir+'plots/noCuts/png/'
        dir_pdf_noCuts = www_dir+'plots/noCuts/pdf/'
        dir_root_noCuts = www_dir+'plots/noCuts/root/'
        dir_png_oneLep = www_dir+'plots/oneLep/png/'
        dir_pdf_oneLep = www_dir+'plots/oneLep/pdf/'
        dir_root_oneLep = www_dir+'plots/oneLep/root/'
        dir_png_HT_500 = www_dir+'plots/HT_500/png/'
        dir_pdf_HT_500 = www_dir+'plots/HT_500/pdf/'
        dir_root_HT_500 = www_dir+'plots/HT_500/root/'

        # create dir, remove if they exist
        if os.path.isdir(dir_png_noCuts):
            shutil.rmtree(dir_png_noCuts)
        call('mkdir -p '+dir_png_noCuts, shell=True)
        if os.path.isdir(dir_pdf_noCuts):
            shutil.rmtree(dir_pdf_noCuts)
        call('mkdir -p '+dir_pdf_noCuts, shell=True)
        if os.path.isdir(dir_root_noCuts):
            shutil.rmtree(dir_root_noCuts)
        call('mkdir -p '+dir_root_noCuts, shell=True)
        if os.path.isdir(dir_png_oneLep):
            shutil.rmtree(dir_png_oneLep)
        call('mkdir -p '+dir_png_oneLep, shell=True)
        if os.path.isdir(dir_pdf_oneLep):
            shutil.rmtree(dir_pdf_oneLep)
        call('mkdir -p '+dir_pdf_oneLep, shell=True)
        if os.path.isdir(dir_root_oneLep):
            shutil.rmtree(dir_root_oneLep)
        call('mkdir -p '+dir_root_oneLep, shell=True)
        if os.path.isdir(dir_png_HT_500):
            shutil.rmtree(dir_png_HT_500)
        call('mkdir -p '+dir_png_HT_500, shell=True)
        if os.path.isdir(dir_pdf_HT_500):
            shutil.rmtree(dir_pdf_HT_500)
        call('mkdir -p '+dir_pdf_HT_500, shell=True)
        if os.path.isdir(dir_root_HT_500):
            shutil.rmtree(dir_root_HT_500)
        call('mkdir -p '+dir_root_HT_500, shell=True)


        ## var spec 
        prefix='CMG_MC_'
        suffix='_his.root'
        '''
        if 'TTH' in fname: return 'nan'
        # define signals
        elif "T1" in fname: return 'sig'
        # define bkg
        elif "" in fname: return 'bkg'
        '''
        """
        signal=['CMG_MC_T1tttt_1500_100','CMG_MC_T1tttt_1200_800',\
                'CMG_MC_T5tttt_1000_280','CMG_MC_T5tttt_1300_280','CMG_MC_T5tttt_1000_285','CMG_MC_T5tttt_1300_285',\
                'CMG_MC_T1ttbbWW_1300_290','CMG_MC_T1ttbbWW_1300_295','CMG_MC_T1ttbbWW_1000_715','CMG_MC_T1ttbbWW_1000_720',\
                'CMG_MC_SqGl_1300_100']
        """

            
        signal=['T1tttt_1500_100','T1tttt_1200_800',\
                'T5tttt_1000_280','T5tttt_1300_280','T5tttt_1000_285','T5tttt_1300_285',\
                'T1ttbbWW_1300_290','T1ttbbWW_1300_295','T1ttbbWW_1000_715','T1ttbbWW_1000_720',\
                'SqGl_1300_100']
        if 'SMS' in ana:
            signal.append(ana)
#            print "--- signal ---"        
#            for p in signal:
#                print p
#            print "--- ---"
        quantity=['nJet_0','nBJet_0','nLep_0','nMu_0','nEl_0',\
                  '0JetpT_0','1JetpT_0','2JetpT_0','3JetpT_0','4JetpT_0','5JetpT_0',\
                  '0BJetpT_0','1BJetpT_0','2BJetpT_0','3BJetpT_0',\
                  'LeppT_0','MupT_0','ElpT_0',\
                  'HT_0','MET_0','ST_0',\
                  'nJet_1','nBJet_1','nLep_1','nMu_1','nEl_1',\
                  '0JetpT_1','1JetpT_1','2JetpT_1','3JetpT_1','4JetpT_1','5JetpT_1',\
                  '0BJetpT_1','1BJetpT_1','2BJetpT_1','3BJetpT_1',\
                  'LeppT_1','MupT_1','ElpT_1',\
                  'HT_1','MET_1','ST_1',\
                  'nJet_2','nBJet_2','nLep_2','nMu_2','nEl_2',\
                  '0JetpT_2','1JetpT_2','2JetpT_2','3JetpT_2','4JetpT_2','5JetpT_2',\
                  '0BJetpT_2','1BJetpT_2','2BJetpT_2','3BJetpT_2',\
                  'LeppT_2','MupT_2','ElpT_2',\
                  'HT_2','MET_2','ST_2']
        label=['N_{ jet}','N_{ b jet}','N_{ e,#mu}','N_{ #mu}','N_{ e}',\
               ' p_{T}(jet_{1}) [GeV]','p_{T}(jet_{2}) [GeV]','p_{T}(jet_{3}) [GeV]',\
               'p_{T}(jet_{4}) [GeV]','p_{T}(jet_{5}) [GeV]','p_{T}(jet_{6}) [GeV]',\
               ' p_{T}(b jet_{1}) [GeV]','p_{T}(b jet_{2}) [GeV]','p_{T}(b jet_{3}) [GeV]','p_{T}(b jet_{4}) [GeV]',\
               'p_{T}(e_{1}/#mu_{1}) [GeV]','p_{T}(#mu_{1}) [GeV]','p_{T}(e_{1}) [GeV]',\
               'H_{T} [GeV]','#slash{E}_{ T} [GeV]','S_{ T} [GeV]',\
               'N_{ jet}','N_{ b jet}','N_{ e,#mu}','N_{ #mu}','N_{ e}',\
               ' p_{T}(jet_{1}) [GeV]','p_{T}(jet_{2}) [GeV]','p_{T}(jet_{3}) [GeV]',\
               'p_{T}(jet_{4}) [GeV]','p_{T}(jet_{5}) [GeV]','p_{T}(jet_{6}) [GeV]',\
               'p_{T}(b jet_{1}) [GeV]','p_{T}(b jet_{2}) [GeV]','p_{T}(b jet_{3}) [GeV]','p_{T}(b jet_{4}) [GeV]',\
               'p_{T}(e_{1}/#mu_{1}) [GeV]','p_{T}(#mu_{1}) [GeV]','p_{T}(e_{1}) [GeV]',\
               'H_{T} [GeV]','#slash{E}_{ T} [GeV]','S_{ T} [GeV]',\
               'N_{ jet}','N_{ b jet}','N_{ e,#mu}','N_{ #mu}','N_{ e}',\
               ' p_{T}(jet_{1}) [GeV]','p_{T}(jet_{2}) [GeV]','p_{T}(jet_{3}) [GeV]',\
               'p_{T}(jet_{4}) [GeV]','p_{T}(jet_{5}) [GeV]','p_{T}(jet_{6}) [GeV]',\
               ' p_{T}(b jet_{1}) [GeV]','p_{T}(b jet_{2}) [GeV]','p_{T}(b jet_{3}) [GeV]','p_{T}(b jet_{4}) [GeV]',\
               'p_{T}(e_{1}/#mu_{1}) [GeV]','p_{T}(#mu_{1}) [GeV]','p_{T}(e_{1}) [GeV]',\
               'H_{T} [GeV]','#slash{E}_{ T} [GeV]','S_{ T} [GeV]']
        xMax=[20,20,10,10,10,\
              2000,2000,2000,2000,2000,2000,\
              2000,2000,2000,2000,\
              1000,1000,1000,\
              4000,1500,2000,\
              20,20,10,10,10,\
              2000,2000,2000,2000,2000,2000,\
              2000,2000,2000,2000,\
              1000,1000,1000,\
              4000,1500,2000,\
              20,20,10,10,10,\
              2000,2000,2000,2000,2000,2000,\
              2000,2000,2000,2000,\
              1000,1000,1000,\
              4000,1500,2000]
        Lfac=1.0
        """ NEED AN UPDATE
        # arrays for all objects
        quantity=['nJet_0','nBJet_0','nLep_0','Jet0pT_0','Jet1pT_0','Jet2pT_0','Jet3pT_0','Jet4pT_0','Jet5pT_0','Lep0pT_0','HT_0','MET_0','ST_0']
        label=['jet multiplicity','b-jet multiplicity','lepton multiplicity','leading jet p_{T} (GeV)','2^{nd} leading jet p_{T} (GeV)','3^{rd} leading jet p_{T} (GeV)','4^{th} leading jet p_{T} (GeV)','5^{th} leading jet p_{T} (GeV)','6^{th} leading jet p_{T}','leading lepton p_{T} (GeV)','H_{T} (GeV)','MET (GeV)','S_{T} (GeV)']
        xMax=[20,20,10,2000,2000,2000,2000,2000,2000,1000,4000,1500,2000]
        """
        # merge ttW, ttZ, ttH in ttV (one bkd sample)
#        if ana in signal:
#            if not  os.path.isfile(inDir+'/'+prefix+"TTV"+suffix):
#                call("rm -f "+inDir+'/'+prefix+"TTV"+suffix, shell=True)
#                call("hadd CMG_MC_TTV_his.root CMG_MC_TTW_his.root CMG_MC_TTZ_his.root CMG_MC_TTH_his.root", shell=True)


        if ana == 'TTbar':
            colour = kBlue-2
        elif ana == 'WJets':
            colour = kGreen-2
        elif ana == 'DYJets':
            colour = kRed-6
        elif ana == 'QCD':
            colour = kBlue-2
        elif ana == 'SingleTop':
            colour = kViolet+5
        elif ana in ['TTH','TTW','TTZ']: 
            colour = kOrange-3
        elif ana in signal:
            colour = kMagenta
        else:
            colour = kBlack

    #if ana == 'CMG_MC_SqGl_1300_100':

        #file_tth    = TFile.Open(inDir+'/'+prefix+'TTH'+suffix)
        #file_ttw    = TFile.Open(inDir+'/'+prefix+'TTW'+suffix)
        #file_ttz    = TFile.Open(inDir+'/'+prefix+'TTZ'+suffix)
        file_ana = TFile.Open(inDir+'/'+prefix+ana+suffix)
        if ana in signal:    
            # open availble bk root files --> stack for signal
            if os.path.isfile(inDir+'/'+prefix+'TTbar'+suffix):
                file_ttbar  = TFile.Open(inDir+'/'+prefix+'TTbar'+suffix)
            if os.path.isfile(inDir+'/'+prefix+'WJets'+suffix):
                file_wjets  = TFile.Open(inDir+'/'+prefix+'WJets'+suffix)
            if os.path.isfile(inDir+'/'+prefix+'DYJets'+suffix):
                file_dyjets = TFile.Open(inDir+'/'+prefix+'DYJets'+suffix)
            if os.path.isfile(inDir+'/'+prefix+'QCD'+suffix):
                file_qcd    = TFile.Open(inDir+'/'+prefix+'QCD'+suffix)
            if os.path.isfile(inDir+'/'+prefix+'SingleTop'+suffix):
                file_t      = TFile.Open(inDir+'/'+prefix+'SingleTop'+suffix)
            if os.path.isfile(inDir+'/'+prefix+'TTV'+suffix):
                file_ttv    = TFile.Open(inDir+'/'+prefix+'TTV'+suffix)

                
        l = 0
    
        for what in quantity:
            if ana in signal:
                #print '---> signal'
                # opening files
                
                # entries
                h_ent={}
                h_leg={} # entries in 
            
                histo    = get(file_ana, what,Lfac,kMagenta,2,2,0,0)
            
                if os.path.isfile(inDir+'/'+prefix+'TTbar'+suffix):
                    h_ttbar  = get(file_ttbar,what,Lfac,1,1,1,kBlue-2,0)
                    h_ent[h_ttbar]=h_ttbar.Integral(0,5000)
                    h_leg[h_ttbar]='t#bar{t}'
                if os.path.isfile(inDir+'/'+prefix+'WJets'+suffix):
                    h_wjets  = get(file_wjets,what,Lfac,1,1,1,kGreen-2,0)
                    h_ent[h_wjets]=h_wjets.Integral(0,5000)
                    h_leg[h_wjets]='W + jets'
                if os.path.isfile(inDir+'/'+prefix+'DYJets'+suffix):
                    h_dyjets = get(file_dyjets,what,Lfac,1,1,1,kRed-6,0)
                    h_ent[h_dyjets]=h_dyjets.Integral(0,5000)
                    h_leg[h_dyjets]='DY + jets'
                if os.path.isfile(inDir+'/'+prefix+'QCD'+suffix):
                    h_qcd    = get(file_qcd,what,Lfac,1,1,1,kCyan-6,0)
                    h_ent[h_qcd]=h_qcd.Integral(0,5000)
                    h_leg[h_qcd]='QCD'
                if os.path.isfile(inDir+'/'+prefix+'SingleTop'+suffix):
                    h_t      = get(file_t,what,Lfac,1,1,1,kViolet+5,0)
                    h_ent[h_t]=h_t.Integral(0,5000)
                    h_leg[h_t]= 't/#bar{t}'
                
                if os.path.isfile(inDir+'/'+prefix+'TTV'+suffix):
                    h_ttv    = get(file_ttv,what,Lfac,1,1,1,kOrange-3,0) 
                    h_ent[h_ttv]=h_ttv.Integral(0,5000)
                    h_leg[h_ttv]= 'ttV (V = W,Z,H)'
                    # set histo properties
                    
            #h_tth    = get(file_tth,what,Lfac,1,1,1,kOrange-3,0)
            #h_ttw    = get(file_ttw,what,Lfac,1,1,1,kOrange-3,0) 
            #h_ttz    = get(file_ttz,what,Lfac,1,1,1,kOrange-3,0) 

                
                maxi = 0
            
                for key in h_ent:
                    #print key
                    maxi = maxi + key.GetMaximum()

                #h_ent[h_tth]= h_tth.Integral(0,5000)
                #h_leg[h_tth]= 'ttH'
                #h_ent[h_ttw]= h_ttw.Integral(0,5000)
                #h_leg[h_ttw]= 'ttW'
                #h_ent[h_ttz]=h_ttz.Integral(0,5000)
                #h_leg[h_ttz]= 'ttZ'

                # calc height of stack
                #Max = h_ttbar.GetMaximum()+h_wjets.GetMaximum()+\
                #    h_dyjets.GetMaximum()+h_qcd.GetMaximum()+\
                #    h_t.GetMaximum()+h_ttv.GetMaximum()
                #Max = Max + 0.5*Max
                maxi = maxi + 0.5 * maxi

                #### maxX = max([x.FindLastBinAbove(0) for x in histList])
            
                sorted_h = sorted(h_ent.iteritems(), key=operator.itemgetter(1))
                plot(ana,sorted_h,h_leg,0.01,maxi,0,xMax[l],label[l],'evts / bin',0) #Max and maxX before 
                l = l + 1
            else:
               # print '---> background'
                #print inDir+'/'+prefix+ana+suffix
                histo = get(file_ana, what,Lfac,colour,2,1,0,0)
                maximum = 1.5 * histo.GetMaximum()
                plot(ana,0,0,0.01,maximum,0,xMax[l],label[l],'evts / bin',0) #xMax[l] or maxX
                l = l + 1
    
    
        #####################  controlPlots.html #####################
        # open, search for line, if there do nothing; if not there, produce line for 'production'
        #searchfile = open(control_dir+'controlPlots.html', 'r')

        # production.html
        # does entry production exists ? if yes, production.html exists
        f = open(control_dir+'controlPlots.html')
        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        if s.find(production) != -1:
            f.close()    
        # production.html does not exist --> produce it
        else:
            # insert entry for production in controlPlots.html #! find the right place to insert
            with open(control_dir+'controlPlots.html','r+') as file:
                lines = file.readlines()
                lines.insert(-5, '<li><a href="'+production+'/'+production+'.html" style="text-decoration:none;">'+production+'</a></li>\n') 
            # important or not ????         file.close()
            with open(control_dir+'controlPlots.html','w') as file:
                file.writelines(lines) 
                file.close()
            from prod_html import prod_html_string
            html = open(prod_dir+production+'.html','w')
            html.write(prod_html_string())
            html.close()
            # production.html exists now at the latest


        ###################### ana.html, cuts.html ##############################
        # 1. look in prod.html for "ana" entry, if not, produce it (i.e. CMG_MC_TTbar)
        # make entry in production.html for sample 
        # ana signal
        f = open(prod_dir+production+'.html')
        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        if s.find(ana) != -1:
            f.close()    
        else:
            # find line for signal or background entry
            search = open(prod_dir+production+'.html', 'r')
            k = 0
            for line in search:
                k = k + 1
                if "Signal" in line:
                    bk_line = k - 1
                if "</html>" in line:
                    sig_line = k 
            search.close()
            
            # write entry for 'ana' in production.html 
            with open(prod_dir+production+'.html','r+') as file:
                lines = file.readlines()
                #print prefix+ana
#                if prefix+ana in signal:
                #print "--- signal ---"        
                #for p in signal:
                #    print p
                #print "--- ---"
                
                if ana in signal:
                    lines.insert(-5, '<li><a href="'+ana+'/noCuts.html" style="text-decoration:none;">'+ana+' </a></li>\n')
                    print 'got it!'
                # ana is bk
                else:
                    #print 'else'
                    lines.insert(bk_line, '<li><a href="'+ana+'/noCuts.html" style="text-decoration:none;">'+ana+' </a></li>\n')                        
            with open(prod_dir+production+'.html','r+') as file:
                file.writelines(lines) 
                file.close()

                # second option
#        f = open(prod_dir+production+'.html','r')    
#        lines = f.readline()
#        for line in lines:
#            if line='<li><a href="'+ana+'/noCuts.html" style="text-decoration:none;">'+ana+' </a></li>\n':
#                f.close()    

#        f.close()
#        f = open(prod_dir+production+'.html','w')

        # 2. and/or create new one


#        f = open(prod_dir+production+'.html')
#        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
#        if s.find(production) != -1:
#            print debug(415)
#            f.close()    

        #! when production + ana already exists, ask if it should be overwritten or skipped
        #! new sample on top or at the bottom of the stack(bk, sig)?

        # produce cuts.html
        # 1. noCuts.html
        from noCuts_html import noCuts_html_string
        html = open(www_dir+'noCuts.html','w')
        html.write(noCuts_html_string())
        html.close()
        
        # 2. oneLep.html
        from oneLep_html import oneLep_html_string
        html = open(www_dir+'oneLep.html','w')
        html.write(oneLep_html_string())
        html.close()
        
        # 3. HT_500.html
        from HT_500_html import HT_500_html_string
        html = open(www_dir+'HT_500.html','w')
        html.write(HT_500_html_string())
        html.close()
        #######################################################################

    print "finished"

