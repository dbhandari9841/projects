import ROOT

# global parameters
intLumi        = 1. # assume histograms are scaled in previous step
intLumiLabel   = "L = 10.8 ab^{-1}"
ana_tex        = 'e^{+}e^{-} #rightarrow ZH #rightarrow ZWW'
energy         = 240. # GeV
collider       = 'FCC-ee'
formats        = ['png','pdf']

outdir         = '/home/submit/dipeshb/fcc-ee/projects/h_ww/H_ww_eeOutput/'
inputDir       = './output/' 

plotStatUnc    = False



procs = {}

procs['signal'] = {'nunuHWW':['wzp6_ee_nunuH_HWW_ecm240'],
                   #'nunuHmumu':['wzp6_ee_nunuH_Hmumu_ecm240'],
                   #'nunuHbb':['wzp6_ee_nunuH_Hbb_ecm240'],
                   #'nunuHss':['wzp6_ee_nunuH_Hss_ecm240'],   #Z-->nunu,H-->mumu,qq
                   #'nunuHcc':['wzp6_ee_nunuH_Hcc_ecm240'],

                   #'eeHmumu':['wzp6_ee_eeH_Hmumu_ecm240'],
                   #'eeHbb':['wzp6_ee_eeH_Hbb_ecm240'],
                   #'eeHss':['wzp6_ee_eeH_Hss_ecm240'],         #Z-->ee,H-->mumu,qq
                   #'eeHcc':['wzp6_ee_eeH_Hcc_ecm240'],

                   #'mumuHmumu':['wzp6_ee_mumuH_Hmumu_ecm240'],
                   #'mumuHbb':['wzp6_ee_mumuH_Hbb_ecm240'],
                   #'mumuHss':['wzp6_ee_mumuH_Hss_ecm240'],      #Z-->mumu,H-->mumu,qq
                   #'mumuHcc':['wzp6_ee_mumuH_Hcc_ecm240']
                   
                   }

procs['backgrounds'] =  {
    
    #'nunuHZZ':['wzp6_ee_nunuH_HZZ_ecm240'],
    #'nunuHaa':['wzp6_ee_nunuH_Haa_ecm240'], #Z-->nunu,H-->WW, ZZ, aa, Za, gg
    #'nunuHZa':['wzp6_ee_nunuH_HZa_ecm240'],
    #'nunuHgg':['wzp6_ee_nunuH_Hgg_ecm240'],

    #'eeHWW':['wzp6_ee_eeH_HWW_ecm240'],
    #'eeHZZ':['wzp6_ee_eeH_HZZ_ecm240'],
    #'eeHaa':['wzp6_ee_eeH_Haa_ecm240'],     #Z-->ee,H-->WW, ZZ, aa, Za, gg
    #'eeHZa':['wzp6_ee_eeH_HZa_ecm240'],
    #'eeHgg':['wzp6_ee_eeH_Hgg_ecm240'],

    #'mumuHWW':['wzp6_ee_mumuH_HWW_ecm240'],
    #'mumuHZZ':['wzp6_ee_mumuH_HZZ_ecm240'],
    #'mumuHaa':['wzp6_ee_mumuH_Haa_ecm240'], #Z-->mumu,H-->WW, ZZ, aa, Za, gg
    #'mumuHZa':['wzp6_ee_mumuH_HZa_ecm240'],
    #'mumuHgg':['wzp6_ee_mumuH_Hgg_ecm240'],
    

    'ee_ZZ':['p8_ee_ZZ_ecm240'],  #Direct ee to ZZ
    'ee_WW':['p8_ee_WW_ecm240'], #Direct ee to WW
    
    }

colors = {}             #Signal
colors['nunuHWW'] = ROOT.kRed
#colors['nunuHmumu'] = ROOT.kRed  #Red because we were looking at it primarily, might need to adjust
#colors['nunuHbb'] = ROOT.kRed+1
#colors['nunuHss'] = ROOT.kRed+2
#colors['nunuHcc'] = ROOT.kRed+3

#colors['eeHmumu'] = ROOT.kYellow
#colors['eeHbb'] = ROOT.kYellow+1
#colors['eeHss'] = ROOT.kYellow+2
#colors['eeHcc'] = ROOT.kYellow+3

#colors['mumuHmumu'] = ROOT.kRed    
#colors['mumuHbb'] = ROOT.kBlue+1
#colors['mumuHss'] = ROOT.kGreen+2
#colors['mumuHcc'] = ROOT.kYellow+3


            #Background

