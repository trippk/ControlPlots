#!/usr/bin/python

import sys, os, shutil, getopt
from subprocess import call
from ROOT import gROOT, gPad, TH1D, TFile, TCanvas, TLatex, TLegend, THStack, TVirtualMutex, kRed, kOrange, kBlue, kCyan, kGreen, kViolet, kOrange, kBlack, kMagenta
# have to specify
#gROOT.LoadMacro("CMS_lumi_v2.C")
#global histo, ana, colour

global histo, h_ttbar, h_wjets, h_dyjets, h_qcd, h_t, h_tth, h_ttz, h_ttw 

def help():
    print 'First argument analysis:'
    print './check.py CMG_TYPE_SAMPLE '
    print ' TYPE = MC, data'
    print ' SAMPLE = TTbar, WJets,'
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
	gROOT.SetBatch(True)                                        # suppress root window popping up
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
#	dum.GetXaxis().SetRangeUser(minX,maxX)
#        last = dum.FindLastBinAbove(0,1)
#        last = last + 0.5 * last
        dum.GetXaxis().SetRange(0,last+10)
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
	leg = TLegend(0.63,0.525,0.87,0.875) #for 33 TeV 
#        leg = TLegend(0.65,0.65,0.9,0.9)
        leg.SetBorderSize(1)
        leg.SetTextFont(62)
        leg.SetTextSize(0.035)
        leg.SetLineColor(0)
        leg.SetLineStyle(1)
        leg.SetLineWidth(1)
        leg.SetFillColor(0)
        leg.SetFillStyle(1001)
	if ana == 'CMG_MC_TTbar':
            title='t#bar{t}'
            leg.AddEntry(histo,title,'l')
	elif ana == 'CMG_MC_WJets':
            leg.AddEntry(histo,'W+jets','l')
        elif ana == 'CMG_MC_DYJets':
            leg.AddEntry(histo,'DY+jets','l')
        elif ana == 'CMG_MC_QCD':
            leg.AddEntry(histo,'QCD','l')
        elif ana == 'CMG_MC_SingleTop':
            leg.AddEntry(histo,'t / #bar{t}','l')
        elif ana == 'CMG_MC_TTH':
            leg.AddEntry(histo,'ttH','l')
        elif ana == 'CMG_MC_TTW':
            leg.AddEntry(histo,'ttW','l')
        elif ana == 'CMG_MC_TTZ':
            leg.AddEntry(histo,'ttZ','l') 
        elif ana == 'CMG_MC_T1tttt_1500_100':
            leg.AddEntry(histo,'T1t^{4}(1500,100)','l') 
        elif ana == 'CMG_MC_T1tttt_1200_800':
            leg.AddEntry(histo,'T1t^{4}(1200,800)','l') 
        elif ana == 'CMG_MC_T5tttt_1000_280':
            leg.AddEntry(histo,'T5t^{4}(1000,280)','l') 
        elif ana == 'CMG_MC_T5tttt_1300_280':
            leg.AddEntry(histo,'T5t^{4}(1300,280)','l') 
        elif ana == 'CMG_MC_T5tttt_1000_285':
            leg.AddEntry(histo,'T5t^{4}(1000,285)','l') 
        elif ana == 'CMG_MC_T5tttt_1300_285':
            leg.AddEntry(histo,'T5t^{4}(1300,285)','l') 
        elif ana == 'CMG_MC_T1ttbbWW_1300_290':
            leg.AddEntry(histo,'T1t^{2}b^{2}W^{2}(1300,290)','l') 
        elif ana == 'CMG_MC_T1ttbbWW_1300_295':
            leg.AddEntry(histo,'T1t^{2}b^{2}W^{2}(1300,295)','l') 
        elif ana == 'CMG_MC_T1ttbbWW_1000_715':
            leg.AddEntry(histo,'T1t^{2}b^{2}W^{2}(1000,715)','l') 
        elif ana == 'CMG_MC_T1ttbbWW_1000_720':
            leg.AddEntry(histo,'T1t^{2}b^{2}W^{2}(1000,720)','l') 
        elif ana == 'CMG_MC_SqGl_1300_100':
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

	c1.SaveAs(www_dir+ana+"/png/"+what+".png")
	c1.SaveAs(www_dir+ana+"/pdf/"+what+".pdf")
	c1.SaveAs(www_dir+ana+"/root/"+what+".root")

#	c1.SaveAs("/afs/desy.de/group/cms/www/html/subgroups/susy/ControlPlots/Plots/"+ana+"/png/"+what+".png")
#	c1.SaveAs("/afs/desy.de/group/cms/www/html/subgroups/susy/ControlPlots/Plots/"+ana+"/pdf/"+what+".pdf")
#	c1.SaveAs("/afs/desy.de/group/cms/www/html/subgroups/susy/ControlPlots/Plots/"+ana+"/root/"+what+".root")

##################################
#-------- program begin ---------

if len(sys.argv)>0:
	ana = sys.argv[1]
else:
    help()

print "drawing histograms"

