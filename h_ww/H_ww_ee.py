
import ROOT
ROOT.TH1.SetDefaultSumw2(ROOT.kTRUE)

#okay, started out with our files, but the same old muon counter/plotter code, and it works. 
#So this code parses out the data, does the counting business, injects to root files, 
#the other code then reads the root files (hists basically) and plots them.
#As with the Delphes code, this first code, with the FCCAnalyses function can count 
#different particles in a single file
#The plots_root.py code then can separately 



# list of all guns
processList = {                  #signal
    #'wzp6_ee_nunuH_Hmumu_ecm240': {'fraction':1},
    #'wzp6_ee_nunuH_Hbb_ecm240': {'fraction':1},  
    #'wzp6_ee_nunuH_Hss_ecm240': {'fraction':1},  #Z-->nunu,H-->mumu,qq
    #'wzp6_ee_nunuH_Hcc_ecm240': {'fraction':1},
    'wzp6_ee_nunuH_HWW_ecm240': {'fraction':1},
    #'wzp6_ee_eeH_Hmumu_ecm240': {'fraction':1},
    #'wzp6_ee_eeH_Hbb_ecm240': {'fraction':1},  
    #'wzp6_ee_eeH_Hss_ecm240': {'fraction':1},          #Z-->ee, H-->mumu,qq 
    #'wzp6_ee_eeH_Hcc_ecm240': {'fraction':1},
                                                                   
    #'wzp6_ee_mumuH_Hmumu_ecm240': {'fraction':1},
    #'wzp6_ee_mumuH_Hbb_ecm240': {'fraction':1},
    #'wzp6_ee_mumuH_Hss_ecm240': {'fraction':1},     #Z-->mumu,H-->mumu,qq
    #'wzp6_ee_mumuH_Hcc_ecm240': {'fraction':1},
   ###############################################################################
                      #background
    #'wzp6_ee_nunuH_HZZ_ecm240': {'fraction':1},
    
    #'wzp6_ee_nunuH_Haa_ecm240': {'fraction':1},     #Z-->nunu,H-->WW, ZZ, aa, Za, gg
    #'wzp6_ee_nunuH_HZa_ecm240': {'fraction':1},
    #'wzp6_ee_nunuH_Hgg_ecm240': {'fraction':1},
    
    #'wzp6_ee_eeH_HZZ_ecm240': {'fraction':1},        
    #'wzp6_ee_eeH_HWW_ecm240': {'fraction':1},
    #'wzp6_ee_eeH_Haa_ecm240': {'fraction':1},       #Z-->ee,H-->WW, ZZ, aa, Za, gg
    #'wzp6_ee_eeH_HZa_ecm240': {'fraction':1},              
    #'wzp6_ee_eeH_Hgg_ecm240': {'fraction':1},

    #'wzp6_ee_mumuH_HZZ_ecm240': {'fraction':1}, 
    #'wzp6_ee_mumuH_HWW_ecm240': {'fraction':1},
    #'wzp6_ee_mumuH_Haa_ecm240':  {'fraction':1},    #Z-->mumu,H-->WW, ZZ, aa, Za, gg
    #'wzp6_ee_mumuH_HZa_ecm240': {'fraction':1},
    #'wzp6_ee_mumuH_Hgg_ecm240': {'fraction':1}


    'p8_ee_ZZ_ecm240': {'fraction':1},  #Direct ee to ZZ .0375
    'p8_ee_WW_ecm240': {'fraction':1}        #Direct ee to WW .011
}

#if I understand this correctly, this code really doesn't care what's signal and what's background, it just plots everything. 
#The signal/background distinction is made in the plotting code, not here.
#meaning in a collider experiment, everything happens, and we then decide what to look at afterwards by 
#doing the slicing and dicing in the plotting code.

inputDir = "/ceph/submit/data/group/fcc/ee/generation/DelphesEvents/winter2023/IDEA/"
procDict = "/ceph/submit/data/group/fcc/ee/generation/DelphesEvents/winter2023/IDEA/samplesDict.json"

# additional/custom C++ functions
includePaths = ["../functions/functions.h", "../functions/functions_gen.h"]
includePaths = ["../functions/functions.h", "../functions/utils.h"]

# output directory
outputDir   = "output/"


# optional: ncpus, default is 4, -1 uses all cores available
nCPUS       = 128

