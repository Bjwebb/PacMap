from xml.etree.ElementTree import ElementTree
import json
import urllib2

def data(req, bbox):
    xml = urllib2.urlopen("http://www.openstreetmap.org/api/0.6/map?bbox="+bbox)
    tree = ElementTree()
    name = "me"
    tree.parse(xml)

    bounds = tree.find("bounds")
    jbounds = {}
    jbounds["minlat"] = bounds.get("minlat")
    jbounds["minlon"] = bounds.get("minlon")
    jbounds["maxlat"] = bounds.get("maxlat")
    jbounds["maxlon"] = bounds.get("maxlon")
    
    nodes = tree.findall("node")
    jnodes = {}
    for node in nodes:
        jnodes[node.get("id")] = {
            "lat":node.get("lat"),
            "lon":node.get("lon"),
            "join":[]
        }
    
    ways = tree.findall("way")
    jways = []
    for way in ways:
        nds = way.findall("nd")
        refs = []
        prev_ref = None
        for nd in nds:
            ref = nd.get("ref")
            if prev_ref:
                jnodes[ref]["join"].append(prev_ref)
                jnodes[prev_ref]["join"].append(ref)
            prev_ref = ref
            #refs.append(ref)
        tags = way.findall("tag")
        #jway = {}
        #jway["nds"] = refs
        #for tag in tags:
        #    k = tag.get("k")
        #    v = tag.get("v")
        #    jway[k] = v
        #jways.append( jway )
        
    data = { "bounds":jbounds, "ways":jways, "nodes":jnodes }
    d = json.dumps(data)
    return "_callback(" + d + ");"