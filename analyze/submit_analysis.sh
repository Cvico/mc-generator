#!/bin/bash
sbatch --wrap 'python3 ttw_nanogen_analysis.py --inputFolder samples --inputFile ttW_gennano_qcut42.root'
sbatch --wrap 'python3 ttw_nanogen_analysis.py --inputFolder samples --inputFile ttW_gennano_qcut150.root'
sbatch --wrap 'python3 ttw_nanogen_analysis.py --inputFolder samples --inputFile central_qCut42.root'
sbatch --wrap 'python3 ttw_nanogen_analysis.py --inputFolder samples --inputFile central_qCut150.root'