# scale the histograms with the cross-section and integrated luminosity
doScale = True
intLumi = 10.8e6 # 44.84 pb-1 = LEP, 100e6=100 ab-1 = FCCee

# define histograms
bins_p_mu = (200, 0, 200) # 1 GeV bins
bins_m_ll = (240, 0, 240) # 1 GeV bins
bins_p_ll = (200, 0, 200) # 1 GeV bins

bins_hadronicEnergy = (200, 0, 300)
bins_invMass = (200, 0, 200)
bins_photonE=(60, 0, 60)
bins_photonN=(30, 0, 30)

bins_theta = (500, -5, 5)
bins_phi = (500, -5, 5)
bins_muon_soft = (200, 0, 200)
bins_electron_soft = (200, 0, 200)

bins_m = (250, 0, 250) 
bins_count = (80, 0, 200)
bins_pdgid = (60, -30, 30)
bins_charge = (10, -5, 5)
bins_cutflow=(50, 0, 50)

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
    df = df.Alias("Particle1", "Particle#1.index")  #these why are these even here? unnecessary
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
    df = df.Define("muons_all_mass", "FCCAnalyses::ReconstructedParticle::get_mass(muons_all)")
    # define cos(theta) of the muons
    #hists.append(df.Histo1D(("muons_all_costheta", "", *bins_cos), "muons_all_costheta"))
    #df = df.Define("muons", "FCCAnalyses::sel_range(0, 0.97, true)(muons_all, muons_all_costheta)")
    #df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
    #df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
    #df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")
    #df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
    #df = df.Define("muons_m", "FCCAnalyses::ReconstructedParticle::get_mass(muons)")

    # define muons with p>25 GeV
    df = df.Define("muons_hard", "FCCAnalyses::ReconstructedParticle::sel_p(25)(muons_all)")
    df = df.Define("muons_hard_tlv", "FCCAnalyses::makeLorentzVectors(muons_hard)")
    df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons_hard)")
    df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons_hard)")
    df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons_hard)")

    df = df.Define("muons_soft", "FCCAnalyses::ReconstructedParticle::sel_p(10)(muons_all)")
    df = df.Define("muons_soft_tlv", "FCCAnalyses::makeLorentzVectors(muons_soft)")
    df = df.Define("muons_soft_p", "FCCAnalyses::ReconstructedParticle::get_p(muons_soft)")
    df = df.Define("muons_soft_no", "FCCAnalyses::ReconstructedParticle::get_n(muons_soft)")
    df = df.Define("muons_soft_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons_soft)")

    # define electrons
    df = df.Alias("Electron0", "Electron#0.index")
    df = df.Define("electrons_all", "FCCAnalyses::ReconstructedParticle::get(Electron0, ReconstructedParticles)")
    df = df.Define("electrons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons_all)")
    hists.append(df.Histo1D(("electrons_all_p", "", *bins_m), "electrons_all_p"))

    df = df.Define("electrons_hard", "FCCAnalyses::ReconstructedParticle::sel_p(25)(electrons_all)")
    df = df.Define("electrons_hard_tlv", "FCCAnalyses::makeLorentzVectors(electrons_hard)")
    df = df.Define("electrons_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons_hard)")
    df = df.Define("electrons_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons_hard)")
    df = df.Define("electrons_q", "FCCAnalyses::ReconstructedParticle::get_charge(electrons_hard)")

    df = df.Define("electrons_soft", "FCCAnalyses::ReconstructedParticle::sel_p(10)(electrons_all)")
    df = df.Define("electrons_soft_tlv", "FCCAnalyses::makeLorentzVectors(electrons_soft)")
    df = df.Define("electrons_soft_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons_soft)")
    df = df.Define("electrons_soft_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons_soft)")
    df = df.Define("electrons_soft_q", "FCCAnalyses::ReconstructedParticle::get_charge(electrons_soft)")

     ##########################
     # Why need all the extra stuff? Just do bottom, strange, charm, that's all the signals we have.
    #(bottom charm strange quarks) It's not function documentation, it's the indexing in the files
    #df = df.Alias("Particle0", "Particle#0.index")
    #df = df.Alias("Particle1", "Particle#1.index")
    #df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    #df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    #df = df.Alias("BottomQuarks", "Bottom#0.index") 
    #df = df.Alias("CharmQuarks", "Charm#0.index")   

    # reconstructed bottom quarks and properties
    #df = df.Define("bottom_all", "FCCAnalyses::ReconstructedParticle::get(BottomQuarks, ReconstructedParticles)")
    #df = df.Define("bottom_all_p", "FCCAnalyses::ReconstructedParticle::get_p(bottom_all)")
    #df = df.Define("bottom_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(bottom_all)")
    #df = df.Define("bottom_all_costheta", "FCCAnalyses::get_costheta(bottom_all)")
    #df = df.Define("bottom_all_phi", "FCCAnalyses::ReconstructedParticle::get_phi(bottom_all)")
    #df = df.Define("bottom_all_q", "FCCAnalyses::ReconstructedParticle::get_charge(bottom_all)")
    #df = df.Define("bottom_all_no", "FCCAnalyses::ReconstructedParticle::get_n(bottom_all)")

    #define cos(theta) for bottom quarks
    #hists.append(df.Histo1D(("bottom_all_costheta", "", *bins_cos), "bottom_all_costheta"))
    #df = df.Define("bottom_quarks", "FCCAnalyses::sel_range(0, 0.97, true)(bottom_all, bottom_all_costheta)")
    #df = df.Define("bottom_p", "FCCAnalyses::ReconstructedParticle::get_p(bottom_quarks)")
    #df = df.Define("bottom_theta", "FCCAnalyses::ReconstructedParticle::get_theta(bottom_quarks)")
    #df = df.Define("bottom_no", "FCCAnalyses::ReconstructedParticle::get_n(bottom_quarks)")
    #df = df.Define("bottom_q", "FCCAnalyses::ReconstructedParticle::get_charge(bottom_quarks)")

    #reconstructed charm quarks and properties
    #df = df.Define("charm_all", "FCCAnalyses::ReconstructedParticle::get(CharmQuarks, ReconstructedParticles)")
    #df = df.Define("charm_all_p", "FCCAnalyses::ReconstructedParticle::get_p(charm_all)")
    #df = df.Define("charm_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(charm_all)")
    #df = df.Define("charm_all_costheta", "FCCAnalyses::get_costheta(charm_all)")
    #df = df.Define("charm_all_phi", "FCCAnalyses::ReconstructedParticle::get_phi(charm_all)")
    #df = df.Define("charm_all_q", "FCCAnalyses::ReconstructedParticle::get_charge(charm_all)")
    #df = df.Define("charm_all_no", "FCCAnalyses::ReconstructedParticle::get_n(charm_all)")

    #def cos(theta) for charm quarks
    #hists.append(df.Histo1D(("charm_all_costheta", "", *bins_cos), "charm_all_costheta"))
    #df = df.Define("charm_quarks", "FCCAnalyses::sel_range(0, 0.97, true)(charm_all, charm_all_costheta)")
    #df = df.Define("charm_p", "FCCAnalyses::ReconstructedParticle::get_p(charm_quarks)")
    #df = df.Define("charm_theta", "FCCAnalyses::ReconstructedParticle::get_theta(charm_quarks)")
    #df = df.Define("charm_no", "FCCAnalyses::ReconstructedParticle::get_n(charm_quarks)")
    #df = df.Define("charm_q", "FCCAnalyses::ReconstructedParticle::get_charge(charm_quarks)")

    #strange quarks)
    #df = df.Alias("Particle0", "Particle#0.index")
    #df = df.Alias("Particle1", "Particle#1.index")
    #df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    #df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    #df = df.Alias("StrangeQuarks", "Strange#0.index")  

