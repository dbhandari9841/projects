
import ROOT
ROOT.TH1.SetDefaultSumw2(ROOT.kTRUE)



# list of all guns
processList = {
    'wzp6_ee_nunuH_Hmumu_ecm240': {'fraction':1},
    'wzp6_ee_nunuH_Hbb_ecm240': {'fraction':1},
    'wzp6_ee_nunuH_Hss_ecm240': {'fraction':1},
    'wzp6_ee_nunuH_Hcc_ecm240': {'fraction':1},
    'wzp6_ee_eeH_Hmumu_ecm240': {'fraction':1},
    'wzp6_ee_mumuH_Hmumu_ecm240': {'fraction':1},        #signal
    'wzp6_ee_eeH_Hbb_ecm240': {'fraction':1},
    'wzp6_ee_eeH_Hss_ecm240': {'fraction':1},
    'wzp6_ee_eeH_Hcc_ecm240': {'fraction':1},
    'wzp6_ee_mumuH_Hbb_ecm240': {'fraction':1},
    'wzp6_ee_mumuH_Hss_ecm240': {'fraction':1},
    'wzp6_ee_mumuH_Hcc_ecm240': {'fraction':1},

    'wzp6_ee_nunuH_HWW_ecm240': {'fraction':1},
    'wzp6_ee_nunuH_Haa_ecm240': {'fraction':1}, #background
    'wzp6_ee_nunuH_Hgg_ecm240': {'fraction':1},
    'wzp6_ee_nunuH_HZZ_ecm240': {'fraction':1},
    'wzp6_ee_nunuH_HZa_ecm240': {'fraction':1},
    'wzp6_ee_eeH_HZZ_ecm240': {'fraction':1},        
    'wzp6_ee_eeH_HWW_ecm240': {'fraction':1},
    'wzp6_ee_eeH_Haa_ecm240': {'fraction':1},
    'wzp6_ee_mumuH_HZZ_ecm240': {'fraction':1}, 
    'wzp6_ee_mumuH_HWW_ecm240': {'fraction':1},
    'wzp6_ee_mumuH_Haa_ecm240':  {'fraction':1},
    'wzp6_ee_mumuH_HZa_ecm240': {'fraction':1},
    'wzp6_ee_mumuH_Hgg_ecm240': {'fraction':1},
    'wzp6_ee_eeH_Hgg_ecm240': {'fraction':1},
    'wzp6_ee_eeH_HZa_ecm240': {'fraction':1}    
}

#if I understand this correctly, this code really doesn't care what's signal and what's background, it just plots everything. 
#The signal/background distinction is made in the plotting code, not here.
#meaning in a collider experiment, everything happens, and we then decide what to look at afterwards by 
#doing the slicing and dicing in the plotting code.

inputDir = "/ceph/submit/data/group/fcc/ee/generation/DelphesEvents/winter2023/IDEA/"
procDict = "/ceph/submit/data/group/fcc/ee/generation/DelphesEvents/winter2023/IDEA/samplesDict.json"

# additional/custom C++ functions
includePaths = ["../functions/functions.h", "../functions/functions_gen.h"]


# output directory
outputDir   = "output/"


# optional: ncpus, default is 4, -1 uses all cores available
nCPUS       = 128

# scale the histograms with the cross-section and integrated luminosity
doScale = False
intLumi = 10.8e9 # 44.84 pb-1 = LEP, 100e6=100 ab-1 = FCCee

# define histograms
bins_p_mu = (200, 0, 200) # 1 GeV bins
bins_m_ll = (200, 0, 200) # 1 GeV bins
bins_p_ll = (200, 0, 200) # 1 GeV bins

bins_theta = (500, -5, 5)
bins_phi = (500, -5, 5)

bins_count = (50, 0, 50)
bins_pdgid = (60, -30, 30)
bins_charge = (10, -5, 5)

bins_cos = (100, -1, 1)
bins_norm = (200, 0, 2)
bins_nparticles = (200, 0, 200)
bins_aco = (800,-4,4)

