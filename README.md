<p align="center">
  <img src="docs/img/PhishingTracker.jpg">
</p>

<h1 align="center">PhishingKitTracker</h1>
<p align="center">
  <a href="https://python.org/">
    <img src="https://img.shields.io/pypi/pyversions/3.svg">
  </a>
    <a href="https://opensource.org">
    <img src="https://img.shields.io/badge/Open%20Source-%E2%9D%A4-brightgreen.svg">
  </a>
</p>

<p align="center">
  An extensible and freshly updated collection of phishingkits for forensics and future analysis topped with simple stats
</p>


## Disclaimer
This repository holds a collection of Phishing Kits used by criminals to steal user information. Almost every file into the `raw` folder is malicious so I strongly recommend you to neither open these files, nor misuse the code to prank your friends. Playing with these kits may lead to irreversible consequences which may affect anything from personal data to passwords and banking information.

**I am not responsible for any damage caused by the malware inside my repository and your negligence in general.**

#### NB: Large File System Hahead
`PhishingKitTracker` is stored into Git Large File System (git-lfs) due to the big amount of data tracked. You *should* install [git-lfs](https://git-lfs.github.com/) before cloning this repository. 

## RAW Data
In `raw` folder are tracked the Phishing Kits in the original format. No manipulation are involved in that data. A backend script goes over malicious harvested websites (harvesting from common sources) and checks if Phishing Kits are in there. In a positive case (if a PhishingKit is found) the resulting file is downloaded and instantly added to that folder. This folder is tracked by using Git Large File System since many files are bigger than 100MB. This is a quite unexplored land since so you would find many interesting topics with high probability.

## STATS 
In `stats` folder are mantained two up to dade files:
1. `files_name` it holds the frequency of the found file names associate with kits. Inother words every phishing kit is saved on the phishing host with a name. This file keeps track about file name. If you are wondering why am I not tracking hashes, is because phishing kits are big specialized compressed archives, so it would make no sense at this stage (but check in `src` folder)
2. `sites` it hols the frequency of the hosting domains. In other words where the phishing kit was found.
No dups are tracked, by meaning that the frequency and the file names are uniques. So for example if you see something like: `3 li.humanbiomics-project.org` it means that in `li.humanbiomics-project.org` have been found three different Phishing Kits over time.

Both of these files have been generate by simple bash scripts like:
- `ls raw/ | cut -d'_' -f1 | uniq -c | sort -bgr > stats/sites.txt`
- `ls raw/ | cut -d'_' -f2 | uniq -c | sort -bgr > stats/files_name.txt`

these scripts are run on every commit making files inline with the raw folder.

On the other side a file called `similarity.csv` is provided with a tremendous delay due to the vast amount of time in generating it.
That file provides the similarity between the tracked Phishing Kits. It's a simple CSV file so that you can import it on your favourite spreadsheet and make graphs, statistics or manipulate it in the way you prefer.  

### SIMILARITY.CSV structure

The similarity structure is like the following one: `FileA,FileB,SimilarityAVG,SimilarityMin,SimilarityMax` where:
- *FileA* is PhishingKit which is considered in that analysis.
- *FileB* is the PhishingKit to be compared to PhishingKit FileA
- *SimilarityAVG* is the Average in similarity. That average is calculated by computing the similarity check to every single (interesting) file in the PhishingKit archive (FileA) to every single (interesting) file in the PhishingKit archive to be compared (FileB)  
- *SimilarityMin* is the lowest similarity value found between PhishingKitA and PhishingKitB
- *SimilarityMax* is the highest similarity value found between PhishingKitA and PhishingKitB


If you want to generate `similarity.csv` by your own I provide a simple and dirty script into the `src` folder. So far it has several limitations (for example it computes ZIP onli files). *please make pull requests for improving and empower it*. Each contribute would be very helpfull.

## SRC

Please check those variables and change them at your will.

```python
EXTENSION_FOR_ANALYSIS = ['.html','.js','.vbs','.xls','.xlsm','.doc','.docm', '.ps1']
OUTPUT_FILE =  'similarity.csv'                                                 
RAW_FOLDER = '/tmp/raw/'                                                        
TEMP_FOLDER = '/tmp/tt'     
```

The Python script is in a super early stage of development. Please help to improve it.

### Credits
* Alen Pavlovic for the amazing image that I borrowed from [here](https://dribbble.com/Type08) 
* agarwalkeshav8399 for code similarity algorithms from [here](https://www.geeksforgeeks.org/measuring-the-document-similarity-in-python/)