#rconstructed strange quarks and their properties
    #df = df.Define("strange_all", "FCCAnalyses::ReconstructedParticle::get(StrangeQuarks, ReconstructedParticles)")
    #df = df.Define("strange_all_p", "FCCAnalyses::ReconstructedParticle::get_p(strange_all)")
    #df = df.Define("strange_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(strange_all)")
    #df = df.Define("strange_all_costheta", "FCCAnalyses::get_costheta(strange_all)")
    #df = df.Define("strange_all_phi", "FCCAnalyses::ReconstructedParticle::get_phi(strange_all)")
    #df = df.Define("strange_all_q", "FCCAnalyses::ReconstructedParticle::get_charge(strange_all)")
    #df = df.Define("strange_all_no", "FCCAnalyses::ReconstructedParticle::get_n(strange_all)")

        #define cos(theta) for strange quarks
    #hists.append(df.Histo1D(("strange_all_costheta", "", *bins_cos), "strange_all_costheta"))
    #df = df.Define("strange_quarks", "FCCAnalyses::sel_range(0, 0.97, true)(strange_all, strange_all_costheta)")
    #df = df.Define("strange_p", "FCCAnalyses::ReconstructedParticle::get_p(strange_quarks)")
    #df = df.Define("strange_theta", "FCCAnalyses::ReconstructedParticle::get_theta(strange_quarks)")
    #df = df.Define("strange_no", "FCCAnalyses::ReconstructedParticle::get_n(strange_quarks)")
    #df = df.Define("strange_q", "FCCAnalyses::ReconstructedParticle::get_charge(strange_quarks)")

    # Z(nunu) WW (mu nu mu nu)
    #df = df.Define("neutrinos", "FCCAnalyses::ReconstructedParticle::get_neutrinos(ReconstructedParticles)")
    #df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::get_muons(ReconstructedParticles)")
    #df = df.Define("Z_nn_mass", "FCCAnalyses::invariant_mass(neutrinos)")
    #df = df.Define("WW_mumu_mass", "FCCAnalyses::invariant_mass(muons)")

    #hists.append(df.Histo1D(("Z_nn_mass", "Z(nunu) mass", 100, 0, 200), "Z_nn_mass"))
    #hists.append(df.Histo1D(("WW_mumu_mass", "WW(munumunu) mass", 100, 0, 200), "WW_mumu_mass"))

    # Z (nunu) WW (bb)
    #df = df.Define("bottom", "FCCAnalyses::ReconstructedParticle::get_quarks(ReconstructedParticles)")
   # df = df.Define("WW_bb_mass", "FCCAnalyses::invariant_mass(bottom)")

    #hists.append(df.Histo1D(("WW_qq_mass", "WW(bb) mass", 100, 0, 200), "WW_qq_mass"))

    # Z (nunu) WW (ss)
    #df = df.Define("strange", "FCCAnalyses::ReconstructedParticle::get_quarks(ReconstructedParticles)")
    #df = df.Define("WW_ss_mass", "FCCAnalyses::invariant_mass(strange)")

    #hists.append(df.Histo1D(("WW_qq_mass", "WW(ss) mass", 100, 0, 200), "WW_qq_mass"))

    # Z (nunu) WW (cc)
    #df = df.Define("charm", "FCCAnalyses::ReconstructedParticle::get_quarks(ReconstructedParticles)")
    #df = df.Define("WW_cc_mass", "FCCAnalyses::invariant_mass(charm)")


    #Okay, cut flow is what shows what remains after each cut... makes sense now.

    

    #hists.append(df.Histo1D(("WW_qq_mass", "WW(cc) mass", 100, 0, 200), "WW_qq_mass"))
    #########
    ### CUT 0: all events
    #########
    df = df.Define("cut0", "0")
    hists.append(df.Histo1D(("cutFlow", "", *bins_cutflow), "cut0"))
    
    ##WWdecay pdgid
    if dataset == "wzp6_ee_nunuH_HWW_ecm240":
        df = df.Define("ww_decay", "FCCAnalyses::ww_decay_mode(Particle, Particle1)")
        df = df.Filter("abs(ww_decay[0]) == 13 || abs(ww_decay[0]) == 11") # muon for first W
        df = df.Filter("abs(ww_decay[2]) == 13 || abs(ww_decay[2]) == 11") # muon for second W
    ##counting the initial number of events

    initial_events = df.Count()
    #########
    ### CUT 1: 2 leptons
    #########
    #########
    df = df.Filter("(electrons_soft_no == 1) && (muons_soft_no == 1) ") 
    df = df.Define("cut1", "1")
    hists.append(df.Histo1D(("cutFlow", "", *bins_cutflow), "cut1"))

    #########
    ### CUT 2: opposite charge on the leptons, trying to see 
    #########
    df = df.Filter("(muons_soft_q[0] == -electrons_soft_q[0])") 
                   #(muons_soft_q[0] == -electrons_soft_q[1]) || (muons_soft_q[1] == -electrons_soft_q[0]) || (muons_soft_q[1] == -electrons_soft_q[1])")
    df = df.Define("cut2", "2")
    hists.append(df.Histo1D(("cutFlow", "", *bins_cutflow), "cut2"))

    ######### SEEMS TO BE WORKING BUT BRINGS DOWN SIGNAL ALONG WITH THE BACKGROUND 
    ### CUT :supressing WW background by requiring missing energy consistent with neutrinos
    ######### remember, the cut means only keep events that have this...
    #df = df.Alias("MissingETs", "MissingET")
    #df = df.Define("missingET_E", "Sum(MissingET.energy)") 
    #df = df.Filter("(missingET_E>82)") 
    #df = df.Define("cut3", "3") 
    #hists.append(df.Histo1D(("cutFlow", "", *bins_cutflow), "cut3"))

    # CUT3: missing energy/mass  #CUTS FOR MISSING ENERGY AND MASS BETTER BASED ON JANS SLIDES
    df = df.Define("missingMass", "FCCAnalyses::missingMass(240., ReconstructedParticles)")
    df = df.Filter("missingMass>130") 
    df = df.Define("cut3", "3") 
    hists.append(df.Histo1D(("cutFlow", "", *bins_cutflow), "cut3"))


    #########
    ### CUT 4: Cutting down the WW background's, looking at the missing transverse energy 
    #########
    df = df.Alias("MissingETs", "MissingET")
    df = df.Define("missingET_E", "Sum(MissingET.energy)") 
    df = df.Filter("(missingET_E>30)&&(missingET_E<70)") 
    df = df.Define("cut4", "4")
    hists.append(df.Histo1D(("cutFlow", "", *bins_cutflow), "cut4"))

    #########
    ### CUT 5: muon momentum has a peak below 10, get rid of any high momentum muons 
    #########
    #df = df.Filter("(muons_soft_p[0] < 50 && muons_soft_p[1] < 50)")
    df = df.Filter("(muons_soft_p[0] < 50 && electrons_soft_p[0] < 50)")
    #df = df.Filter("(electrons_soft_p[0] < 50 && muons_soft_p[0] < 50)")
    #df = df.Filter(" (electrons_soft_p[0] < 50 && electrons_soft_p[1] < 50)")
    df = df.Define("cut5", "5")
    hists.append(df.Histo1D(("cutFlow", "", *bins_cutflow), "cut5"))

    #########
    ### CUT 6: Hadronic energy, get rid of events with high hadronic energy
    #########
    df = df.Define("rps_no_muons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, muons_all)")
    df = df.Define("rps_no_muons_electrons", "FCCAnalyses::ReconstructedParticle::remove(rps_no_muons, electrons_all)")
    df = df.Define("hadronicEnergy", "FCCAnalyses::visibleEnergy(rps_no_muons_electrons)")
    df = df.Filter("hadronicEnergy < 20")
    df = df.Define("cut6", "6")
    hists.append(df.Histo1D(("cutFlow", "", *bins_cutflow), "cut6"))

    #########
    ### CUT : require opposite-sign muons close to Z boson mass, (this is only to study Z peak) 
    #########
    #df = df.Define("leps_tlv", "FCCAnalyses::makeLorentzVectors(muons)")
    #df = df.Define("invariant_mass", "(leps_tlv[0] + leps_tlv[1]).M()") 
    #df = df.Filter("invariant_mass > 81")
    #df = df.Define("cut4", "4")
    #hists.append(df.Histo1D(("cutFlow", "", *bins_cutflow), "cut4"))

    #########
    ### CUT : require opposite-sign muons close to Z boson mass, (this is only to study Z peak) 
    #########
    df = df.Define("leps_tlv", "FCCAnalyses::makeLorentzVectors(muons_soft)")
    df = df.Define("invariant_mass", "(leps_tlv[0] + leps_tlv[1]).M()") 
    #df = df.Filter("abs(invariant_mass - 91.2) < 10")
    #df = df.Define("cut4", "4")
    #hists.append(df.Histo1D(("cutFlow", "", *bins_cutflow), "cut4"))

    ######### NOT REALLY FUNCTIONING
    # ####### PROBABLY BECAUSE WE'VE ALREADY FILTERED OUT THE MUONS
    ### CUT :getting rid of events with the additional high-momentum leptons to suppress WW, qqqq gone
    #########
    #df = df.Define("additional_muons", "FCCAnalyses::ReconstructedParticle::remove(muons_all, muons)")  #excluding muons selected so far
    #df = df.Define("additional_muons_p", "FCCAnalyses::ReconstructedParticle::get_p(additional_muons)")  #remaining ones' momentum
    #df = df.Filter("Sum(additional_muons_p) <= 6.0")  # events with additional high-pT muons (need to adjust)
    #df = df.Define("cut5", "5")
    #hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut5"))

   

    
    
    ### CUT 7: getting rid of some of the ZZ background, photons from the lepton channel
    ######### #Max, min typa cuts are so good! More like what you'd expect when you do cuts
    #photon alias
    df = df.Alias("Photons", "Photon#0.index")
    df = df.Define("photons", "FCCAnalyses::ReconstructedParticle::get(Photons, ReconstructedParticles)") #photon object, get transverse momentum
    df = df.Define("photons_e", "FCCAnalyses::ReconstructedParticle::get_e(photons)")
    df = df.Define("n_photons", "FCCAnalyses::ReconstructedParticle::get_n(photons)") #getn
    df = df.Filter("n_photons <3  && photons_e[0] < 7") 
    df = df.Define("cut7", "7")   #Max was the only way to make this work, otherwise it was giving me an error
    hists.append(df.Histo1D(("cutFlow", "", *bins_cutflow), "cut7"))

    ######### WORKS BUT NOT DOING ANYTHING
    ### CUT 8 :Jets, cutting out exactly 4 jets for fully hadronic ZZ decay
    ######### remember, the cut means only keep events that have this...
    #maybe jets are like MissingET here, fix that.
    df = df.Alias("Jets", "Jet")
    df = df.Define("n_jets",  "Jets.size()")
    df = df.Filter("n_jets<=2")
    df = df.Define("cut8", "8") 
    hists.append(df.Histo1D(("cutFlow", "", *bins_cutflow), "cut8"))

   
    # CUT: WW decay mode  #FIXED STRUCTURE LOGIC, BUT < > LOGIC NEEDS TO BE FIXED
    #It seems 100% means 99.999999
    df = df.Define("ww_decay_mode", "FCCAnalyses::ww_decay_mode(Particle, Particle0)")
    #hists.append(df.Histo1D(("ww_decay_mode", "", *(50, -25, 25)), "ww_decay_mode"))
    #if dataset == "wzp6_ee_nunuH_HWW_ecm240":
            #df = df.Filter("(abs(ww_decay_mode[0])==13 && abs(ww_decay_mode[2])==13)")
    #df = df.Define("cut8", "8") 
    #hists.append(df.Histo1D(("cutFlow", "", *bins_cutflow), "cut8"))

    #final number of events count
    final_events=df.Count()
    print("percent drop in events: ", (initial_events.GetValue()-final_events.GetValue())/initial_events.GetValue()*100)

    if dataset == "wzp6_ee_nunuH_HWW_ecm240":
        signal_events = df.Count()
        print(f"Remaining number of signal events: {signal_events.GetValue()}")

    elif dataset == "p8_ee_ZZ_ecm240":
        background_events_ZZ = df.Count()
        print(f"Remaining number of background events (ZZ): {background_events_ZZ.GetValue()}")
    elif dataset == "p8_ee_WW_ecm240":
        background_events_WW = df.Count()
        print(f"Remaining number of background events (WW): {background_events_WW.GetValue()}")
    


    
