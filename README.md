Sample code to take in VMWare XML input and auto-generate OCPV migration artefacts (eg NMState, NAD, NNCP YAMLs)
![Input represented as graph](./visualization.jpg)

<ul>
<li>
  <h5>file.xml :</h5> Input vmware deployment as xml
</li>
<li>
<h5>main.py :</h5>
<li>Parse VMWare XML input to populate graph data structure, visualized like shown above.</li>
<li>Walks the graph recursively, applying specific treatments for migration</li>
<li>Only one treatment is currently implemented : look for vSWitches and attached PortGroups = VLANs, generate NAD YAMLs per VLAN, generate 1 global NNCP YAML, 1 global NMState YAML.</li>
<li>Assumes hardcoded 'eth0' and 'eth1' physical interfaces on the ESX node to be bonded (should be generalized to read from ESX node in XML input) </li>
</li>
<li>
  <h5>nad.py, nncp.py, nmstate.py</h5> Generate YAMLs from given template 
</li>
<li>
  <h5>TODO </h5> Generate XML from VMWare discovery input
</li>

</ul>
