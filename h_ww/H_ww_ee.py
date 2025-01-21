
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
    'wzp6_ee_nunuH_Hmumu_ecm240': {'fraction':1},
    #'wzp6_ee_nunuH_Hbb_ecm240': {'fraction':1},  
    #'wzp6_ee_nunuH_Hss_ecm240': {'fraction':1},  #Z-->nunu,H-->mumu,qq
    #'wzp6_ee_nunuH_Hcc_ecm240': {'fraction':1},

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
    'wzp6_ee_nunuH_HZZ_ecm240': {'fraction':1},
    'wzp6_ee_nunuH_HWW_ecm240': {'fraction':1},
    #'wzp6_ee_nunuH_Haa_ecm240': {'fraction':1},     #Z-->nunu,H-->WW, ZZ, aa, Za, gg
    'wzp6_ee_nunuH_HZa_ecm240': {'fraction':1},
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
    hists.append(df.Histo1D(("muons_all_costheta", "", *bins_cos), "muons_all_costheta"))
    df = df.Define("muons", "FCCAnalyses::sel_range(0, 0.97, true)(muons_all, muons_all_costheta)")
    df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
    df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
    df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")
    df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
    df = df.Define("muons_m", "FCCAnalyses::ReconstructedParticle::get_mass(muons)")

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
    hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut0"))

    #########
    ### CUT 1: select at least 2 muons
    #########
    df = df.Filter("muons_no >= 2")

    df = df.Define("cut1", "1")
    hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut1"))

    #########
    ### CUT 2: require exactly 2 opposite-sign muons, this already is a good cut 
                #to separate out the 4 leptons that come from ZZ->4l
    #########
    df = df.Filter("muons_no == 2 && (muons_q[0] + muons_q[1]) == 0")

    df = df.Define("cut2", "2")
    hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut2"))

    #########
    ### CUT 3: muon momentum has a peak below 23, get rid of anything below 23 
    #########
    #df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
    df = df.Filter("muons_p[0] > 30 && muons_p[1] > 30")
    df = df.Define("cut3", "3")
    hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut3"))
    
    #########
    ### CUT 4: require opposite-sign muons close to Z boson mass, (this is only to study Z peak) 
    #########
    df = df.Define("leps_tlv", "FCCAnalyses::makeLorentzVectors(muons)")
    df = df.Define("invariant_mass", "(leps_tlv[0] + leps_tlv[1]).M()") 
    df = df.Filter("invariant_mass>63")
    df = df.Define("cut4", "4")
    hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut4"))

    #########
    ### CUT : require opposite-sign muons close to Z boson mass, (this is only to study Z peak) 
    #########
    #df = df.Define("leps_tlv", "FCCAnalyses::makeLorentzVectors(muons)")
    #df = df.Define("invariant_mass", "(leps_tlv[0] + leps_tlv[1]).M()") 
    #df = df.Filter("abs(invariant_mass - 91.2) < 10")
    #df = df.Define("cut4", "4")
    #hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut4"))

    ######### NOT REALLY FUNCTIONING
    # ####### PROBABLY BECAUSE WE'VE ALREADY FILTERED OUT THE MUONS
    ### CUT 5:getting rid of events with the additional high-momentum leptons to suppress WW, qqqq gone
    #########
    #df = df.Define("additional_muons", "FCCAnalyses::ReconstructedParticle::remove(muons_all, muons)")  #excluding muons selected so far
    #df = df.Define("additional_muons_p", "FCCAnalyses::ReconstructedParticle::get_p(additional_muons)")  #remaining ones' momentum
    #df = df.Filter("Sum(additional_muons_p) <= 6.0")  # events with additional high-pT muons (need to adjust)
    #df = df.Define("cut5", "5")
    #hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut5"))

    ######### WORKS BUT BRINGS DOWN SIGNAL ALONG WITH THE BACKGROUND
    ### CUT :  looking at Zγ events, counting photon #s, removing events with energetic photons
    ######### #this works but brings down the signal line together with the background
    #photon alias
    df = df.Alias("Photons", "Photon#0.index")
    df = df.Define("photons", "FCCAnalyses::ReconstructedParticle::get(Photons, ReconstructedParticles)") #photon object, get transverse momentum
    #df = df.Define("photons_e", "FCCAnalyses::ReconstructedParticle::get_e(photons)")
    #df = df.Define("n_photons", "FCCAnalyses::ReconstructedParticle::get_n(photons)") #getn
    #df = df.Filter("n_photons == 0 || Max(photons_e) > 4") #requiring no photons or photons with pT < 4GeV
    #df = df.Define("cut6", "6")
    #hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut6"))

    ######### SEEMS TO BE WORKING BUT BRINGS DOWN SIGNAL ALONG WITH THE BACKGROUND 
    ### CUT 6:supressing WW background by requiring missing energy consistent with neutrinos
    ######### remember, the cut means only keep events that have this...
    df = df.Alias("MissingETs", "MissingET")
    df = df.Define("missingET_E", "Sum(MissingET.energy)") 
    df = df.Filter("missingET_E > 47") 
    df = df.Define("cut5", "5") 
    hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut5"))


    ######### WORKS BUT NOT DOING ANYTHING
    ### CUT 8:Jets, cutting out a lot of jets
    ######### remember, the cut means only keep events that have this...
    #maybe jets are like MissingET here, fix that.
    #df = df.Alias("Jets", "Jet")
    #df = df.Define("n_jets",  "Jets.size()")
    #df = df.Filter("n_jets <2 || (2<= n_jets < 4)")
    #df = df.Define("cut8", "8") 
    #hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut8"))

    #########
    ### CUT : Cutting down the WW background's, looking at the missing transverse energy 
    #########
    #df = df.Define("MET", "FCCAnalyses::getMET(ReconstructedParticles)")
    #df = df.Filter("MET < 30")
    #df = df.Define("cut5", "5")
    #hists.append(df.Histo1D(("cutFlow", "", *bins_count), "cut5"))


    
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
    df = df.Define("acolinearity", "FCCAnalyses::acolinearity(muons)")
    hists.append(df.Histo1D(("acolinearity", "", *bins_aco), "acolinearity"))

    # plot invariant mass of both muons
    #df = df.Define("leps_tlv", "FCCAnalyses::makeLorentzVectors(muons)")
    #df = df.Define("invariant_mass", "(leps_tlv[0]+leps_tlv[1]).M()")
    hists.append(df.Histo1D(("invariant_mass", "", *bins_m_ll), "invariant_mass"))

    #plot the missing transverse energy distribution
    #df = df.Alias("MissingETs", "MissingET")
    #df = df.Define("missingET_E", "Sum(MissingET.energy)")
    hists.append(df.Histo1D(("MissingET_dist", "", *bins_count), "missingET_E"))

    #plot the muon momentum
    hists.append(df.Histo1D(("muon_p_dist", "", *bins_count), "muons_p"))

    #LATER PLOT THE ELECTRON MOMENTUM DISTRIBUTION


    # Plot invariant mass of bottom quark pairs
    #df = df.Define("bottoms_tlv", "FCCAnalyses::makeLorentzVectors(bottoms)")
    #df = df.Define("bottom_invariant_mass", "(bottoms_tlv[0] + bottoms_tlv[1]).M()")
    #hists.append(df.Histo1D(("bottom_invariant_mass", "", *bins_m_ll), "bottom_invariant_mass"))

    # Plot invariant mass of charm quark pairs
    #df = df.Define("charms_tlv", "FCCAnalyses::makeLorentzVectors(charms)")
    #df = df.Define("charm_invariant_mass", "(charms_tlv[0] + charms_tlv[1]).M()")
    #hists.append(df.Histo1D(("charm_invariant_mass", "", *bins_m_ll), "charm_invariant_mass"))

    #Plotting Energy Distributions of the Photons #perhaps move these to before the cuts
    df = df.Define("photon_energy", "FCCAnalyses::ReconstructedParticle::get_e(photons)")
    hists.append(df.Histo1D(("photon_energy", "", *bins_count), "photon_energy"))

    #Plotting number dist of the Photons
    df = df.Define("photon_num", "FCCAnalyses::ReconstructedParticle::get_n(photons)")
    hists.append(df.Histo1D(("photon_num", "", *bins_count), "photon_num"))

    #Plotting missing energy dist

    return hists, weightsum