def build_graph(df, dataset):

    hists = []

    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    #Here, only muons, need to add the relevant particles for the four different outcome states
    #we are focusing on...
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    df = df.Alias("Muons", "Muon#0.index")
    #something wrong... maybe need something like "Muons" downstairs
    #maybe there is no nutrinos... missing energy remember.
    # defining the reconstructed muons, and variables associated to them
    df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muons, ReconstructedParticles)")
    df = df.Define("muons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(muons_all)")
    df = df.Define("muons_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons_all)")
    df = df.Define("muons_all_costheta", "FCCAnalyses::get_costheta(muons_all)")
    df = df.Define("muons_all_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons_all)")
    df = df.Define("muons_all_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons_all)")
    df = df.Define("muons_all_no", "FCCAnalyses::ReconstructedParticle::get_n(muons_all)")

    # define cos(theta) of the muons
    hists.append(df.Histo1D(("muons_all_costheta", "", *bins_cos), "muons_all_costheta"))
    df = df.Define("muons", "FCCAnalyses::sel_range(0, 0.97, true)(muons_all, muons_all_costheta)")
    df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
    df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
    df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")
    df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")

    # Z(nunu) WW (mu nu mu nu)
    #df = df.Define("neutrinos", "FCCAnalyses::ReconstructedParticle::get_neutrinos(ReconstructedParticles)")
    df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::get_muons(ReconstructedParticles)")
    df = df.Define("Z_nn_mass", "FCCAnalyses::invariant_mass(neutrinos)")
    df = df.Define("WW_mumu_mass", "FCCAnalyses::invariant_mass(muons)")

    hists.append(df.Histo1D(("Z_nn_mass", "Z(nunu) mass", 100, 0, 200), "Z_nn_mass"))
    hists.append(df.Histo1D(("WW_mumu_mass", "WW(munumunu) mass", 100, 0, 200), "WW_mumu_mass"))

    # Z (nunu) WW (bb)
    df = df.Define("bottom", "FCCAnalyses::ReconstructedParticle::get_quarks(ReconstructedParticles)")
    df = df.Define("WW_bb_mass", "FCCAnalyses::invariant_mass(bottom)")

    hists.append(df.Histo1D(("WW_qq_mass", "WW(bb) mass", 100, 0, 200), "WW_qq_mass"))

    # Z (nunu) WW (ss)
    df = df.Define("strange", "FCCAnalyses::ReconstructedParticle::get_quarks(ReconstructedParticles)")
    df = df.Define("WW_ss_mass", "FCCAnalyses::invariant_mass(strange)")

    hists.append(df.Histo1D(("WW_qq_mass", "WW(ss) mass", 100, 0, 200), "WW_qq_mass"))

    # Z (nunu) WW (cc)
    df = df.Define("charm", "FCCAnalyses::ReconstructedParticle::get_quarks(ReconstructedParticles)")
    df = df.Define("WW_cc_mass", "FCCAnalyses::invariant_mass(charm)")

    hists.append(df.Histo1D(("WW_qq_mass", "WW(cc) mass", 100, 0, 200), "WW_qq_mass"))

    # Z (e+e−) WW (munumunu)
    df = df.Define("Z_mumu_mass", "FCCAnalyses::invariant_mass(muons)")
    hists.append(df.Histo1D(("Z_mumu_mass", "Z(e+e−) mass", 100, 0, 200), "Z_mumu_mass"))

    # Z (mumu) WW (munumunu)
    df = df.Define("Z_mumu_mass", "FCCAnalyses::invariant_mass(muons)")
    hists.append(df.Histo1D(("Z_mumu_mass", "Z(mumu) mass", 100, 0, 200), "Z_mumu_mass"))

    # Z (e+e−) WW (bb)
    df = df.Define("WW_bb_mass", "FCCAnalyses::invariant_mass(leptons, quarks)")
    hists.append(df.Histo1D(("WW_bb_mass", "WW(ee) mass", 100, 0, 200), "WW_bb_mass"))

    # Z (e+e−) WW (ss)
    df = df.Define("WW_ss_mass", "FCCAnalyses::invariant_mass(leptons, quarks)")
    hists.append(df.Histo1D(("WW_ss_mass", "WW(ee) mass", 100, 0, 200), "WW_ss_mass"))

    # Z (e+e−) WW (cc)
    df = df.Define("WW_cc_mass", "FCCAnalyses::invariant_mass(leptons, quarks)")
    hists.append(df.Histo1D(("WW_cc_mass", "WW(ee) mass", 100, 0, 200), "WW_cc_mass"))

    # Z (mu+mu-) WW (bb)
    df = df.Define("WW_bb_mass", "FCCAnalyses::invariant_mass(leptons, quarks)")
    hists.append(df.Histo1D(("WW_bb_mass", "WW(mumu) mass", 100, 0, 200), "WW_bb_mass"))

    # Z (mu+mu-) WW (ss)
    df = df.Define("WW_ss_mass", "FCCAnalyses::invariant_mass(leptons, quarks)")
    hists.append(df.Histo1D(("WW_ss_mass", "WW(mumu) mass", 100, 0, 200), "WW_ss_mass"))

    # Z (mu+mu-) WW (cc)
    df = df.Define("WW_cc_mass", "FCCAnalyses::invariant_mass(leptons, quarks)")
    hists.append(df.Histo1D(("WW_cc_mass", "WW(mumu) mass", 100, 0, 200), "WW_cc_mass"))
    #########
    ### CUT 0: all events
    #########
    df = df.Define("cut0", "0")
    hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut0"))

    #########
    ### CUT 1: select at least 1 muon
    #########
    #df = df.Filter("muons_no >= 1")

    #df = df.Define("cut1", "1")
    #hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut1"))

    #########
    ### CUT 2: select at least 2 muons
    #########
    #df = df.Filter("muons_no >= 2")

    #df = df.Define("cut2", "2")
    #hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut2"))


    #########
    ### CUT 3: require exactly 2 opposite-sign muons
    #########
    df = df.Filter("muons_no == 2 && (muons_q[0] + muons_q[1]) == 0")

    df = df.Define("cut3", "3")
    hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut3"))


    #########
    ### CUT 4: max normalized muon momentum > 0.6
    #########
    #df = df.Define("muon_max_p", "(muons_p[0] > muons_p[1]) ? muons_p[0] : muons_p[1]")
    #df = df.Define("muon_max_p_norm", "muon_max_p/45.6")
    #hists.append(df.Histo1D(("muon_max_p_norm", "", *bins_norm), "muon_max_p_norm"))
    #df = df.Filter("muon_max_p_norm > 0.6")

    #df = df.Define("cut4", "4")
    #hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut4"))


    ############################################################################
    # acolinearity between 2 muons
    df = df.Define("acolinearity", "FCCAnalyses::acolinearity(muons)")
    hists.append(df.Histo1D(("acolinearity", "", *bins_aco), "acolinearity"))

    # plot invariant mass of both muons
    df = df.Define("leps_tlv", "FCCAnalyses::makeLorentzVectors(muons)")
    df = df.Define("invariant_mass", "(leps_tlv[0]+leps_tlv[1]).M()")
    hists.append(df.Histo1D(("invariant_mass", "", *bins_m_ll), "invariant_mass"))



    return hists, weightsum