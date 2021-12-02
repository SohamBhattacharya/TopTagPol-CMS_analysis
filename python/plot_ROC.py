from __future__ import print_function

import argparse
import array
import copy
import matplotlib
import matplotlib.pyplot
import multiprocessing
import numpy
import os
import pprint
import scipy
import scipy.interpolate
import scipy.special
#import tabulate
import time
import uproot

import CMS_lumi
import utils

import ROOT
ROOT.gROOT.SetBatch(1)
ROOT.ROOT.EnableImplicitMT(20)


pprinter = pprint.PrettyPrinter(width = 500, depth = 2)


def main() :
    
    # Argument parser
    parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
    
    
    parser.add_argument(
        "--config",
        help = "Configuration file",
        type = str,
        required = True,
    )
    
    
    # Parse arguments
    args = parser.parse_args()
    d_args = vars(args)
    
    
    d_config = utils.load_config(args.config)
    
    final_weight_name = "final_weight"
    classifier_name = "classifier"
    
    l_hist = []
    l_graph = []
    
    for iCurve, d_curve in enumerate(d_config["curves"]) :
        
        d_rdframe = {}
        
        d_count_num = {}
        d_count_den = {}
        
        l_classifiercut = [0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.97, 0.99, 0.995, 0.999, 0.9999]
        
        for type_key in ["sig", "bkg"] :
            
            d_rdframe[type_key] = []
            
            l_tree_sample = []
            l_tree_friend = []
            
            l_sample_name   = d_config["samples"][d_curve[type_key]["sample"]]["names"]
            l_sample_weight = d_config["samples"][d_curve[type_key]["sample"]]["weights"]
            l_sample_norm   = [1] * len(l_sample_weight)
            
            weight_expr = d_curve[type_key]["weight"].format(**d_curve["vardict"])
            classifier_expr = d_curve["classifier"].format(**d_curve["vardict"])
            
            d_count_num[type_key] = numpy.zeros((len(l_sample_name), len(l_classifiercut)))
            d_count_den[type_key] = numpy.zeros((len(l_sample_name), len(l_classifiercut)))
            
            for iSample, sample_entry in enumerate(l_sample_name) :
                
                verbosetag_sample = "[sample %d/%d]" %(iSample+1, len(l_sample_name))
                
                sample, tag = sample_entry.split(":")
                sample_weight = l_sample_weight[iSample]
                
                sample_source = d_curve[type_key]["source"].format(
                    sample = sample,
                    tag = tag,
                )
                
                l_sample_file = numpy.loadtxt(sample_source, dtype = str, delimiter = "x"*100) ##[0: 1]
                l_sample_filename = [entry.split("/")[-1] for entry in l_sample_file]
                
                print("l_sample_file:\n", "\n".join(l_sample_file))
                
                tree_sample = ROOT.TChain(d_curve[type_key]["tree"])
                
                for entry in l_sample_file :
                    
                    print("%s adding file: %s" %(verbosetag_sample, entry))
                    tree_sample.Add(entry)
                
                l_tree_friend.append([])
                
                for iFriend, d_friend in enumerate(d_curve["friends"]) :
                    
                    verbosetag_friend = "[friend %d/%d]" %(iFriend+1, len(d_curve["friends"]))
                    
                    l_sample_friend = [
                        "{dir}/{sample}_{tag}/{entry}".format(
                            dir = d_friend["dir"],
                            sample = sample,
                            tag = d_friend["tag"] if (d_friend["tag"] is not None) else tag,
                            entry = entry,
                        ) for entry in l_sample_filename
                    ]
                    
                    print("l_sample_friend:\n", "\n".join(l_sample_friend))
                    
                    tree_friend = ROOT.TChain(d_friend["tree"])
                    
                    for entry in l_sample_friend :
                        
                        print("%s %s adding file: %s" %(verbosetag_sample, verbosetag_friend, entry))
                        tree_friend.Add(entry)
                    
                    # Need to keep a reference to the tree chain
                    l_tree_friend[-1].append(tree_friend)
                    
                    tree_sample.AddFriend(tree_friend)
                
                # Need to keep a reference to the tree chain
                l_tree_sample.append(tree_sample)
                
                
                rdframe_sample = ROOT.RDataFrame(tree_sample)
                
                #weight_expr_sample = "({sample_weight}) * ({weight_expr}) * {norm}".format(
                #    sample_weight = sample_weight,
                #    weight_expr = weight_expr,
                #    #norm = 1,
                #    norm = 1.0/tree_sample.GetEntries(),
                #)
                
                weight_expr_sample = weight_expr
                l_sample_norm[iSample] = float(sample_weight)/tree_sample.GetEntries()
                
                rdframe_sample = rdframe_sample.Define(final_weight_name, weight_expr_sample)
                rdframe_sample = rdframe_sample.Define(classifier_name, classifier_expr)
                
                d_rdframe[type_key].append(rdframe_sample)
            
            
            #l_count_sample_num = []
            l_count_sample_den = []
            
            for iSample, rdframe in enumerate(d_rdframe[type_key]) :
                
                print("")
                print(l_sample_name[iSample])
                
                weight = l_sample_norm[iSample]
                
                count = rdframe.Sum(final_weight_name).GetValue()
                weighted_count = count * weight
                #l_count_sample_den.append(weighted_count)
                #print(count, weighted_count)
                
                classifiercut_expr = "(%s) * (%s)" %(final_weight_name, d_curve["classifiercut"])
                #print(classifiercut_expr)
                
                d_count_den[type_key][iSample:] = weighted_count
                
                for iCut, cutval in enumerate(l_classifiercut) :
                    
                    classifiercut_expr_mod = classifiercut_expr.format(
                        classifier = classifier_name,
                        value = cutval,
                    )
                    
                    rdframe_mod = rdframe.Define("classifier_cut", classifiercut_expr_mod)
                    
                    count = rdframe_mod.Sum("classifier_cut").GetValue()
                    weighted_count = count * weight
                    #l_count_sample_num.append(weighted_count)
                    
                    d_count_num[type_key][iSample, iCut] = weighted_count
                    #print(count, weighted_count)
                    
                    #print("eff", l_count_sample_num[-1]/l_count_sample_den[-1])
                    
                    eff = d_count_num[type_key][iSample, iCut] / d_count_den[type_key][iSample, iCut] if (d_count_den[type_key][iSample, iCut]) else 0
                    
                    print("[%s] cut %0.6f, num %0.6e, den %0.6e, eff %0.4e" %(type_key, cutval, d_count_num[type_key][iSample, iCut], d_count_den[type_key][iSample, iCut], eff))
            
            #num = sum(l_count_sample_num)
            #den = sum(l_count_sample_den)
            #eff = num/den if (den) else 0
            #
            #print("")
            #print("Final:")
            #print(num, den, eff)
        
        
        print("")
        print("Final:")
        
        
        a_eff_sig = numpy.zeros(len(l_classifiercut))
        a_eff_bkg = numpy.zeros(len(l_classifiercut))
        
        for iCut, cutval in enumerate(l_classifiercut) :
            
            num_sig = numpy.sum(d_count_num["sig"][:, iCut])
            den_sig = numpy.sum(d_count_den["sig"][:, iCut])
            eff_sig = num_sig/den_sig if (den_sig) else 0
            a_eff_sig[iCut] = eff_sig
            
            num_bkg = numpy.sum(d_count_num["bkg"][:, iCut])
            den_bkg = numpy.sum(d_count_den["bkg"][:, iCut])
            eff_bkg = num_bkg/den_bkg if (den_bkg) else 0
            a_eff_bkg[iCut] = eff_bkg
            
            
            print("cut %0.6f, eff_sig %0.4e, eff_bkg %0.4e" %(cutval, eff_sig, eff_bkg))
        
        
        #a_eff_sig = array.array("f", numpy.linspace(0.1, 1, 1000))
        #a_eff_bkg = array.array("f", numpy.linspace(0.1, 1, 1000))
        
        gr_ROC = ROOT.TGraph(len(a_eff_sig), a_eff_sig, a_eff_bkg)
        gr_ROC.SetName("graph_%d" %(iCurve+1))
        h1_ROC = utils.root_TGraph_to_TH1(graph = gr_ROC, setError = False)
        
        gr_ROC.GetXaxis().SetRangeUser(d_config["xrange"][0], d_config["xrange"][1])
        gr_ROC.SetLineColor(d_curve["color"])
        gr_ROC.SetLineStyle(d_curve["linestyle"])
        gr_ROC.SetLineWidth(3)
        gr_ROC.SetMarkerSize(0)
        gr_ROC.SetFillStyle(0)
        
        h1_ROC.GetXaxis().SetRangeUser(d_config["xrange"][0], d_config["xrange"][1])
        h1_ROC.SetLineColor(d_curve["color"])
        h1_ROC.SetLineStyle(d_curve["linestyle"])
        h1_ROC.SetLineWidth(3)
        h1_ROC.SetMarkerSize(0)
        h1_ROC.SetFillStyle(0)
        
        print(h1_ROC.GetEntries())
        print(h1_ROC.GetNbinsX())
        
        l_hist.append(h1_ROC)
        l_graph.append(gr_ROC)
    
    
    
    ROOT.gROOT.LoadMacro("utils/tdrstyle.C")
    ROOT.gROOT.ProcessLine("setTDRStyle()")
    
    ROOT.gROOT.SetStyle("tdrStyle")
    ROOT.gROOT.ForceStyle(True)
    
    canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
    canvas.UseCurrentStyle()
    
    canvas.SetLeftMargin(0.165)
    canvas.SetRightMargin(0.05)
    canvas.SetTopMargin(0.1)
    canvas.SetBottomMargin(0.135)
    
    
    legendHeightScale = 1
    legendWidthScale = 1
    
    legendHeight = legendHeightScale * 0.05 * len(l_hist)
    legendWidth = legendWidthScale * 0.65
    
    padTop = 1 - canvas.GetTopMargin() - 1*ROOT.gStyle.GetTickLength("y")
    padRight = 1 - canvas.GetRightMargin() - 0.6*ROOT.gStyle.GetTickLength("x")
    padBottom = canvas.GetBottomMargin() + 0.6*ROOT.gStyle.GetTickLength("y")
    padLeft = canvas.GetLeftMargin() + 0.6*ROOT.gStyle.GetTickLength("x")
    
    legendpos = d_config["legendpos"]
    
    if(legendpos == "UR") :
        
        legend = ROOT.TLegend(padRight-legendWidth, padTop-legendHeight, padRight, padTop)
    
    elif(legendpos == "LR") :
        
        legend = ROOT.TLegend(padRight-legendWidth, padBottom, padRight, padBottom+legendHeight)
    
    elif(legendpos == "LL") :
        
        legend = ROOT.TLegend(padLeft, padBottom, padLeft+legendWidth, padBottom+legendHeight)
    
    elif(legendpos == "UL") :
        
        legend = ROOT.TLegend(padLeft, padTop-legendHeight, padLeft+legendWidth, padTop)
    
    else :
        
        print("Wrong legend position option:", legendpos)
        exit(1)
    
    
    #legend.SetNColumns(legendNcol)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(d_config["legendtextsize"])
    
    #ROOT.SetOwnership(legend, 0)
    
    #if (len(legendTitle)) :
    #    
    #    legend.SetHeader(legendTitle)
    #    legendHeader = legend.GetListOfPrimitives().First()
    #    legendHeader.SetTextAlign(23)
    #    
    #    # For whatever reason, SetHeader("Header", "C") does not accept the second argument in python
    #    # So, center the header this way
    #    # EVEN THIS DOESN'T WORK! Gives a seg-fault when calling the plot1D(...) function for the second time
    #    #legend.GetListOfPrimitives().First().SetTextAlign(22)
    
    #legend.SetLegendBorderMode(0)
    
    stack = ROOT.THStack()
    
    # Add a dummy histogram so that the X-axis range can be beyond the histogram range
    h1_xRange = ROOT.TH1F("h1_xRange", "h1_xRange", 1, d_config["xrange"][0], d_config["xrange"][1])
    stack.Add(h1_xRange)
    
    stack.Draw("nostack")
    legend.Draw()
    
    stack.GetXaxis().SetRangeUser(d_config["xrange"][0], d_config["xrange"][1])
    stack.SetMinimum(d_config["yrange"][0])
    stack.SetMaximum(d_config["yrange"][1])
    
    #stack.GetXaxis().SetLabelSize(ROOT.gStyle.GetLabelSize("X") * xLabelSizeScale)
    #stack.GetYaxis().SetLabelSize(ROOT.gStyle.GetLabelSize("Y") * yLabelSizeScale)
    
    stack.GetXaxis().SetTitle(d_config["xtitle"])
    #stack.GetXaxis().SetTitleSize(ROOT.gStyle.GetTitleSize("X") * xTitleSizeScale)
    stack.GetXaxis().SetTitleOffset(ROOT.gStyle.GetTitleOffset("X") * 1.1)
    
    stack.GetYaxis().SetTitle(d_config["ytitle"])
    #stack.GetYaxis().SetTitleSize(ROOT.gStyle.GetTitleSize("Y") * yTitleSizeScale)
    stack.GetYaxis().SetTitleOffset(ROOT.gStyle.GetTitleOffset("Y") * 1)
    
    #stack.SetTitle(title)

    stack.GetXaxis().CenterTitle(True)
    stack.GetYaxis().CenterTitle(True)
    
    # Bin label position
    #if (centerLabelsX) :
    #    
    #    stack.GetXaxis().CenterLabels()
    #
    #if (centerLabelsY) :
    #    
    #    stack.GetYaxis().CenterLabels()
    
    
    for iCurve, d_curve in enumerate(d_config["curves"]) :
        
        hist = l_hist[iCurve]
        graph = l_graph[iCurve]
        label = d_curve["label"]
        
        draw_opt = "L"
        
        graph.Draw("%s SAME" %(draw_opt))
        #stack.Add(hist, draw_opt)
        legend.AddEntry(graph, label, "L")
    
    
    canvas.SetLogx(d_config["logx"])
    canvas.SetLogy(d_config["logy"])
    
    canvas.SetGridx(d_config["gridx"])
    canvas.SetGridy(d_config["gridy"])
    
    
    CMS_lumi.CMS_lumi(pad = canvas, iPeriod = 0, iPosX = 0, CMSextraText = "Simulation Preliminary", lumiText = "(13 TeV)")
    
    if ("/" in d_config["outfile"]) :
        
        outdir = d_config["outfile"]
        outdir = outdir[0: outdir.rfind("/")]
        
        os.system("mkdir -p %s" %(outdir))
    
    canvas.SaveAs(d_config["outfile"])
    
    return 0


if (__name__ == "__main__") :
    
    main()
