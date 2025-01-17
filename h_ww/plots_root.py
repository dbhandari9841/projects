import ROOT

# global parameters
intLumi        = 1. # assume histograms are scaled in previous step
intLumiLabel   = "L = 10.8 ab^{-1}"
ana_tex        = 'e^{+}e^{-} #rightarrow Z #rightarrow #mu^{#plus}#mu^{#minus}'
energy         = 240. # GeV
collider       = 'FCC-ee'
formats        = ['png','pdf']

outdir         = '/home/submit/dipeshb/fcc-ee/projects/h_ww/H_ww_eeOutput/'
inputDir       = './output/' 

plotStatUnc    = False



procs = {}
procs['signal'] = {'nunuHmumu':['wzp6_ee_nunuH_Hmumu_ecm240'],
                   'nunuHbb':['wzp6_ee_nunuH_Hbb_ecm240'],
                   'nunuHss':['wzp6_ee_nunuH_Hss_ecm240'],   #Z-->nunu,H-->mumu,qq
                   'nunuHcc':['wzp6_ee_nunuH_Hcc_ecm240'],

                   'eeHmumu':['wzp6_ee_eeH_Hmumu_ecm240'],
                   'eeHbb':['wzp6_ee_eeH_Hbb_ecm240'],
                   'eeHss':['wzp6_ee_eeH_Hss_ecm240'],         #Z-->ee,H-->mumu,qq
                   'eeHcc':['wzp6_ee_eeH_Hcc_ecm240'],

                   'mumuHmumu':['wzp6_ee_mumuH_Hmumu_ecm240'],
                   'mumuHbb':['wzp6_ee_mumuH_Hbb_ecm240'],
                   'mumuHss':['wzp6_ee_mumuH_Hss_ecm240'],      #Z-->mumu,H-->mumu,qq
                   'mumuHcc':['wzp6_ee_mumuH_Hcc_ecm240']
                   }

procs['backgrounds'] =  {
    'nunuHWW':['wzp6_ee_nunuH_HWW_ecm240'],
    'nunuHZZ':['wzp6_ee_nunuH_HZZ_ecm240'],
    'nunuHaa':['wzp6_ee_nunuH_Haa_ecm240'], #Z-->nunu,H-->WW, ZZ, aa, Za, gg
    'nunuHZa':['wzp6_ee_nunuH_HZa_ecm240'],
    'nunuHgg':['wzp6_ee_nunuH_Hgg_ecm240'],

    'eeHWW':['wzp6_ee_eeH_HWW_ecm240'],
    'eeHZZ':['wzp6_ee_eeH_HZZ_ecm240'],
    'eeHaa':['wzp6_ee_eeH_Haa_ecm240'],     #Z-->ee,H-->WW, ZZ, aa, Za, gg
    'eeHZa':['wzp6_ee_eeH_HZa_ecm240'],
    'eeHgg':['wzp6_ee_eeH_Hgg_ecm240'],

    'mumuHWW':['wzp6_ee_mumuH_HWW_ecm240'],
    'mumuHZZ':['wzp6_ee_mumuH_HZZ_ecm240'],
    'mumuHaa':['wzp6_ee_mumuH_Haa_ecm240'], #Z-->mumu,H-->WW, ZZ, aa, Za, gg
    'mumuHZa':['wzp6_ee_mumuH_HZa_ecm240'],
    'mumuHgg':['wzp6_ee_mumuH_Hgg_ecm240'],
    }


colors = {}             #Signal
colors['nunuHmumu'] = ROOT.kRed  #Red because we were looking at it primarily, might need to adjust
colors['nunuHbb'] = ROOT.kBlue+1
colors['nunuHss'] = ROOT.kRed+2
colors['nunuHcc'] = ROOT.kRed

colors['eeHmumu'] = ROOT.kBlue+1
colors['eeHbb'] = ROOT.kRed
colors['eeHss'] = ROOT.kBlue+1
colors['eeHcc'] = ROOT.kRed+2

colors['mumuHmumu'] = ROOT.kRed+2
colors['mumuHbb'] = ROOT.kRed
colors['mumuHss'] = ROOT.kBlue+1
colors['mumuHcc'] = ROOT.kRed+2


            #Background
colors['nunuHWW'] = ROOT.kRed
colors['nunuHaa'] = ROOT.kBlue+1
colors['nunuHgg'] = ROOT.kRed+2
colors['nunuHZZ'] = ROOT.kRed
colors['nunuHZa'] = ROOT.kBlue+1

colors['eeHWW'] = ROOT.kRed
colors['eeHaa'] = ROOT.kBlue+1
colors['eeHgg'] = ROOT.kRed+2
colors['eeHZZ'] = ROOT.kRed+2
colors['eeHZa'] = ROOT.kRed+2

