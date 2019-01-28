# Wall Thickness Calculator

Wall thickness is calculated by taking the median of Wt_Calc field of a section of Girthwelds as indicated by the marked girth weld ups and downs. Girth weld ups and downs may be determined as well. Casings, sleeves and installations will not change Wall thickness wt calc field if identified.

## Getting Started

Using executable - open and select file, pipe size, edit list of wall thickness, select options and run

Generating executable 
- create virtual env (virtualenv) 
- download libs (numpy, pandas, dbfread, pyinstaller, pyqt5, path(possibily incomplete))
- run pyinstaller onefile install on App.py "pyinstaller --onefile App.py"
- if using anaconda distribution, edit spec file hiddenimports=['pandas._libs.tslibs.timedeltas']
  - run pyinstaller onefile install using spec file "pyinstaller --onefile App.spec"

### Files

App.py contains view and controller
model.py contains model
qtwindow.ui file generated from qt designer
qtwindow.py ui file converted to py

### Prerequisites

If executable provided - windows
Anaconda distribution not recommended, pyinstaller may then create 500 mb apps
python 3.6

![alt text](https://github.com/esolty/WT_App/blob/master/WT_tool.PNG "Pipe Wall Thickness Calculator")

#### Application and README is underdevelopment - 20190122