#colors['nunuHZZ'] = ROOT.kGreen
#colors['nunuHZa'] = ROOT.kYellow
#colors['nunuHaa'] = ROOT.kPink+1
#colors['nunuHgg'] = ROOT.kPink+2

#colors['eeHWW'] = ROOT.kMagenta
#colors['eeHZZ'] = ROOT.kMagenta+3
#colors['eeHZa'] = ROOT.kMagenta+4
#colors['eeHaa'] = ROOT.kMagenta+1
#colors['eeHgg'] = ROOT.kMagenta+2

#colors['mumuHWW'] = ROOT.kPink
#colors['mumuHZZ'] = ROOT.kMagenta+3
#colors['mumuHZa'] = ROOT.kOrange+4
#colors['mumuHaa'] = ROOT.kPink+2
#colors['mumuHgg'] = ROOT.kOrange+2

colors['ee_ZZ'] = ROOT.kBlue
colors['ee_WW'] = ROOT.kGreen


legend = {}
#legend['nunuHmumu'] = "#nu #nu H #rightarrow #mu^{#plus}#mu^{#minus}"
legend['nunuHWW'] = "#nu #nu H #rightarrow WW"
#legend['nunuHbb'] = "#nu #nu H #rightarrow b#bar{b}"
#legend['nunuHss'] = "#nu #nu H #rightarrow s#bar{s}"
#legend['nunuHcc'] = "#nu #nu H #rightarrow c#bar{c}"
#legend['eeHmumu'] = "e^{#plus}e^{#minus}H #rightarrow #mu^{#plus}#mu^{#minus}"
#legend['eeHbb'] = "e^{#plus}e^{#minus}H #rightarrow b#bar{b}"
#legend['eeHss'] = "e^{#plus}e^{#minus}H #rightarrow s#bar{s}"
#legend['eeHcc'] = "e^{#plus}e^{#minus}H #rightarrow c#bar{c}"
#legend['mumuHmumu'] = "#mu^{#plus}#mu^{#minus}H #rightarrow #mu^{#plus}#mu^{#minus}#mu^{#plus}#mu^{#minus}"
#legend['mumuHbb'] = "#mu^{#plus}#mu^{#minus}H #rightarrow #mu^{#plus}#mu^{#minus}b#bar{b}"
#legend['mumuHss'] = "#mu^{#plus}#mu^{#minus}H #rightarrow #mu^{#plus}#mu^{#minus}s#bar{s}"
#legend['mumuHcc'] = "#mu^{#plus}#mu^{#minus}H #rightarrow #mu^{#plus}#mu^{#minus}c#bar{c}"


#legend['nunuHZZ'] = "#nu #nu H #rightarrow ZZ"
#legend['nunuHaa'] = "#nu #nu H #rightarrow aa"
#legend['nunuHZa'] = "#nu #nu H #rightarrow Za"
#legend['nunuHgg'] = "#nu #nu H #rightarrow gg"
#legend['eeHWW'] = "e^{#plus}e^{#minus}H #rightarrow WW"
#legend['eeHZZ'] = "e^{#plus}e^{#minus}H #rightarrow ZZ"
#legend['eeHaa'] = "e^{#plus}e^{#minus}H #rightarrow aa"
#legend['eeHZa'] = "e^{#plus}e^{#minus}H #rightarrow Za"
#legend['eeHgg'] = "e^{#plus}e^{#minus}H #rightarrow gg"
#legend['mumuHWW'] = "#mu^{#plus}#mu^{#minus}H #rightarrow #mu^{#plus}#mu^{#minus}WW"
#legend['mumuHZZ'] = "#mu^{#plus}#mu^{#minus}H #rightarrow #mu^{#plus}#mu^{#minus}ZZ"
#legend['mumuHaa'] = "#mu^{#plus}#mu^{#minus}H #rightarrow #mu^{#plus}#mu^{#minus}aa"
#legend['mumuHZa'] = "#mu^{#plus}#mu^{#minus}H #rightarrow #mu^{#plus}#mu^{#minus}Za"
#legend['mumuHgg'] = "#mu^{#plus}#mu^{#minus}H #rightarrow #mu^{#plus}#mu^{#minus}gg"

legend['ee_ZZ'] = "e^{#plus}e^{#minus} #rightarrow ZZ"
legend['ee_WW'] = "e^{#plus}e^{#minus} #rightarrow WW"


