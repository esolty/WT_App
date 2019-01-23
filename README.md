# Wall Thickness Calculator

Wall thickness is calculated by taking the median of Wt_Calc field of a section of Girthwelds as indicated by the marked girth weld ups and downs. 

## Getting Started

Using executable - open and select file, pipe size, edit list of wall thickness, select options and run

Generating executable (possibily incomplete)
- use python 3.6
- create virtual env (recommended venv), 
- download libs (numpy, pandas, dbfread, pyinstaller, pyqt5, path)
- run pyinstaller onefile install
- if using anaconda distribution, edit spec file hiddenimports=['pandas._libs.tslibs.timedeltas']
  - run pyinstaller onefile install using spec file

### Files

App.py contains view and controller
model.py contains model
qtwindow.ui file generated from qt designer
qtwindow.py ui file converted to py

### Prerequisites

If executable provided - windows
Anaconda distribution not recommended, pyinstaller may then create 500 mb apps
python 3.6 and associated libraries

#### Application and README is underdevelopment - 20190122
