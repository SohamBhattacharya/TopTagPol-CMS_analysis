#!/usr/bin/env python

import os


l_pdgid = [11, 13, 211]#, 13, 22, 211, 130]
l_pdgidName = ["e", "#mu", "CH"]#, "#mu", "#gamma", "CH", "NH"]

outDir = "plots/variables"

for pdgid, pdgidName in zip(l_pdgid, l_pdgidName) :
    
    command = """
        python -u plot_variable.py \
        --fileAndTreeNames \
            "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/ntupleTree_ZprimeToTT_M1000_W10_new.root:treeMaker/tree" \
            "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/ntupleTree_ZprimeToTT_M1000_W10_new.root:treeMaker/tree" \
            "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/ntupleTree_QCD_Pt_470to600_PREMIX_RECODEBUG_new.root:treeMaker/tree" \
            "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/ntupleTree_QCD_bEnriched_HT700to1000.root:treeMaker/tree" \
        --plotVars \
            "jet_selectedPatJetsAK15PFPuppi_consti_dxy_reco" \
            "jet_selectedPatJetsAK15PFPuppi_consti_dxy_reco" \
            "jet_selectedPatJetsAK15PFPuppi_consti_dxy_reco" \
            "jet_selectedPatJetsAK15PFPuppi_consti_dxy_reco" \
        --cuts \
            "(jet_selectedPatJetsAK15PFPuppi_pT_reco > 200) & (fabs(jet_selectedPatJetsAK15PFPuppi_eta_reco) < 2.4) & (jet_selectedPatJetsAK15PFPuppi_nConsti_reco >= 3) & (jet_selectedPatJetsAK15PFPuppi_nearestGenTopDR_reco < 1) & (jet_selectedPatJetsAK15PFPuppi_nearestGenTopIsLeptonic_reco > 0.5) & (abs(jet_selectedPatJetsAK15PFPuppi_consti_id_reco) == {pdgid}) & (jet_selectedPatJetsAK15PFPuppi_consti_pT_reco > 20)" \
            "(jet_selectedPatJetsAK15PFPuppi_pT_reco > 200) & (fabs(jet_selectedPatJetsAK15PFPuppi_eta_reco) < 2.4) & (jet_selectedPatJetsAK15PFPuppi_nConsti_reco >= 3) & (jet_selectedPatJetsAK15PFPuppi_nearestGenTopDR_reco < 1) & (jet_selectedPatJetsAK15PFPuppi_nearestGenTopIsLeptonic_reco < 0.5) & (abs(jet_selectedPatJetsAK15PFPuppi_consti_id_reco) == {pdgid}) & (jet_selectedPatJetsAK15PFPuppi_consti_pT_reco > 20)" \
            "(jet_selectedPatJetsAK15PFPuppi_pT_reco > 200) & (fabs(jet_selectedPatJetsAK15PFPuppi_eta_reco) < 2.4) & (jet_selectedPatJetsAK15PFPuppi_nConsti_reco >= 3) & (abs(jet_selectedPatJetsAK15PFPuppi_consti_id_reco) == {pdgid}) & (jet_selectedPatJetsAK15PFPuppi_consti_pT_reco > 20)" \
            "(jet_selectedPatJetsAK15PFPuppi_pT_reco > 200) & (fabs(jet_selectedPatJetsAK15PFPuppi_eta_reco) < 2.4) & (jet_selectedPatJetsAK15PFPuppi_nConsti_reco >= 3) & (abs(jet_selectedPatJetsAK15PFPuppi_consti_id_reco) == {pdgid}) & (jet_selectedPatJetsAK15PFPuppi_consti_pT_reco > 20)" \
        --labels \
            "t^{{lep}}" \
            "t^{{had}}" \
            "QCD" \
            "QCD (b)" \
        --lineColors \
            2 \
            4 \
            6 \
            8 \
        --plotBin 1000 0 50 \
        --xRange 0 5 \
        --yRange 1e-6 10 \
        --logY \
        --xTitle "|d_{{xy}}({pdgidName}, SV)|" \
        --yTitle "arbitrary unit" \
        --title "title" \
        --titlePos 0 0 \
        --outFileName "out_svdxy_id{pdgid}.pdf" \
    """.format(
        pdgid = pdgid,
        pdgidName = pdgidName,
        outDir = outDir,
    )
    
    os.system(command)
    print("\n")
    
    
    
    command = """
        python -u plot_variable.py \
        --fileAndTreeNames \
            "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/ntupleTree_ZprimeToTT_M1000_W10_new.root:treeMaker/tree" \
            "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/ntupleTree_ZprimeToTT_M1000_W10_new.root:treeMaker/tree" \
            "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/ntupleTree_QCD_Pt_470to600_PREMIX_RECODEBUG_new.root:treeMaker/tree" \
            "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/ntupleTree_QCD_bEnriched_HT700to1000.root:treeMaker/tree" \
        --plotVars \
            "where(jet_selectedPatJetsAK15PFPuppi_consti_dxy_reco < 0, 0, 1.0-min(3, jet_selectedPatJetsAK15PFPuppi_consti_dxy_reco)/3.0)" \
            "where(jet_selectedPatJetsAK15PFPuppi_consti_dxy_reco < 0, 0, 1.0-min(3, jet_selectedPatJetsAK15PFPuppi_consti_dxy_reco)/3.0)" \
            "where(jet_selectedPatJetsAK15PFPuppi_consti_dxy_reco < 0, 0, 1.0-min(3, jet_selectedPatJetsAK15PFPuppi_consti_dxy_reco)/3.0)" \
            "where(jet_selectedPatJetsAK15PFPuppi_consti_dxy_reco < 0, 0, 1.0-min(3, jet_selectedPatJetsAK15PFPuppi_consti_dxy_reco)/3.0)" \
        --cuts \
            "(jet_selectedPatJetsAK15PFPuppi_pT_reco > 200) & (fabs(jet_selectedPatJetsAK15PFPuppi_eta_reco) < 2.4) & (jet_selectedPatJetsAK15PFPuppi_nConsti_reco >= 3) & (jet_selectedPatJetsAK15PFPuppi_nearestGenTopDR_reco < 1) & (jet_selectedPatJetsAK15PFPuppi_nearestGenTopIsLeptonic_reco > 0.5) & (abs(jet_selectedPatJetsAK15PFPuppi_consti_id_reco) == {pdgid}) & (jet_selectedPatJetsAK15PFPuppi_consti_pT_reco > 20)" \
            "(jet_selectedPatJetsAK15PFPuppi_pT_reco > 200) & (fabs(jet_selectedPatJetsAK15PFPuppi_eta_reco) < 2.4) & (jet_selectedPatJetsAK15PFPuppi_nConsti_reco >= 3) & (jet_selectedPatJetsAK15PFPuppi_nearestGenTopDR_reco < 1) & (jet_selectedPatJetsAK15PFPuppi_nearestGenTopIsLeptonic_reco < 0.5) & (abs(jet_selectedPatJetsAK15PFPuppi_consti_id_reco) == {pdgid}) & (jet_selectedPatJetsAK15PFPuppi_consti_pT_reco > 20)" \
            "(jet_selectedPatJetsAK15PFPuppi_pT_reco > 200) & (fabs(jet_selectedPatJetsAK15PFPuppi_eta_reco) < 2.4) & (jet_selectedPatJetsAK15PFPuppi_nConsti_reco >= 3) & (abs(jet_selectedPatJetsAK15PFPuppi_consti_id_reco) == {pdgid}) & (jet_selectedPatJetsAK15PFPuppi_consti_pT_reco > 20)" \
            "(jet_selectedPatJetsAK15PFPuppi_pT_reco > 200) & (fabs(jet_selectedPatJetsAK15PFPuppi_eta_reco) < 2.4) & (jet_selectedPatJetsAK15PFPuppi_nConsti_reco >= 3) & (abs(jet_selectedPatJetsAK15PFPuppi_consti_id_reco) == {pdgid}) & (jet_selectedPatJetsAK15PFPuppi_consti_pT_reco > 20)" \
        --labels \
            "t^{{lep}}" \
            "t^{{had}}" \
            "QCD" \
            "QCD (b)" \
        --lineColors \
            2 \
            4 \
            6 \
            8 \
        --plotBin 100 0 1.001 \
        --xRange 0 1.001 \
        --yRange 1e-6 10 \
        --logY \
        --xTitle "Transformed |d_{{xy}}({pdgidName}, SV)|" \
        --yTitle "arbitrary unit" \
        --title "title" \
        --titlePos 0 0 \
        --outFileName "out_transformed-svdxy_id{pdgid}.pdf" \
    """.format(
        pdgid = pdgid,
        pdgidName = pdgidName,
        outDir = outDir,
    )
    
    os.system(command)
    print("\n")



