import argparse
import awkward
import matplotlib
import matplotlib.colors
import matplotlib.pyplot
import mplhep
import numpy
import os
import re
import sortedcontainers
import time
import uproot

import ROOT
ROOT.gROOT.SetBatch(1)

import CMS_lumi
#import tdrstyle

import Common


def main() :
    
    
    # Argument parser
    parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
    
    parser.add_argument(
        "--fileAndTreeNames",
        help = "Syntanx: fileName1:treeName1 fileName2:treeName2 ...",
        type = str,
        nargs = "*",
        required = True,
    )
    
    parser.add_argument(
        "--cuts",
        help = "Cuts",
        type = str,
        nargs = "*",
        required = True,
    )
    
    parser.add_argument(
        "--plotVars",
        help = "Plot variables",
        type = str,
        nargs = "*",
        required = True,
    )
    
    parser.add_argument(
        "--wVars",
        help = "Weight variables",
        type = str,
        nargs = "*",
        required = False,
        default = None,
    )
    
    parser.add_argument(
        "--labels",
        help = "Plot labels",
        type = str,
        nargs = "*",
        required = True,
    )
    
    parser.add_argument(
        "--lineColors",
        help = "Line colors",
        type = int,
        nargs = "*",
        required = True,
    )
    
    parser.add_argument(
        "--lineStyles",
        help = "Line styles",
        type = int,
        nargs = "*",
        required = False,
        default = None,
    )
    
    parser.add_argument(
        "--lineWidths",
        help = "Line widths",
        type = int,
        nargs = "*",
        required = False,
        default = None,
    )
    
    parser.add_argument(
        "--plotBin",
        help = "Bins: nBin min max",
        type = float,
        nargs = 3,
        required = True,
    )
    
    parser.add_argument(
        "--xRange",
        help = "x-axis display range",
        type = float,
        nargs = 2,
        required = True,
    )
    
    parser.add_argument(
        "--yRange",
        help = "y-axis range",
        type = float,
        nargs = 2,
        required = True,
    )
    
    parser.add_argument(
        "--logY",
        help = "y-axis in log scale",
        default = False,
        action = "store_true",
    )
    
    parser.add_argument(
        "--xTitle",
        help = "X-axis title",
        type = str,
        required = False,
        default = "X",
    )
    
    parser.add_argument(
        "--yTitle",
        help = "Y-axis title",
        type = str,
        required = False,
        default = "Y",
    )
    
    parser.add_argument(
        "--nDivX",
        help = "X-axis divisions (ROOT): primary seconday tertiary. E.g. 5 5 0",
        type = int,
        nargs = 3,
        required = False,
        default = None,
    )
    
    parser.add_argument(
        "--nDivY",
        help = "Y-axis divisions (ROOT): primary seconday tertiary. E.g. 5 5 0",
        type = int,
        nargs = 3,
        required = False,
        default = None,
    )
    
    parser.add_argument(
        "--title",
        help = "Plot title",
        type = str,
        required = False,
        default = "",
    )
    
    parser.add_argument(
        "--titlePos",
        help = "Title position (in data coordinates): x y",
        type = float,
        nargs = 2,
        required = False,
        default = [0, 0],
    )
    
    parser.add_argument(
        "--outFileName",
        help = "Output file name",
        type = str,
        required = True,
    )
    
    
    # Parse arguments
    args = parser.parse_args()
    d_args = vars(args)
    
    
    if (args.lineStyles is None) :
        
        args.lineStyles = [1] * len(args.plotVars)
    
    if (args.lineWidths is None) :
        
        args.lineWidths = [2] * len(args.plotVars)
    
    
    l_hist = []
    
    for iVar, varName in enumerate(args.plotVars) :
        
        histName = "h1_var%d" %(iVar+1)
        h1_var = ROOT.TH1F(histName, histName, int(args.plotBin[0]), args.plotBin[1], args.plotBin[2])
        
        plotVarName = "plotVar"
        weightVarName = "wVar"
        
        d_branchName_alias = {}
        d_branchName_alias[plotVarName] = args.plotVars[iVar]
        
        if (args.wVars is not None) :
            
            d_branchName_alias[weightVarName] = args.wVars[iVar]
        
        l_branchName = list(d_branchName_alias.keys())
        
        for tree_branches in uproot.iterate(
            files = args.fileAndTreeNames[iVar],
            expressions = l_branchName,
            aliases = d_branchName_alias,
            cut = args.cuts[iVar],
            language = Common.uproot_lang,
            step_size = 100000,
        ) :
            
            print(args.fileAndTreeNames[iVar])
            
            a_plotVar = awkward.flatten(tree_branches[plotVarName], axis = None).to_numpy()
            
            a_wVar = awkward.flatten(tree_branches[weightVarName], axis = None).to_numpy() if (args.wVars is not None) else numpy.ones(len(a_plotVar))
            
            h1_var.FillN(len(a_plotVar), a_plotVar, a_wVar)
        
        
        print(h1_var.Integral(), h1_var.GetEntries())
        h1_var.Scale(1.0 / h1_var.Integral())
        #h1_var.Scale(1.0 / h1_var.GetEntries())
        
        h1_var.SetLineColor(args.lineColors[iVar])
        h1_var.SetLineStyle(args.lineStyles[iVar])
        h1_var.SetLineWidth(args.lineWidths[iVar])
        
        h1_var.SetMarkerColor(args.lineColors[iVar])
        h1_var.SetMarkerSize(0)
        h1_var.SetFillStyle(0)
        
        
        l_hist.append(h1_var)
    
    
    
    canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
    
    stack = ROOT.THStack("stack", "")
    
    legendHeightScale = 1
    legendWidthScale = 1
    
    legendPos = "UR"
    
    legendHeight = legendHeightScale * 0.05 * len(l_hist)
    legendWidth = legendWidthScale * 0.65
    
    padTop = 1 - canvas.GetTopMargin() - 0.6*ROOT.gStyle.GetTickLength("y")
    padRight = 1 - canvas.GetRightMargin() - 0.6*ROOT.gStyle.GetTickLength("x")
    padBottom = canvas.GetBottomMargin() + 0.6*ROOT.gStyle.GetTickLength("y")
    padLeft = canvas.GetLeftMargin() + 0.6*ROOT.gStyle.GetTickLength("x")
    
    if(legendPos == "UR") :
        
        legend = ROOT.TLegend(padRight-legendWidth, padTop-legendHeight, padRight, padTop)
    
    elif(legendPos == "LR") :
        
        legend = ROOT.TLegend(padRight-legendWidth, padBottom, padRight, padBottom+legendHeight)
    
    elif(legendPos == "LL") :
        
        legend = ROOT.TLegend(padLeft, padBottom, padLeft+legendWidth, padBottom+legendHeight)
    
    elif(legendPos == "UL") :
        
        legend = ROOT.TLegend(padLeft, padTop-legendHeight, padLeft+legendWidth, padTop)
    
    
    for iVar, varName in enumerate(args.plotVars) :
        
        stack.Add(l_hist[iVar], "hist")
        
        legend.AddEntry(l_hist[iVar], "%s (#mu=%0.2f, #sigma=%0.2f)" %(args.labels[iVar], l_hist[iVar].GetMean(), l_hist[iVar].GetStdDev()), "LP")
    
    
    stack.Draw("nostack")
    legend.Draw()
    
    stack.GetXaxis().SetRangeUser(*args.xRange)
    
    stack.SetMinimum(args.yRange[0])
    stack.SetMaximum(args.yRange[1])
    
    stack.GetXaxis().SetTitle(args.xTitle)
    stack.GetYaxis().SetTitle(args.yTitle)
    
    canvas.SetLogy(args.logY)
    
    canvas.SaveAs(args.outFileName)
    
    
    return 0


if (__name__ == "__main__") :
    
    main()
