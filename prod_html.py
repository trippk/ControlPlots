#!/usr/bin/python

def prod_html_string():
    return """\
    <!DOCTYPE html>
     <html>
      <head>
       <title>DESY CMS SUSY Group</title>
        <link rel="stylesheet" href="../../css/style.css" type="text/css"/>
      </head>
     <body>
       <div id="head">
         <h1 id="headline">SUSY Group</h1>
        <div id="head-left">
          <a href="http://www.desy.de/">
           <img id="head-logo-right" src="../../images/DESY-Logo-cyan-RGB_mitVorschau_ger.png" alt="DESY-Logo"/>
          </a>
        </div>
        <div id="head-left">
          <a href="http://cms.web.cern.ch/">
            <img id="head-logo" src="../../images/CMS-Color.png" alt="CMS-Logo"/>
          </a>
        </div>
      </div>
     <div id="newcontent">
      <div id="sidebar"><h2>Samples</h2>
        <ul>
          <li><a><h3> Background </h3></a></li>
          <li><a><h3> Signal </h3></a></li>
        </ul>
      </div>
    </div>
   </body>
 </html>
"""