command = """
    python -u plot_variable.py \
    --fileAndTreeNames \
        "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/ntupleTree_ZprimeToTT_M1000_W10_new.root:treeMaker/tree" \
        "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/ntupleTree_ZprimeToTT_M1000_W10_new.root:treeMaker/tree" \
        "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/ntupleTree_QCD_Pt_470to600_PREMIX_RECODEBUG_new.root:treeMaker/tree" \
        "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/ntupleTree_QCD_bEnriched_HT700to1000.root:treeMaker/tree" \
    --plotVars \
        "jet_selectedPatJetsAK15PFPuppi_nSecVtxInJet_reco" \
        "jet_selectedPatJetsAK15PFPuppi_nSecVtxInJet_reco" \
        "jet_selectedPatJetsAK15PFPuppi_nSecVtxInJet_reco" \
        "jet_selectedPatJetsAK15PFPuppi_nSecVtxInJet_reco" \
    --cuts \
        "(jet_selectedPatJetsAK15PFPuppi_pT_reco > 200) & (fabs(jet_selectedPatJetsAK15PFPuppi_eta_reco) < 2.4) & (jet_selectedPatJetsAK15PFPuppi_nConsti_reco >= 3) & (jet_selectedPatJetsAK15PFPuppi_nearestGenTopDR_reco < 1) & (jet_selectedPatJetsAK15PFPuppi_nearestGenTopIsLeptonic_reco > 0.5)" \
        "(jet_selectedPatJetsAK15PFPuppi_pT_reco > 200) & (fabs(jet_selectedPatJetsAK15PFPuppi_eta_reco) < 2.4) & (jet_selectedPatJetsAK15PFPuppi_nConsti_reco >= 3) & (jet_selectedPatJetsAK15PFPuppi_nearestGenTopDR_reco < 1) & (jet_selectedPatJetsAK15PFPuppi_nearestGenTopIsLeptonic_reco < 0.5)" \
        "(jet_selectedPatJetsAK15PFPuppi_pT_reco > 200) & (fabs(jet_selectedPatJetsAK15PFPuppi_eta_reco) < 2.4) & (jet_selectedPatJetsAK15PFPuppi_nConsti_reco >= 3)" \
        "(jet_selectedPatJetsAK15PFPuppi_pT_reco > 200) & (fabs(jet_selectedPatJetsAK15PFPuppi_eta_reco) < 2.4) & (jet_selectedPatJetsAK15PFPuppi_nConsti_reco >= 3)" \
    --labels \
        "t^{{lep}}" \
        "t^{{had}}" \
        "QCD" \
        "QCD (b)" \
    --lineColors \
        2 \
        4 \
        6 \
        8 \
    --plotBin 50 0 50 \
    --xRange 0 10 \
    --yRange 0 1 \
    --xTitle "n_{{SV}} in jet" \
    --yTitle "arbitrary unit" \
    --title "title" \
    --titlePos 0 0 \
    --outFileName "out_nSecVtxInJet.pdf" \
""".format(
    outDir = outDir,
)

os.system(command)
print("\n")



#--fileAndTreeNames
#--cuts
#--plotVars
#--wVars
#--labels
#--lineColors
#--lineStyles
#--lineWidths
#--plotBin
#--xRange
#--yRange
#--logY
#--xTitle
#--yTitle
#--nDivX
#--nDivY
#--title
#--titlePos
#--outFileName
