#!/usr/bin/python

def noCuts_html_string():
    return """\
<!DOCTYPE html>
 <html>
  <head>
    <title>DESY CMS SUSY Group</title>
    <link rel="stylesheet" href="../../../css/style.css" type="text/css"/>
  </head>
 
  <body>
    <!-- headline -->  
    <div id="head">
      <h1 id="headline">SUSY Group</h1>     
      <div id="head-left">
        <a href="http://www.desy.de/">
          <img id="head-logo-right" src="../../../images/DESY-Logo-cyan-RGB_mitVorschau_ger.png" alt="DESY-Logo"/>
	</a>
      </div>
      <div id="head-left">
        <a href="http://cms.web.cern.ch/">
          <img id="head-logo" src="../../../images/CMS-Color.png" alt="CMS-Logo"/>
        </a>
      </div>
    </div>
    <!-- sidebar -->
    <div id="newcontent">
      <div id="sidebar"><h2>Cuts</h2>
	<ul>
	  <li><a href="noCuts.html" style="text-decoration:none;"> No Cuts </a>
	  </li>
	</ul>
      </div> 
    </div>
    <!-- main part -->
    <div id="content">
    <!-- multiplicity plots --> 
      <p id="title"> Multiplicities </p>
      <div id="picture">
	<a href="plots/noCuts/pdf/nJet_0.pdf">
	  <img src="plots/noCuts/png/nJet_0.png" />
	</a>
      </div>
      <div id="picture">
	<a href="plots/noCuts/pdf/nBJet_0.pdf">
	  <img src="plots/noCuts/png/nBJet_0.png" />
	</a>
      </div>
      <div id="picture">
	<a href="plots/noCuts/pdf/nLep_0.pdf">
	  <img src="plots/noCuts/png/nLep_0.png" />
	</a>
      </div>
      <div id="picture">
	<a href="plots/noCuts/pdf/nMu_0.pdf">
	  <img src="plots/noCuts/png/nMu_0.png" />
	</a>
      </div>
      <div id="picture">
	<a href="plots/noCuts/pdf/nEl_0.pdf">
	  <img src="plots/noCuts/png/nEl_0.png" />
	</a>
      </div>
      <!-- jet pT -->
      <br class="blank" />
      <p style="clear:left;"></p>
      <p id="title"> Jet pT </p>
      <div id="picture">
	<a href="plots/noCuts/pdf/0JetpT_0.pdf">
	  <img src="plots/noCuts/png/0JetpT_0.png" />
	</a>
      </div>
      <div id="picture">
	<a href="plots/noCuts/pdf/1JetpT_0.pdf">
	  <img src="plots/noCuts/png/1JetpT_0.png"/>
	</a>
      </div>
      <div id="picture">
	<a href="plots/noCuts/pdf/2JetpT_0.pdf">
	  <img src="plots/noCuts/png/2JetpT_0.png" />
	</a>
      </div>
      <div id="picture">
	<a href="plots/noCuts/pdf/3JetpT_0.pdf">
	  <img src="plots/noCuts/png/3JetpT_0.png" />
	</a>
      </div>
      <div id="picture">
	<a href="plots/noCuts/pdf/4JetpT_0.pdf">
	  <img src="plots/noCuts/png/4JetpT_0.png" />
	</a>
      </div>
      <div id="picture">
	<a href="plots/noCuts/pdf/5JetpT_0.pdf">
	  <img src="plots/noCuts/png/5JetpT_0.png" />
	</a>
      </div>
      <!-- b jet pT -->
      <br class="blank" />
      <p style="clear:left;"></p>
      <p id="title">B Jet pT </p>
      <div id="picture">
	<a href="plots/noCuts/pdf/0BJetpT_0.pdf">
	  <img src="plots/noCuts/png/0BJetpT_0.png" />
	</a>
      </div>
      <div id="picture">
	<a href="plots/noCuts/pdf/1BJetpT_0.pdf">
	  <img src="plots/noCuts/png/1BJetpT_0.png"/>
	</a>
      </div>
      <div id="picture">
	<a href="plots/noCuts/pdf/2BJetpT_0.pdf">
	  <img src="plots/noCuts/png/2BJetpT_0.png" />
	</a>
      </div>
      <div id="picture">
	<a href="plots/noCuts/pdf/3BJetpT_0.pdf">
	  <img src="plots/noCuts/png/3BJetpT_0.png" />
	</a>
      </div>
      <!-- lepton pT -->
      <br class="blank" />
      <p style="clear:left;"></p>
      <p id="title"> Lepton pT </p>
      <div id="picture">
	  <a href="plots/noCuts/pdf/LeppT_0.pdf">
	    <img src="plots/noCuts/png/LeppT_0.png" />
	  </a>
      </div>
      <div id="picture">
	<a href="plots/noCuts/pdf/MupT_0.pdf">
	  <img src="plots/noCuts/png/MupT_0.png" />
	</a>
      </div>
      <div id="picture">
	<a href="plots/noCuts/pdf/ElpT_0.pdf">
	  <img src="plots/noCuts/png/ElpT_0.png" />
	</a>
      </div>
      <!-- kinematic variables -->
      <br class="blank" />
      <p style="clear:left;"></p>
      <p id="title"> Kinematic Variables </p>
      <div id="picture">
	<a href="plots/noCuts/pdf/HT_0.pdf">
	  <img src="plots/noCuts/png/HT_0.png" />
	</a>
      </div>
        <div id="picture">
	  <a href="plots/noCuts/pdf/MET_0.pdf">
	    <img src="plots/noCuts/png/MET_0.png" />
	  </a>
	</div>
	<div id="picture">
	  <a href="plots/noCuts/pdf/ST_0.pdf">
	    <img src="plots/noCuts/png/ST_0.png" />
	  </a>
	</div>
    </div>
  </body>
 </html>
""" 
