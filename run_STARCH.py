from STARCH import STARCH
import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
 
parser.add_argument('-t','--threads',required=False,type=float,default=0,help="threads") 
parser.add_argument('-beta_spot','--beta_spot',required=False,default=2.0,type=float,help="spot")  
parser.add_argument('-c','--n_clusters',required=True,type=int,help="number of clones")   
parser.add_argument('-i','--input',required=True,nargs='+',help="name of input file (either expression matrix in .csv, .tsv, .txt format or 10X directory containing barcodes.tsv, features.tsv, matrix.mtx, and tissue_positions_list.csv)")   
parser.add_argument('-normal_spots','--normal_spots',required=False,type=str,help="name of input file containing indices of normal spots",default=0)
parser.add_argument('-returnnormal','--returnnormal',required=False,type=int,default=1)   
parser.add_argument('-o','--output',required=False,type=str,default='STITCH_output',help='output name (ex. prostate1)') 
parser.add_argument('-outdir','--outdir',required=False,type=str,default='.',help='output directory') 
parser.add_argument('-m','--gene_mapping_file_name',required=False,type=str,default='hgTables_hg19.txt',help='gene mapping file name') 
args = parser.parse_args()

nthreads = int(args.threads)
beta_spot = args.beta_spot
n_clusters = args.n_clusters
returnnormal = args.returnnormal
i = args.input
normal_spots = args.normal_spots
out = args.output
gene_mapping_file_name = args.gene_mapping_file_name
outdir = args.outdir

if normal_spots !=0:
	normal_spots = np.asarray(pd.read_csv(normal_spots,header=None)).flatten()
else:
	normal_spots = []

operator = STARCH(i,n_clusters=n_clusters,num_states=3,normal_spots=normal_spots,beta_spots = beta_spot,nthreads=nthreads,gene_mapping_file_name=gene_mapping_file_name)
posteriors = operator.callCNA(beta_spots=beta_spot,nthreads=nthreads,returnnormal=returnnormal)

pd.DataFrame(operator.states).to_csv('%s/states_%s.csv'%(outdir,out),sep=',')
pd.DataFrame(operator.labels).to_csv('%s/labels_%s.csv'%(outdir,out),sep=',')
