Sample code to take in VMWare XML input and auto-generate OCPV migration artefacts (eg NMState, NAD, NNCP YAMLs)
<ul>
<li>
  <h5>file.xml :</h5> Input vmware deployment as xml
</li>


<h5>main.py :</h5>
<br> parse VMWare XML input to populate graph data structure, visualized like so :
<br>![alt text](./visualization.jpg)
<br>walks the graph recursively, applying specific treatments for migration
<br>only one treatment is currently implemented : look for vSWitches and attached PortGroups = VLANs, generate NAD YAMLs per VLAN, generate 1 global NNCP YAML, 1 global NMState YAML.
<br>assumes hardcoded 'eth0' and 'eth1' physical interfaces on the ESX node to be bonded (should be generalized to read from ESX node in XML input) 
<h5>nad.py, nncp.py, nmstate.py</h5> : Generate YAMLs from given template 
<h5>TODO:</h5>h5> 
<br>generate XML from VMWare discovery input

</ul>