histogram_stack = {
    "wzp6_ee_nunuH_HWW_ecm240": {"stack": False},
    "p8_ee_ZZ_ecm240": {"stack": True},
    "p8_ee_WW_ecm240": {"stack": True},
}

hists = {}

hists["cutFlow"] = {
    "output":   "cutFlow",
    "stack":    [  
        {"name": "wzp6_ee_nunuH_HWW_ecm240", "stack": histogram_stack["wzp6_ee_nunuH_HWW_ecm240"]["stack"]},
        {"name": "p8_ee_ZZ_ecm240", "stack": histogram_stack["p8_ee_ZZ_ecm240"]["stack"]},
        {"name": "p8_ee_WW_ecm240", "stack": histogram_stack["p8_ee_WW_ecm240"]["stack"]},
    ],
    "logy":     True,
    "xmin":     0,
    "xmax":     8,
    "ymin":     1e2,
    "ymax":     1e8,
    "xtitle":   ["All events", "#geq 2 #mu^{#pm}", "2 OS #mu","missingMass>102", "16<#mu_p<50", 
                 "#gamma_n>=7 || Max#gamma_E>7", "Jets<=2", "|PdgID|=13"],
                   #mu_p<30#
                   
    "ytitle":   "Events ",
    "scaleSig": 1
}


hists["muons_all_costheta"] = {
    "output":   "muons_all_costheta",
    "logy":     False,
    "stack":    True,
    "rebin":    1,
    "xmin":     -1,
    "xmax":     1,
    "ymin":     0.1,
    #"ymax":     1e8,
    "xtitle":   "cos(#theta)",
    "ytitle":   "Events",
}

#hists["muon_max_p_norm"] = {
 #   "output":   "muon_max_p_norm",
  #  "logy":     True,
  #  "stack":    True,
  #  "rebin":    1,
  #  "xmin":     0,
  #  "xmax":     2,
  #  "ymin":     0.1,
  #  "ymax":     1e8,
  #  "xtitle":   "p(#mu_{max})/E_{beam}",
  #  "ytitle":   "Events",
#}

hists["acolinearity"] = {
    "output":   "acolinearity",
    "logy":     False,
    "stack":    [  
        {"name": "wzp6_ee_nunuH_HWW_ecm240", "stack": histogram_stack["wzp6_ee_nunuH_HWW_ecm240"]["stack"]},
        {"name": "p8_ee_ZZ_ecm240", "stack": histogram_stack["p8_ee_ZZ_ecm240"]["stack"]},
        {"name": "p8_ee_WW_ecm240", "stack": histogram_stack["p8_ee_WW_ecm240"]["stack"]},
    ],
    "rebin":    1,
    "xmin":     0,
    "xmax":     1,
    "ymin":     1e-2,
    #"ymax":     1e8,
    "xtitle":   "Acolinearity (rad)",
    "ytitle":   "Events",
}
#hists["MissingET_dist"] = {
   # "output":   "MissingET_dist",
   # "logy":     False,
   # "stack":    [  
   #     {"name": "wzp6_ee_nunuH_HWW_ecm240", "stack": histogram_stack["wzp6_ee_nunuH_HWW_ecm240"]["stack"]},
   #     {"name": "p8_ee_ZZ_ecm240", "stack": histogram_stack["p8_ee_ZZ_ecm240"]["stack"]},
   ##     {"name": "p8_ee_WW_ecm240", "stack": histogram_stack["p8_ee_WW_ecm240"]["stack"]},
   # ],
   ## "rebin":    1,
    #"xmin":     0,
    #"xmax":     100,
    #"ymin":     1e-2,
    #"ymax":     1e8,
   # "xtitle":   "Missing Energy (GeV)",
   # "ytitle":   "Events",
#}