# defining
## dirs
www_dir = '/afs/desy.de/group/cms/www/html/subgroups/susy/ControlPlots/Plots/'
dir_png = www_dir+ana+'/png/'
dir_pdf = www_dir+ana+'/pdf/'
dir_root = www_dir+ana+'/root/'
## var spec 
prefix='CMG_MC_'
suffix='_his.root'
signal=['CMG_MC_T1tttt_1500_100','CMG_MC_T1tttt_1200_800',\
        'CMG_MC_T5tttt_1000_280','CMG_MC_T5tttt_1300_280','CMG_MC_T5tttt_1000_285','CMG_MC_T5tttt_1300_285',\
        'CMG_MC_T1ttbbWW_1300_290','CMG_MC_T1ttbbWW_1300_295','CMG_MC_T1ttbbWW_1000_715','CMG_MC_T1ttbbWW_1000_720',\
        'CMG_MC_SqGl_1300_100']
quantity=['nJet_0','nBJet_0','nLep_0','nMu_0','nEl_0',\
          'Jet0pT_0','Jet1pT_0','Jet2pT_0','Jet3pT_0','Jet4pT_0','Jet5pT_0',\
          'BJet0pT_0','BJet1pT_0','BJet2pT_0','BJet3pT_0',\
          'Lep0pT_0',\
          'HT_0','MET_0','ST_0']
label=['N_{ jet}','N_{ b jet}','N_{ e,#mu}','N_{ #mu}','N_{ e}',\
       ' p_{T}(jet_{1}) [GeV]','p_{T}(jet_{2}) [GeV]','p_{T}(jet_{3}) [GeV]',\
       'p_{T}(jet_{4}) [GeV]','p_{T}(jet_{5}) [GeV]','p_{T}(jet_{6}) [GeV]',\
       ' p_{T}(b jet_{1}) [GeV]','p_{T}(b jet_{2}) [GeV]','p_{T}(b jet_{3}) [GeV]',\
       'p_{T}(b jet) [GeV]',\
       'p_{T}(e_{1}/#mu_{1}) [GeV]',\
       'H_{T} [GeV]','#slash{E}_{ T} [GeV]','S_{ T} [GeV]']
xMax=[20,20,10,10,10,\
      2000,2000,2000,2000,2000,2000,
      2000,2000,2000,2000,\
      1000,\
      4000,1500,2000]
Lfac=1.0

"""
# arrays for all objects
quantity=['nJet_0','nBJet_0','nLep_0','Jet0pT_0','Jet1pT_0','Jet2pT_0','Jet3pT_0','Jet4pT_0','Jet5pT_0','Lep0pT_0','HT_0','MET_0','ST_0']
label=['jet multiplicity','b-jet multiplicity','lepton multiplicity','leading jet p_{T} (GeV)','2^{nd} leading jet p_{T} (GeV)','3^{rd} leading jet p_{T} (GeV)','4^{th} leading jet p_{T} (GeV)','5^{th} leading jet p_{T} (GeV)','6^{th} leading jet p_{T}','leading lepton p_{T} (GeV)','H_{T} (GeV)','MET (GeV)','S_{T} (GeV)']
xMax=[20,20,10,2000,2000,2000,2000,2000,2000,1000,4000,1500,2000]
"""
# merge ttW, ttZ, ttH in ttV (one bkd sample)
if ana in signal:
    if not  os.path.isfile(prefix+"TTV"+suffix):
        call("rm -f "+prefix+"TTV"+suffix, shell=True)
        call("hadd CMG_MC_TTV_his.root CMG_MC_TTW_his.root CMG_MC_TTZ_his.root CMG_MC_TTH_his.root", shell=True)

# create dir, remove if they exist
### replace os with subprocess!?
if os.path.isdir(dir_png):
    shutil.rmtree(dir_png)
call('mkdir -p '+dir_png, shell=True)
if os.path.isdir(dir_pdf):
    shutil.rmtree(dir_pdf)
call('mkdir -p '+dir_pdf, shell=True)
if os.path.isdir(dir_root):
    shutil.rmtree(dir_root)
call('mkdir -p '+dir_root, shell=True)

if ana == 'CMG_MC_TTbar':
    colour = kBlue-2
elif ana == 'CMG_MC_WJets':
    colour = kGreen-2
elif ana == 'CMG_MC_DYJets':
    colour = kRed-6
elif ana == 'CMG_MC_QCD':
    colour = kCyan-6
elif ana == 'CMG_MC_SingleTop':
    colour = kViolet+5
elif ana in ['CMG_MC_TTH','CMG_MC_TTW','CMG_MC_TTZ']: 
    colour = kOrange-3
elif ana in signal:
    colour = kMagenta

#if ana == 'CMG_MC_SqGl_1300_100':