#muons_no == 2 && (muons_q[0] + muons_q[1]) == 0 && 
    #########
    ### CUT 4: max normalized muon momentum > 0.6
    #########
    #df = df.Define("muon_max_p", "(muons_p[0] > muons_p[1]) ? muons_p[0] : muons_p[1]")
    #if 0 > 1 then 0 else 1
    #df = df.Define("muon_max_p_norm", "muon_max_p/45.6")
    #hists.append(df.Histo1D(("muon_max_p_norm", "", *bins_norm), "muon_max_p_norm"))
    #df = df.Filter("muon_max_p_norm > 0.6")

    #df = df.Define("cut4", "4")
    #hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut4"))


    ############################################################################
    # acolinearity between 2 muons
    df = df.Define("acolinearity", "FCCAnalyses::acolinearity(muons_soft)")
    hists.append(df.Histo1D(("acolinearity", "", *bins_aco), "acolinearity"))

    # plot invariant mass of both muons
    #df = df.Define("leps_tlv", "FCCAnalyses::makeLorentzVectors(muons)")
    #df = df.Define("invariant_mass", "(leps_tlv[0]+leps_tlv[1]).M()")
    overflow_invMass = 199  #assigning overflow events to the last bin
    df = df.Define("invMass_clamped", f"invariant_mass > {overflow_invMass} ? {overflow_invMass} : invariant_mass")
    hists.append(df.Histo1D(("invariant_mass", "invariant_mass", *bins_invMass), "invMass_clamped"))
    #hists.append(df.Histo1D(("invariant_mass", "", *bins_invMass), "invariant_mass"))

    #plot the missing transverse energy distribution, no overflow for this one, ends early
    hists.append(df.Histo1D(("MissingET_dist", "", *bins_count), "missingET_E"))
   
    hists.append(df.Histo1D(("n_jets", "", *bins_count), "n_jets"))
    

    #plot the hadronic energy
    overflow_hadronicEnergy = 249
    df = df.Define("hadronicEnergy_clamped", f"hadronicEnergy > {overflow_hadronicEnergy} ? {overflow_hadronicEnergy} : hadronicEnergy")
    hists.append(df.Histo1D(("hadronicEnergy", "hadronicEnergy", *bins_hadronicEnergy), "hadronicEnergy_clamped"))
    
    #plot the muon momentum
    overflow_muon_p = 123
    overflow_electron_p = 123
    df = df.Define("muons_soft_p_clamped", f"muons_soft_p[0] > {overflow_muon_p} ? {overflow_muon_p} : muons_soft_p[0]")
    df = df.Define("electrons_soft_p_clamped", f"electrons_soft_p[0] > {overflow_electron_p} ? {overflow_electron_p} : electrons_soft_p[0]")
    hists.append(df.Histo1D(("muons_soft_p_dist", "muons_soft_p_dist", *bins_muon_soft), "muons_soft_p_clamped"))
    hists.append(df.Histo1D(("electrons_soft_p_dist", "electrons_soft_p_dist", *bins_electron_soft), "electrons_soft_p_clamped"))

    #LATER PLOT THE ELECTRON MOMENTUM DISTRIBUTION

    # Plot invariant mass of bottom quark pairs
    #df = df.Define("bottoms_tlv", "FCCAnalyses::makeLorentzVectors(bottoms)")
    #df = df.Define("bottom_invariant_mass", "(bottoms_tlv[0] + bottoms_tlv[1]).M()")
    #hists.append(df.Histo1D(("bottom_invariant_mass", "", *bins_m_ll), "bottom_invariant_mass"))

    # Plot invariant mass of charm quark pairs
    #df = df.Define("charms_tlv", "FCCAnalyses::makeLorentzVectors(charms)")
    #df = df.Define("charm_invariant_mass", "(charms_tlv[0] + charms_tlv[1]).M()")
    #hists.append(df.Histo1D(("charm_invariant_mass", "", *bins_m_ll), "charm_invariant_mass"))

   
    #Plotting number dist of the Photons
    overflow_photonN = 29
    df = df.Define("photon_num", "FCCAnalyses::ReconstructedParticle::get_n(photons)")
    df = df.Define("photon_num_clamped", f"photon_num > {overflow_photonN} ? {overflow_photonN} : photon_num")
    hists.append(df.Histo1D(("photon_num", "photon_num", *bins_photonN), "photon_num_clamped"))
    
    #missing mass
    overflow_missingMass = 239  #assigning overflow events to the last bin
    df = df.Define("missingMass_clamped", f"missingMass > {overflow_missingMass} ? {overflow_missingMass} : missingMass")
    hists.append(df.Histo1D(("missingMass", "missingMass", *bins_m_ll), "missingMass_clamped"))

    #hists.append(df.Histo1D(("missingMass", "", *bins_count), "missingMass"))

    #Plotting Energy Distributions of the Photons #perhaps move these to before the cuts
    overflow_photonE = 59 
    df = df.Define("photon_energy", "FCCAnalyses::ReconstructedParticle::get_e(photons)")
    df = df.Define("photon_energy_clamped", f"photon_energy[0] > {overflow_photonE} ? {overflow_photonE} : photon_energy[0]")
    hists.append(df.Histo1D(("photon_energy", "photon_energy", *bins_photonE), "photon_energy_clamped"))


    return hists, weightsum