hists["muon_p_dist"] = {
    "output":   "muon_p_dist",
    "logy":     False,
    "stack":    [  
        {"name": "wzp6_ee_nunuH_HWW_ecm240", "stack": histogram_stack["wzp6_ee_nunuH_HWW_ecm240"]["stack"]},
        {"name": "p8_ee_ZZ_ecm240", "stack": histogram_stack["p8_ee_ZZ_ecm240"]["stack"]},
        {"name": "p8_ee_WW_ecm240", "stack": histogram_stack["p8_ee_WW_ecm240"]["stack"]},
    ],
    "rebin":    1,
    "xmin":     0,
    "xmax":     100,
    "ymin":     1e-2,
    #"ymax":     1e8,
    "xtitle":   "muon momentum",
    "ytitle":   "Events",
}
hists["photon_energy"] = {
    "output":   "photon_energy",
    "logy":     False,
    "stack":    [  
        {"name": "wzp6_ee_nunuH_HWW_ecm240", "stack": histogram_stack["wzp6_ee_nunuH_HWW_ecm240"]["stack"]},
        {"name": "p8_ee_ZZ_ecm240", "stack": histogram_stack["p8_ee_ZZ_ecm240"]["stack"]},
        {"name": "p8_ee_WW_ecm240", "stack": histogram_stack["p8_ee_WW_ecm240"]["stack"]},
    ],
    "rebin":    1,
    "xmin":     0,
    "xmax":     30,
    "ymin":     1e-2,
    #"ymax":     1e8,
    "xtitle":   "Photon Energy(GeV)",
    "ytitle":   "Events",
} 
hists["photon_num"] = {
    "output":   "photon_num",
    "logy":     False,
    "stack":    [  
        {"name": "wzp6_ee_nunuH_HWW_ecm240", "stack": histogram_stack["wzp6_ee_nunuH_HWW_ecm240"]["stack"]},
        {"name": "p8_ee_ZZ_ecm240", "stack": histogram_stack["p8_ee_ZZ_ecm240"]["stack"]},
        {"name": "p8_ee_WW_ecm240", "stack": histogram_stack["p8_ee_WW_ecm240"]["stack"]},
    ],
    "rebin":    1,
    "xmin":     0,
    "xmax":     18,
    "ymin":     1e-2,
    #"ymax":     1e8,
    "xtitle":   "Photon number",
    "ytitle":   "Events",
}

hists["invariant_mass"] = {
    "output":   "invariant_mass",
    "logy":     True,
    "stack":    [  
        {"name": "wzp6_ee_nunuH_HWW_ecm240", "stack": histogram_stack["wzp6_ee_nunuH_HWW_ecm240"]["stack"]},
        {"name": "p8_ee_ZZ_ecm240", "stack": histogram_stack["p8_ee_ZZ_ecm240"]["stack"]},
        {"name": "p8_ee_WW_ecm240", "stack": histogram_stack["p8_ee_WW_ecm240"]["stack"]},
    ],
    "rebin":    1,
    "xmin":     0,
    "xmax":     130,
    "ymin":     1e1,
    "ymax":     1e5,
    "xtitle":   "Invariant mass (GeV)",
    "ytitle":   "Events",
}
if 'signal' == "wzp6_ee_nunuH_HWW_ecm240":
    hists["ww_decay_mode"] = {
        "output":   "ww_decay_mode",
        "logy":     True,
        "stack":    False,
        "rebin":    1,
        "xmin":     -20,
        "xmax":     20,
        "ymin":     1e1,
        "ymax":     1e8,
        "xtitle":   "ww_decay_mode",
        "ytitle":   "Events",
}
hists["missingMass"] = {
    "output":   "missingMass",
    "logy":     True,
    "stack":    [  
        {"name": "wzp6_ee_nunuH_HWW_ecm240", "stack": histogram_stack["wzp6_ee_nunuH_HWW_ecm240"]["stack"]},
        {"name": "p8_ee_ZZ_ecm240", "stack": histogram_stack["p8_ee_ZZ_ecm240"]["stack"]},
        {"name": "p8_ee_WW_ecm240", "stack": histogram_stack["p8_ee_WW_ecm240"]["stack"]},
    ],
    "rebin":    1,
    "xmin":     0,
    "xmax":     200,
    "ymin":     1e1,
    "ymax":     1e8,
    "xtitle":   "missingMass",
    "ytitle":   "Events",
}
#hists["muon1_p"] = {
#    "output":   "muon1_p",
#    "logy":     True,
#    "stack":    True,
#    "rebin":    1,
#    "xmin":     0,
#    "xmax":     150,
#    "ymin":     1e-3,
#    #"ymax":     1e6,
#    "xtitle":   "muon1_momentum",
#    "ytitle":   "Events",
#}

#hists["muon2_p"] = {
#    "output":   "muon2_p",
#    "logy":     True,
#    "stack":    True,
#    "rebin":    1,
#    "xmin":     0,
#    "xmax":     150,
#    "ymin":     1e-3,
#    #"ymax":     1e6,
 #   "xtitle":   "muon2_momentum",
 #   "ytitle":   "Events",
#}