l = 0
for what in quantity:
    if ana in signal:
        # opening files
        file_ana    = TFile.Open(ana+suffix)
        file_ttbar  = TFile.Open(prefix+'TTbar'+suffix)
        file_wjets  = TFile.Open(prefix+'WJets'+suffix)
        file_dyjets = TFile.Open(prefix+'DYJets'+suffix)
        file_qcd    = TFile.Open(prefix+'QCD'+suffix)
        file_t      = TFile.Open(prefix+'SingleTop'+suffix)
        #file_tth    = TFile.Open(prefix+'TTH'+suffix)
        #file_ttw    = TFile.Open(prefix+'TTW'+suffix)
        #file_ttz    = TFile.Open(prefix+'TTZ'+suffix)
        file_ttv    = TFile.Open(prefix+'TTV'+suffix)
        # set histo properties
        histo    = get(file_ana, what,Lfac,kMagenta,2,2,0,0)
        h_ttbar  = get(file_ttbar,what,Lfac,1,1,1,kBlue-2,0)
        h_wjets  = get(file_wjets,what,Lfac,1,1,1,kGreen-2,0)
        h_dyjets = get(file_dyjets,what,Lfac,1,1,1,kRed-6,0)
        h_qcd    = get(file_qcd,what,Lfac,1,1,1,kCyan-6,0)
        h_t      = get(file_t,what,Lfac,1,1,1,kViolet+5,0)
        #h_tth    = get(file_tth,what,Lfac,1,1,1,kOrange-3,0)
        #h_ttw    = get(file_ttw,what,Lfac,1,1,1,kOrange-3,0) 
        #h_ttz    = get(file_ttz,what,Lfac,1,1,1,kOrange-3,0) 
        h_ttv    = get(file_ttv,what,Lfac,1,1,1,kOrange-3,0) 
        # entries
        h_ent={}
        h_leg={} # entries in 
        h_ent[h_ttbar]=h_ttbar.Integral(0,5000)
        h_leg[h_ttbar]='t#bar{t}'
        h_ent[h_wjets]=h_wjets.Integral(0,5000)
        h_leg[h_wjets]='W + jets'
        h_ent[h_dyjets]=h_dyjets.Integral(0,5000)
        h_leg[h_dyjets]='DY + jets'
        h_ent[h_qcd]=h_qcd.Integral(0,5000)
        h_leg[h_qcd]='QCD'
        h_ent[h_t]=h_t.Integral(0,5000)
        h_leg[h_t]= 't/#bar{t}'
        #h_ent[h_tth]= h_tth.Integral(0,5000)
        #h_leg[h_tth]= 'ttH'
        #h_ent[h_ttw]= h_ttw.Integral(0,5000)
        #h_leg[h_ttw]= 'ttW'
        #h_ent[h_ttz]=h_ttz.Integral(0,5000)
        #h_leg[h_ttz]= 'ttZ'
        h_ent[h_ttv]=h_ttv.Integral(0,5000)
        h_leg[h_ttv]= 'ttV (V = W,Z,H)'
        # calc height of stack
        Max = h_ttbar.GetMaximum()+h_wjets.GetMaximum()+\
              h_dyjets.GetMaximum()+h_qcd.GetMaximum()+\
              h_t.GetMaximum()+h_ttv.GetMaximum()
#h_tth.GetMaximum()+h_ttw.GetMaximum()+h_ttz.GetMaximum()
        Max = Max + 0.5*Max
        maxX = max([x.FindLastBinAbove(0) for x in histList])
        import operator
        sorted_h = sorted(h_ent.iteritems(), key=operator.itemgetter(1))
        plot(ana,sorted_h,h_leg,0.01,Max,0,maxX,label[l],'evts / bin',0) 
        l = l + 1
    else:
        file_ana = TFile.Open(ana+suffix)
        histo = get(file_ana, what,Lfac,colour,2,1,0,0)
        maximum = 1.5 * histo.GetMaximum()
        plot(ana,0,0,0.01,maximum,0,maxX,label[l],'evts / bin',0) #xMax[l]
        l = l + 1

###################
### write html file
#### html string is in html.py
from html import html_string
# in addition with an index.html # 'a'(append): writing at the end of an existing file 

##os.path.join(save_path, name_of_file+".txt")
print "printing html code"
# open controlPlots_''.html in www/ControlPlots
html = open('/afs/desy.de/group/cms/www/html/subgroups/susy/ControlPlots/controlPlots_'+ana+'.html','w')
html.write(html_string(ana))
html.close()

#################################
# make new entry in 'index.html'

with open('/afs/desy.de/group/cms/www/html/subgroups/susy/index.html','r+') as file:
    lines = file.readlines()
#    lines[len(lines)-7] = '<h2><a href="ControlPlots/controlPlots_'+ana+'.html" style="text-decoration:none;"> test2'+ana+'</a></h2>'+'\n'
#    file.close()
#    lines = lines[:-7] + ['<h2><a href="ControlPlots/controlPlots_'+ana+'.html" style="text-decoration:none;"> test3'+ana+'</a></h2>\n'] + lines[-7:]
    lines.insert(-6, '<h5><a href="ControlPlots/controlPlots_'+ana+'.html" style="text-decoration:none;">'+ana+'</a></h5>\n')
#with open('/afs/desy.de/user/t/trippk/www/index_new.html','w') as file:
with open('/afs/desy.de/group/cms/www/html/subgroups/susy/index.html','w') as file:
    file.writelines(lines) 
    file.close()
print "finished"