colors['mumuHWW'] = ROOT.kRed+2
colors['mumuHaa'] = ROOT.kRed+2
colors['mumuHgg'] = ROOT.kRed+2
colors['mumuHZZ'] = ROOT.kRed+2
colors['mumuHZa'] = ROOT.kRed+2


legend = {}
legend['mumu'] = "#mu^{#plus}#mu^{#minus}"
legend['gaga'] = "e^{#plus}e^{#minus}qq"
legend['tautau'] = "#tau^{#plus}#tau^{#minus}"
legend['mumu'] = "#mu^{#plus}#mu^{#minus}"
legend['gaga'] = "e^{#plus}e^{#minus}qq"
legend['tautau'] = "#tau^{#plus}#tau^{#minus}"
legend['mumu'] = "#mu^{#plus}#mu^{#minus}"
legend['gaga'] = "e^{#plus}e^{#minus}qq"
legend['tautau'] = "#tau^{#plus}#tau^{#minus}"
legend['mumu'] = "#mu^{#plus}#mu^{#minus}"
legend['gaga'] = "e^{#plus}e^{#minus}qq"
legend['tautau'] = "#tau^{#plus}#tau^{#minus}"
legend['mumu'] = "#mu^{#plus}#mu^{#minus}"
legend['gaga'] = "e^{#plus}e^{#minus}qq"
legend['tautau'] = "#tau^{#plus}#tau^{#minus}"
legend['mumu'] = "#mu^{#plus}#mu^{#minus}"
legend['gaga'] = "e^{#plus}e^{#minus}qq"
legend['tautau'] = "#tau^{#plus}#tau^{#minus}"
legend['mumu'] = "#mu^{#plus}#mu^{#minus}"
legend['gaga'] = "e^{#plus}e^{#minus}qq"
legend['tautau'] = "#tau^{#plus}#tau^{#minus}"
legend['mumu'] = "#mu^{#plus}#mu^{#minus}"
legend['gaga'] = "e^{#plus}e^{#minus}qq"
legend['tautau'] = "#tau^{#plus}#tau^{#minus}"

hists = {}

hists["cutFlow"] = {
    "output":   "cutFlow",
    "logy":     True,
    "stack":    True,
    "xmin":     0,
    "xmax":     5,
    "ymin":     1e1,
    #"ymax":     1e11,
    "xtitle":   ["All events", "#geq 1 #mu", "#geq 2 #mu^{#pm}", "2 OS #mu", "p_{#mu}^{max} > 0.6 p_{beam}"],
    "ytitle":   "Events ",
    "scaleSig": 1
}


hists["muons_all_costheta"] = {
    "output":   "muons_all_costheta",
    "logy":     True,
    "stack":    True,
    "rebin":    1,
    "xmin":     -1,
    "xmax":     1,
    "ymin":     0.1,
    #"ymax":     1e8,
    "xtitle":   "cos(#theta)",
    "ytitle":   "Events",
}

hists["muon_max_p_norm"] = {
    "output":   "muon_max_p_norm",
    "logy":     True,
    "stack":    True,
    "rebin":    1,
    "xmin":     0,
    "xmax":     2,
    "ymin":     0.1,
    #"ymax":     1e8,
    "xtitle":   "p(#mu_{max})/E_{beam}",
    "ytitle":   "Events",
}

hists["acolinearity"] = {
    "output":   "acolinearity",
    "logy":     True,
    "stack":    True,
    "rebin":    1,
    "xmin":     0,
    "xmax":     1,
    "ymin":     1e-2,
    #"ymax":     1e8,
    "xtitle":   "Acolinearity (rad)",
    "ytitle":   "Events",
}


hists["invariant_mass"] = {
    "output":   "invariant_mass",
    "logy":     True,
    "stack":    True,
    "rebin":    1,
    "xmin":     0,
    "xmax":     150,
    "ymin":     1e-3,
    #"ymax":     1e6,
    "xtitle":   "Invariant mass (GeV)",
    "ytitle":   "Events",
}

hists["muon1_p"] = {
    "output":   "muon1_p",
    "logy":     True,
    "stack":    True,
    "rebin":    1,
    "xmin":     0,
    "xmax":     150,
    "ymin":     1e-3,
    #"ymax":     1e6,
    "xtitle":   "muon1_momentum",
    "ytitle":   "Events",
}

hists["muon2_p"] = {
    "output":   "muon2_p",
    "logy":     True,
    "stack":    True,
    "rebin":    1,
    "xmin":     0,
    "xmax":     150,
    "ymin":     1e-3,
    #"ymax":     1e6,
    "xtitle":   "muon2_momentum",
    "ytitle":   "Events",
}